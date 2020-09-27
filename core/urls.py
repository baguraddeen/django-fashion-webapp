from django.urls import path
from . import views
from .views import ProductDeleteView



app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-create/', views.product_create, name='product_create'),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('product/<int:id>/update/', views.product_update, name='product-update'),
    path('product/<pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    # path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
]