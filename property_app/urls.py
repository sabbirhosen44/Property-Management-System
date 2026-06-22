from django.urls import path
from .views import HomeView, PropertyListView, PropertyDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("properties/", PropertyListView.as_view(), name="property_list"),
    path(
        "properties/<slug:slug>/", PropertyDetailView.as_view(), name="property_detail"
    ),
]
