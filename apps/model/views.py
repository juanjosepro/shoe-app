from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from apps.category.models import Category
from .models import Model
from .forms import ModelForm


#not working...
@login_required(login_url="/login/")
def index(request):
    models = Model.objects.all()

    data = {
        'models': models,
    }

    return render(request, 'pages/models/index.html', data)


@login_required(login_url="/login/")
def show(request, name):
    category = get_object_or_404(Category, name = name)
    models = Model.objects.filter(category_id = category.id)
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(models, 10)
        models = paginator.page(page)
    except:
        raise Http404

    data = {
        'category': category, #for the navigation route
        #must be called entity required for pagination
        'entity': models,
        #necessary for paginator
        'paginator': paginator,
    }

    return render(request, 'pages/models/index.html', data)


@login_required(login_url="/login/")
def store(request, name):
    category = get_object_or_404(Category, name = name)
    sizes = category.product.sizes.all()

    data = {
        'form': ModelForm(),
        'category': category, # for the navigation route
        'sizes': sizes,
    }

    if request.method == 'POST':
        #multiselect - convert an list to a comma separated string
        sizes = ", ".join(request.POST.getlist('sizes'))

        formulario = ModelForm(data={
            'category': request.POST['category'],
            'name': request.POST['name'],
            'sizes': sizes,
            'price': request.POST['price'],
        })

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Modelo creado satisfactoriamente')
            return redirect(to="models.show", id = category.id)
        else:
            data['form'] = formulario
            messages.error(request, 'Error al crear el modelo')

    return render(request, 'pages/models/create.html', data)


@login_required(login_url="/login/")
def update(request, name):
    model = get_object_or_404(Model, name = name)
    #get all sizes for this product
    sizes = model.category.product.sizes.all()

    # I bring all the sizes and I see which ones coincide with
    # those of the created model and I create a new property for it to be selected
    for size in sizes:
        for s in model.sizes.split(','):
            if size.name.strip() == s.strip():
                size.selected = True

    data = {
        'form': ModelForm(instance=model),
        'sizes': sizes,
        'model': model, # for the navigation route
    }

    if request.method == 'POST':
        sizes = ", ".join(request.POST.getlist('sizes'))
        formulario = ModelForm(data={
            'category': request.POST['category'],
            'name': request.POST['name'],
            'sizes': sizes,
            'price': request.POST['price'],
        }, instance=model)
        
        if formulario.is_valid():
            formulario.save()
            category_id = formulario['category'].value()
            messages.success(request, 'Modelo actualizado satisfactoriamente')
            
            return redirect(to="models.show", id = category_id)
        else:
            data['form'] = formulario
            messages.error(request, 'Error no se pudo actualizar el modelo')

    return render(request, 'pages/models/update.html', data)