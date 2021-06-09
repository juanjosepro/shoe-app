from django.urls import path
from .views import index, store, update

urlpatterns = [
    path('docenas/<name>/crear/', store, name='dozens.store'),
    path('docenas/<name>/', index, name='dozens.index'),
    path('docenas/<id>/actualizar/', update, name='dozens.update'),
]