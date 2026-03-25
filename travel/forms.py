from django import forms
from django.core.exceptions import ValidationError
from .models import Place, Review, Trip, TripPlace


MAX_IMAGE_SIZE = 2 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}

class PlaceForm(forms.ModelForm):
    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude")
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180.")
        return longitude

    def clean_place_image(self):
        place_image = self.cleaned_data.get("place_image")

        if not place_image:
            return place_image

        if place_image.size > MAX_IMAGE_SIZE:
            raise ValidationError("Image size must be 2MB or smaller.")

        content_type = getattr(place_image, "content_type", None)
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError("Only JPEG and PNG image files are allowed.")

        return place_image

    class Meta:
        model = Place
        fields = [
            "place_name",
            "place_desc",
            "estimated_cost",
            "region",
            "latitude",
            "longitude",
            "place_image",
        ]
        widgets = {
            "place_name": forms.TextInput(attrs={"class": "form-control"}),
            "place_desc": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estimated_cost": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "region": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001", "placeholder": "Optional"}
            ),
            "longitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001", "placeholder": "Optional"}
            ),
            "place_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Share your experience..."}
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None or not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class TripPlaceForm(forms.ModelForm):
    class Meta:
        model = TripPlace
        fields = ["place", "day_number"]
        widgets = {
            "place": forms.Select(attrs={"class": "form-select"}),
            "day_number": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["place"].queryset = Place.objects.order_by("place_name")
