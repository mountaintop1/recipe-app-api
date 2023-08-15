"""
Serializers for recipe app
"""
from core.models import Recipe

from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    class Meta:
        """Serializer meta class"""
        model = Recipe
        fields = (
            'id', 'title', 'time_minutes', 'price', 'link',
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects"""
    class Meta(RecipeSerializer.Meta):
        """Serializer meta class"""
        fields = RecipeSerializer.Meta.fields + ('description',)
