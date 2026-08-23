import io
import re
import zipfile

from django import forms
from django.contrib import admin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from neworld.services.crawler import persist_scripture
from neworld.services.scripture_parser import parse_yearly_scripture_texts
from neworld.services.wol_client import WolClientError
from neworld.models import Question, Scripture, Answer, Meditation, Comment, WeeklyBible, \
    Research, Bible, WBsummary, PubsIndex, Customer, Gpt, GptAnswer


# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['username']
#
# admin.site.register(User, UserAdmin)


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)


class AnnualScriptureUploadForm(forms.Form):
    year = forms.IntegerField(min_value=1900, max_value=2100, label="\uc5f0\ub3c4")
    zip_file = forms.FileField(label="TXT ZIP \ud30c\uc77c")


def _read_uploaded_txt_zip(uploaded_file):
    if uploaded_file.size > 2 * 1024 * 1024:
        raise ValueError("ZIP file exceeds the 2 MB limit")
    raw = uploaded_file.read()
    if not raw.strip():
        raise ValueError("ZIP file is empty")
    try:
        archive = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile as exc:
        raise ValueError("Uploaded file is not a valid ZIP archive") from exc

    monthly_texts = {}
    total_size = 0
    filename_pattern = re.compile(r"(?:^|/).+_(\d{2})\.txt$", re.IGNORECASE)
    for info in archive.infolist():
        if info.is_dir():
            continue
        match = filename_pattern.search(info.filename)
        if not match:
            continue
        month = int(match.group(1))
        if month == 0:
            continue
        if not 1 <= month <= 12:
            continue
        if month in monthly_texts:
            raise ValueError("ZIP contains duplicate monthly TXT files")
        if info.file_size > 1024 * 1024:
            raise ValueError("A TXT file exceeds the 1 MB limit")
        total_size += info.file_size
        if total_size > 8 * 1024 * 1024:
            raise ValueError("Uncompressed TXT content exceeds the 8 MB limit")
        data = archive.read(info)
        for encoding in ("utf-8-sig", "utf-8", "cp949"):
            try:
                monthly_texts[month] = data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("TXT files must be UTF-8 or CP949 encoded")
    return monthly_texts


class ScriptureAdmin(admin.ModelAdmin):
    search_fields = ['real_date']
    change_list_template = "admin/neworld/scripture/change_list.html"

    def get_urls(self):
        custom_urls = [
            path("import-year/", self.admin_site.admin_view(self.import_year_view),
                 name="neworld_scripture_import_year"),
        ]
        return custom_urls + super().get_urls()

    def import_year_view(self, request):
        form = AnnualScriptureUploadForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            uploaded_file = form.cleaned_data["zip_file"]
            try:
                monthly_texts = _read_uploaded_txt_zip(uploaded_file)
                items = parse_yearly_scripture_texts(
                    monthly_texts, form.cleaned_data["year"], "upload://%s" % uploaded_file.name)
                counts = {"inserted": 0, "skipped": 0}
                with transaction.atomic():
                    for item in items:
                        counts[persist_scripture(item)] += 1
            except (ValueError, WolClientError) as exc:
                form.add_error(None, str(exc))
            else:
                self.message_user(
                    request,
                    "Year imported: parsed=%s, inserted=%s, skipped=%s" % (
                        len(items), counts["inserted"], counts["skipped"]),
                )
                return HttpResponseRedirect(reverse("admin:neworld_scripture_changelist"))
        context = {
            **self.admin_site.each_context(request),
            "title": "Import yearly Scripture HTML",
            "opts": self.model._meta,
            "form": form,
        }
        return TemplateResponse(request, "admin/neworld/scripture/import_year.html", context)

admin.site.register(Scripture, ScriptureAdmin)


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Answer, AnswerAdmin)


class MeditationAdmin(admin.ModelAdmin):
    search_fields = ['real_date']

admin.site.register(Meditation, MeditationAdmin)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)


class WeeklyBibleAdmin(admin.ModelAdmin):
    search_fields = ['n_week']

admin.site.register(WeeklyBible, WeeklyBibleAdmin)


class ResearchAdmin(admin.ModelAdmin):
    search_fields = ['n_week']

admin.site.register(Research, ResearchAdmin)


class BibleAdmin(admin.ModelAdmin):
    search_fields = ['bible']

admin.site.register(Bible, BibleAdmin)


class WBsummaryAdmin(admin.ModelAdmin):
    search_fields = ['bible_summary']

admin.site.register(WBsummary, WBsummaryAdmin)


class PubsIndexAdmin(admin.ModelAdmin):
    search_fields = ['pi_title']

admin.site.register(PubsIndex, PubsIndexAdmin)


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Customer, CustomerAdmin)


class GptAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Gpt, GptAdmin)


class GptAnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(GptAnswer, GptAnswerAdmin)
