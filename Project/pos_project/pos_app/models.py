from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity_in_stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True) 
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('out_of_stock', 'Out of Stock')], default="available")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_low_stock(self):
        return self.quantity_in_stock < 5  # You can customize this threshold
    
class Customer(models.Model):
    name = models.CharField(max_length=100, null=True, default='Guest')
   
class Sale(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card')])
    created_at = models.DateTimeField(auto_now_add=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
class POSSetting(models.Model):
    name = models.CharField(max_length=255, default="My Company")
    address = models.CharField(max_length=255, default="Address Here")
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    def __str__(self):
        return self.name