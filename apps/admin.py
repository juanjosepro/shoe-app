from django.contrib import admin
from .product.models import Product
from .sizes.models import Sizes
from .category.models import Category
from .model.models import Model

# Register your models here.


admin.site.register(Product)
admin.site.register(Sizes)
admin.site.register(Category)
admin.site.register(Model)
