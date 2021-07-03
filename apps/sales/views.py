from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from apps.dozens.models import Dozen
from apps.providers_and_customers.models import ProvidersAndCustomers
from .models import Sales
from .forms import SalesForm


@login_required(login_url="/login/")
def index(request):
    sales = Sales.objects.all().order_by("-created_at")
    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(sales, 25)
        sales = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": sales,
        "paginator": paginator,
    }

    return render(request, "pages/sales/index.html", data)


@login_required(login_url="/login/")
def filter(request, filter):
    sales = None
    if filter == "todos":
        sales = Sales.objects.all().order_by("-created_at")
    if filter == "estado-de-pago-completo":
        sales = Sales.objects.filter(total_money_owed=0).order_by("-created_at")
    if filter == "estado-de-pago-incompleto":
        sales = Sales.objects.filter(total_money_owed__gte=1).order_by("-created_at")
    else:
        Http404

    page = request.GET.get("page", 1)

    try:
        paginator = Paginator(sales, 25)
        sales = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": sales,
        "paginator": paginator,
        "filter_by": filter,
    }
    return render(request, "pages/sales/index.html", data)


@login_required(login_url="/login/")
def show(request, id):
    customer = get_object_or_404(ProvidersAndCustomers, id=id)
    sales = Sales.objects.filter(customer_id=id).order_by(
        "-created_at"
    )
    res = []

    for sale in sales:
        result = {}
        result["title"] = sale.created_at
        result["note"] = sale.note
        result["status"] = sale.status
        result["total_price"] = sale.total_price
        result["money_paid"] = sale.money_paid
        result["total_money_owed"] = sale.total_money_owed
        result["owe_money"] = bool(int(sale.total_money_owed))
        result["id"] = sale.id
        dozens_list = sale.dozens_list.split(",")  # of '2,4,5' to ['2', '4', '5']
        result["number_of_dozens"] = len(dozens_list)

        dozens = []
        for id in dozens_list:  # id = 2
            dozen = Dozen.objects.get(id=id.strip())  # <dozen>
            model = dozen.model.sizesandmodels_set.get(size_id=dozen.size_id)
            dozen.price = model.price
            dozens.append(dozen)

        result["data"] = dozens
        res.append(result)

    data = {
        "customer": customer,
        "dozens": res,
    }

    return render(request, "pages/sales/show.html", data)


@login_required(login_url="/login/")
def summary_of_selected_items(request):
    if request.method == 'POST':
        dozens = request.POST.getlist("dozens[]")

        if dozens:
            list = []

            for id in dozens:
                item = Dozen.objects.get(id=id.strip())
                list.append(item)

            data = {"dozens": list}
            messages.info(
                request,
                "Genial ahora solo confirme que todas las docenas seleccionadas \
                sean las que eligio anteriormente",
            )
            return render(request, "pages/sales/items_selected.html", data)
        else:
            messages.info(
                request, "Es necesario que seleccione al menos una docena para su venta"
            )
            return redirect(to="dozens.dozens_ready_to_sell")
    else:
        return redirect(to='home')


@login_required(login_url="/login/")
def confirm_selected_items(request):
    if  request.method == 'POST':
        dozens = request.POST.getlist("dozens[]")

        if dozens:
            list = []
            total = 0

            for id in dozens:
                item = Dozen.objects.get(id=id.strip())
                model = item.model.sizesandmodels_set.get(size_id=item.size_id)
                item.price = model.price
                total += model.price
                list.append(item)

            data = {
                "dozens_list": list,
                "dozens": dozens,
                "total": total,
                "form": SalesForm(),
            }

            return render(request, "pages/sales/create.html", data)
        else:
            messages.info(
                request, "Intentelo nuevamente!!!. Es necesario que seleccione al menos una docena para su venta"
            )
            return redirect(to="dozens.dozens_ready_to_sell")

    else:
        return redirect(to='home')

@login_required(login_url="/login/")
def store(request):
    if request.method == "POST":
        dozens = request.POST.getlist("dozens[]")
        total = 0

        if dozens:
            for id in dozens:
                dozen = Dozen.objects.get(id=id.strip())
                model = dozen.model.sizesandmodels_set.get(size_id=dozen.size_id)
                dozen.price = model.price
                total += model.price

            data = {"total": total, "form": SalesForm()}
            money_paid = 0

            if not request.POST["just_a_quantity"].strip():
                money_paid = total
            else:
                money_paid = request.POST["just_a_quantity"].strip()

            form = SalesForm(
                data={
                    "customer": request.POST["customer"].strip(),
                    "dozens_list": ",".join(dozens),
                    "number_of_dozens": len(dozens),
                    "total_price": total,
                    "money_paid": money_paid,
                    "total_money_owed": int(total) - int(money_paid),
                    "status": request.POST["status"], #equal to the mode of payment
                    "note": request.POST["note"].strip(),
                }
            )

            if form.is_valid():
                for id in dozens:
                    dozen = Dozen.objects.get(id=id.strip())
                    dozen.status = "vendido"
                    dozen.save()

                form.save()
                messages.success(request, "Genial!. La venta a sido realizada con exito!")

                return redirect(to="sales.show", id=form["customer"].value())
            else:
                messages.error(request, "Error!. Lo sentimos no pudimos procesar esta venta \
                    es necesario que llene correctamente el formulario")

                return render(request, "pages/sales/create.html", data)


        else:
            messages.info(
                request, "Es necesario que seleccione al menos una docena para su venta"
            )
            return redirect(to="dozens.dozens_ready_to_sell")
    else:
        return redirect(to='home')


@login_required(login_url="/login/")
def update(request, id):
    if request.method == "POST":
        sale = get_object_or_404(Sales, id=id)
        if not request.POST["just_a_quantity"].strip():
            sale.total_money_owed = 0
            sale.money_paid = sale.total_price
            messages.success(request, "Genial!. Ahora esta venta ya no tiene deudas!")
        else:
            if int(request.POST["just_a_quantity"].strip()) > sale.total_money_owed:
                messages.error(
                    request, f"Error!. Esta venta tiene una deuda de S/{sale.total_money_owed} \
                        y el monto que trata de pagar es mayor a esa deuda, por favor \
                        llene correctamente el formulario"
                )
                return redirect(to="sales.show", id=sale.customer_id)
            else:
                money_paid = int(request.POST["just_a_quantity"].strip())
                sale.total_money_owed = int(sale.total_money_owed) - money_paid
                sale.money_paid = sale.money_paid + money_paid
                messages.success(
                    request, f"Genial ahora solo debe S/{sale.total_money_owed}!"
                )

        sale.save()
        return redirect(to="sales.show", id=sale.customer_id)
    else:
        return redirect(to='home')
