from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Brand, Product
from .serializers import CategorySerializer

# Create your views here.


class CategoryViewSet (viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


def home(request):
    return render(request, 'ecommerce/index.html')
