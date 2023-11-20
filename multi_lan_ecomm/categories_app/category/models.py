from django.db import models
from django.conf import settings
import os
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _


class Category(TranslatableModel):
    languages = TranslatedFields(
    category_name = models.CharField(_("category_name"),max_length=255, unique=True),
    description = models.CharField(
        _("description"),max_length=255, blank=True, null=True, default=""),
    )

    def __str__(self):
        return self.category_name
    
def category_image_location(instance, filename):
    upload_path=f"categories/{instance.category.category_name}/category_images/"
    return os.path.join(upload_path, filename)

class CategoryImage(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE,
                             related_name='category_image', to_field='id')
    image = models.ImageField(
        upload_to=category_image_location, blank=True, null=True,)

    def __str__(self):
        return str(self.category.category_name)