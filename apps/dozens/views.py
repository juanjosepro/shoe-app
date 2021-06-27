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
    filter = filter.strip()

    if filter == "todos":
        dozens = Dozen.objects.all().order_by("-created_at")
    elif filter == "disponibles":
        dozens = Dozen.objects.filter(status="disponible").order_by("-created_at")
    elif filter == "aparado-en-produccion":
        dozens = Dozen.objects.filter(status="aparado_en_produccion").order_by(
            "-created_at"
        )
    elif filter == "aparado-finalizado":
        dozens = Dozen.objects.filter(status="aparado_finalizado").order_by(
            "-created_at"
        )
    elif filter == "armado-en-produccion":
        dozens = Dozen.objects.filter(status="armado_en_produccion").order_by(
            "-created_at"
        )
    elif filter == "armado-finalizado":
        dozens = Dozen.objects.filter(status="armado_finalizado").order_by(
            "-created_at"
        )
    elif filter == "produccion-finalizada":
        dozens = Dozen.objects.filter(status="produccion_finalizada").order_by(
            "-created_at"
        )
    elif filter == "docenas-vendidas":
        dozens = Dozen.objects.filter(status="vendido").order_by(
            "-created_at"
        )
    else:
        raise Http404

    data = {}

    if filter == "todos":
        page = request.GET.get("page", 1)

        try:
            paginator = Paginator(dozens, 25)
            dozens = paginator.page(page)
        except:
            raise Http404

        data = {
            "entity": dozens,
            "paginator": paginator,
        }
    else:
        data = {
            "entity": dozens,
            "filter_by": filter,
        }

    return render(request, "pages/dozens/index.html", data)


@login_required(login_url="/login/")
def show(request, name, filter):
    model = get_object_or_404(Model, name=name.strip())
    dozens = None
    filter = filter.strip()

    if filter == "todos":
        dozens = Dozen.objects.filter(model_id=model.id).order_by("-created_at")
    if filter == "disponibles":
        dozens = Dozen.objects.filter(
            Q(status="disponible") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "aparado-en-produccion":
        dozens = Dozen.objects.filter(
            Q(status="aparado_en_produccion") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "aparado-finalizado":
        dozens = Dozen.objects.filter(
            Q(status="aparado_finalizado") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "armado-en-produccion":
        dozens = Dozen.objects.filter(
            Q(status="armado_en_produccion") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "armado-finalizado":
        dozens = Dozen.objects.filter(
            Q(status="armado_finalizado") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "produccion-finalizada":
        dozens = Dozen.objects.filter(
            Q(status="produccion_finalizada") & Q(model_id=model.id)
        ).order_by("-created_at")
    if filter == "docenas-vendidas":
        dozens = Dozen.objects.filter(
            Q(status="vendido") & Q(model_id=model.id)
        ).order_by("-created_at")


    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(dozens, 25)
        dozens = paginator.page(page)
    except:
        raise Http404

    data = {
        "model": model,  # for the navigation route
        "entity": dozens,
        "paginator": paginator,
        "filter_by": filter,
    }

    return render(request, "pages/dozens/show.html", data)


@login_required(login_url="/login/")
def dozens_ready_to_sell(request):
    dozens = Dozen.objects.filter(status="produccion_finalizada").order_by(
        "-created_at"
    )

    data = {
        "dozens": dozens,
    }

    return render(request, "pages/dozens/dozens_ready_to_sell.html", data)


@login_required(login_url="/login/")
def dozens_for_the_aparador(request):
    aparadors = User.objects.filter(groups__name="aparadores")
    dozens = Dozen.objects.filter(status="disponible")

    data = {
        "dozens": dozens,
        "aparadors": aparadors,
    }

    return render(request, "pages/dozens/dozens_available_for_aparador.html", data)


@login_required(login_url="/login/")
def dozens_for_the_armador(request):
    armadors = User.objects.filter(groups__name="armadores")
    dozens = Dozen.objects.filter(status="aparado_finalizado")

    data = {
        "dozens": dozens,
        "armadors": armadors,
    }

    return render(request, "pages/dozens/dozens_available_for_armador.html", data)


@login_required(login_url="/login/")
def dozens_for_the_rematador(request):
    rematadors = User.objects.filter(groups__name="rematadores")
    dozens = Dozen.objects.filter(status="armado_finalizado")

    data = {
        "dozens": dozens,
        "rematadors": rematadors,
    }

    return render(request, "pages/dozens/dozens_for_the_rematador.html", data)


@login_required(login_url="/login/")
def store(request, name):
    model = get_object_or_404(Model, name=name)
    model.all_your_sizes = model.sizes.all()
    cortadors = User.objects.filter(groups__name="cortadores")

    data = {
        "form": DozenCreateForm(),
        "cortadors": cortadors,
        "model": model,  # for the navigation route
    }

    if request.method == "POST":
        if request.POST["user"]:
            user = get_object_or_404(User, id=request.POST["user"])
            form_dozen = DozenCreateForm(data=request.POST)

            if form_dozen.is_valid():
                dozen = Dozen.objects.create(
                    model_id=request.POST["model"],
                    size_id=request.POST["size"],
                    material=request.POST["material"],
                    color=request.POST["color"],
                    note=request.POST["note"],
                )

                form_cortadors = DozensOfCortadoresForm(
                    data={
                        "dozen": dozen,
                        "user": user,
                        "note": request.POST["note_user"],
                    }
                )

                if form_cortadors.is_valid():
                    DozensOfCortadores.objects.create(
                        dozen=dozen,
                        user=user,
                        note=request.POST["note_user"],
                    )
                    messages.success(request, "Docena agregada satisfactoriamente")

                    return redirect(to="dozens.index", filter="disponibles")
                else:
                    dozen.delete()
                    messages.error(
                        request,
                        "Lo sentimos no se pudo registrar esta docena intentelo neuvamente",
                    )
            else:
                data["form"] = form_dozen
        else:
            data["error_user"] = "Es necesario que seleccione un usuario"
            messages.error(request, "Error al registrar esta docena")

    return render(request, "pages/dozens/create.html", data)


@login_required(login_url="/login/")
def update(request, id):
    dozen = get_object_or_404(Dozen, id=id)
    data = {
        "form": DozenUpdateForm(instance=dozen),
        "dozen": dozen,  # for the navigation route
    }

    if request.method == "POST":
        formulario = DozenUpdateForm(data=request.POST, instance=dozen)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Docena actualizado satisfactoriamente")

            return redirect(to="dozens.index", filter="disponibles")
        else:
            data["form"] = formulario
            messages.error(request, "Error al actualizar la docena")

    return render(request, "pages/dozens/update.html", data)


@login_required(login_url="/login/")
def history_of_the_process_of_each_dozen(request, id):
    dozen = get_object_or_404(Dozen, id=id.strip())
    data = {"dozen": dozen}
    return render(
        request, "pages/dozens/history_of_the_process_of_each_dozen.html", data
    )


@login_required(login_url="/login/")
def search(request):
    data = {}
    if request.method == "POST":
        id = int(request.POST['id'].strip())
        if Dozen.objects.filter(id=id).exists():
            dozen = Dozen.objects.get(id=id)
            data["dozen"] = dozen
            messages.success(request, "Docena encontrada!")
            return redirect(
                to="dozens.history_of_the_process_of_each_dozen", id=dozen.id
            )

        messages.error(
            request,
            "No se encontro ningun resultado que coincida, intentelo nuevamente!",
        )
    return render(request, "pages/dozens/search_dozen.html", data)
