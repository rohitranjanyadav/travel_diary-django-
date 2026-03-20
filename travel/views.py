from django.shortcuts import render
from django.http import HttpResponse
from .models import Place
from django.template import loader


# Create your views here.
def index(request):
    place_list = Place.objects.all()
    context = {
        "place_list": place_list,
    }
    return render(request, "travel/index.html", context)


def place(request):
    return HttpResponse("This is place")


def detail(request, place_id):
  place= Place.objects.get(pk=place_id)
  context = {
      "place": place
  }
  return render(request, "travel/detail.html", context)