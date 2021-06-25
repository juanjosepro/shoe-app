from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import Http404
from .models import Material
from .forms import MaterialForm
from django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    materials = Material.objects.all()
    
    modified_material = []
    for material in materials:
        if not material.types:
            material.types = []
        else:
            material.types = material.types.split(',')
        modified_material.append(material)

    materials = modified_material

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(materials, 16)
        materials = paginator.page(page)
    except:
        raise Http404
    data = {
        'entity': materials,
        'paginator': paginator,
        'form': MaterialForm
    }

    if request.method == 'POST':
        types = []

        #looks for empty fields of the form and ignores them
        for type in request.POST.getlist('types[]'):
            if len(type.strip()) > 3:
                types.append(type.strip())
        
        formulario = MaterialForm(data={
            'name': request.POST['name'],
            'types': ",".join(types),
        })

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Material agregado satisfactoriamente')
            return redirect(to='materials.index')
        else:
            data['form'] = formulario
            messages.error(request, 'Error al crear el modelo')

    return render(request, 'pages/materials/index.html', data)


@login_required(login_url="/login/")
def update(request, name):
    material = get_object_or_404(Material, name = name)

    data = {
        'form': MaterialForm(instance=material),
    }

    if request.method == 'POST':
        types = []

        #looks for empty fields of the form and ignores them
        for type in request.POST.getlist('types[]'):
            if len(type.strip()) > 3:
                types.append(type.strip())

        formulario = MaterialForm(data={
            'name': request.POST['name'],
            'types': ",".join(types)
        }, instance=material)
        
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Modelo actualizado satisfactoriamente')
            return redirect(to='materials.index')
        else:
            data['form'] = formulario
            messages.error(request, 'Error no se pudo actualizar el modelo')

    #important to turn it into a list to display the data and update it.
    types = []
    for type in material.types.split(','):
        types.append(type.strip())

    material.types = types    
    data['material'] = material

    return render(request, 'pages/materials/update.html', data)