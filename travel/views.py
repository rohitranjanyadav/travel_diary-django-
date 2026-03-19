from django.shortcuts import render
from django.http import HttpResponse
from .models import Place

# Create your views here.
def index(request):
    place_list = Place.objects.all()
    return HttpResponse(place_list)


def place(request):
    return HttpResponse("This is place")