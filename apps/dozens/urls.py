from django.urls import path
from .views import index, filter, show, store, update

urlpatterns = [
    path('docenas/<name>/crear/', store, name='dozens.store'),
    path('docenas/', index, name='dozens.index'),
    path('docenas/<name>/', show, name='dozens.show'),
    path('docenas/filtrado-por/<filter>/', filter, name='dozens.filter'),
    path('docenas/<id>/actualizar/', update, name='dozens.update'),
]