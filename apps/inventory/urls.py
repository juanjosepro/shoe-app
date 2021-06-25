from django.urls import path
from .views import index, show, filter, store, update, update_stock

urlpatterns = [
    path('inventario/', index, name='inventory.index'),
    path('inventario/<name>/', show, name='inventory.show'),
    path('inventario/<id>/actualizar/', update, name='inventory.update'),
    path('inventario/<id>/actualizar-existencias/', update_stock, name='inventory.update_stock'),
    path('inventario/<name>/<filter>/', filter, name='inventory.filter'),
    path('<name>/inventario/crear/', store, name='inventory.store'),
]