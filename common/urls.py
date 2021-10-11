from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]



# path('login/url/', views.RequestLoginViaUrlView.as_view(template_name='common/request_login_via_url_form.html'), name='request_login_via_url'),
# path('login/<uidb64>/<token>/', views.login_via_url, name='login_via_url'),

# path('activate/<uidb64>/<token>/', views.activate, name='activate'),
