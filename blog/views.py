from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
import smtplib
from django.core.mail import get_connection, send_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from blog.models import Blog


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'img', 'data_create', 'is_published', 'count_views',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'img', 'data_create', 'is_published', 'count_views',)

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


class ArticleListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


@login_required
def toggle_activity(request, pk):
    article_item = get_object_or_404(Blog, pk=pk)
    if article_item.is_published:
        article_item.is_published = False
    else:
        article_item.is_published = True
    article_item.save()

    return redirect(reverse('blog:list'))


@login_required
def send_msg(request, pk):
    txt = 'hello, my dear! Congratulations! you have more than 100 views'
    article_item = get_object_or_404(Blog, pk=pk)
    sender = 'galatsoktoeva@yandex.ru'
    send_email(sender, 'Python', txt)

    return redirect(reverse('blog:view', args=[pk]))


def send_email(to_addr, subject, text):
    sender = 'galatsoktoeva@yandex.ru'
    sender_password = 'EuKH21t1!'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = sender
    msg['Subject'] = subject
    msg.attach(
        MIMEText(text, 'plain')
    )
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(sender)
    server.login(sender, sender_password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()