from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from PIL import Image
from django.urls import reverse


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    country = CountryField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    # parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(default='no_image.jpg', upload_to='category_pics')

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
    brand = models.CharField(max_length=40)
    brand_image = models.ImageField(default='no_image.jpg', upload_to='brand_pics')

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Currency(models.Model):
    currency_name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.symbol


class UnitsOfMeasure(models.Model):
    unit_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.unit_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    dimensions = models.CharField(max_length=50)
    weight = models.CharField(max_length=100)
    unit_of_measure = models.ForeignKey(UnitsOfMeasure, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    date = models.DateTimeField()
    order_total = models.FloatField()
    order_status = models.CharField(max_length=100)

    def __str__(self):
        return self.order_number


class CartItem(models.Model):
    line_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    line_total = models.FloatField()

    def __str__(self):
        return str(self.line_item)


class LogisticsSupplier(models.Model):
    courier_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    billing_unit = models.ForeignKey(UnitsOfMeasure, on_delete=models.CASCADE)
    billing_rate = models.FloatField()

    def __str__(self):
        return self.courier_name


class Invoice(models.Model):
    order_number = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.order_number


class Images(models.Model):
    upload = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)