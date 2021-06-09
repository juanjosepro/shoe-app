from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("apps.product.urls")),
    path("", include("apps.category.urls")),
    path("", include("apps.model.urls")),
    path("", include("apps.dozens.urls")),
    path("", include("apps.materials.urls")),
    path("", include("apps.inventory.urls")),
    path("", include("apps.urls")),            # UI Kits Html files

]
