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
    # add place
    path("add/", views.add_place, name="add_place"),
    # edit
    path("update/<int:id>/", views.update_place, name="update_place"),
    # delete place
    path("delete/<int:id>/", views.delete_place, name="delete_place"),
    # view place
    path("view/", views.view_place, name="view_place"),
]
