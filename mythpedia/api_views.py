from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from .models import Mythology, Character, MythStory, Comment, Rating
from .serializers import (
    MythologySerializer, CharacterSerializer, MythStorySerializer,
    CommentSerializer, RatingSerializer
)

class MythologyFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Mythology
        fields = ['title', 'description']

class CharacterFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    role = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    mythology = ModelChoiceFilter(queryset=Mythology.objects.all())
    
    class Meta:
        model = Character
        fields = ['name', 'role', 'description', 'mythology']

class MythStoryFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    summary = CharFilter(lookup_expr='icontains')
    themes = CharFilter(lookup_expr='icontains')
    mythology = ModelChoiceFilter(queryset=Mythology.objects.all())
    
    class Meta:
        model = MythStory
        fields = ['title', 'summary', 'themes', 'mythology']

class MythologyViewSet(viewsets.ModelViewSet):
    queryset = Mythology.objects.all()
    serializer_class = MythologySerializer
    filterset_class = MythologyFilter
    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', 'description', 'card_summary']
    
    @action(detail=True, methods=['get'])
    def characters(self, request, pk=None):
        """Retourne tous les personnages d'une mythologie spécifique"""
        mythology = self.get_object()
        characters = mythology.characters.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        """Retourne toutes les histoires d'une mythologie spécifique"""
        mythology = self.get_object()
        stories = mythology.stories.all()
        serializer = MythStorySerializer(stories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ratings_summary(self, request, pk=None):
        """Retourne un résumé des notations pour une mythologie spécifique"""
        mythology = self.get_object()
        ratings = Rating.objects.filter(
            content_type='MYTHOLOGY',
            object_id=mythology.id
        )
        
        # Calculer les statistiques
        avg_rating = ratings.aggregate(avg=Avg('score'))['avg'] or 0
        total_ratings = ratings.count()
        
        return Response({
            'mythology': mythology.title,
            'average_rating': round(avg_rating, 1),
            'total_ratings': total_ratings,
            'rating_distribution': {
                '1_star': ratings.filter(score=1).count(),
                '2_stars': ratings.filter(score=2).count(),
                '3_stars': ratings.filter(score=3).count(),
                '4_stars': ratings.filter(score=4).count(),
                '5_stars': ratings.filter(score=5).count(),
            }
        })

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.select_related('mythology')
    serializer_class = CharacterSerializer
    filterset_class = CharacterFilter
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name', 'role', 'description']
    
    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        """Retourne toutes les histoires où ce personnage apparaît"""
        character = self.get_object()
        stories = character.featured_in_stories.all()
        serializer = MythStorySerializer(stories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ratings_summary(self, request, pk=None):
        """Retourne un résumé des notations pour un personnage spécifique"""
        character = self.get_object()
        ratings = Rating.objects.filter(
            content_type='CHARACTER',
            object_id=character.id
        )
        
        # Calculer les statistiques
        avg_rating = ratings.aggregate(avg=Avg('score'))['avg'] or 0
        total_ratings = ratings.count()
        
        return Response({
            'character': character.name,
            'mythology': character.mythology.title,
            'average_rating': round(avg_rating, 1),
            'total_ratings': total_ratings,
            'rating_distribution': {
                '1_star': ratings.filter(score=1).count(),
                '2_stars': ratings.filter(score=2).count(),
                '3_stars': ratings.filter(score=3).count(),
                '4_stars': ratings.filter(score=4).count(),
                '5_stars': ratings.filter(score=5).count(),
            }
        })

class MythStoryViewSet(viewsets.ModelViewSet):
    queryset = MythStory.objects.select_related('mythology').prefetch_related('characters')
    serializer_class = MythStorySerializer
    filterset_class = MythStoryFilter
    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', 'summary', 'full_text', 'themes']
    
    @action(detail=True, methods=['get'])
    def characters(self, request, pk=None):
        """Retourne tous les personnages d'une histoire spécifique"""
        story = self.get_object()
        characters = story.characters.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ratings_summary(self, request, pk=None):
        """Retourne un résumé des notations pour une histoire spécifique"""
        story = self.get_object()
        ratings = Rating.objects.filter(
            content_type='STORY',
            object_id=story.id
        )
        
        # Calculer les statistiques
        avg_rating = ratings.aggregate(avg=Avg('score'))['avg'] or 0
        total_ratings = ratings.count()
        
        return Response({
            'story': story.title,
            'mythology': story.mythology.title,
            'average_rating': round(avg_rating, 1),
            'total_ratings': total_ratings,
            'rating_distribution': {
                '1_star': ratings.filter(score=1).count(),
                '2_stars': ratings.filter(score=2).count(),
                '3_stars': ratings.filter(score=3).count(),
                '4_stars': ratings.filter(score=4).count(),
                '5_stars': ratings.filter(score=5).count(),
            }
        })

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_approved=True).select_related('user')
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['text']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Permettre aux utilisateurs de voir tous les commentaires, mais limiter les actions
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return queryset  # Les admin peuvent voir tous les commentaires
            else:
                # Les utilisateurs non-admin ne voient que leurs propres commentaires non approuvés
                return queryset.filter(user=self.request.user) | queryset.filter(is_approved=True)
        return queryset.filter(is_approved=True)  # Les utilisateurs non connectés ne voient que les commentaires approuvés

class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rating.objects.select_related('user')
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Seuls les admin peuvent voir toutes les notations
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)  # Les utilisateurs ne voient que leurs propres notations