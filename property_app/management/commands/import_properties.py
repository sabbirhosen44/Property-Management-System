import pandas as pd

from django.core.management.base import BaseCommand

from property_app.models import (
    Location,
    Property,
)


class Command(BaseCommand):

    help = "Import properties from CSV"

    def add_arguments(self, parser):

        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):

        csv_file = options["csv_file"]

        df = pd.read_csv(csv_file)

        imported = 0

        for _, row in df.iterrows():

            location, _ = Location.objects.get_or_create(
                name=row["city"],
                defaults={
                    "slug": row["city"].lower().replace(" ", "-"),
                    "country": row["country"],
                    "state": row["state"],
                    "city": row["city"],
                },
            )

            Property.objects.get_or_create(
                slug=row["slug"],
                defaults={
                    "location": location,
                    "title": row["title"],
                    "description": "",
                    "property_type": row["property_type"],
                    "status": row["status"],
                    "price": row["price"],
                    "bedrooms": row["bedrooms"],
                    "bathrooms": row["bathrooms"],
                    "address": row["address"],
                },
            )

            imported += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {imported} properties")
        )
