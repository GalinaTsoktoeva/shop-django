from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog import views
from catalog.apps import MainConfig
from catalog.views import index,contacts,product

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>/', views.product, name='product')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)