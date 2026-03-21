from django import forms
from .models import Place

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["place_name", "place_desc", "estimated_cost", "place_image"]
