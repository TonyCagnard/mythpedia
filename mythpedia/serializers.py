from rest_framework import serializers
from .models import Mythology, Character, MythStory, Comment, Rating

class MythologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mythology
        fields = ['id', 'title', 'slug', 'icon_class', 'color_from', 'color_to', 
                  'description', 'card_summary']
        read_only_fields = ['id']

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'slug', 'role', 'description', 'image_url', 
                  'mythology']
        read_only_fields = ['id']
        depth = 1  # Inclure les données de la mythologie associée

class MythStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MythStory
        fields = ['id', 'title', 'slug', 'summary', 'full_text', 'themes', 
                  'image_url', 'mythology', 'characters']
        read_only_fields = ['id']
        depth = 1  # Inclure les données de la mythologie associée

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'text', 
                  'created_at', 'updated_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'user', 'content_type', 'object_id', 'score', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']