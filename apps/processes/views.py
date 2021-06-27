from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from apps.user.models import User
from apps.dozens.models import Dozen
from apps.dozens.models import DozensOfAparadores, DozensOfArmadores
from apps.dozens.forms import (
    DozensOfAparadoresForm,
    DozensOfArmadoresForm,
    DozensOfRematadoresForm,
)
import json


@login_required(login_url="/login/")
def all_aparador_processes(request, filter):
    statuses = DozensOfAparadores.statuses_choices
    processes = None
    filter = filter.strip()

    if filter == "todos":
        processes = DozensOfAparadores.objects.all().order_by("-created_at")
    if filter == "aparado-en-produccion":
        processes = DozensOfAparadores.objects.filter(status="produccion").order_by(
            "-created_at"
        )
    if filter == "aparado-finalizado":
        processes = DozensOfAparadores.objects.filter(status="finalizado").order_by(
            "-created_at"
        )

    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(processes, 25)
        processes = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": processes,
        "paginator": paginator,
        "statuses": statuses,
        "filter_by": filter,
    }

    return render(request, "pages/processes/all_aparador_processes.html", data)


@login_required(login_url="/login/")
def all_armador_processes(request, filter):
    statuses = DozensOfArmadores.statuses_choices
    processes = None
    filter = filter.strip()

    if filter == "todos":
        processes = DozensOfArmadores.objects.all().order_by("-created_at")
    if filter == "armado-en-produccion":
        processes = DozensOfArmadores.objects.filter(status="produccion").order_by(
            "-created_at"
        )
    if filter == "armado-finalizado":
        processes = DozensOfArmadores.objects.filter(status="finalizado").order_by(
            "-created_at"
        )

    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(processes, 25)
        processes = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": processes,
        "paginator": paginator,
        "statuses": statuses,
        "filter_by": filter,
    }

    return render(request, "pages/processes/all_armador_processes.html", data)


@login_required(login_url="/login/")
def store(request):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == "POST":
        dozen = get_object_or_404(Dozen, id=data["dozen"].strip())  # id = id
        user = User.objects.get(id=data["user"].strip())  # id = id

        is_aparador, is_armador = False, False
        form_process = None

        if user.groups.filter(name="aparadores").exists():
            is_aparador = True
        elif user.groups.filter(name="armadores").exists():
            is_armador = True

        dataForm = {
            "dozen": dozen.id,
            "user": user.id,
            "status": "produccion",  # for table dozen_of_rematadoras not exists field status
            "note": data["note"].strip(),
        }

        if is_aparador:
            form_process = DozensOfAparadoresForm(data=dataForm)
        elif is_armador:
            form_process = DozensOfArmadoresForm(data=dataForm)

        if form_process.is_valid():
            form_process.save()
            if is_aparador:
                dozen.status = "aparado_en_produccion"
            elif is_armador:
                dozen.status = "armado_en_produccion"
            dozen.save()
            msg = {"success": "Genial!. La docena a sido entregada satisfactoriamente."}
            return JsonResponse(msg)
        else:
            msg = {
                "error": "Error! No se pudo entregar la docena verifique que todos los campos requeridos sean correctos e intentelo nuevamente"
            }
            return JsonResponse(msg)


@login_required(login_url="/login/")
def update_aparador_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == "POST":
        process_aparador = get_object_or_404(
            DozensOfAparadores, id=id.strip()
        )  # id = id

        dataForm = {
            "dozen": process_aparador.dozen.id,
            "user": process_aparador.user.id,
            "status": "finalizado",
            "note": data["note"].strip(),
        }

        if process_aparador.user.groups.filter(name="aparadores").exists():
            formulario = DozensOfAparadoresForm(
                data=dataForm, instance=process_aparador
            )

            if formulario.is_valid():
                formulario.save()
                process_aparador.dozen.status = "aparado_finalizado"
                process_aparador.dozen.save()

                msg = {"success": "Docena entregada correctamente"}
                return JsonResponse(msg)
            else:
                msg = {"error": "No se pudo entregar la docena"}
                return JsonResponse(msg)

        msg = {
            "error": "Error!. No perteneces al grupo de Aparadores por eso no puedes actualizar el estado de esta docena."
        }
        return JsonResponse(msg)


@login_required(login_url="/login/")
def update_armador_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == "POST":
        process_armador = get_object_or_404(DozensOfArmadores, id=id.strip())  # id = id

        if process_armador.user.groups.filter(name="armadores").exists():
            formulario = DozensOfArmadoresForm(
                data={
                    "dozen": process_armador.dozen.id,
                    "user": process_armador.user.id,
                    "status": "finalizado",
                    "note": data["note"].strip(),
                },
                instance=process_armador,
            )

            if formulario.is_valid():
                formulario.save()
                process_armador.dozen.status = "armado_finalizado"
                process_armador.dozen.save()

                msg = {
                    "success": "Genial!. Esta docena a terminado el proceso de armado satisfactoriamente"
                }
                return JsonResponse(msg)
            else:
                msg = {"error": "Error!. No se pudo Actualizar la docena"}
                return JsonResponse(msg)

        msg = {
            "error": "Error!. No perteneces al grupo de Armadores por eso no puedes actualizar el estado de esta docena."
        }
        return JsonResponse(msg)


@login_required(login_url="/login/")
def store_and_update_rematadoras_dozen(request, id):
    data = json.loads(request.body.decode("utf-8"))

    if request.method == "POST":
        dozen = get_object_or_404(Dozen, id=id.strip())
        user = get_object_or_404(User, id=data["user"].strip())

        if user.groups.filter(name="rematadores").exists():
            formulario = DozensOfRematadoresForm(
                data={
                    "dozen": dozen.id,
                    "user": user.id,
                    "note": data["note"].strip(),
                }
            )

            if formulario.is_valid():
                formulario.save()
                dozen.status = "produccion_finalizada"
                dozen.save()

                msg = {
                    "success": "Esta docena a terminado todo el proceso de produccion satisfactoriamente"
                }
                return JsonResponse(msg)
            else:
                msg = {"error": "No se pudo Actualizar la docena"}
                return JsonResponse(msg)

        msg = {
            "error": "Error!. No perteneces al grupo de Rematadores por eso no puedes actualizar el estado de esta docena."
        }
        return JsonResponse(msg)
