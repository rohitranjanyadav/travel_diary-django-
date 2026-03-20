from . import views
from django.urls import path


app_name = "travel"
urlpatterns = [
    # /travel-diary/
    path("", views.index, name="index"),
    # /travel-diary/:id
    path("<int:place_id>/", views.detail, name="detail"),
    # /travel-diary/place
    path("place/", views.place, name="place"),
]
