from .models import Category, Brand


def navlist(request):
    return {
        'categories': Category.objects.filter(level=0),
        'brands': Brand.objects.all()
    }
