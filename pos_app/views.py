from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.conf import settings


# Create your views here.
def home(request):
    products = Product.objects.all()
    print(settings.MEDIA_ROOT)
    return render (request, 'pos_app/pos.html', {"products": products})
