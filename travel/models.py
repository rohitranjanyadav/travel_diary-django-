from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Place(models.Model):

    def __str__(self):
        return self.place_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    place_name = models.CharField(max_length=200)
    place_desc = models.CharField(max_length=500)
    estimated_cost = models.IntegerField()
    place_image = models.CharField(
        max_length=500,
        default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT36fqQUPeXvmxYZlOAzqiIFNwMOcXwRQHBgw&s",
    )
    
    def get_absolute_url(self):
        return reverse("travel:detail", kwargs={"pk": self.pk})
