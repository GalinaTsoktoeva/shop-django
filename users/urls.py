from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailVerificationView, gen_new_pass, ActivationSuccess, ActivationFailed

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('success', ActivationSuccess.as_view(), name='verify_yes'),
    path('failed', ActivationFailed.as_view(), name='verify_no'),
    path('gen_new_pass/', gen_new_pass, name='gen_new_pass'),
]