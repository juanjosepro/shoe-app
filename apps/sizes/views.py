from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sizes
from .forms import SizesForm


@login_required(login_url="/login/")
def index(request):
    sizes = Sizes.objects.all().order_by('-created_at')
    data = {
        'sizes': sizes,
        'form':SizesForm(),
    }
    return render(request, 'pages/sizes/index.html', data)


@login_required(login_url="/login/")
def store(request):
    if request.method == 'POST':
        form_size = SizesForm(data=request.POST)

        if form_size.is_valid():
            form_size.save()
            messages.success(request, 'Talla creada satisfactoriamente')
            return redirect(to='sizes.index')
        
        messages.error(request, 'No se pudo crear intentelo de nuevo')
        return redirect(to='sizes.index')


@login_required(login_url="/login/")
def update(request, id):
    size = get_object_or_404(Sizes, id=id)
    data = {'form':SizesForm(instance=size)}
    
    if request.method == 'POST':
        form_size = SizesForm(data=request.POST, instance=size)

        if form_size.is_valid():
            form_size.save()
            messages.success(request, 'Talla actualizada satisfactoriamente')
            return redirect(to='sizes.index')
        
        data['form'] = form_size
        messages.success(request, 'No se pudo actualizar esta talla')
        return redirect(to='sizes.index')

    return render(request, 'pages/sizes/update.html', data)