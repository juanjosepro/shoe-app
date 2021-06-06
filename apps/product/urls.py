from django.urls import path
from .views import index, store, filterByName

urlpatterns = [
    # get the data by ajax
    path('productos/', index, name='products.index'),
    path('productos/crear/', store, name='products.store'),
    path('producto/<str:name>/', filterByName, name='products.filter-by-name'),
]