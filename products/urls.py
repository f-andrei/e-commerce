from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('services/', views.ListProducts.as_view(), name="list"),
    path('<slug>', views.ProductDetails.as_view(), name="product_details"),
    path('add-to-cart/', views.AddToCart.as_view(), name="add_to_cart"),
    path('remove-from-cart/', views.RemoveFromCart.as_view(),
          name="remove_from_cart"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('overview/', views.Overview.as_view(), name="overview"),
    path('search/', views.Search.as_view(), name="search"),
    path('about/', views.About.as_view(), name="about"),
]