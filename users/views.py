from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import RegisterForm
from .models import Profile
from travel.models import Place, Review, Trip

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Welcome {username}! Your account has been created."
            )
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        context["profile"] = profile
        context["user_places"] = (
            Place.objects.filter(user_name=self.request.user)
            .only("id", "place_name", "created_at")
            .order_by("-created_at")[:8]
        )
        context["user_trips"] = (
            Trip.objects.filter(user=self.request.user)
            .only("id", "name", "created_at")
            .order_by("-created_at")[:8]
        )
        context["user_reviews"] = (
            Review.objects.filter(user=self.request.user)
            .select_related("place")
            .only("id", "rating", "created_at", "place__id", "place__place_name")
            .order_by("-created_at")[:8]
        )
        return context
