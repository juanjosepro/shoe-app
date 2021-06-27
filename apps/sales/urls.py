from django.urls import path
from .views import index, filter, show, summary_of_selected_items, confirm_selected_items, store ,update

urlpatterns = [
    path('ventas/', index, name='sales.index'),
    path('ventas/filtradas-por/<filter>/', filter, name='sales.filter'),
    path('realizar-venta/', store, name='sales.store'),
    path('confirmar-docenas-seleccionadas/', summary_of_selected_items, name='sales.summary_of_selected_items'),
    path('finalizar-venta/', confirm_selected_items, name='sales.confirm_selected_items'),
    path('historial-de-venta/<id>/', show, name='sales.show'),
    path('actualizar-venta/<id>/', update, name='sales.update'),
]