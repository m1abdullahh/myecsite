from django.contrib import admin
from .models import Product, OrderItem, ShoppingCart, PaymentDetails, ShippingDetails, ProductReview
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "discounted_price", "in_stock","id"]


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(PaymentDetails)
admin.site.register(ShippingDetails)
admin.site.register(ProductReview)