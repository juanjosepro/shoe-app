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
    sales = Sales.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(sales, 10)
        sales = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': sales,
        'paginator': paginator,
    }
    
    return render(request, 'pages/sales/index.html', data)


@login_required(login_url="/login/")
def filter(request, filter):
    sales = None
    if filter == 'todos':
        sales = Sales.objects.all().order_by('-created_at')
    if filter == 'estado-de-pago-completo':
        sales = Sales.objects.filter(total_money_owed = 0).order_by('-created_at')
    if filter == 'estado-de-pago-incompleto':
        sales = Sales.objects.filter(total_money_owed__gte = 1).order_by('-created_at')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(sales, 15)
        sales = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': sales,
        'paginator': paginator,
        'filter_by': filter,
    }
    return render(request, 'pages/sales/index.html', data)


@login_required(login_url="/login/")
def show(request, id):
    customer = get_object_or_404(ProvidersAndCustomers, id = id)
    sales = Sales.objects.filter(customer_id = id).order_by('-created_at') #[<dozen>, <dozen>]
    res = []
    for sale in sales: #<dozen>
        result = {}
        result['title'] = sale.created_at
        result['note'] = sale.note
        result['status'] = sale.status
        result['total_price'] = sale.total_price
        result['money_paid'] = sale.money_paid
        result['total_money_owed'] = sale.total_money_owed
        result['owe_money'] = bool(int(sale.total_money_owed))
        result['id'] = sale.id
        dozens_list = sale.dozens_list.split(',') # of '2,4,5' to ['2', '4', '5']
        result['number_of_dozens'] = len(dozens_list)

        dozens = []
        for id in dozens_list: #id = 2
            dozen = Dozen.objects.get(id = id) #<dozen>
            dozens.append(dozen)
        
        result['data'] = dozens
        res.append(result)

    data = {
        'customer': customer,
        'dozens': res,    
    }

    return render(request, 'pages/sales/show.html', data)


@login_required(login_url="/login/")
def summary_of_selected_items(request):
    dozens = request.POST.getlist('dozens[]')
    list = []

    for id in dozens:
        item = Dozen.objects.get(id = id)
        list.append(item)

    data = {'dozens': list}

    return render(request, 'pages/sales/items_selected.html', data)


@login_required(login_url="/login/")
def confirm_selected_items(request):
    customers = ProvidersAndCustomers.objects.filter(types = 'cliente')
    dozens = request.POST.getlist('dozens[]')
    list = []
    total = 0
    for id in dozens:
        item = Dozen.objects.get(id = id)
        total += item.model.price
        list.append(item)

    data = {
        'dozens_list': list,
        'dozens': dozens,
        'total': total,
        'customers': customers,
        'form': SalesForm()
    }
    return render(request, 'pages/sales/create.html', data)


@login_required(login_url="/login/")
def store(request):
    dozens = request.POST.getlist('dozens[]')
    total = 0
    for id in dozens:
        item = Dozen.objects.get(id = id)
        total += item.model.price

    data = {
        'total': total, #decimal
        'form': SalesForm()
    }
    print(type(total))
    print(request.POST)
    if request.method == 'POST':
        money_paid = 0
        if not request.POST['just_a_quantity'].strip():
            money_paid = total
        else:
            money_paid = request.POST['just_a_quantity'].strip()

        formulario = SalesForm(data={
            'customer': request.POST['customer'],
            'dozens_list': ",".join(dozens),
            'number_of_dozens': len(dozens),
            'total_price': total,
            'money_paid': money_paid,
            'total_money_owed': int(total) - int(money_paid),
            'status': request.POST['status'],
            'note': request.POST['note'],
        })

        if formulario.is_valid():
            for id in dozens:
                model = Dozen.objects.get(id = id)
                model.status = 'vendido'
                model.save()

            formulario.save()
            messages.success(request, "Venta realizada con exito!")
        else:
            messages.error(request, "No se pudo completar la venta!")
            return render(request, 'pages/sales/create.html', data)

    return redirect(to='sales.show', id = formulario['customer'].value())


@login_required(login_url="/login/")
def update(request, id):
    sale = get_object_or_404(Sales, id = id)

    if request.method == 'POST':
        if not request.POST['just_a_quantity'].strip():
            sale.total_money_owed = 0
            sale.money_paid = sale.total_price
            messages.success(request, "Venta sin deudas!")
        else:
            money_paid = int(request.POST['just_a_quantity'].strip())
            sale.total_money_owed = int(sale.total_money_owed) - money_paid
            sale.money_paid = sale.money_paid + money_paid
            messages.success(request, f"Genial ahora solo debe S/{sale.total_money_owed}!")
        
        sale.save()

    return redirect(to='sales.show', id = sale.customer_id)