from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from .models import Property, Location


class HomeView(TemplateView):

    template_name = "property_app/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["featured_properties"] = Property.objects.select_related(
            "location"
        ).filter(is_active=True)[:6]

        context["total_properties"] = Property.objects.filter(is_active=True).count()

        return context


class PropertyListView(ListView):

    model = Property
    template_name = "property_app/property_list.html"
    context_object_name = "properties"
    paginate_by = 9

    def get_queryset(self):

        queryset = Property.objects.select_related("location").filter(is_active=True)

        # City Search
        city = self.request.GET.get("city")

        if city:
            queryset = queryset.filter(location__city__icontains=city)

        # Radius Search
        latitude = self.request.GET.get("lat")
        longitude = self.request.GET.get("lng")
        radius = self.request.GET.get("radius", 5)

        if latitude and longitude:

            search_point = Point(float(longitude), float(latitude), srid=4326)

            queryset = queryset.filter(
                point__distance_lte=(search_point, D(km=float(radius)))
            )

        return queryset


class PropertyDetailView(DetailView):

    model = Property
    slug_field = "slug"
    template_name = "property_app/property_detail.html"
    context_object_name = "property"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        property_obj = self.object

        if property_obj.location and property_obj.location.point and property_obj.point:

            # Distance in kilometers
            context["distance"] = round(
                property_obj.location.point.distance(property_obj.point) * 111.32, 2
            )

        return context


class CityAutocompleteView(TemplateView):
    """Returns JSON list of matching city and property names for the autocomplete widget."""

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        results = []

        if len(query) >= 1:
            # 1. Cities matching query
            cities = (
                Location.objects.filter(city__icontains=query, is_active=True)
                .values_list("city", "state", "country")
                .distinct()
                .order_by("city")[:5]
            )
            for city, state, country in cities:
                subtitle = f"{state}, {country}" if state else country
                results.append({
                    "type": "city",
                    "value": city,
                    "display": city,
                    "subtitle": subtitle,
                    "url": None
                })

            # 2. Properties matching query (by title)
            properties = (
                Property.objects.select_related("location")
                .filter(title__icontains=query, is_active=True)[:5]
            )
            for prop in properties:
                results.append({
                    "type": "property",
                    "value": prop.title,
                    "display": prop.title,
                    "subtitle": f"{prop.property_type} in {prop.location.city}",
                    "url": f"/properties/{prop.slug}/"
                })

        return JsonResponse({"results": results})
