from django.contrib import admin
from .models import (Customer,
                     Category,
                     Brand,
                     Currency,
                     UnitsOfMeasure,
                     Product,
                     PurchaseOrder,
                     CartItem,
                     LogisticsSupplier,
                     Invoice,
                     Images)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Currency)
admin.site.register(UnitsOfMeasure)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(CartItem)
admin.site.register(LogisticsSupplier)
admin.site.register(Invoice)
admin.site.register(Images)
