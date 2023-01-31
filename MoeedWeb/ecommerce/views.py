from django.shortcuts import render

from .models import Category, Brand, Product

# Create your views here.

def home(request):
    return render(request, 'ecommerce/index.html')
