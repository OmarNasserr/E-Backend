from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product,ProductColor,ProductVariations


admin.site.register(Product,TranslatableAdmin)
admin.site.register(ProductColor)
admin.site.register(ProductVariations)
