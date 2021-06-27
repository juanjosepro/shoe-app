from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import Http404
from .models import Material
from .forms import MaterialForm
from django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    materials = Material.objects.all().order_by('-created_at')
    
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
        'form': MaterialForm(),
    }

    if request.method == 'POST':
        types = []

        #looks for empty fields of the form and ignores them
        for type in request.POST.getlist('types[]'):
            if len(type.strip()) > 3: #must be more than 3 characters
                types.append(type.strip())

        form = MaterialForm(data={
            'name': request.POST['name'].strip(),
            'types': ",".join(types),
        })

        if form.is_valid():
            form.save()
            messages.success(request, 'Material registrado satisfactoriamente')
            return redirect(to='materials.index')
        else:
            data['form'] = form
            messages.error(request, 'Error!. Lo sentimos no pudimos registrar\
                este material, llene correctamente el formulario e intentelo nuevamente')

    return render(request, 'pages/materials/index.html', data)


@login_required(login_url="/login/")
def update(request, name):
    material = get_object_or_404(Material, name = name.strip())

    #important to turn it into a list to display the data and update it.
    list_types = []
    for type in material.types.split(','):
        list_types.append(type.strip())

    material.types = list_types

    data = {
        'form': MaterialForm(instance=material),
        'material': material,
    }

    if request.method == 'POST':
        types = []

        #looks for empty fields of the form and ignores them
        for type in request.POST.getlist('types[]'):
            if len(type.strip()) > 3:
                types.append(type.strip())

        formulario = MaterialForm(data={
            'name': request.POST['name'].strip(),
            'types': ",".join(types)
        }, instance=material)
        
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Modelo actualizado satisfactoriamente')
            return redirect(to='materials.index')
        else:
            data['form'] = formulario
            messages.error(request, 'Error no se pudo actualizar el modelo \
                verifique que todos los campos del formulario sena correctos')



    return render(request, 'pages/materials/update.html', data)