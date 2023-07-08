from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    toggle_activity
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('view/<int:pk>', ArticleDetailView.as_view(), name='view'),
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('edit/<int:pk>', ArticleUpdateView.as_view(), name='update_article'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete_article'),
    path('publish/<int:pk>', toggle_activity, name='toggle_activity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)