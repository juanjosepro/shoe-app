from django.urls import path
from .views import index, update

urlpatterns = [
    path('materiales/', index, name='materials.index'),
    path('actualizar-material/<name>/', update, name='materials.update'),
]