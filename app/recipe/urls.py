"""
URL patterns for the recipe app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
#  This is how we register a viewset with a router
router.register('recipes', views.RecipeViewSet)

#  Setting app name for the URL patterns for reverse() lookup function
app_name = 'recipe'

urlpatterns = [
    #  This is how we include a router in the URL patterns
    path('', include(router.urls)),
]
