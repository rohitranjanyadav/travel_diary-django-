from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Place
from django.template import loader
from .forms import PlaceForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

# Create your views here.
# def index(request):
#     place_list = Place.objects.all()
#     context = {
#         "place_list": place_list,
#     }
#     return render(request, "travel/index.html", context)


# Class Based View
class IndexClassView(ListView):
    model = Place
    template_name = "travel/index.html"
    context_object_name = "place_list"


def place(request):
    return HttpResponse("This is place")


# def detail(request, place_id):
#     place = get_object_or_404(Place, pk=place_id)
#     context = {"place": place}
#     return render(request, "travel/detail.html", context)


class PlaceDetail(DetailView):
    model = Place
    template_name = "travel/detail.html"


def add_place(request):
    form = PlaceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("travel:index")

    return render(request, "travel/place-form.html", {"form": form})


class AddPlace(CreateView):
    model = Place
    fields = ["place_name", "place_desc", "estimated_cost", "place_image"]
    template_name = "travel/place-form.html"

    def form_valid(self, form):
        form.instance.user_name = self.request.user

        return super().form_valid(form)


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
