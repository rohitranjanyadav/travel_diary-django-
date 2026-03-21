from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Place
from django.template import loader
from .forms import PlaceForm


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
    place = get_object_or_404(Place, pk=place_id)
    context = {"place": place}
    return render(request, "travel/detail.html", context)


def add_place(request):
    form = PlaceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("travel:index")

    return render(request, "travel/place-form.html", {"form": form})


def update_place(request, id):
    place = get_object_or_404(Place, pk=id)
    form = PlaceForm(request.POST or None, instance=place)

    if form.is_valid():
        form.save()
        return redirect("travel:index")

    return render(request, "travel/place-form.html", {"form": form, "place": place})


def delete_place(request, id):
    place = Place.objects.get(id=id)

    if request.method == "POST":
        place.delete()
        return redirect("travel:index")

    return render(request, "travel/place-delete.html", {"place": place})


def view_place(request):
    return redirect("travel:index")



def view_place(request):
    return redirect("travel:index")
