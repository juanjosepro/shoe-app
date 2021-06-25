from django.urls import path
from .views import show, store ,update

urlpatterns = [
    #path('proveedores/', index, name='providers.and.customers.index'),
    path('crear/proveedor/', store, name='providers.store'),
    path('proveedores/<type>/<filter>/', show, name='providers.show'),
    path('proveedor/<id>/actualizar/', update, name='providers.update'),
    
    #path('clientes/', index, name='providers.and.customers.index'),
    path('crear/cliente/', store, name='customers.store'),
    path('clientes/<type>/<filter>/', show, name='customers.show'),
    path('cliente/<id>/actualizar/', update, name='customers.update'),
]