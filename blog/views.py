from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class ArticleCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'img', 'data_create', 'is_published', 'count_views',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'img', 'data_create', 'is_published', 'count_views',)
    #success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


class ArticleListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object

def toggle_activity(request, pk):
    article_item = get_object_or_404(Blog, pk=pk)
    if article_item.is_published:
        article_item.is_published = False
    else:
        article_item.is_published = True
    article_item.save()

    return redirect(reverse('blog:list'))
