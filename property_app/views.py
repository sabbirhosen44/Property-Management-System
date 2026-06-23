from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from .models import Property, Location


class HomeView(TemplateView):
    template_name = "property_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_properties"] = (
            Property.objects
            .select_related("location")
            .prefetch_related("images")
            .filter(is_active=True, is_featured=True)
            .order_by("-created_at")[:6]
        )
        context["total_properties"] = Property.objects.filter(is_active=True).count()
        return context


class PropertyListView(ListView):
    model = Property
    template_name = "property_app/property_list.html"
    context_object_name = "properties"
    paginate_by = 9

    def get_queryset(self):
        qs = (
            Property.objects
            .select_related("location")
            .prefetch_related("images")
            .filter(is_active=True)
        )

        city = self.request.GET.get("city", "").strip()
        if city:
            qs = qs.filter(location__city__icontains=city)

        lat = self.request.GET.get("lat", "").strip()
        lng = self.request.GET.get("lng", "").strip()

        if lat and lng:
            try:
                radius = int(self.request.GET.get("radius", 10))
            except (ValueError, TypeError):
                radius = 10
            radius = max(1, min(radius, 500))

            try:
                user_point = Point(float(lng), float(lat), srid=4326)
                qs = qs.filter(
                    point__distance_lte=(user_point, D(km=radius))
                ).annotate(
                    distance=Distance("point", user_point)
                ).order_by("distance")
                return qs
            except (ValueError, TypeError):
                pass

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lat = self.request.GET.get("lat", "").strip()
        lng = self.request.GET.get("lng", "").strip()

        try:
            radius_km = max(1, min(int(self.request.GET.get("radius", 10)), 500))
        except (ValueError, TypeError):
            radius_km = 10

        context["geo_active"] = bool(lat and lng)
        context["user_lat"] = lat
        context["user_lng"] = lng
        context["radius_km"] = radius_km
        context["city_q"] = self.request.GET.get("city", "").strip()
        context["selected_type"] = self.request.GET.get("type", "").strip()
        context["property_types"] = (
            Property.objects
            .filter(is_active=True)
            .values_list("property_type", flat=True)
            .distinct()
            .order_by("property_type")
        )
        return context


class PropertyDetailView(DetailView):
    model = Property
    slug_field = "slug"
    template_name = "property_app/property_detail.html"
    context_object_name = "property"

    def get_queryset(self):
        return (
            Property.objects
            .select_related("location")
            .prefetch_related("images")
            .filter(is_active=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prop = self.object

        distance_km = None
        if prop.point and prop.location and prop.location.point:
            annotated = (
                Property.objects
                .filter(pk=prop.pk)
                .annotate(dist_to_city=Distance("point", prop.location.point))
                .first()
            )
            if annotated and annotated.dist_to_city is not None:
                distance_km = round(annotated.dist_to_city.km, 2)

        context["distance"] = distance_km
        context["distance_label"] = (
            f"{distance_km} km from {prop.location.city} city centre"
            if distance_km is not None and prop.location
            else None
        )
        return context


class CityAutocompleteView(TemplateView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        results = []

        if len(query) >= 1:
            locations = (
                Location.objects
                .filter(city__icontains=query, is_active=True)
                .distinct()
                .order_by("city")[:5]
            )
            for loc in locations:
                subtitle = f"{loc.state}, {loc.country}" if loc.state else loc.country
                entry = {
                    "type":     "location",
                    "value":    loc.city,
                    "display":  loc.city,
                    "subtitle": subtitle,
                    "url":      None,
                }
                if loc.point:
                    entry["lat"] = loc.point.y
                    entry["lng"] = loc.point.x
                results.append(entry)

            properties = (
                Property.objects
                .select_related("location")
                .filter(title__icontains=query, is_active=True)[:5]
            )
            for prop in properties:
                results.append({
                    "type":     "property",
                    "value":    prop.title,
                    "display":  prop.title,
                    "subtitle": (
                        f"{prop.property_type} in {prop.location.city}"
                        if prop.location else prop.property_type
                    ),
                    "url": f"/properties/{prop.slug}/",
                })

        return JsonResponse({"results": results})