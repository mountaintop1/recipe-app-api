"""
Views for recipe app
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Views to manage recipes APIs in the """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id') # This is how we filter objects by user

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list': # This is how we check the action of the request
            return serializers.RecipeSerializer

        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)