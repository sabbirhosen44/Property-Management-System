from django.urls import path
from .views import HomeView, PropertyListView, PropertyDetailView, CityAutocompleteView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("properties/", PropertyListView.as_view(), name="property_list"),
    path(
        "properties/<slug:slug>/", PropertyDetailView.as_view(), name="property_detail"
    ),
    path("api/cities/", CityAutocompleteView.as_view(), name="city_autocomplete"),
]
