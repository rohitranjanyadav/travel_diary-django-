from collections import defaultdict
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.db.models import Avg, Count, FloatField, Prefetch, Value
from django.db.models.functions import Coalesce
from .models import Place, Review, Trip, TripPlace
from .forms import PlaceForm, ReviewForm, TripForm, TripPlaceForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            Place.objects.select_related("user_name")
            .annotate(
                avg_rating=Coalesce(
                    Avg("reviews__rating"), Value(0.0), output_field=FloatField()
                ),
                review_count=Count("reviews"),
            )
            .order_by("-created_at")
        )

        search_query = self.request.GET.get("q", "").strip()
        region = self.request.GET.get("region", "").strip()
        min_cost = self.request.GET.get("min_cost", "").strip()
        max_cost = self.request.GET.get("max_cost", "").strip()
        min_rating = self.request.GET.get("min_rating", "").strip()
        sort_by = self.request.GET.get("sort", "newest").strip()

        if search_query:
            queryset = queryset.filter(place_name__icontains=search_query)

        if region:
            queryset = queryset.filter(region=region)

        if min_cost.isdigit():
            queryset = queryset.filter(estimated_cost__gte=int(min_cost))

        if max_cost.isdigit():
            queryset = queryset.filter(estimated_cost__lte=int(max_cost))

        try:
            if min_rating:
                queryset = queryset.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

        if sort_by == "highest_rated":
            queryset = queryset.order_by("-avg_rating", "-review_count", "-created_at")
        elif sort_by == "most_reviewed":
            queryset = queryset.order_by("-review_count", "-avg_rating", "-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_region"] = self.request.GET.get("region", "").strip()
        context["min_cost"] = self.request.GET.get("min_cost", "").strip()
        context["max_cost"] = self.request.GET.get("max_cost", "").strip()
        context["min_rating"] = self.request.GET.get("min_rating", "").strip()
        context["sort_by"] = self.request.GET.get("sort", "newest").strip()
        context["region_choices"] = Place.REGION_CHOICES

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context


def place(request):
    return HttpResponse("This is place")


# def detail(request, place_id):
#     place = get_object_or_404(Place, pk=place_id)
#     context = {"place": place}
#     return render(request, "travel/detail.html", context)


class PlaceDetail(DetailView):
    model = Place
    template_name = "travel/detail.html"

    def get_queryset(self):
        return Place.objects.select_related("user_name").prefetch_related(
            Prefetch("reviews", queryset=Review.objects.select_related("user").order_by("-created_at"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = self.object

        context["reviews"] = place.reviews.all()
        context["average_rating"] = place.reviews.aggregate(
            avg=Coalesce(Avg("rating"), Value(0.0), output_field=FloatField())
        )["avg"]
        context["review_count"] = place.reviews.count()

        if self.request.user.is_authenticated:
            existing_review = Review.objects.filter(
                user=self.request.user, place=place
            ).first()
            context["can_review"] = existing_review is None
            context["review_form"] = ReviewForm()
            context["existing_review"] = existing_review

        return context


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user_name == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to modify this place.")
        return redirect("travel:index")


class AddPlace(LoginRequiredMixin, CreateView):
    model = Place
    form_class = PlaceForm
    template_name = "travel/place-form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user_name = self.request.user

        return super().form_valid(form)


class UpdatePlace(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Place
    form_class = PlaceForm
    template_name = "travel/place-form.html"
    login_url = "login"


class DeletePlace(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Place
    template_name = "travel/place-delete.html"
    success_url = reverse_lazy("travel:index")
    login_url = "login"


def view_place(request):
    return redirect("travel:index")


class AddReview(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    http_method_names = ["post"]
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.place = get_object_or_404(Place, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.place = self.place

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "You have already reviewed this place.")
            return redirect("travel:detail", pk=self.place.pk)

    def get_success_url(self):
        messages.success(self.request, "Your review has been posted.")
        return reverse_lazy("travel:detail", kwargs={"pk": self.place.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the review form errors.")
        return redirect("travel:detail", pk=self.place.pk)


class TripOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to modify this trip.")
        return redirect("travel:trip_list")


class TripList(LoginRequiredMixin, ListView):
    model = Trip
    template_name = "travel/trip-list.html"
    context_object_name = "trip_list"
    paginate_by = 8
    login_url = "login"

    def get_queryset(self):
        return (
            Trip.objects.filter(user=self.request.user)
            .prefetch_related("trip_places__place")
            .annotate(total_places=Count("trip_places"))
            .order_by("-created_at")
        )


class TripDetail(LoginRequiredMixin, TripOwnerRequiredMixin, DetailView):
    model = Trip
    template_name = "travel/trip-detail.html"
    login_url = "login"

    def get_queryset(self):
        return Trip.objects.select_related("user").prefetch_related(
            Prefetch(
                "trip_places",
                queryset=TripPlace.objects.select_related("place").order_by(
                    "day_number", "id"
                ).prefetch_related("place__reviews"),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_itinerary = defaultdict(list)
        map_points = []

        for item in self.object.trip_places.all():
            grouped_itinerary[item.day_number].append(item)
            if item.place.latitude is not None and item.place.longitude is not None:
                ratings = [review.rating for review in item.place.reviews.all()]
                average_rating = (sum(ratings) / len(ratings)) if ratings else 0
                map_points.append(
                    {
                        "name": item.place.place_name,
                        "latitude": item.place.latitude,
                        "longitude": item.place.longitude,
                        "day_number": item.day_number,
                        "rating": average_rating,
                    }
                )

        context["grouped_itinerary"] = dict(grouped_itinerary)
        context["trip_place_form"] = TripPlaceForm()
        context["map_points"] = map_points
        return context


class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = "travel/trip-form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Trip created successfully.")
        return super().form_valid(form)


class TripUpdate(LoginRequiredMixin, TripOwnerRequiredMixin, UpdateView):
    model = Trip
    form_class = TripForm
    template_name = "travel/trip-form.html"
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Trip updated successfully.")
        return super().form_valid(form)


class TripDelete(LoginRequiredMixin, TripOwnerRequiredMixin, DeleteView):
    model = Trip
    template_name = "travel/trip-delete.html"
    success_url = reverse_lazy("travel:trip_list")
    login_url = "login"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Trip deleted successfully.")
        return super().delete(request, *args, **kwargs)


class AddTripPlace(LoginRequiredMixin, CreateView):
    model = TripPlace
    form_class = TripPlaceForm
    http_method_names = ["post"]
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, pk=self.kwargs["pk"])
        if self.trip.user != request.user:
            messages.error(request, "You are not authorized to modify this trip.")
            return redirect("travel:trip_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.trip = self.trip
        messages.success(self.request, "Place added to trip itinerary.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("travel:trip_detail", kwargs={"pk": self.trip.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Please provide a valid place and day number.")
        return redirect("travel:trip_detail", pk=self.trip.pk)


class DeleteTripPlace(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TripPlace
    template_name = "travel/tripplace-delete.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().trip.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to modify this trip.")
        return redirect("travel:trip_list")

    def get_success_url(self):
        messages.success(self.request, "Itinerary item removed.")
        return reverse_lazy("travel:trip_detail", kwargs={"pk": self.object.trip.pk})
