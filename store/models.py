
from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from clients.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    # Optionally, add more fields like `caption` or `alt_text` if needed

    def __str__(self):
        return f"Image for {self.product.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    main_img = models.ImageField(upload_to='product_images/', blank=True, null=True)
    #options = models.JSONField(null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    availables = models.IntegerField()
    puntuation = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    GBP = 'GBP'
    CURRENCY_CHOICES = [
        (EUR, 'Euro'),
        (USD, 'Dollar'),
        (GBP, 'Pound'),
    ]
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default=EUR,
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def order_item_ids(self):
        return [item.id for item in self.items.all()]
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Check if the instance already exists in the database
            original = Order.objects.get(pk=self.pk)
            if original.customer != self.customer:
                raise ValueError("Cannot change the customer associated with this order.")
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customization_details = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.order} - {self.id}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Check if the instance already exists in the database
            original = OrderItem.objects.get(pk=self.pk)
            if original.order != self.order:
                raise ValueError("Cannot change the order associated with this order item.")
        super().save(*args, **kwargs)

class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='discounts', null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

    def __str__(self):
        return f"Discount {self.code} for Order {self.order.id}" 