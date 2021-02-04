from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import product_views

urlpatterns = [
    path('<int:page>', product_views.ProductList.as_view()),
    path('<str:category>/<int:page>', product_views.ProductCategoryList.as_view()),
    path('categories', product_views.CategoryList.as_view()),
]
