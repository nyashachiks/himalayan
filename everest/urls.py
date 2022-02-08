from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'everest'
urlpatterns = [
    path('', views.store, name='store'),
    path('product', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('updateitem', views.updateitem, name='updateitem')
    ]
