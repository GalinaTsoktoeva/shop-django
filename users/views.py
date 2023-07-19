import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        #Генерируем уникальный токен для верификации
        user = form.save(commit=False)
        # Деактивируем пользователя, пока он не подтвердит почту
        user.is_active = False
        #Устанавливаем ненужный пароль
        #user.set_unusable_password()
        user.save()

        #Отправляем письмо с токеном для верификации
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Активация аккаунта'
        message = render_to_string(
            'users/verification_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            }
        )
        print(user.email)
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verify_yes.html'

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                #user.set_password()
                user.save()
                return self.render_to_response({})
            else:
                return redirect('users:verify_no')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return redirect('users:verify_no')


@login_required
def gen_new_pass(request):
    new_password = ''
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(8):
        new_password += random.choice(chars)

    request.user.set_password(new_password)
    request.user.save()
    send_mail('Ваш пароль изменен',
              f"Ваш пароль: {new_password}", settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

    return redirect('catalog:index')


class ActivationSuccess(TemplateView):
    template_name = 'users/email_verify_yes.html'


class ActivationFailed(TemplateView):
    template_name = 'users/email_verify_no.html'