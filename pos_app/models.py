from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Product(models.Model):  # Class name should be capitalized (Product instead of product)
    name = models.CharField(max_length=225, default='No name')
    
    description = models.TextField(default='No description')
    stock_quantity = models.IntegerField(default=0)  # Correct default for IntegerField
    image = models.ImageField(upload_to='media/products/', default='No image')  # Assuming you want to store product images
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default='fsa')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Add this line
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def discounted_price(self):
        return self.price - self.discount

    def clean(self):  # ✅ Put it here inside Product model
        if self.discount > self.price:
            raise ValidationError("Discount cannot be greater than price.")