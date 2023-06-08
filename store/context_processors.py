from .models import Category, Material


def navlist(request):
    return {
        'categories': Category.objects.all(),
        'materials': Material.objects.all()
    }
