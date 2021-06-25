from django.urls import path
from .views import all_aparador_processes, store, update_aparador_dozen
from .views import all_armador_processes, update_armador_dozen
from .views import store_and_update_rematadoras_dozen


urlpatterns = [
    #Route from the aparadores
    path('procesos/aparador/<filter>/',
        all_aparador_processes,
        name='processes.aparador.index'),
    path('agregar-docena-a-produccion/',
        store, 
        name='processes.store'),
    path('actualizar-docena-del-aparador-a-finalizado/<id>/',
        update_aparador_dozen,
        name='processes.aparador.update'),
    
    #Route from the aparadores
    path('procesos/armador/<filter>/',
        all_armador_processes,
        name='processes.armador.index'),
    path('actualizar-docena-del-armador-a-finalizado/<id>/',
        update_armador_dozen,
        name='processes.aparador.update'),

    path('actualizar-docena-con-el-estado-produccion-finalizada/<id>/',
        store_and_update_rematadoras_dozen,
        name='processes.rematadora.store.and.update'),
]
