from django.urls import path
from .views import index, show, store ,update

urlpatterns = [
    path('modelos/', index, name='models.index'),
    path('modelos/<name>/crear/', store, name='models.store'),
    path('modelos/<name>/', show, name='models.show'),
    path('modelos/<name>/actualizar/', update, name='models.update'),
]