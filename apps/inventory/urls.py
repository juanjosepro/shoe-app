from django.urls import path
from .views import index, show, filter, store, readonly, update_stock

urlpatterns = [
    #path('inventario/', index, name='inventory.index'),
    path('lista-de-inventario-del-material/<name>/', show, name='inventory.show'),
    path('detalles-del-registro-de-inventario/<id>/', readonly, name='inventory.readonly'),
    path('actualizar-existencias/<id>/', update_stock, name='inventory.update_stock'),
    path('inventario-del-material/<name>/filtrado-por/<filter>/', filter, name='inventory.filter'),
    path('registrar-nuevo-inventario-al-material/<name>/', store, name='inventory.store'),
]