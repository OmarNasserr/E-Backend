import datetime
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
import os

from categories_app.subsubcategory.models import SubSubCategory
from colors_app.models import Color
from sizes_app.models import Size


#as a product might have multiple variations, like the same t-shirt can have different sizes of different 
#colors but images are associated with the product color and different sizes willn't affect
#the product images, therefore tables are created in a hierarchy manner
#
#
#                                              product ----------> productThumbnailIamge
#                           color               ^    ^                    
#                             ^                 |    |
#                             |                 |    |                    sizes
#                             |                 |    |                      ^
# productImage <--------- productColor _________|    |                      |
#                             ^                      |                      |
#                             |                      |                      |
#                             |_______________ productVaraitions ___________|
#
# Color table contains colors to be able to choose from them and that makes searching and filtering
# with color.id easier
#
# Size table contains sizes to be able to choose from them and that makes searching and filtering
# with size.id easier
#
# ProductColor table contains the combination of a prodcut and its available colors with their images, 
# as a red t-shirt of size S has the same images of a a red t-shirt of size M
#
# ProdcutVariations table contains the combination of ProductColor and its avaialbe sizes
# to show different sizes of a prodcut with their color using the same set of images
# without ProdcutVariations table realtion with the ProductColor table 
# we will have to upload the same images again and again for different product-color-size variations
#
# ProductThumbnailImage stores Product thumnail image to display in a product card
#
# Product table contains the basic info about the product in multi-languages
# such as name, description and price
#
# nseted serialization are explained in serializers.py


class Product(TranslatableModel):
    
    languages = TranslatedFields(
        product_name = models.CharField(_("product_name"),max_length=255,blank=False,null=False),
        description = models.CharField(_("description"),
            max_length=255, blank=True, null=True, default=""),
        price=models.DecimalField(_("price"),blank=False,null=False,decimal_places=2,max_digits=8),
    )
    total_num_in_stock=models.IntegerField(blank=True,null=True,default=0)
    subsubcategory= models.ForeignKey(SubSubCategory, on_delete=models.CASCADE,
                                       related_name='products', to_field='id')
    
    def __str__(self):
        return str(self.product_name)

# ProductImages are associated with this class, as the product color has the same images 
# whatever the sizes of that product color are
# ex: a t-shirt has multiple colors 'red','green',..etc
# the red t-shirt has the same images whatever the size of that t-shirt is.

class ProductColor(models.Model):
    color=models.ForeignKey(Color,related_name='color',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,blank=True,null=True,related_name='product',on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.product.product_name)+'-'+str(self.color.color_name)

class ProductVariations(models.Model):
    product=models.ForeignKey(Product,related_name='stock',on_delete=models.CASCADE)
    product_color_variations=models.ManyToManyField(ProductColor,related_name='product_variations')
    size=models.ManyToManyField(Size,related_name='size')
    number_in_stock=models.IntegerField(blank=True,null=True,default=0)
        
    def save(self, *args, **kwargs):
        
        variations=ProductVariations.objects.get(product=self.product)
        total_num_in_stock=0
        for variation in variations:
            total_num_in_stock=total_num_in_stock+variation.total_num_in_stock
            
        total_num_in_stock=total_num_in_stock+self.number_in_stock
        Product.objects.filter(pk=self.product.id).update(total_num_in_stock=total_num_in_stock)
        
        super(ProductVariations, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.product.product_name)+'-'+str(self.product_color_variations.get().color.color_name)+'-'+str(self.size.get().size_name)
        
def product_image_location(instance, filename):
    upload_path=f"categories/{instance.productColor.product.subsubcategory.subcategory.category.category_name}/{instance.productColor.product.subsubcategory.subcategory.subcategory_name}/{instance.productColor.product.subsubcategory.subsubcategory_name}/{instance.productColor.product.product_name}/{instance.productColor.color.color_name}/"
    return os.path.join(upload_path, filename)

class ProductImage(models.Model):
    productColor= models.ForeignKey(ProductColor, on_delete=models.CASCADE,
                             related_name='product_color_images', to_field='id')
    image = models.ImageField(
        upload_to=product_image_location, blank=True, null=True,)
    
    def __str__(self):
        return str(self.productColor.product.product_name)


def product_thumbnail_image_location(instance, filename):
    upload_path=f"categories/{instance.product.subsubcategory.subcategory.category.category_name}/{instance.product.subsubcategory.subcategory.subcategory_name}/{instance.product.subsubcategory.subsubcategory_name}/{instance.product.product_name}/thumbnail/"
    return os.path.join(upload_path, filename)

class ProductThumbnailImage(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE,
                             related_name='thumbnail', to_field='id')
    image = models.ImageField(
        upload_to=product_thumbnail_image_location, blank=True, null=True,)
    
    def __str__(self):
        return str(self.product.product_name)+" "+"thumbnail"

