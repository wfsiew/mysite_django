from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import order_views

urlpatterns = [
    path('', order_views.OrderList.as_view()),
    path('markshipped/<int:id>', order_views.OrderMarkShipped.as_view()),
    path('checkout', order_views.OrderCheckout.as_view()),
]
