from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from apps.category.forms import CategoryForm
from apps.product.forms import ProductForm
from .forms import ProductForm
from .models import Product
from django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    products = serializers.serialize(
        "json", Product.objects.all().order_by('-created_at'))
    return HttpResponse(products)


@login_required(login_url="/login/")
def filterByName(request, name):
    product = get_object_or_404(Product, name=name)
    categories = product.categories.all().order_by('-created_at')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(categories, 16)
        categories = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': categories,
        'paginator': paginator,
        'form': CategoryForm(),
        'category': name  # for the navigation route
    }
    return render(request, 'pages/categories/index.html', data)


@login_required(login_url="/login/")
def store(request):
    if request.method == 'POST':
        product = ProductForm(request.POST)
        if product.is_valid():
            product.save()
            messages.success(request, "Producto creado satisfactoriamente")
            return redirect(to="products.filter-by-name", name=product['name'].value())
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
