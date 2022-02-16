from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
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
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
        cart_quantity = purchaseorder.get_cart_quantity
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0, 'shipping': False}
        cart_quantity = purchaseorder['get_cart_quantity']

    products = Product.objects.all()
    context = {'products': products, 'cart_quantity': cart_quantity}
    return render(request, 'store/store.html', context)


def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
        cart_quantity = purchaseorder.get_cart_quantity
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0, 'shipping': False}
        cart_quantity = purchaseorder['get_cart_quantity']

    context = {'cart_quantity': cart_quantity}
    return render(request, 'store/product.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
        cart_quantity = purchaseorder.get_cart_quantity
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0, 'shipping': False}
        cart_quantity = purchaseorder['get_cart_quantity']

    context = {'items': items, 'purchaseorder': purchaseorder, 'cart_quantity': cart_quantity}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        items = purchaseorder.cartitem_set.all()
        cart_quantity = purchaseorder.get_cart_quantity
    else:
        items = []
        purchaseorder = {'get_cart_total': 0, 'get_cart_quantity': 0, 'shipping': False}
        cart_quantity = purchaseorder['get_cart_quantity']

    context = {'items': items, 'purchaseorder': purchaseorder, 'cart_quantity': cart_quantity}
    return render(request, 'store/checkout.html', context)


def updateitem(request):
    data = json.loads(request.read())
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
    cart_item, created = CartItem.objects.get_or_create(purchase_order=purchaseorder, line_item=product)

    if action == 'add':
        cart_item.quantity = (cart_item.quantity + 1)
    elif action == 'remove':
        cart_item.quantity = (cart_item.quantity - 1)

    cart_item.save()

    if cart_item.quantity <= 0:
        cart_item.delete()

    return JsonResponse('Item was added', safe=False)


def processPurchaseOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        purchaseorder, created = PurchaseOrder.objects.get_or_create(customer=customer, is_order_complete=False)
        total = float(data['form']['total'])
        purchaseorder.order_number = transaction_id

        if total == purchaseorder.get_cart_total:
            purchaseorder.is_order_complete = True
        purchaseorder.save()

        if purchaseorder.shipping == True:
            ShippingAddress.objects.create(customer=customer,
                                           purchase_order=purchaseorder,
                                           address1=data['shipping']['address1'],
                                           address2=data['shipping']['address2'],
                                           city=data['shipping']['city'],
                                           country=data['shipping']['country'],)

    else:
        print("User is not logged in")
    return JsonResponse('Payment complete', safe=False)