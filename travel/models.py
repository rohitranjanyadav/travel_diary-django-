from django.db import models


# Create your models here.
class Place(models.Model):
  
    def __str__(self):
        return self.place_name
  
    place_name = models.CharField(max_length=200)
    place_desc = models.CharField(max_length=200)
    estimated_cost = models.IntegerField()
