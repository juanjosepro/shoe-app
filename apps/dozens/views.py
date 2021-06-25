from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from apps.user.models import User
from django.db.models import Q
from apps.category.models import Category
from apps.model.models import Model
from .models import Dozen, DozensOfCortadores
from .forms import DozenCreateForm, DozenUpdateForm, DozensOfCortadoresForm


@login_required(login_url="/login/")
def index(request, filter):
    dozens = None

    if filter.strip() == 'todos':
        dozens = Dozen.objects.all().order_by('-created_at')
    elif filter.strip() == 'disponibles':
        dozens = Dozen.objects.filter(status='disponible').order_by('-created_at')
    elif filter.strip() == 'aparado-en-produccion':
        dozens = Dozen.objects.filter(status='aparado_en_produccion').order_by('-created_at')
    elif filter.strip() == 'aparado-finalizado':
        dozens = Dozen.objects.filter(status='aparado_finalizado').order_by('-created_at')
    elif filter.strip() == 'armado-en-produccion':
        dozens = Dozen.objects.filter(status='armado_en_produccion').order_by('-created_at')
    elif filter.strip() == 'armado-finalizado':
        dozens = Dozen.objects.filter(status='armado_finalizado').order_by('-created_at')
    elif filter.strip() == 'produccion-finalizada':
        dozens = Dozen.objects.filter(status='produccion_finalizada').order_by('-created_at')
    else:
        raise Http404

    data = {}

    if filter.strip() == 'todos':
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
    else:
        data = {
            'entity': dozens,
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
    if filter.strip() == 'aparado-en-produccion':
        dozens = Dozen.objects.filter(Q(status='aparado_en_produccion') & Q(
            model_id=model.id)).order_by('-created_at')
    if filter.strip() == 'aparado-finalizado':
        dozens = Dozen.objects.filter(Q(status='aparado_finalizado') & Q(
            model_id=model.id)).order_by('-created_at')
    if filter.strip() == 'armado-en-produccion':
        dozens = Dozen.objects.filter(Q(status='armado_en_produccion') & Q(
            model_id=model.id)).order_by('-created_at')
    if filter.strip() == 'armado-finalizado':
        dozens = Dozen.objects.filter(Q(status='armado_finalizado') & Q(
            model_id=model.id)).order_by('-created_at')
    if filter.strip() == 'produccion-finalizada':
        dozens = Dozen.objects.filter(Q(status='produccion_finalizada') & Q(
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
def dozens_ready_to_sell(request):
    dozens = Dozen.objects.filter(status='produccion_finalizada').order_by('-created_at')

    data = {
        'dozens': dozens,
    }

    return render(request, 'pages/dozens/dozens_ready_to_sell.html', data)


@login_required(login_url="/login/")
def dozens_for_the_aparador(request):
    aparadors = User.objects.filter(groups__name='aparadores')
    dozens = Dozen.objects.filter(status='disponible')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 16)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': dozens,
        'paginator': paginator,
        'aparadors': aparadors,
    }

    return render(request, 'pages/dozens/dozens_available_for_aparador.html', data)


@login_required(login_url="/login/")
def dozens_for_the_armador(request):
    armadors = User.objects.filter(groups__name='armadores')
    dozens = Dozen.objects.filter(status='aparado_finalizado')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 16)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': dozens,
        'paginator': paginator,
        'armadors': armadors,
    }

    return render(request, 'pages/dozens/dozens_available_for_armador.html', data)


@login_required(login_url="/login/")
def dozens_for_the_rematador(request):
    rematadors = User.objects.filter(groups__name='rematadores')
    dozens = Dozen.objects.filter(status='armado_finalizado')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(dozens, 16)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': dozens,
        'paginator': paginator,
        'rematadors': rematadors,
    }

    return render(request, 'pages/dozens/dozens_for_the_rematador.html', data)


@login_required(login_url="/login/")
def store(request, name):
    model = get_object_or_404(Model, name=name)
    model.all_your_sizes = model.sizes.all()
    cortadores = User.objects.filter(groups__name='cortadores')

    data = {
        'form': DozenCreateForm(),
        'cortadors': cortadores,
        'model': model,
    }

    if request.method == 'POST':
        if request.POST['user']:
            user = get_object_or_404(User, id = request.POST['user'])
            form_dozen = DozenCreateForm(data=request.POST)

            if form_dozen.is_valid():
                dozen = Dozen.objects.create(
                    model_id = request.POST['model'],
                    size_id = request.POST['size'],
                    material = request.POST['material'],
                    color =   request.POST['color'],
                    note =   request.POST['note'],
                )
                
                form_cortadores = DozensOfCortadoresForm(data={
                    'dozen': dozen,
                    'user': user,
                    'note': request.POST['note_user']
                })
                
                if form_cortadores.is_valid():
                    DozensOfCortadores.objects.create(
                        dozen = dozen,
                        user = user,
                        note = request.POST['note_user'],
                    )
                    messages.success(request, "Docena agregada satisfactoriamente")

                    return redirect(to='dozens.index', filter='disponibles')
                else:
                    dozen.delete()
                    messages.error(request, "Lo sentimos no se pudo registrar esta docena")
            else:
                data['form'] = form_dozen
        else:
            data['error_user'] = 'Es necesario que seleccione un usuario'
            messages.error(request, "Error al registrar esta docena")

    return render(request, 'pages/dozens/create.html', data)


@login_required(login_url="/login/")
def update(request, id):
    dozen = get_object_or_404(Dozen, id=id)
    data = {
        'form': DozenUpdateForm(instance=dozen),
        'dozen': dozen  # for the navigation route
    }

    if request.method == 'POST':
        formulario = DozenUpdateForm(data=request.POST, instance=dozen)
        if formulario.is_valid():
            formulario.save()
            messages.success(
                request, "Docena actualizado satisfactoriamente")

            return redirect(to='dozens.index', filter='disponibles')
        else:
            data['form'] = formulario
            messages.error(request, "Error al actualizar la docena")

    return render(request, 'pages/dozens/update.html', data)


@login_required(login_url="/login/")
def history_of_the_process_of_each_dozen(request, id):
    dozen = get_object_or_404(Dozen, id=id)
    data = {'dozen': dozen}
    return render(request, 'pages/dozens/history_of_the_process_of_each_dozen.html', data)


@login_required(login_url="/login/")
def search(request):
    data = {}
    if request.method == 'POST':
        if Dozen.objects.filter(id=request.POST['id'].strip()).exists():
            dozen = Dozen.objects.get(id=request.POST['id'].strip())
            data['dozen'] = dozen
            messages.success(request, "Docena encontrada!")
            return redirect(to='dozens.history_of_the_process_of_each_dozen',id=dozen.id)

        messages.error(request, "No se encontro ningun resultado que coincida, intentelo nuevamente!")
    return render(request, 'pages/dozens/search_dozen.html', data)