from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from apps.user.models import User
from apps.dozens.models import Dozen
from apps.dozens.models import DozensOfAparadores, DozensOfArmadores
from apps.dozens.forms import DozensOfAparadoresForm, DozensOfArmadoresForm, DozensOfRematadorasForm
import json


@login_required(login_url="/login/")
def all_aparador_processes(request, filter):
    statuses = DozensOfAparadores.statuses_choices
    processes = None

    if filter.strip() == 'todos':
        processes = DozensOfAparadores.objects.all().order_by('-created_at')
    if filter.strip() == 'aparado-en-produccion':
        processes = DozensOfAparadores.objects.filter(
            status='produccion').order_by('-created_at')
    if filter.strip() == 'aparado-completado':
        processes = DozensOfAparadores.objects.filter(
            status='finalizado').order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(processes, 16)
        processes = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': processes,
        'paginator': paginator,
        'statuses': statuses,
        'filter_by': filter,
    }

    return render(request, 'pages/processes/all_aparador_processes.html', data)


@login_required(login_url="/login/")
def all_armador_processes(request, filter):
    statuses = DozensOfArmadores.statuses_choices
    processes = None

    if filter.strip() == 'todos':
        processes = DozensOfArmadores.objects.all().order_by('-created_at')
    if filter.strip() == 'armado-en-produccion':
        processes = DozensOfArmadores.objects.filter(
            status='produccion').order_by('-created_at')
    if filter.strip() == 'armado-completado':
        processes = DozensOfArmadores.objects.filter(
            status='finalizado').order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(processes, 16)
        processes = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': processes,
        'paginator': paginator,
        'statuses': statuses,
        'filter_by': filter,
    }

    return render(request, 'pages/processes/all_armador_processes.html', data)


@login_required(login_url="/login/")
def store(request):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        dozen = get_object_or_404(Dozen, id=data['dozen'])  # id = id
        user = User.objects.get(id=data['user'])  # id = id

        isAparador, isArmador = False, False
        formulario = None

        if user.groups.filter(name="aparadores").exists():
            isAparador = True
        elif user.groups.filter(name="armadores").exists():
            isArmador = True

        dataForm = {
            'dozen': dozen.id,
            'user': user.id,
            'status': 'produccion', #for table dozen_of_rematadoras not exists field status
            'note': data['note'],
        }

        if isAparador:
            formulario = DozensOfAparadoresForm(data=dataForm)
        elif isArmador:
            formulario = DozensOfArmadoresForm(data=dataForm)
        
        if formulario.is_valid():
            formulario.save()
            msg = {'success': 'Docena entregada correctamente'}
            if isAparador:
                dozen.status = 'aparado_en_produccion'
            elif isArmador:
                dozen.status = 'armado_en_produccion'
            dozen.save()
            return JsonResponse(msg)
        else:
            print('error')
            msg = {'error': 'No se pudo entregar la docena'}
            return JsonResponse(msg)


@login_required(login_url="/login/")
def update_aparador_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        process_aparador = get_object_or_404(DozensOfAparadores, id=id)  # id = id
        isAparador = False

        if process_aparador.user.groups.filter(name="aparadores").exists():
            isAparador = True

        dataForm = {
            'dozen': process_aparador.dozen.id,
            'user': process_aparador.user.id,
            'status': 'finalizado',
            'note': data['note'],
        }

        if isAparador:
            formulario = DozensOfAparadoresForm(data=dataForm, instance=process_aparador)
        
            if formulario.is_valid():
                formulario.save()
                process_aparador.dozen.status = 'aparado_finalizado'
                process_aparador.dozen.save()
                
                msg = {'success': 'Docena entregada correctamente'}
                return JsonResponse(msg)
            else:
                msg = {'error': 'No se pudo entregar la docena'}
            return JsonResponse(msg)
        
        msg = {'error': 'No perteneces al grupo requerido para actualizar'}
        return JsonResponse(msg)


@login_required(login_url="/login/")
def update_armador_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        process_armador = get_object_or_404(DozensOfArmadores, id=id)  # id = id
        isArmador = False

        if process_armador.user.groups.filter(name="armadores").exists():
            isArmador = True

        if isArmador:
            formulario = DozensOfArmadoresForm(data={
                'dozen': process_armador.dozen.id,
                'user': process_armador.user.id,
                'status': 'finalizado',
                'note': data['note'],
            }, instance=process_armador)
        
            if formulario.is_valid():
                formulario.save()
                process_armador.dozen.status = 'armado_finalizado'
                process_armador.dozen.save()
                
                msg = {'success': 'Esta docena a terminado el proceso de armado satisfactoriamente'}
                return JsonResponse(msg)
            else:
                msg = {'error': 'No se pudo Actualizar la docena'}
            return JsonResponse(msg)
        
        msg = {'error': 'No perteneces al grupo requerido para actualizar'}
        return JsonResponse(msg)




@login_required(login_url="/login/")
def store_and_update_rematadoras_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        dozen = get_object_or_404(Dozen, id=id)
        user = get_object_or_404(User, id=data['user'])
        isRematadora = False

        if user.groups.filter(name="rematadores").exists():
            isRematadora = True

        if isRematadora:
            formulario = DozensOfRematadorasForm(data={
                'dozen': dozen.id,
                'user': user.id,
                'note': data['note'],
            })
        
            if formulario.is_valid():
                formulario.save()
                dozen.status = 'produccion_finalizada'
                dozen.save()
                
                msg = {'success': 'Esta docena a terminado todo el proceso de produccion satisfactoriamente'}
                return JsonResponse(msg)
            else:
                msg = {'error': 'No se pudo Actualizar la docena'}
            return JsonResponse(msg)
        
        msg = {'error': 'No perteneces al grupo requerido para actualizar'}
        return JsonResponse(msg)