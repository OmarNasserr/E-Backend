from django.contrib import admin
from parler.admin import TranslatableAdmin
from .category.models import Category
from .subcategory.models import SubCategory
from .subsubcategory.models import SubSubCategory


admin.site.register(Category,TranslatableAdmin)
admin.site.register(SubCategory,TranslatableAdmin)
admin.site.register(SubSubCategory,TranslatableAdmin)
