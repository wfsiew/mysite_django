from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from app import admin_urls, product_urls, order_urls

urlpatterns = [
    path('admin/', include(admin_urls)),
    path('product/', include(product_urls)),
    path('order/', include(order_urls)),
]
