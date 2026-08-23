import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from neworld.models import WeeklyBible

logger = logging.getLogger("neworld")


def current_iso_week(value=None):
    iso = (value or datetime.date.today()).isocalendar()
    return iso[0], iso[1]


@login_required(login_url="common:login")
def weeklybible(request):
    target_year, target_week = current_iso_week()
    page, kw, so = request.GET.get("page", "1"), request.GET.get("kw", ""), request.GET.get("so", "recent")
    rows = WeeklyBible.objects.all()
    if so == "recommend":
        rows = rows.annotate(num_voter=Count("research__voter")).order_by("-num_voter", "-year", "-n_week")
    elif so == "popular":
        rows = rows.annotate(num_research=Count("research")).order_by("-num_research", "-year", "-n_week")
    else:
        rows = rows.order_by("-year", "-n_week", "-id")
    if kw:
        rows = rows.filter(Q(year__icontains=kw) | Q(week__icontains=kw) |
                           Q(bible_range__icontains=kw) |
                           Q(research__author__first_name__icontains=kw)).distinct()
    page_obj = Paginator(rows, 10).get_page(page)
    any_rows = rows.exists()
    has_current = rows.filter(year=target_year, n_week=target_week).exists()
    if not has_current:
        logger.warning("event=WEEKLYBIBLE_VIEW_FALLBACK target_year=%s target_week=%s status=%s",
                       target_year, target_week, "historical" if any_rows else "empty")
    return render(request, "neworld/weeklybible.html", {
        "weeklybible_list": page_obj, "target_year": target_year, "target_week": target_week,
        "weeklybible_is_fallback": bool(any_rows and not has_current),
        "weeklybible_is_empty": not any_rows, "page": page, "kw": kw, "so": so,
    })


@login_required(login_url="common:login")
def weeklybible_detail(request, weeklybible_id):
    weeklybible = get_object_or_404(WeeklyBible, pk=weeklybible_id)
    user = User.objects.get(username=request.user)
    group = [item.id for item in user.groups.all()]
    return render(request, "neworld/weeklybible_detail.html", {"weeklybible": weeklybible, "group_list": group})
