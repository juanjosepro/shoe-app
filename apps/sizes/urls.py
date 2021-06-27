from django.urls import path
from .views import index, store, update

urlpatterns = [
    path('tallas/', index, name='sizes.index'),
    path('crear-nueva-talla/', store, name='sizes.store'),
    path('actualizar-talla/<id>/', update, name='sizes.update'),
]