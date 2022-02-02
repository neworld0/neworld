from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import ActivityForm
from ..models import Customer, Activity



# Bulletin Board 답변등록
@login_required(login_url='common:login')
def activity_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.author = request.user
            activity.create_date = timezone.now()
            activity.customer = customer
            activity.save()
            return redirect('{}#activity_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=customer.id), activity.id))
    else:
        form = ActivityForm()
    context = {'customer': customer, 'form': form}
    return render(request, 'neworld/customer_detail.html', context)


# Bulletin Board 답변 수정
@login_required(login_url='common:login')
def activity_modify(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.user != activity.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=activity.customer.id)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.modify_date = timezone.now()
            activity.save()
            return redirect('{}#activity_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=activity.customer.id), activity.id))
    else:
        form = ActivityForm(instance=activity)
    context = {'activity': activity, 'form': form}
    return render(request, 'neworld/activity_form.html', context)


# Bulletin Board 답변 삭제
@login_required(login_url='common:login')
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.user != activity.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        activity.delete()
    return redirect('neworld:customer_detail', customer_id=activity.customer.id)

