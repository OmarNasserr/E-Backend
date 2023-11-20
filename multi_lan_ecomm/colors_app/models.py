from django.db import models

class Color(models.Model):
    color_name=models.CharField(max_length=15,unique=True)
    hex_color=models.CharField(max_length=7,unique=True)
    
    def __str__(self):
        return str(self.color_name)