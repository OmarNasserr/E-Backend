from django.db import models
from django.conf import settings
import os
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

from categories_app.subcategory.models import SubCategory

class SubSubCategory(TranslatableModel):
    
    languages = TranslatedFields(
    subsubcategory_name = models.CharField(_("subsubcategory_name"),max_length=255),
    description = models.CharField(_("description"),
        max_length=255, blank=True, null=True, default=""),
    )
    subcategory= models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                                       related_name='subsubcategories', to_field='id')
    def __str__(self):
        return str(self.subsubcategory_name)
    
    # class Meta:
    #     unique_together = ['subsubcategory_name', 'subcategory']
        
def sub_sub_image_location(instance, filename):
    upload_path=f"categories/{instance.subsubcategory.subcategory.category.category_name}/{instance.subsubcategory.subcategory.subcategory_name}/{instance.subsubcategory.subsubcategory_name}/"
    return os.path.join(upload_path, filename)

class SubSubCategoryImage(models.Model):
    subsubcategory= models.ForeignKey(SubSubCategory, on_delete=models.CASCADE,
                             related_name='subsubcategory_image', to_field='id')
    image = models.ImageField(
        upload_to=sub_sub_image_location, blank=True, null=True,)
    
    def __str__(self):
        return str(self.subsubcategory.subsubcategory_name)