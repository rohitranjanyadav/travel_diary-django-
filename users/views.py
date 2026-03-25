from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile

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

@login_required
def profilepage(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "users/profile.html", {"profile": profile})
