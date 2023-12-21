from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('close-order/', views.CloseOrder.as_view(), name='close_order'),
    path('view-order/', views.ViewOrder.as_view(), name='view_order'),
    path('details/<int:pk>', views.Detail.as_view(), name='details')
]