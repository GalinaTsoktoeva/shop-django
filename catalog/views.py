from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product


class ProductListView(ListView):
    model = Product


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}, {phone}: {message}")
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'price', 'category', 'img')
    success_url = reverse_lazy('catalog:index')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'price', 'category', 'img')
    success_url = reverse_lazy('catalog:index')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')


