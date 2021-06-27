from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from .models import ProvidersAndCustomers
from .forms import ProviderAndCustomerCreateForm, ProviderAndCustomerUpdateForm


@login_required(login_url="/login/")
def show(request, type, filter):
    filter = filter.strip()
    is_of_type = ""

    if type.strip() == "proveedores":
        is_of_type = "proveedor"
    elif type.strip() == "clientes":
        is_of_type = "cliente"
    else:
        Http404

    # type = cliente o proveedor
    if filter == "todos":
        model = ProvidersAndCustomers.objects.filter(types=is_of_type).order_by(
            "-created_at"
        )
    if filter == "activos":
        model = ProvidersAndCustomers.objects.filter(
            Q(status="activo") & Q(types=is_of_type)
        ).order_by("-created_at")
    if filter == "inactivos":
        model = ProvidersAndCustomers.objects.filter(
            Q(status="inactivo") & Q(types=is_of_type)
        ).order_by("-created_at")

    data = {
        "models": model,  # model = cliente o proveedor
        "type": type,  # for dropdown menu
        "filter_by": filter,
    }
    return render(request, "pages/providers_and_customers/index.html", data)


@login_required(login_url="/login/")
def store(request):

    data = {"form": ProviderAndCustomerCreateForm()}

    if request.method == "POST":
        formulario = ProviderAndCustomerCreateForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro creado satisfactoriamente")
            if formulario["types"].value() == "cliente":
                return redirect(to="customers.show", type="clientes", filter="todos")

            return redirect(to="providers.show", type="proveedores", filter="todos")

        else:
            data["form"] = formulario
            messages.error(
                request,
                "Error al crear el registro, por favor ingrese correctamente los datos",
            )

    return render(request, "pages/providers_and_customers/create.html", data)


@login_required(login_url="/login/")
def update(request, id):
    provider_or_customer = get_object_or_404(ProvidersAndCustomers, id=id.strip())
    data = {
        "form": ProviderAndCustomerUpdateForm(instance=provider_or_customer),
        "provider_or_customer": provider_or_customer,
    }

    if request.method == "POST":
        formulario = ProviderAndCustomerUpdateForm(
            data=request.POST, instance=provider_or_customer
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro actualizado satisfactoriamente")
            if formulario["types"].value() == "cliente":
                return redirect(to="customers.show", type="clientes", filter="todos")

            return redirect(to="providers.show", type="proveedores", filter="todos")

        else:
            data["form"] = formulario
            messages.error(
                request,
                "Error al actualizar el registro, por favor ingrese correctamente los datos",
            )

    return render(request, "pages/providers_and_customers/update.html", data)