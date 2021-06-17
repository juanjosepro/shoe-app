from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from apps.category.models import Category
from apps.model.models import Model
from .models import Dozen
from .forms import DozenForm


@login_required(login_url="/login/")
def index(request):
    dozens = Dozen.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 25)
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
    if filter.strip() == 'todos':
        dozens = Dozen.objects.all().order_by('-created_at')
    if filter.strip() == 'disponibles':
        dozens = Dozen.objects.filter(
            status='disponible').order_by('-created_at')
    if filter.strip() == 'vendidos':
        dozens = Dozen.objects.filter(status='vendido').order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 25)
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
def show(request, name, filter):
    model = get_object_or_404(Model, name=name.strip())

    dozens = None
    if filter.strip() == 'todos':
        dozens = Dozen.objects.filter(
            model_id=model.id).order_by('-created_at')
    if filter.strip() == 'disponibles':
        dozens = Dozen.objects.filter(Q(status='disponible') & Q(
            model_id=model.id)).order_by('-created_at')
    if filter.strip() == 'vendidos':
        dozens = Dozen.objects.filter(Q(status='vendido') & Q(
            model_id=model.id)).order_by('-created_at')

    category = Category.objects.get(id=model.category_id)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 25)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        'category': category,  # for the navigation route
        'model': model,  # for the navigation route
        'entity': dozens,
        'paginator': paginator,
        'filter_by': filter,
    }

    return render(request, 'pages/dozens/show.html', data)


@login_required(login_url="/login/")
def store(request, name):
    model = get_object_or_404(Model, name=name)
    model.all_your_sizes = model.sizes.all()

    data = {
        'form': DozenForm(),
        'category': model.category,  # for the navigation route
        'model': model,  # for the navigation route and select to form
    }

    if request.method == 'POST':
        print(request.POST)
        formulario = DozenForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Docena agregada satisfactoriamente')

            return redirect(to="dozens.show", name=model.name, filter="todos")
        else:
            data['form'] = formulario
            messages.error(request, 'Error al agregar la docena')

    return render(request, 'pages/dozens/create.html', data)


@login_required(login_url="/login/")
def update(request, id):
    dozen = get_object_or_404(Dozen, id=id)
    dozen.all_your_sizes = dozen.model.sizes.all()

    data = {
        'category': dozen.model.category,  # for the navigation route
        'model': dozen.model,  # for the navigation route
        'dozen': dozen,
        'form': DozenForm(instance=dozen)
    }

    if request.method == 'POST':
        formulario = DozenForm(data=request.POST, instance=dozen)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Docena actualizada satisfactoriamente')

            return redirect(to="dozens.show", name=dozen.model.name, filter="todos")
        else:
            data['form'] = formulario
            messages.error(request, 'Error al actualizar la docena')

    return render(request, 'pages/dozens/update.html', data)
