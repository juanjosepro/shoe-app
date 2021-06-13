from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from apps.product.models import Product
from apps.category.models import Category
from apps.model.models import Model
from .models import Dozen
from .forms import DozenForm
from  django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    dozens = Dozen.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 40)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': dozens,
        'paginator': paginator,    
    }
    return render(request, 'pages/dozens/index.html', data)


@login_required(login_url="/login/")
def filter(request, filter):
    dozens = None
    if filter == 'todos':
        dozens = Dozen.objects.all().order_by('-created_at')
    if filter == 'disponibles':
        dozens = Dozen.objects.filter(status = 'disponible').order_by('-created_at')
    if filter == 'vendidos':
        dozens = Dozen.objects.filter(status = 'vendido').order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 15)
        dozens = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': dozens,
        'paginator': paginator,
        'filter_by': filter,
    }
    return render(request, 'pages/dozens/index.html', data)


@login_required(login_url="/login/")
def show(request, name):
    model = get_object_or_404(Model, name = name)

    dozens = Dozen.objects.filter(model_id = model.id)
    category = Category.objects.get(id = model.category_id)
    product = Product.objects.get(id = category.product_id)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 15)
        dozens = paginator.page(page)
    except:
        raise Http404
        
    data = {
        'product': product, #for the navigation route
        'category': category, #for the navigation route
        'model': model, #for the navigation route
        'entity': dozens,
        'paginator': paginator,
    }

    return render(request, 'pages/dozens/show.html', data)


@login_required(login_url="/login/")
def store(request, name):
    model = get_object_or_404(Model, name = name)
    sizes = model.category.product.sizes.all()

    data = {
        'form': DozenForm(),
        'sizes': sizes,
        'product': model.category.product, #for the navigation route
        'category': model.category, #for the navigation route         
        'model': model, #for the navigation route
    }
    
    if request.method == 'POST':
        formulario = DozenForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Docena agregada satisfactoriamente')
            
            return redirect(to="dozens.show", name = model.name)
        else:
            data['form'] = formulario
            messages.error(request, 'Error al agregar la docena')
    
    return render(request, 'pages/dozens/create.html', data)


@login_required(login_url="/login/")
def update(request, id):
    dozen = get_object_or_404(Dozen, id = id)

    data = {
        'product': dozen.model.category.product, #for the navigation route
        'category': dozen.model.category, #for the navigation route
        'model': dozen.model, #for the navigation route
        'form': DozenForm(instance=dozen)
    }

    if request.method == 'POST':
        formulario = DozenForm(data=request.POST, instance=dozen)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Docena actualizada satisfactoriamente')

            return redirect(to="dozens.show", name = dozen.model.name)
        else:
            data['form'] = formulario
            messages.error(request, 'Error al actualizar la docena')

    return render(request, 'pages/dozens/update.html', data)