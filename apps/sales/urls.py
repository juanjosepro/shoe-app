from django.urls import path
from .views import index, filter, show, summary_of_selected_items, confirm_selected_items, store ,update

urlpatterns = [
    path('ventas/', index, name='sales.index'),
    path('ventas/filtradas-por/<filter>/', filter, name='sales.filter'),
    path('crear/venta/', store, name='sales.store'),
    path('docenas-seleccionadas/', summary_of_selected_items, name='sales.summary_of_selected_items'),
    path('confirmar-docenas-seleccionadas/', confirm_selected_items, name='sales.confirm_selected_items'),
    path('historial-de-venta/<id>/', show, name='sales.show'),
    path('venta/<id>/actualizar/', update, name='sales.update'),
]