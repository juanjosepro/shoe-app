from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Category
from .forms import CategoryForm
from .models import Category

@login_required(login_url="/login/")
def index(request):
    categories = Category.objects.all()

    data = {
        'categories': categories,
        'form': CategoryForm(),
    }

    return render(request, 'pages/categories/index.html', data)


@login_required(login_url="/login/")
def store(request):
    if request.method == 'POST':
        formulario = CategoryForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Categoria creada satisfactoriamente")
        else:
            messages.error(request, "Error al crear la categoria")
    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url="/login/")
def update(request, name):
    category = get_object_or_404(Category, name = name)
    data = {
        'form': CategoryForm(instance=category),
        'product': category.product, #for the navigation route
        'category': category #for the navigation route
    }

    if request.method == 'POST':
        formulario = CategoryForm(data=request.POST, instance=category)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Categoria actualizada satisfactoriamente")
            
            return redirect(to='products.filter-by-name', name = category.product)
        else:
            data['form'] = formulario
            messages.error(request, "Error al actualizar la categoria")
            
    return render(request, 'pages/categories/update.html', data)