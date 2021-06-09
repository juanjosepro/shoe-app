from django.urls import path
from .views import index, show, filter, store, update

urlpatterns = [
    path('inventario/', index, name='inventory.index'),
    path('inventario/<name>/', show, name='inventory.show'),
    path('inventario/<id>/actualizar/', update, name='inventory.update'),
    path('inventario/<name>/<filter>/', filter, name='inventory.filter'),
    path('<name>/inventario/crear/', store, name='inventory.store'),
]