from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    extra_context = {
        'is_active_main': 'active'
    }

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = Product.objects.none

        try:
            for product in queryset:
                version = product.version_set.all().filter(is_current=True).first()
                product.version = version
        except TypeError:
            return queryset
        return queryset


@login_required
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'#('name', 'price', 'category', 'img')
    success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')


