from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from .models import Property


class HomeView(TemplateView):

    template_name = "property_app/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["featured_properties"] = Property.objects.select_related(
            "location"
        ).all()[:6]

        context["total_properties"] = Property.objects.count()

        return context


class PropertyListView(ListView):

    model = Property
    template_name = "property_app/property_list.html"
    context_object_name = "properties"
    paginate_by = 10

    def get_queryset(self):

        queryset = Property.objects.select_related("location")

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

        if property_obj.location.point and property_obj.point:

            # Distance in kilometers
            context["distance"] = round(
                property_obj.location.point.distance(property_obj.point) * 111.32, 2
            )

        return context
