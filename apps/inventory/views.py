from django.contrib.auth.decorators import login_required
from apps.materials.models import Material
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
from .models import Inventory
from .forms import InventoryForm

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    inventory = Inventory.objects.all()
    data = {'entity': inventory}
    return render(request, 'pages/inventory/index.html', data)


@login_required(login_url="/login/")
def store(request, name):
    material = get_object_or_404(Material, name = name)

    types = []
    
    for type in material.types.split(','):
        types.append(type.strip())
    
    material.types = types

    data = {'material': material, 'form': InventoryForm}

    if request.method == 'POST':
        formulario = InventoryForm(data={
            'material': request.POST['material'],
            'type': request.POST['type'],
            'amount': request.POST['amount'],
            'color': request.POST['color'],
            'price': request.POST['price'],
            'note': request.POST['note'],
        })

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Material agregado satisfactoriamente')
            return redirect(to='inventory.show', name = material.name)
        else:
            data['form'] = formulario
            messages.error(request, 'Error al crear')

    return render(request, 'pages/inventory/create.html', data)


@login_required(login_url="/login/")
def show(request, name):
    material = get_object_or_404(Material, name = name)
    inventory = Inventory.objects.filter(material_id = material.id).order_by('-created_at')
    
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(inventory, 15)
        inventory = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': inventory,
        'material': material, #for the button of create
    }
    return render(request, 'pages/inventory/show.html', data)


@login_required(login_url="/login/")
def filter(request, name, filter):
    material = get_object_or_404(Material, name = name)

    if filter == 'todos':
        #filter = id of material
        inventory = Inventory.objects.filter(material_id = material.id).order_by('-created_at')
    if filter == 'disponibles':
        #param = amount >= 1
        inventory = Inventory.objects.filter(Q(amount__gte = 1) & Q(material_id = material.id)).order_by('-created_at')
    if filter == 'vendidos':
        #param = amount <= 0
        inventory = Inventory.objects.filter(amount__lte = 0) & Inventory.objects.filter(material_id = material.id).order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(inventory, 15)
        inventory = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': inventory,
        'material': material, #for dropdown menu
        'filter_by': filter,
    }
    return render(request, 'pages/inventory/show.html', data)


@login_required(login_url="/login/")
def update(request, id):
    inventory = get_object_or_404(Inventory, id = id)
    
    types = []
    for type in inventory.material.types.split(','):
        types.append(type.strip())

    data = {
        'form': InventoryForm(instance=inventory),
        'material_types': types,
        'inventory': inventory #for the navigation route
    }

    if request.method == 'POST':
        formulario = InventoryForm(data=request.POST, instance=inventory)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Actualizado satisfactoriamente")
            
            return redirect(to='inventory.show', name = inventory.material.name)
        else:
            data['form'] = formulario
            messages.error(request, "Error al actualizar")
            
    return render(request, 'pages/inventory/update.html', data)