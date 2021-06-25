from django.urls import path
from .views import index, search, show, dozens_ready_to_sell, dozens_for_the_aparador, dozens_for_the_armador, dozens_for_the_rematador, store, update
from .views import history_of_the_process_of_each_dozen


urlpatterns = [
    path('registrar-nueva-docena/<name>/', store, name='dozens.store'),
    path('docenas-listas-para-vender/', dozens_ready_to_sell, name='dozens.dozens_ready_to_sell'),
    path('docenas-disponibles-para-los-aparadores/',
        dozens_for_the_aparador,
        name='dozens.dozens_for_the_aparador'),
    path('docenas-disponibles-para-los-armadores/',
        dozens_for_the_armador,
        name='dozens.dozens_for_the_armador'),
    path('docenas-disponibles-para-las-rematadoras/',
        dozens_for_the_rematador,
        name='dozens.dozens_for_the_rematador'),
    path('mostrar-docenas-por/<filter>/', index, name='dozens.index'),
    path('docenas/modelo/<name>/filtrado-por/<filter>/', show, name='dozens.show'),
    path('docenas/<id>/actualizar-docena/', update, name='dozens.update'),
    path('buscar-docena-por-codigo/', search, name='dozens.search'),
    path('historia-del-proceso-de-cada-docena/<id>/',
        history_of_the_process_of_each_dozen,
        name='dozens.history_of_the_process_of_each_dozen'),
]