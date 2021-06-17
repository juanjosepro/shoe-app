from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from decimal import Decimal
from apps.category.models import Category
from apps.sizes.models import Sizes
from .models import Model
from .forms import ModelForm


# not working...
@login_required(login_url="/login/")
def index(request):
    models = Model.objects.all().order_by('-created-at')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(models, 16)
        models = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': models,
        'paginator': paginator,
    }

    return render(request, 'pages/models/index.html', data)


@login_required(login_url="/login/")
def show(request, name):
    category = get_object_or_404(Category, name=name)
    models = Model.objects.filter(category_id=category.id).order_by('-created_at')

    modified_model = []
    for model in models:
        model.all_your_sizes = model.sizesandmodels_set.all()
        modified_model.append(model)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(modified_model, 16)
        modified_model = paginator.page(page)
    except:
        raise Http404

    data = {
        'category': category,  # for the navigation route
        # must be called entity required for pagination
        'entity': modified_model,
        # necessary for paginator
        'paginator': paginator,
    }

    return render(request, 'pages/models/index.html', data)


@login_required(login_url="/login/")
def store(request, name):
    category = get_object_or_404(Category, name=name.strip())
    sizes = Sizes.objects.all().order_by('-created_at')

    data = {
        'form': ModelForm(),
        'category': category,  # for the navigation route
        'sizes': sizes,
    }

    if request.method == 'POST':
        sizes = request.POST.getlist('sizes')
        prices = request.POST.getlist('prices')
        container_of_new_sizes = []
        
        if len(sizes) == len(prices):
            for i in range(len(sizes)):
                obj = {}
                obj['size'] = int(sizes[i].strip())
                obj['price'] = Decimal(prices[i].strip())
                container_of_new_sizes.append(obj)

        model_form = ModelForm(data=request.POST)

        if model_form.is_valid():
            model = Model.objects.create(
                category_id=model_form.cleaned_data['category'].id,
                name=model_form.cleaned_data['name'],
            )

            for new in container_of_new_sizes:
                size = Sizes.objects.get(id=new['size'])  # id = id from size
                model.sizes.add(size, through_defaults={'price': new['price']})

            messages.success(request, 'Modelo creado satisfactoriamente')
            return redirect(to="models.show", name=category.name)
        else:
            data['form'] = model_form
            messages.error(request, 'Error al crear el modelo')

    return render(request, 'pages/models/create.html', data)


@login_required(login_url="/login/")
def update(request, name):
    model = get_object_or_404(Model, name=name)
    model.all_your_sizes = model.sizesandmodels_set.all()

    sizes = Sizes.objects.all().order_by('-created_at')

    data = {
        'form': ModelForm(instance=model),
        'sizes': sizes,
        'model': model,  # for the navigation route
    }

    if request.method == 'POST':
        sizes = request.POST.getlist('sizes')
        prices = request.POST.getlist('price')

        # only if you decide to add more sizes to that model
        more_sizes = request.POST.getlist('more_sizes')
        more_price = request.POST.getlist('more_price')

        container_of_existing_sizes = []
        if len(sizes) == len(prices):
            for i in range(len(sizes)):
                obj = {}
                obj['size'] = int(sizes[i].strip())
                obj['price'] = Decimal(prices[i].strip())
                container_of_existing_sizes.append(obj)

        container_of_new_sizes = []
        if len(more_sizes) == len(more_price):
            for i in range(len(more_sizes)):
                if more_sizes[i].strip() and more_price[i].strip():
                    obj = {}
                    obj['size'] = int(more_sizes[i].strip())
                    obj['price'] = Decimal(more_price[i].strip())
                    container_of_new_sizes.append(obj)

        # update the field
        model_form = ModelForm(data=request.POST, instance=model)

        if model_form.is_valid():
            model_form.save()

            for existing_size in container_of_existing_sizes:
                for size in model.all_your_sizes:
                    if size.size.id == existing_size['size']:  # id = id from size
                        if size.price != existing_size['price']:
                            sizesandmodels = model.sizesandmodels_set.get(
                                id=size.id)
                            sizesandmodels.price = existing_size['price']
                            sizesandmodels.save()

            if container_of_new_sizes:  # if not empty
                for new in container_of_new_sizes:
                    size = Sizes.objects.get(id=new['size'])  # id = id from size
                    model.sizes.add(size, through_defaults={'price': new['price']})

            messages.success(request, 'Modelo actualizado satisfactoriamente')
            return redirect(to='models.show', name=model.category)
        else:
            data['form'] = model_form
            messages.error(request, 'Error al actualizar el modelo')

    return render(request, 'pages/models/update.html', data)
