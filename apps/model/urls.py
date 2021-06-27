from django.urls import path
from .views import index, show, store, update

urlpatterns = [
    path('modelos/', index, name='models.index'),
    path('registrar-nuevo-modelo-a-la-categoria/<name>/', store, name='models.store'),
    path('modelos-pertenecientes-a-la-categoria/<name>/', show, name='models.show'),
    path('actualizar-modelo/<name>/', update, name='models.update'),
]