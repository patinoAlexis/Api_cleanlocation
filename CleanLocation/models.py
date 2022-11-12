from django.db import models

# Create your models here.
class point_location(models.Model):
    latitud= models.IntegerField()
    longitud= models.IntegerField()
    
