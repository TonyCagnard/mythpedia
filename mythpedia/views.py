from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .models import Mythology, Character, FavoriteMythology, FavoriteCharacter, Suggestion, MythStory, Comment, Rating
from .forms import SuggestionForm, AdvancedSearchForm, CommentForm, RatingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail # <<< AJOUTÉ pour l'envoi d'email
from django.urls import reverse # <<< AJOUTÉ pour construire des URLs absolues pour l'email

@login_required
def mythology_list(request):
    # Optimisation : précharger les données associées pour éviter les requêtes N+1
    all_mythologies = Mythology.objects.all().order_by('title').prefetch_related('characters', 'stories')
    paginator = Paginator(all_mythologies, 6)  # 6 mythologies par page
    page_number = request.GET.get('page')
    try:
        mythologies_page = paginator.page(page_number)
    except PageNotAnInteger:
        mythologies_page = paginator.page(1)
    except EmptyPage:
        mythologies_page = paginator.page(paginator.num_pages)
    
    context = {
        'mythologies_page': mythologies_page,
        'page_title': 'Liste des Mythologies'
    }
    return render(request, 'mythpedia/mythology_list.html', context)

@login_required
def mythology_detail(request, mythology_slug):
    mythology = get_object_or_404(Mythology, slug=mythology_slug)
    characters = Character.objects.filter(mythology=mythology).order_by('name')
    stories = mythology.stories.all().order_by('title') # Maintenant que MythStory est défini
    
    # Récupérer les commentaires pour cette mythologie
    from django.contrib.contenttypes.models import ContentType
    mythology_ct = ContentType.objects.get_for_model(Mythology)
    comments = Comment.objects.filter(
        content_type='MYTHOLOGY',
        object_id=mythology.id,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Récupérer les notations pour cette mythologie
    ratings = Rating.objects.filter(
        content_type='MYTHOLOGY',
        object_id=mythology.id
    ).select_related('user')
    
    # Calculer la note moyenne
    average_rating = 0
    total_ratings = ratings.count()
    if total_ratings > 0:
        average_rating = sum(r.score for r in ratings) / total_ratings
    
    # Note de l'utilisateur actuel
    user_rating = None
    if request.user.is_authenticated:
        user_rating_obj = ratings.filter(user=request.user).first()
        if user_rating_obj:
            user_rating = user_rating_obj.score
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteMythology.objects.filter(user=request.user, mythology=mythology).exists()
            
    context = {
        'mythology': mythology,
        'characters': characters,
        'stories': stories, # Maintenant actif avec MythStory
        'comments': comments,
        'average_rating': average_rating,
        'total_ratings': total_ratings,
        'user_rating': user_rating,
        'content_type': 'mythology',
        'object_id': mythology.id,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
        'is_favorite': is_favorite,
        'page_title': mythology.title
    }
    return render(request, 'mythpedia/mythology_detail.html', context)

@login_required
def character_detail(request, mythology_slug, character_slug):
    character = get_object_or_404(
        Character.objects.select_related('mythology'), 
        slug=character_slug, 
        mythology__slug=mythology_slug
    )
    is_favorite_character = False
    if request.user.is_authenticated:
        is_favorite_character = FavoriteCharacter.objects.filter(user=request.user, character=character).exists()
    stories_featuring_character = character.featured_in_stories.all().order_by('title') # Maintenant actif avec MythStory
    
    # Récupérer les commentaires pour ce personnage
    from django.contrib.contenttypes.models import ContentType
    character_ct = ContentType.objects.get_for_model(Character)
    comments = Comment.objects.filter(
        content_type='CHARACTER',
        object_id=character.id,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Récupérer les notations pour ce personnage
    ratings = Rating.objects.filter(
        content_type='CHARACTER',
        object_id=character.id
    ).select_related('user')
    
    # Calculer la note moyenne
    average_rating = 0
    total_ratings = ratings.count()
    if total_ratings > 0:
        average_rating = sum(r.score for r in ratings) / total_ratings
    
    # Note de l'utilisateur actuel
    user_rating = None
    if request.user.is_authenticated:
        user_rating_obj = ratings.filter(user=request.user).first()
        if user_rating_obj:
            user_rating = user_rating_obj.score
    
    context = {
        'character': character,
        'mythology': character.mythology,
        'is_favorite_character': is_favorite_character,
        'stories_featuring_character': stories_featuring_character, # Maintenant actif
        'comments': comments,
        'average_rating': average_rating,
        'total_ratings': total_ratings,
        'user_rating': user_rating,
        'content_type': 'character',
        'object_id': character.id,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
        'page_title': character.name
    }
    return render(request, 'mythpedia/character_detail.html', context)

@login_required
def add_to_favorites(request, mythology_slug):
    mythology = get_object_or_404(Mythology, slug=mythology_slug)
    FavoriteMythology.objects.get_or_create(user=request.user, mythology=mythology)
    messages.success(request, f"'{mythology.title}' a été ajoutée à vos favoris.")
    return redirect('mythpedia:mythology_detail', mythology_slug=mythology_slug)

@login_required
def remove_from_favorites(request, mythology_slug):
    mythology = get_object_or_404(Mythology, slug=mythology_slug)
    favorite_entry = FavoriteMythology.objects.filter(user=request.user, mythology=mythology)
    if favorite_entry.exists():
        favorite_entry.delete()
        messages.success(request, f"'{mythology.title}' a été retirée de vos favoris.")
    else:
        messages.info(request, f"'{mythology.title}' n'était pas dans vos favoris.")
    return redirect('mythpedia:mythology_detail', mythology_slug=mythology_slug)

@login_required
def add_character_to_favorites(request, mythology_slug, character_slug):
    character = get_object_or_404(
        Character.objects.select_related('mythology'), 
        slug=character_slug, 
        mythology__slug=mythology_slug
    )
    FavoriteCharacter.objects.get_or_create(user=request.user, character=character)
    messages.success(request, f"'{character.name}' a été ajouté à vos personnages favoris.")
    return redirect('mythpedia:character_detail', mythology_slug=character.mythology.slug, character_slug=character.slug)

@login_required
def remove_character_from_favorites(request, mythology_slug, character_slug):
    character = get_object_or_404(
        Character.objects.select_related('mythology'), 
        slug=character_slug, 
        mythology__slug=mythology_slug
    )
    favorite_entry = FavoriteCharacter.objects.filter(user=request.user, character=character)
    if favorite_entry.exists():
        favorite_entry.delete()
        messages.success(request, f"'{character.name}' a été retiré de vos personnages favoris.")
    else:
        messages.info(request, f"'{character.name}' n'était pas dans vos personnages favoris.")
    return redirect('mythpedia:character_detail', mythology_slug=character.mythology.slug, character_slug=character.slug)

@login_required
def user_favorites_list(request):
    favorite_mythologies_entries = FavoriteMythology.objects.filter(user=request.user).select_related('mythology').order_by('-added_on')
    mythologies_in_favorites = [fav.mythology for fav in favorite_mythologies_entries]
    favorite_characters_entries = FavoriteCharacter.objects.filter(user=request.user).select_related('character', 'character__mythology').order_by('-added_on')
    characters_in_favorites = [fav.character for fav in favorite_characters_entries]
    context = {
        'favorite_mythologies': mythologies_in_favorites,
        'favorite_characters': characters_in_favorites,
        'page_title': 'Mes Favoris'
    }
    return render(request, 'mythpedia/user_favorites_list.html', context)

# --- VUE POUR LES SUGGESTIONS AVEC NOTIFICATION EMAIL ---
def submit_suggestion(request):
    form_kwargs = {}
    if request.user.is_authenticated:
        form_kwargs['user'] = request.user
        
    if request.method == 'POST':
        form = SuggestionForm(request.POST, **form_kwargs)
        if form.is_valid():
            suggestion = form.save(commit=False)
            if request.user.is_authenticated:
                suggestion.user = request.user
            suggestion.save()
            
            # --- Envoi de l'email de notification ---
            try:
                subject = f"Nouvelle Suggestion sur MythPedia: {suggestion.title[:50]}"
                user_info = suggestion.user.username if suggestion.user else suggestion.name_or_email or "Anonyme"
                
                # Construire l'URL absolue vers la suggestion dans l'admin
                # Note: admin:app_label_model_change ou admin:app_label_model_changelist
                try:
                    admin_url_path = reverse('admin:mythpedia_suggestion_change', args=[suggestion.id])
                    admin_url_full = request.build_absolute_uri(admin_url_path)
                except Exception: # Au cas où le reverse échoue pour une raison quelconque
                    admin_url_full = request.build_absolute_uri(f'/admin/mythpedia/suggestion/{suggestion.id}/change/')


                message_body = (
                    f"Une nouvelle suggestion a été soumise :\n\n"
                    f"Type: {suggestion.get_submission_type_display()}\n"
                    f"Titre: {suggestion.title}\n"
                    f"Soumis par: {user_info}\n\n"
                    f"Description:\n{suggestion.description}\n\n"
                    f"Voir dans l'admin : {admin_url_full}\n"
                )
                
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL, # Votre adresse d'expéditeur configurée
                    [settings.ADMIN_EMAIL_FOR_SUGGESTIONS], # L'adresse admin configurée
                    fail_silently=False, # Mettre à True en production pour ne pas bloquer si l'email échoue
                )
                messages.success(request, "Merci ! Votre suggestion a été envoyée et sera examinée.")
            except Exception as e:
                # Loggez l'erreur d'email ici si vous avez un système de logging
                print(f"Erreur lors de l'envoi de l'email de notification de suggestion: {e}")
                messages.warning(request, "Votre suggestion a été enregistrée, mais une erreur est survenue lors de l'envoi de la notification à l'administrateur.")

            return redirect('mythpedia:mythology_list') 
        else:
            messages.error(request, "Il y a eu une erreur dans votre formulaire. Veuillez vérifier les champs et les messages ci-dessous.")
    else:
        form = SuggestionForm(**form_kwargs)
    context = {
        'form': form,
        'page_title': 'Suggérer du Contenu'
    }
    return render(request, 'mythpedia/submit_suggestion.html', context)

# --- Vues d'Authentification ---
def register_request(request):
    if request.user.is_authenticated:
        return redirect('mythpedia:mythology_list')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue.")
            return redirect('mythpedia:mythology_list')
        else:
            for field_name, error_list in form.errors.as_data().items():
                for error in error_list:
                    field_label = form.fields[field_name].label if field_name != '__all__' and field_name in form.fields else ''
                    messages.error(request, f"{field_label or 'Erreur Générale'}: {error.message}")
    else:
        form = UserCreationForm()
    return render(request, "mythpedia/register.html", {"register_form": form, "page_title": "Inscription"})

def login_request(request):
    if request.user.is_authenticated:
        next_page = request.GET.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(settings.LOGIN_REDIRECT_URL) 
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Vous êtes maintenant connecté en tant que {username}.")
                next_page_from_form = request.POST.get('next', '')
                next_page_from_get = request.GET.get('next', '')
                next_page = next_page_from_form or next_page_from_get
                if next_page:
                    return redirect(next_page)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            for field_name, error_list in form.errors.as_data().items():
                for error in error_list:
                    field_label = form.fields[field_name].label if field_name != '__all__' and field_name in form.fields else 'Erreur'
                    messages.error(request, f"{field_label or 'Erreur Générale'}: {error.message}")
            if not form.errors.items():
                 messages.error(request,"Nom d'utilisateur ou mot de passe invalide (vérification générale).")
    else:
        form = AuthenticationForm()
    return render(request, "mythpedia/login.html", {"login_form": form, "page_title": "Connexion", "next_page": request.GET.get('next', '')})

def logout_request(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect(settings.LOGOUT_REDIRECT_URL)

# --- VUES POUR LES HISTOIRES/MYTHES ---
@login_required
def mythstory_detail(request, mythology_slug, story_slug):
    story = get_object_or_404(
        MythStory.objects.select_related('mythology').prefetch_related('characters'),
        slug=story_slug,
        mythology__slug=mythology_slug
    )
    key_characters = story.characters.all().order_by('name')
    
    # Récupérer les commentaires pour cette histoire
    from django.contrib.contenttypes.models import ContentType
    story_ct = ContentType.objects.get_for_model(MythStory)
    comments = Comment.objects.filter(
        content_type='STORY',
        object_id=story.id,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Récupérer les notations pour cette histoire
    ratings = Rating.objects.filter(
        content_type='STORY',
        object_id=story.id
    ).select_related('user')
    
    # Calculer la note moyenne
    average_rating = 0
    total_ratings = ratings.count()
    if total_ratings > 0:
        average_rating = sum(r.score for r in ratings) / total_ratings
    
    # Note de l'utilisateur actuel
    user_rating = None
    if request.user.is_authenticated:
        user_rating_obj = ratings.filter(user=request.user).first()
        if user_rating_obj:
            user_rating = user_rating_obj.score
    
    context = {
        'story': story,
        'mythology': story.mythology,
        'key_characters': key_characters,
        'comments': comments,
        'average_rating': average_rating,
        'total_ratings': total_ratings,
        'user_rating': user_rating,
        'content_type': 'story',
        'object_id': story.id,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
        'page_title': story.title
    }
    return render(request, 'mythpedia/mythstory_detail.html', context)

# --- VUE POUR LA RECHERCHE AVANCÉE ---
@login_required
def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    results = {
        'mythologies': [],
        'characters': [],
        'stories': []
    }
    query = None
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        search_type = form.cleaned_data.get('search_type', 'all')
        mythology_filter = form.cleaned_data.get('mythology_filter')
        
        # Si une requête est fournie
        if query:
            query_lower = query.lower()
            
            # Recherche dans les mythologies
            if search_type in ['all', 'mythology']:
                mythologies_qs = Mythology.objects.all()
                if mythology_filter:
                    mythologies_qs = mythologies_qs.filter(id=mythology_filter.id)
                results['mythologies'] = mythologies_qs.filter(
                    models.Q(title__icontains=query) |
                    models.Q(description__icontains=query) |
                    models.Q(card_summary__icontains=query)
                ).distinct()
            
            # Recherche dans les personnages
            if search_type in ['all', 'character']:
                characters_qs = Character.objects.select_related('mythology')
                if mythology_filter:
                    characters_qs = characters_qs.filter(mythology=mythology_filter)
                results['characters'] = characters_qs.filter(
                    models.Q(name__icontains=query) |
                    models.Q(role__icontains=query) |
                    models.Q(description__icontains=query)
                ).distinct()
            
            # Recherche dans les histoires
            if search_type in ['all', 'story']:
                stories_qs = MythStory.objects.select_related('mythology').prefetch_related('characters')
                if mythology_filter:
                    stories_qs = stories_qs.filter(mythology=mythology_filter)
                results['stories'] = stories_qs.filter(
                    models.Q(title__icontains=query) |
                    models.Q(summary__icontains=query) |
                    models.Q(full_text__icontains=query) |
                    models.Q(themes__icontains=query) |
                    models.Q(characters__name__icontains=query)
                ).distinct()
    
    context = {
        'form': form,
        'results': results,
        'query': query,
        'page_title': 'Recherche Avancée'
    }
    return render(request, 'mythpedia/search_results.html', context)

# --- VUES POUR LES COMMENTAIRES ET NOTATIONS ---
@login_required
def add_comment(request, content_type, object_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type.upper()
            comment.object_id = object_id
            
            # Récupérer le ContentType approprié
            if content_type == 'mythology':
                ct = ContentType.objects.get_for_model(Mythology)
            elif content_type == 'character':
                ct = ContentType.objects.get_for_model(Character)
            elif content_type == 'story':
                ct = ContentType.objects.get_for_model(MythStory)
            else:
                messages.error(request, "Type de contenu invalide.")
                return redirect('mythpedia:mythology_list')
            
            comment.content_type_field = ct
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")
            
            # Rediriger vers la page appropriée
            if content_type == 'mythology':
                mythology = Mythology.objects.get(pk=object_id)
                return redirect('mythpedia:mythology_detail', mythology_slug=mythology.slug)
            elif content_type == 'character':
                character = Character.objects.get(pk=object_id)
                return redirect('mythpedia:character_detail', mythology_slug=character.mythology.slug, character_slug=character.slug)
            elif content_type == 'story':
                story = MythStory.objects.get(pk=object_id)
                return redirect('mythpedia:mythstory_detail', mythology_slug=story.mythology.slug, story_slug=story.slug)
    else:
        form = CommentForm()
    
    # En cas d'erreur ou de GET, rediriger vers la liste des mythologies
    return redirect('mythpedia:mythology_list')

@login_required
def add_rating(request, content_type, object_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.content_type = content_type.upper()
            rating.object_id = object_id
            
            # Récupérer le ContentType approprié
            if content_type == 'mythology':
                ct = ContentType.objects.get_for_model(Mythology)
            elif content_type == 'character':
                ct = ContentType.objects.get_for_model(Character)
            elif content_type == 'story':
                ct = ContentType.objects.get_for_model(MythStory)
            else:
                messages.error(request, "Type de contenu invalide.")
                return redirect('mythpedia:mythology_list')
            
            rating.content_type_field = ct
            
            # Vérifier si l'utilisateur a déjà noté cet objet
            existing_rating = Rating.objects.filter(
                user=request.user,
                content_type=content_type.upper(),
                object_id=object_id
            ).first()
            
            if existing_rating:
                # Mettre à jour la note existante
                existing_rating.score = rating.score
                existing_rating.save()
                messages.success(request, "Votre note a été mise à jour avec succès.")
            else:
                # Créer une nouvelle note
                rating.save()
                messages.success(request, "Votre note a été ajoutée avec succès.")
            
            # Rediriger vers la page appropriée
            if content_type == 'mythology':
                mythology = Mythology.objects.get(pk=object_id)
                return redirect('mythpedia:mythology_detail', mythology_slug=mythology.slug)
            elif content_type == 'character':
                character = Character.objects.get(pk=object_id)
                return redirect('mythpedia:character_detail', mythology_slug=character.mythology.slug, character_slug=character.slug)
            elif content_type == 'story':
                story = MythStory.objects.get(pk=object_id)
                return redirect('mythpedia:mythstory_detail', mythology_slug=story.mythology.slug, story_slug=story.slug)
    else:
        form = RatingForm()
    
    # En cas d'erreur ou de GET, rediriger vers la liste des mythologies
    return redirect('mythpedia:mythology_list')