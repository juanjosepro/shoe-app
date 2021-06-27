from django.urls import path
from .views import index, store, update

urlpatterns = [
    path('categorias/', index, name='categories.index'),
    path('crear-nueva-categoria/', store, name='categories.store'),
    path('actualizar-categoria/<name>/', update, name='categories.update'),
]