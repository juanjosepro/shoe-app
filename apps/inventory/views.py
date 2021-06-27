from django.contrib.auth.decorators import login_required
from apps.materials.models import Material
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.db.models import Q
from .models import Inventory
from .forms import InventoryForm, UpdateStockForm, ReadonlyForm
from datetime import datetime, timedelta


# not WORNIG...
@login_required(login_url="/login/")
def index(request):
    inventory = Inventory.objects.annotate(day=TruncDay('created_at')).values(
        'day', 'id', 'type', 'color').annotate(c=Count('id')).values('day', 'c').order_by('-created_at')
    #inventory = Inventory.objects.all().order_by('-created_at')
    for i in inventory:
        print(i['day'])
        print(i['c'])
    """ page = request.GET.get('page', 1)

    try:
        paginator = Paginator(inventory, 40)
        inventory = paginator.page(page)
    except:
        raise Http404 """

    data = {
        'entity': inventory,
    }
    return render(request, 'pages/inventory/index.html', data)


@login_required(login_url="/login/")
def store(request, name):
    material = get_object_or_404(Material, name=name)
    types = []

    if material.types:
        for type in material.types.split(','):
            types.append(type.strip())

    material.types = types

    data = {'material': material, 'form': InventoryForm()}

    if request.method == 'POST':
        if material.id == int(request.POST['materials']):#validations
            formulario = InventoryForm(data={
                'material': material.id,
                'provider': request.POST['provider'],
                'type': request.POST['type2'],
                'amount': request.POST['amount'],
                'stock': request.POST['amount'],#same as the amount when registering
                'color': request.POST['color'],
                'price': request.POST['price'],
                'note': request.POST['note'],
            })
        else:
            messages.error(request, 'A sucedido un error inesperado por favor \
                    recargue la página e intentelo nuevamente')
            return redirect(to='inventory.show', name=material.name)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Material agregado al inventario satisfactoriamente')
            return redirect(to='inventory.show', name=material.name)
        else:
            data['form'] = formulario
            messages.error(request, 'Error!. Por favor verifique que todos los campos sean correctos')

    return render(request, 'pages/inventory/create.html', data)


@login_required(login_url="/login/")
def show(request, name):
    material = get_object_or_404(Material, name=name)
    inventory = Inventory.objects.filter(
        material_id=material.id).order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(inventory, 25)
        inventory = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': inventory,
        'paginator': paginator,
        'material': material,  # for the button of create
    }
    return render(request, 'pages/inventory/show.html', data)


@login_required(login_url="/login/")
def filter(request, name, filter):
    material = get_object_or_404(Material, name=name.strip())
    filter = filter.strip()

    if filter == 'todos':
        # filter = id of material
        inventory = Inventory.objects.filter(
            material_id=material.id).order_by('-created_at')
    if filter == 'disponibles':
        #param = stock >= 1
        inventory = Inventory.objects.filter(Q(stock__gte=1) & Q(
            material_id=material.id)).order_by('-created_at')
    if filter == 'agotados':
        #param = stock <= 0
        inventory = Inventory.objects.filter(stock__lte=0) & Inventory.objects.filter(
            material_id=material.id).order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(inventory, 25)
        inventory = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': inventory,
        'paginator': paginator,
        'material': material,  # for dropdown menu
        'filter_by': filter,
    }
    return render(request, 'pages/inventory/show.html', data)


@login_required(login_url="/login/")
def readonly(request, id):
    inventory = get_object_or_404(Inventory, id=id.strip())

    data = {
        'form': ReadonlyForm(instance=inventory),
        'inventory': inventory  # for the navigation route
    }
    return render(request, 'pages/inventory/readonly.html', data)


@login_required(login_url="/login/")
def update_stock(request, id):
    inventory = get_object_or_404(Inventory, id=id.strip())

    date = inventory.created_at
    print(date)
    date2 =  date + timedelta(days = 1)
    print(date2)
    now = datetime.now()
    print(now)

    if now == date:
        print('soniguales')
    else:
        print('no lo son')

    data = {
        'form': UpdateStockForm(instance=inventory),
        'inventory': inventory  # for the navigation route
    }
    if request.method == 'POST':
        if int(request.POST['stock']) <= inventory.amount:
            inventory.stock = int(request.POST['stock'])
            inventory.save()
            messages.success(request, "Existencias actualizadas satisfactoriamente")
            return redirect(to='inventory.show', name=inventory.material.name)

        messages.error(request, "Las existencias no pueden ser mayor al monto inicial!")
        return redirect(to='inventory.update_stock', id=inventory.id)

    return render(request, 'pages/inventory/update_stock.html', data)