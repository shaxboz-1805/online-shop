from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductsAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path('user_cart/<int:pk>/', CartAPIView.as_view()),
    path('create_cart/', CartAPIView.as_view()),
    path('update_cart/<int:pk>/', CartAPIView.as_view()),
    path('delete_cart/<int:pk>/', CartAPIView.as_view()),
    path('checkout/', CheckoutAPIView.as_view()),
    path('history/<str:pk>/', HistoryAPIView.as_view()),
    path('saleproducts/', SaleProductsAPIView.as_view()),
    path('newproducts/', NewProductsAPIView.as_view()),
]