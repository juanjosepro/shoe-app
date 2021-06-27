from django.urls import path
from .views import show, store ,update

urlpatterns = [
    #providers
    path('registrar-un-nuevo-proveedor/', store, name='providers.store'),
    path('mostrar-todos-los/<type>/filtrados-por/<filter>/', show, name='providers.show'),
    path('actualizar-el-proveedor/<id>/', update, name='providers.update'),
    
    #customers
    path('registrar-un-nuevo-cliente/', store, name='customers.store'),
    path('mostrar-todos-los/<type>/filtrados-por/<filter>/', show, name='customers.show'),
    path('actualizar-el-cliente/<id>/', update, name='customers.update'),
]