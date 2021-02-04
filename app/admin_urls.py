from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import admin_views

urlpatterns = [
    path('products', admin_views.ProductList.as_view()),
    path('product/<int:id>', admin_views.ProductEdit.as_view()),
    path('product-seed', admin_views.ProductSeed.as_view()),
]
