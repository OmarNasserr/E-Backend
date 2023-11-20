from django.db import models
from django.conf import settings
import os
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

from categories_app.category.models import Category


class SubCategory(TranslatableModel):
    
    category= models.ForeignKey(Category, on_delete=models.CASCADE,
                                       related_name='subcategories',to_field='id')
    languages = TranslatedFields(
    subcategory_name = models.CharField(_("subcategory_name"),max_length=255),
    description = models.CharField(_("description"),
        max_length=255, blank=True, null=True, default=""),
    )

    def __str__(self):
        return str(self.subcategory_name)


def sub_image_location(instance, filename):
    upload_path=f"categories/{instance.subcategory.category.category_name}/{instance.subcategory.subcategory_name}/subcategory_images/"
    return os.path.join(upload_path, filename)

class SubCategoryImage(models.Model):
    subcategory= models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                             related_name='subcategory_image', to_field='id')
    image = models.ImageField(  
        upload_to=sub_image_location, blank=True, null=True,)
    
    def __str__(self):
        return str(self.subcategory.subcategory_name)