from django.db import models

class Size(models.Model):
    size_name=models.CharField(max_length=10,unique=True)
    
    def __str__(self):
        return str(self.size_name)