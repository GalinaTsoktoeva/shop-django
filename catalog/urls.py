from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog import views
from catalog.apps import MainConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, category

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(ProductListView.as_view()), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('category/', category, name='category'),
    path('view/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('create/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)