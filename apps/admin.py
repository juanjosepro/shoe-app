from django.contrib import admin
from .sizes.models import Sizes
from .category.models import Category
from .model.models import Model
from .materials.models import Material
from .inventory.models import Inventory
from .providers_and_customers.models import ProvidersAndCustomers
from .sales.models import Sales


admin.site.register(Sizes)
admin.site.register(Category)
admin.site.register(Model)
admin.site.register(Material)
admin.site.register(Inventory)
admin.site.register(ProvidersAndCustomers)
admin.site.register(Sales)

