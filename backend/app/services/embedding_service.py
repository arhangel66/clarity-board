"""Embedding service for semantic positioning."""

import math
import random

import numpy as np
from openai import OpenAI

from app.models import Card


class EmbeddingService:
    """Service for generating embeddings and calculating positions."""

    def __init__(self, openai_client: OpenAI) -> None:
        """Initialize embedding service.

        Args:
            openai_client: OpenAI client instance.
        """
        self.client = openai_client
        self.model = "text-embedding-3-small"
        self.embedding_dimension = 1536  # Default for text-embedding-3-small

    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding vector for text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding

    def cosine_similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.

        Returns:
            Cosine similarity score between -1 and 1.
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def find_similar_cards(
        self,
        new_embedding: list[float],
        existing_cards: list[Card],
        top_k: int = 3,
    ) -> list[Card]:
        """Find most similar existing cards to a new embedding.

        Args:
            new_embedding: Embedding of the new card.
            existing_cards: List of existing cards with embeddings.
            top_k: Number of similar cards to return.

        Returns:
            List of most similar cards.
        """
        if not existing_cards:
            return []

        cards_with_embeddings = [c for c in existing_cards if c.embedding]

        if not cards_with_embeddings:
            return []

        similarities = []
        for card in cards_with_embeddings:
            if card.embedding:
                sim = self.cosine_similarity(new_embedding, card.embedding)
                similarities.append((card, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)

        return [card for card, _ in similarities[:top_k]]

    def get_position_for_new_card(
        self,
        new_embedding: list[float],
        existing_cards: list[Card],
        is_root: bool = False,
    ) -> tuple[float, float]:
        """Calculate position for a new card based on embeddings.

        Args:
            new_embedding: Embedding of the new card.
            existing_cards: List of existing cards.
            is_root: Whether this is the root card.

        Returns:
            Tuple of (x, y) coordinates in [0, 1] range.
        """
        # Root card always goes to center
        if is_root or not existing_cards:
            return (0.5, 0.5)

        # Find similar cards
        similar_cards = self.find_similar_cards(new_embedding, existing_cards, top_k=3)

        if not similar_cards:
            # No similar cards found, place randomly around center
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0.15, 0.35)
            return (
                self._clamp(0.5 + math.cos(angle) * radius),
                self._clamp(0.5 + math.sin(angle) * radius),
            )

        # Calculate centroid of similar cards
        cx = sum(c.x for c in similar_cards) / len(similar_cards)
        cy = sum(c.y for c in similar_cards) / len(similar_cards)

        # Add offset to avoid overlap
        angle = random.uniform(0, 2 * math.pi)
        offset = 0.1  # 10% of canvas

        new_x = cx + math.cos(angle) * offset
        new_y = cy + math.sin(angle) * offset

        # Avoid collisions with existing cards
        new_x, new_y = self._avoid_collisions(new_x, new_y, existing_cards)

        return (self._clamp(new_x), self._clamp(new_y))

    def _avoid_collisions(
        self,
        x: float,
        y: float,
        existing_cards: list[Card],
        min_distance: float = 0.08,
        max_attempts: int = 10,
    ) -> tuple[float, float]:
        """Adjust position to avoid overlapping with existing cards.

        Args:
            x: Initial x coordinate.
            y: Initial y coordinate.
            existing_cards: List of existing cards.
            min_distance: Minimum distance between card centers.
            max_attempts: Maximum repositioning attempts.

        Returns:
            Adjusted (x, y) coordinates.
        """
        for _ in range(max_attempts):
            collision = False

            for card in existing_cards:
                distance = math.sqrt((x - card.x) ** 2 + (y - card.y) ** 2)

                if distance < min_distance:
                    collision = True
                    # Push away from the colliding card
                    if distance > 0:
                        dx = (x - card.x) / distance
                        dy = (y - card.y) / distance
                    else:
                        # Same position, random direction
                        angle = random.uniform(0, 2 * math.pi)
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                    x += dx * min_distance * 0.5
                    y += dy * min_distance * 0.5
                    break

            if not collision:
                break

        return (x, y)

    def _clamp(self, value: float, min_val: float = 0.05, max_val: float = 0.95) -> float:
        """Clamp value to range, keeping cards within canvas bounds.

        Args:
            value: Value to clamp.
            min_val: Minimum allowed value.
            max_val: Maximum allowed value.

        Returns:
            Clamped value.
        """
        return max(min_val, min(max_val, value))
