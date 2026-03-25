from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Place(models.Model):
    REGION_CHOICES = [
        ("TERAI", "Terai"),
        ("HILLS", "Hills"),
        ("HIMALAYA", "Himalaya"),
    ]

    def __str__(self):
        return self.place_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    place_name = models.CharField(max_length=200)
    place_desc = models.CharField(max_length=500)
    estimated_cost = models.IntegerField()
    region = models.CharField(
        max_length=20, choices=REGION_CHOICES, default="HILLS", db_index=True
    )
    place_image = models.ImageField(upload_to="places/", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("travel:detail", kwargs={"pk": self.pk})


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="reviews", db_index=True
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "place"], name="unique_user_place_review")
        ]
        indexes = [
            models.Index(fields=["place", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.place.place_name} ({self.rating})"


class Trip(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trips", db_index=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("travel:trip_detail", kwargs={"pk": self.pk})


class TripPlace(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_places")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="trip_places")
    day_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["day_number", "id"]

    def __str__(self):
        return f"{self.trip.name} - Day {self.day_number}: {self.place.place_name}"
