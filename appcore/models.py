from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.FloatField(verbose_name="Price")
    product_type = models.CharField(max_length=20)
    quantity_left = models.IntegerField(default=1)
    tags = ArrayField(
        base_field=models.CharField(max_length=20),
        default=list,
    )
    product_tagline = models.CharField(max_length=50, blank=True)
    info_lines = ArrayField(
        base_field=models.CharField(max_length=100),
        default=list
    )
    discount = models.IntegerField(default=0)
    manufacturer = models.CharField(max_length=30, default="")
    descriptions = models.JSONField(default=dict, blank=True)
    page_photos = ArrayField(
        base_field=models.CharField(max_length=200), default=list
    )
    additional_info = models.JSONField(default=dict, blank=True)
    price_id = models.CharField(max_length=200, default="")
    product_image = models.ImageField(upload_to='images/', verbose_name="Primary Image")

    
    def __str__(self) -> str:
        return self.product_name

    @admin.display(
            boolean=True,
            description="In Stock?"
    )
    def in_stock(self) -> bool:
        return self.quantity_left > 0
    
    def discounted_price(self):
        return round(float(int(self.product_price * (1 - (self.discount / 100)))), 2)
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "product_id": f"{self.id}"
        })
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.product.discounted_price() * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity}x{self.product}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.email}"
    
    @property
    def subtotal(self):
        total = 0
        for each in self.items.all():
            total += each.quantity * each.product.discounted_price()
        return total


class ShippingDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    company_name = models.CharField(max_length=40, blank=True)
    area_code = models.IntegerField(blank=False)
    primary_phone = models.CharField(max_length=30)
    address_1 = models.CharField(max_length=100, blank=False)
    address_2 = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=False)

    def __str__(self) -> str:
        return self.user.email

class PaymentDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cardholder = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16)
    payment_type = models.CharField(max_length=20, blank=True)
    mm = models.CharField(max_length=2)
    yy = models.CharField(max_length=4)
    number = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.user.email


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    review = models.CharField(max_length=500)
    rating = models.CharField(default="5", max_length=1)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self) -> str:
        return f"{self.product}-{self.user.email}"
