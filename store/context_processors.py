from .models import Category, Material


def navlist(request):
    return {
        'categories': Category.objects.filter(level=0),
        'materials': Material.objects.all()
    }
