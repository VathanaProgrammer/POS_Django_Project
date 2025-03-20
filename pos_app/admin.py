# pos_app/admin.py
from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'category', 'image']  # Include image in list view if you want
    search_fields = ['name', 'description']
    list_filter = ['price', 'category']

    fields = ['category', 'name', 'price', 'description', 'stock_quantity', 'image' , 'discount']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)