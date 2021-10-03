from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.views.generic import CreateView

from common.forms import UserForm
from config.settings import base
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from common.models import User
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth import get_user_model
# from django.contrib import auth
# from common.models import Profile
#
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.core.mail import EmailMessage
# from common.tokens import account_activation_token
# from django.utils.encoding import force_bytes, force_text
# from django.utils import timezone
#
# from django.core.exceptions import ValidationError
# from django.contrib.auth.tokens import default_token_generator
# from django.http import Http404


# 계정 생성
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user_id = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user_id, password=raw_password)   # 사용자 인증
            login(request, user)  # 로그인
            next_url = request.GET.get('next') or 'profile'
            return redirect(next_url)
    else:
        form = UserForm()
    return render(request, 'common/signup_test.html', {'form': form})



class SignupView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'common/signup_test.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

signup = SignupView.as_view()


# class RequestLoginViaUrlView(PasswordResetView):
#     template_name = 'common/request_login_via_url_form.html'
#     title = '이메일을 통한 로그인'
#     email_template_name = 'common/login_via_url.html'
#     success_url = base.LOGIN_REDIRECT_URL
#
#
# def login_via_url(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         current_user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
#         raise Http404
#
#     if default_token_generator.check_token(current_user, token):
#         login(request, current_user)
#         messages.info(request, '로그인이 승인되었습니다.')
#         return redirect('neworld:index')
#
#     messages.error(request, '로그인이 거부되었습니다.')
#     return redirect('neworld:index')
#
#
#
# def signup(request):
#     if request.method == "POST":
#         if request.POST["password1"] == request.POST["password2"]:
#             user = User.objects.create_user(
#                 username=request.POST["username"],
#                 password=request.POST["password1"],
#                 first_name=request.POST['first_name'],
#                 last_name=request.POST['last_name'],
#                 nickname=request.POST['nickname'])
#             user.is_active = False
#             user.is_superuser = False
#             user.is_staff = False
#             user.save()
#             current_site = get_current_site(request)
#             # localhost:8000
#             message = render_to_string('common/user_activate_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
#                 'token': account_activation_token.make_token(user),
#             })
#             mail_subject = "[SOT] 회원가입 인증 메일입니다."
#             user_email = user.email
#             email = EmailMessage(mail_subject, message, to=[user_email])
#             email.send()
#             return HttpResponse(
#                 '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
#                 'justify-content: center; align-items: center;">'
#                 '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
#                 '</div>'
#             )
#         return redirect('neworld:index')
#     else:
#         form = UserForm()
#         return render(request, 'common/signup_test.html', {'form': form})
#
#
#
# def activate(request, uid64, token):
#
#     uid = force_text(urlsafe_base64_decode(uid64))
#     user = User.objects.get(pk=uid)
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.date_joined = timezone.now()
#         user.save()
#         login(request, user)
#         return redirect('neworld:index')
#     else:
#         return HttpResponse('비정상적인 접근입니다.')




@login_required(login_url='common:login')
def profile(request):
    return render(request, 'common/profile.html')


def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'common/404.html', {})


def internal_server_error(request, *args, **argv):
    """
    500 Internal Server Error
    """
    return render(request, 'common/500.html', status=500)


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('common:profile')
    template_name = 'common/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('common:login')
    template_name = 'common/password_reset_form.html'
    email_template_name = 'common/password_reset.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('common:login')
    template_name = 'common/password_reset_confirm.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 초기화를 완료했습니다.')
        return super().form_valid(form)


