from . import views
from django.urls import path


app_name = "travel"
urlpatterns = [
    # /travel-diary/
    path("", views.IndexClassView.as_view(), name="index"),
    # /travel-diary/:id
    path("<int:pk>/", views.PlaceDetail.as_view(), name="detail"),
    # add review
    path("<int:pk>/review/add/", views.AddReview.as_view(), name="add_review"),
    # /travel-diary/place
    path("place/", views.place, name="place"),
    # add place
    path("add/", views.AddPlace.as_view(), name="add_place"),
    # edit
    path("update/<int:pk>/", views.UpdatePlace.as_view(), name="update_place"),
    # delete place
    path("delete/<int:pk>/", views.DeletePlace.as_view(), name="delete_place"),
    # view place
    path("view/", views.view_place, name="view_place"),
    # trips
    path("trips/", views.TripList.as_view(), name="trip_list"),
    path("trips/add/", views.TripCreate.as_view(), name="trip_add"),
    path("trips/<int:pk>/", views.TripDetail.as_view(), name="trip_detail"),
    path("trips/<int:pk>/update/", views.TripUpdate.as_view(), name="trip_update"),
    path("trips/<int:pk>/delete/", views.TripDelete.as_view(), name="trip_delete"),
    path(
        "trips/<int:pk>/places/add/",
        views.AddTripPlace.as_view(),
        name="trip_place_add",
    ),
    path(
        "trip-places/<int:pk>/delete/",
        views.DeleteTripPlace.as_view(),
        name="trip_place_delete",
    ),
]
