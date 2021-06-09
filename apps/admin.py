from django.contrib import admin
from .product.models import Product
from .sizes.models import Sizes
from .category.models import Category
from .model.models import Model
from .materials.models import Material
from .inventory.models import Inventory

# Register your models here.


admin.site.register(Product)
admin.site.register(Sizes)
admin.site.register(Category)
admin.site.register(Model)
admin.site.register(Material)
admin.site.register(Inventory)