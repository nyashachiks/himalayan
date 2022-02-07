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
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0}

    context = {'items': items, 'purchaseorder': purchaseorder}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0}

    context = {'items': items, 'purchaseorder': purchaseorder}
    return render(request, 'store/checkout.html', context)