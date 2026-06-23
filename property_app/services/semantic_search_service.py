from pgvector.django import CosineDistance

from property_app.models import Location

from property_app.services.embedding_service import (
    EmbeddingService
)


class SemanticSearchService:

    @staticmethod
    def search(query):

        query_embedding = (
            EmbeddingService.generate_embedding(
                query
            )
        )

        return (
            Location.objects
            .exclude(embedding=None)
            .order_by(
                CosineDistance(
                    "embedding",
                    query_embedding
                )
            )[:10]
        )