from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from PIL import Image
from django.urls import reverse


class Customer(models.Model):
    customer = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    street1 = models.CharField(max_length=100, null=True, blank=True)
    street2 = models.CharField(max_length=100,  null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    country = CountryField()
    mobile = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.customer)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(default='no_image.jpg', upload_to='category_images', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Brand(models.Model):
    brand = models.CharField(max_length=40, null=True, blank=True)
    brand_image = models.ImageField(default='no_image.jpg', upload_to='brand_images')

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.brand_image.path)
        if img.height > 300 or img.width > 300:
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Currency(models.Model):
    currency_name = models.CharField(max_length=40, null=True, blank=True)
    symbol = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.symbol


class UnitsOfMeasure(models.Model):
    unit_name = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.unit_name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    is_digital = models.BooleanField(default=False, null=True, blank=False)
    unit_of_measure = models.ForeignKey(UnitsOfMeasure, on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(default='no_image.jpg', upload_to='product_images', null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_order_complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.order_number

    @property
    def shipping(self):
        shipping = False
        cart_items = self.cartitem_set.all()
        for i in cart_items:
            if i.line_item.is_digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        cart_items = self.cartitem_set.all()
        cart_total = sum(item.get_total for item in cart_items)
        return cart_total

    @property
    def get_cart_quantity(self):
        cart_items = self.cartitem_set.all()
        cart_total = sum(item.quantity for item in cart_items)
        return cart_total


class CartItem(models.Model):
    line_item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.line_item.price * self.quantity
        return total


class LogisticsSupplier(models.Model):
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    billing_unit = models.ForeignKey(UnitsOfMeasure, on_delete=models.CASCADE)
    billing_rate = models.FloatField()

    def __str__(self):
        return self.courier_name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"


class Invoice(models.Model):
    order_number = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.order_number


class Images(models.Model):
    upload = models.ImageField(default='no_image.jpg', upload_to='more_product_images', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)