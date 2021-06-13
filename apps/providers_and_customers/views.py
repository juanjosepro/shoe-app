from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
from .models import ProvidersAndCustomers
from .forms import ProviderAndCustomerForm


@login_required(login_url="/login/")
def show(request, type, filter):

    #type = cliente o proveedor
    if filter == 'todos':
        model = ProvidersAndCustomers.objects.filter(types = type).order_by('-created_at')
    if filter == 'activos':
        model = ProvidersAndCustomers.objects.filter(Q(status = 'activo') & Q(types = type)).order_by('-created_at')
    if filter == 'inactivos':
        model = ProvidersAndCustomers.objects.filter(Q(status = 'inactivo') & Q(types = type)).order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(model, 15)
        model = paginator.page(page)
    except:
        raise Http404
    
    data = {
        #model = cliente o proveedor
        'entity': model,
        'paginator': paginator,
        'type': type, #for dropdown menu
        'filter_by': filter,
    }
    return render(request, 'pages/providers_and_customers/index.html', data)


@login_required(login_url="/login/")
def store(request):

    data = {'form': ProviderAndCustomerForm}

    if request.method == 'POST':
        formulario = ProviderAndCustomerForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Creado satisfactoriamente')
            if formulario['types'].value() == 'cliente':
                return redirect(to='customers.show', type = formulario['types'].value(), filter = 'todos')
            
            return redirect(to='providers.show', type = formulario['types'].value(), filter = 'todos')
            
        else:
            data['form'] = formulario
            messages.error(request, 'Error al crear')

    return render(request, 'pages/providers_and_customers/create.html', data)


@login_required(login_url="/login/")
def update(request, id):
    model = get_object_or_404(ProvidersAndCustomers, id = id)
    data = {'form': ProviderAndCustomerForm(instance=model)}

    if request.method == 'POST':
        formulario = ProviderAndCustomerForm(data=request.POST, instance=model)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Actualizado satisfactoriamente')
            if formulario['types'].value() == 'cliente':
                return redirect(to='customers.show', type = formulario['types'].value(), filter = 'todos')
            
            return redirect(to='providers.show', type = formulario['types'].value(), filter = 'todos')
            
        else:
            data['form'] = formulario
            messages.error(request, 'Error al Actualizar')

    return render(request, 'pages/providers_and_customers/update.html', data)