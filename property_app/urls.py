from django.urls import path
from .views import HomeView, PropertyListView, PropertyDetailView, CityAutocompleteView,SemanticLocationSearchView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("properties/", PropertyListView.as_view(), name="property_list"),
    path(
        "properties/<slug:slug>/", PropertyDetailView.as_view(), name="property_detail"
    ),
    path("api/cities/", CityAutocompleteView.as_view(), name="city_autocomplete"),
    path("api/semantic-search/",SemanticLocationSearchView.as_view(),name="semantic_search",),
]
