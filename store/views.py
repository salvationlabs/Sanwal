from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from .forms import ProductForm
from .models import Images, Product
from account.models import User


# Create your views here.
class HomeView(ListView):
    model = Product
    paginate_by = 8
    template_name = 'store/index.html'

    def get_queryset(self):
        return Product.products.all()

def ExtraView(request):
    return render(request, 'store/extra.html')

class CategoryListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'store/products.html'

    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        qs = Product.products.all()
        return qs.filter(category__slug=self.kwargs['category_slug']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = self.kwargs['category_slug']
        return context


class SubCategoryListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'store/products.html'

    def get_queryset(self, **kwargs):
        qs = Product.products.all()
        return qs.filter(subcategory__slug=self.kwargs['subcategory_slug']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = self.kwargs['category_slug']
        context['subheading'] = self.kwargs['subcategory_slug']
        return context


class MaterialListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'store/products.html'

    def get_queryset(self, **kwargs):
        qs = Product.products.all()
        return qs.filter(material__slug=self.kwargs['material_slug']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = self.kwargs['material_slug']
        return context


class ItemDetailView (DetailView):
    model = Product
    template_name = 'store/product.html'


@staff_member_required
def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        images = request.FILES.getlist('images')

        if product_form.is_valid():
            product_obj = product_form.save(commit=False)
            product_obj.creator = request.user
            product_obj.save()

            for img in images:
                Images.objects.create(item=product_obj, image=img)

            messages.success(request, "Yeew, check it out on the home page!")
            return redirect("store:index")

        else:
            for field in product_form:
                for error in field.errors:
                    messages.error(request, f"{field.name}: {error}")

            print(product_form.errors)
            return render(
                request, 'store/createProduct.html', {
                    'form': product_form
                })

    product_form = ProductForm()
    return render(request, 'store/createProduct.html', {
        'form': product_form,
    })
