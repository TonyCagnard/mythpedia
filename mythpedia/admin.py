from django.contrib import admin
# MODIFICATION ICI : Ajouter Suggestion et MythStory à la liste des imports
from .models import Mythology, Character, FavoriteMythology, FavoriteCharacter, Suggestion, MythStory

@admin.register(Mythology)
class MythologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'icon_class', 'color_from', 'color_to', 'card_summary') # Ajout de card_summary pour visibilité
    search_fields = ('title', 'description', 'card_summary')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20 # Optionnel: nombre d'items par page

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'mythology', 'role', 'slug') # Ajout de slug pour visibilité
    list_filter = ('mythology',)
    search_fields = ('name', 'role', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ('mythology',)
    list_per_page = 20

@admin.register(FavoriteMythology)
class FavoriteMythologyAdmin(admin.ModelAdmin):
    list_display = ('user', 'mythology', 'added_on')
    list_filter = ('user', 'mythology__title') # Filtrer par titre de mythologie
    date_hierarchy = 'added_on'
    search_fields = ('user__username', 'mythology__title')
    list_select_related = ('user', 'mythology') # Optimisation
    list_per_page = 25

@admin.register(FavoriteCharacter)
class FavoriteCharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'character_name_with_mythology', 'added_on')
    list_filter = ('user', 'character__mythology__title') # Filtre par mythologie du personnage
    date_hierarchy = 'added_on'
    search_fields = ('user__username', 'character__name', 'character__mythology__title')
    list_select_related = ('user', 'character', 'character__mythology') # Optimisation

    @admin.display(description='Personnage (Mythologie)', ordering='character__name')
    def character_name_with_mythology(self, obj):
        return f"{obj.character.name} ({obj.character.mythology.title})"

# --- NOUVELLE CLASSE ADMIN POUR LES SUGGESTIONS ---
@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'submission_type', 'user_display', 'status', 'submitted_on_formatted')
    list_filter = ('status', 'submission_type', 'submitted_on')
    search_fields = ('title', 'description', 'user__username', 'name_or_email')
    list_editable = ('status',) # Permet de changer le statut directement depuis la liste
    readonly_fields = ('submitted_on', 'user', 'name_or_email') # Ces champs ne sont pas modifiables par l'admin directement ici
    
    fieldsets = (
        ("Détails de la Suggestion", {
            'fields': ('submission_type', 'title', 'description')
        }),
        ("Informations du Soumissionnaire", {
            'classes': ('collapse',), # Peut être réduit
            'fields': ('user', 'name_or_email', 'submitted_on')
        }),
        ("Contenu Concerné (si applicable pour une correction/ajout)", {
            'classes': ('collapse',),
            'fields': ('related_mythology', 'related_character') # Ajoutez 'related_story' si vous l'avez
        }),
        ("Gestion et Suivi par l'Administration", {
            'fields': ('status', 'admin_notes')
        }),
    )
    date_hierarchy = 'submitted_on'
    list_per_page = 20

    @admin.display(description='Soumis par', ordering='user__username') # Permet de trier par nom d'utilisateur
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return obj.name_or_email or "Anonyme"

    @admin.display(description='Date de Soumission', ordering='submitted_on')
    def submitted_on_formatted(self, obj):
        return obj.submitted_on.strftime("%d %b %Y, %H:%M")

# --- NOUVELLE CLASSE ADMIN POUR LES HISTOIRES/MYTHES ---
@admin.register(MythStory)
class MythStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'mythology', 'get_themes_display', 'get_characters_count', 'slug')
    list_filter = ('mythology', 'characters')
    search_fields = ('title', 'summary', 'full_text', 'mythology__title', 'characters__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('characters',)
    list_select_related = ('mythology',)
    list_per_page = 20
    
    fieldsets = (
        ("Informations Principales", {
            'fields': ('mythology', 'title', 'slug')
        }),
        ("Contenu de l'Histoire", {
            'fields': ('summary', 'full_text', 'image_url')
        }),
        ("Personnages et Thèmes", {
            'fields': ('characters', 'themes')
        }),
    )
    
    @admin.display(description='Thèmes')
    def get_themes_display(self, obj):
        if obj.themes:
            # Affiche les 3 premiers thèmes si trop nombreux
            themes_list = [t.strip() for t in obj.themes.split(',')]
            if len(themes_list) > 3:
                return ', '.join(themes_list[:3]) + '...'
            return ', '.join(themes_list)
        return "Aucun"
    
    @admin.display(description='Nb. Personnages')
    def get_characters_count(self, obj):
        return obj.characters.count()