from django.core.management.base import BaseCommand

from property_app.models import Location

from property_app.services.embedding_service import (
    EmbeddingService,
)


class Command(BaseCommand):

    help = "Generate location embeddings"

    def handle(self, *args, **kwargs):

        locations = Location.objects.all()

        for location in locations:

            text = (
                f"{location.city} "
                f"{location.state} "
                f"{location.country}"
                f"{location.description}"
            )

            location.embedding = (
                EmbeddingService.generate_embedding(
                    text
                )
            )

            location.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Embedded {location.city}"
                )
            )