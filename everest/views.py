from django.shortcuts import render
from .models import (Customer,
                     Category,
                     Brand,
                     Currency,
                     UnitsOfMeasure,
                     Product,
                     PurchaseOrder,
                     CartItem,
                     LogisticsSupplier,
                     ShippingAddress,
                     Invoice,
                     Images)


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product(request):
    context = {}
    return render(request, 'store/product.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)