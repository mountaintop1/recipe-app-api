"""
URL patterns for the recipe app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet) # This is how we register a viewset with a router

app_name = 'recipe' # This is how we set the app name for the URL patterns for reverse() lookup function

urlpatterns = [
    path('', include(router.urls)), # This is how we include a router in the URL patterns
]
