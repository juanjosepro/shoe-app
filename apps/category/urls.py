from django.urls import path
from .views import index, store, update

urlpatterns = [
    path('categorias/', index, name='categories.index'),
    path('categorias/crear/', store, name='categories.store'),
    path('categoria/<name>/actualizar/', update, name='categories.update'),
]