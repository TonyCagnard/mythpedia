from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views_simple import (
    MythologyViewSet, CharacterViewSet, MythStoryViewSet,
    CommentViewSet, RatingViewSet
)

# Créer un routeur pour les ViewSets de l'API
router = DefaultRouter()
router.register(r'mythologies', MythologyViewSet)
router.register(r'characters', CharacterViewSet)
router.register(r'stories', MythStoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)

# Les URLs de l'API sont déterminées automatiquement par le routeur
urlpatterns = [
    path('', include(router.urls)),
]