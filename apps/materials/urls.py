from django.urls import path
from .views import index, update

urlpatterns = [
    path('materiales/', index, name='materials.index'),
    path('materiales/<name>/actualizar/', update, name='materials.update'),
]