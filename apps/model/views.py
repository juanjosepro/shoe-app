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


#shows all models to choose which to register a dozen
@login_required(login_url="/login/")
def index(request):
    models = Model.objects.all().order_by("-created_at")
    modified_model = []

    for model in models:
        model.all_your_sizes = model.sizesandmodels_set.all()
        modified_model.append(model)

    data = {
        "models": modified_model,
    }

    return render(request, "pages/models/index.html", data)


#shows all models that belong to a category
@login_required(login_url="/login/")
def show(request, name):
    category = get_object_or_404(Category, name=name)
    models = Model.objects.filter(category_id=category.id).order_by("-created_at")
    modified_model = []

    for model in models:
        model.all_your_sizes = model.sizesandmodels_set.all()
        modified_model.append(model)

    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(modified_model, 16)
        models = paginator.page(page)
    except:
        raise Http404

    data = {
        "category": category,  # for the navigation route
        "entity": models,
        "paginator": paginator,
    }

    return render(request, "pages/models/show_models_by_category.html", data)


#validates that the size and price fields are the same length
# ejem. sizes['juvenil, 'adulto'] prices['80'] = False
def verify_that_each_size_has_its_price(sizes, prices):
        sizes_length, prices_length = 0, 0

        for size in sizes:
            if size.strip():
                sizes_length = sizes_length + 1
        
        for price in prices:
            if price.strip():
                prices_length = prices_length + 1
        
        if sizes_length == prices_length:
            return True
        
        return False


@login_required(login_url="/login/")
def store(request, name):
    category = get_object_or_404(Category, name=name.strip())
    sizes = Sizes.objects.all().order_by("-created_at")

    data = {
        "form": ModelForm(),
        "category": category,  # for the navigation route
        "sizes": sizes,
    }

    if request.method == "POST":
        sizes = request.POST.getlist("sizes")
        prices = request.POST.getlist("prices")
        container_of_new_sizes = []

        #validations
        if verify_that_each_size_has_its_price(sizes, prices):

            for i in range(len(sizes)):
                obj = {}
                obj["size"] = int(sizes[i].strip())
                obj["price"] = Decimal(prices[i].strip())
                container_of_new_sizes.append(obj)

            model_form = ModelForm(data=request.POST)

            if model_form.is_valid():
                model = Model.objects.create(
                    category_id=model_form.cleaned_data["category"].id,
                    name=model_form.cleaned_data["name"],
                )

                for new in container_of_new_sizes:
                    size = Sizes.objects.get(id=new["size"])  # id = id from size
                    model.sizes.add(size, through_defaults={"price": new["price"]})

                messages.success(request, "Modelo creado satisfactoriamente")

                return redirect(to="models.show", name=category.name)
            else:
                messages.error(
                    request,
                    "No se pudo crear el modelo, verifique que todos lo campos esten bien e intentelo de nuevo",
                )
                data["form"] = model_form
        else:
            messages.error(
                request,
                "Por favor es necesario que llene correctamente la talla y su respectivo precio",
            )
            return redirect(to="models.store", name=category.name)

    return render(request, "pages/models/create.html", data)


@login_required(login_url="/login/")
def update(request, name):
    model = get_object_or_404(Model, name=name)
    model.all_your_sizes = model.sizesandmodels_set.all()

    sizes = Sizes.objects.all().order_by("-created_at")

    data = {
        "form": ModelForm(instance=model),
        "sizes": sizes,
        "model": model,  # for the navigation route
    }

    if request.method == "POST":
        sizes = request.POST.getlist("sizes")
        prices = request.POST.getlist("price")

        #validations
        if verify_that_each_size_has_its_price(sizes, prices):
            # only if you decide to add more sizes to that model
            more_sizes = request.POST.getlist("more_sizes")
            more_price = request.POST.getlist("more_price")
            print(more_sizes)
            print(more_price)
            #validations
            if verify_that_each_size_has_its_price(more_sizes, more_price):
                print('yes')
                container_of_existing_sizes, container_of_new_sizes = [], []

                for i in range(len(sizes)):
                    obj = {}
                    obj["size"] = int(sizes[i].strip())
                    obj["price"] = Decimal(prices[i].strip())
                    container_of_existing_sizes.append(obj)

                for i in range(len(more_sizes)):
                    #in case it comes empty more_sizes[''] more_price[''] it will return false
                    if more_sizes[i].strip() and more_price[i].strip(): #important
                        obj = {}
                        obj["size"] = int(more_sizes[i].strip())
                        obj["price"] = Decimal(more_price[i].strip())
                        container_of_new_sizes.append(obj)

                model_form = ModelForm(data=request.POST, instance=model)

                if model_form.is_valid():
                    model_form.save()

                    for existing_size in container_of_existing_sizes:
                        for size in model.all_your_sizes:
                            if size.size.id == existing_size["size"]:  # id = id from size
                                if size.price != existing_size["price"]:
                                    sizesandmodels = model.sizesandmodels_set.get(id=size.id)
                                    sizesandmodels.price = existing_size["price"]
                                    sizesandmodels.save()

                    if container_of_new_sizes:  # if not empty
                        for new in container_of_new_sizes:
                            size = Sizes.objects.get(id=new["size"])  # id = id from size
                            model.sizes.add(size, through_defaults={"price": new["price"]})

                    messages.success(request, "Modelo actualizado satisfactoriamente")
                    return redirect(to="models.show", name=model.category)
                else:
                    data["form"] = model_form
                    messages.error(request, "Error al actualizar el modelo verifique que todos los campos esten llenados correctamente")
            else:
                messages.error(
                    request,
                    "Al agregar nuevas tallas es necesario que llene correctamente la talla y su respectivo precio",
                )
                return redirect(to="models.update", name=model.name)
        else:
            messages.error(
                request,
                "Por favor es necesario que llene correctamente la talla y su respectivo precio",
            )
            return redirect(to="models.update", name=model.name)

    return render(request, "pages/models/update.html", data)
