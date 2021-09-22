from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import CreateView

from common.forms import UserForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# 계정 생성
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user_ID = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user_ID, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            next_url = request.GET.get('next') or 'profile'
            return redirect(next_url)
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


class SignupView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'common/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

signup = SignupView.as_view()


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

