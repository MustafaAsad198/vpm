from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    re_path(r'^api/vendors$',views.vendors),
    re_path(r'^api/vendors/(?P<pk>[a-zA-Z0-9]+)$', views.vendorDetail),
    re_path(r'^api/purchase_orders$',views.purchaseOrders),
    re_path(r'^api/purchase_orders/(?P<pk>[a-zA-Z0-9]+)$', views.purchaseOrderDetail),
    re_path(r'^api/vendors/(?P<pk>[a-zA-Z0-9]+)/performance', views.vendorPerformance),
    re_path(r'^api/purchase_orders/(?P<pk>[a-zA-Z0-9]+)/acknowledge', views.acknowledgePO),
]