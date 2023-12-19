from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('close-order/', views.CloseOrder.as_view(), name='close_order'),
    path('details/', views.Detail.as_view(), name='details')
]