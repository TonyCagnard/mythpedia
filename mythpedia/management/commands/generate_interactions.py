from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from mythpedia.models import Comment, Rating, Mythology, Character, MythStory
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Génère des commentaires et des notations aléatoires pour rendre le site plus vivant'

    def handle(self, *args, **options):
        self.stdout.write('Génération d\'interactions (commentaires et notations)...')
        
        # Créer des utilisateurs de démonstration si nécessaire
        demo_users = []
        usernames = ['zeus_fan', 'odin_lover', 'ra_worshipper', 'thor_follower', 'athena_scholar']
        
        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': username.split('_')[0].title(),
                    'last_name': username.split('_')[1].title() if '_' in username else 'User',
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
            demo_users.append(user)
        
        self.stdout.write(f'-> {len(demo_users)} utilisateurs de démonstration créés/vérifiés')
        
        # Commentaires prédéfinis pour différents types de contenu
        mythology_comments = [
            "Cette mythologie est fascinante ! J'adore apprendre les origines de ces croyances.",
            "Les récits sont incroyablement riches en symbolisme et en leçons de vie.",
            "Je suis émerveillé par la complexité de ce panthéon divin.",
            "Les connections entre les différents dieux sont vraiment intéressantes à étudier.",
            "C'est étonnant de voir comment ces mythes ont influencé notre culture moderne.",
        ]
        
        character_comments = [
            "Quel personnage fascinant ! Son histoire est vraiment inspirante.",
            "Je ne connaissais pas ce dieu/déesse, merci pour cette découverte.",
            "Les pouvoirs décrits sont incroyables, j'aimerais en savoir plus.",
            "Ce personnage a une place spéciale dans mon cœur depuis mon enfance.",
            "Les détails sur son rôle sont très bien expliqués, bravo !",
        ]
        
        story_comments = [
            "Ce récit est absolument captivant ! Je n'ai pas pu m'arrêter de lire.",
            "La manière dont cette histoire explique des phénomènes naturels est géniale.",
            "J'adore les leçons morales cachées dans ce mythe.",
            "C'est l'une de mes histoires préférées de cette mythologie.",
            "Les personnages sont si bien développés dans ce récit.",
        ]
        
        # Générer des commentaires pour les mythologies
        mythologies = Mythology.objects.all()
        comments_created = 0
        
        for mythology in mythologies:
            # 2-5 commentaires par mythologie
            num_comments = random.randint(2, 5)
            for _ in range(num_comments):
                user = random.choice(demo_users)
                text = random.choice(mythology_comments)
                
                Comment.objects.create(
                    user=user,
                    content_type='MYTHOLOGY',
                    object_id=mythology.id,
                    content_type_field=ContentType.objects.get_for_model(Mythology),
                    text=text,
                    created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                )
                comments_created += 1
        
        # Générer des commentaires pour les personnages
        characters = Character.objects.all()
        for character in characters:
            # 1-3 commentaires par personnage
            num_comments = random.randint(1, 3)
            for _ in range(num_comments):
                user = random.choice(demo_users)
                text = random.choice(character_comments)
                
                Comment.objects.create(
                    user=user,
                    content_type='CHARACTER',
                    object_id=character.id,
                    content_type_field=ContentType.objects.get_for_model(Character),
                    text=text,
                    created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                )
                comments_created += 1
        
        # Générer des commentaires pour les histoires
        stories = MythStory.objects.all()
        for story in stories:
            # 2-4 commentaires par histoire
            num_comments = random.randint(2, 4)
            for _ in range(num_comments):
                user = random.choice(demo_users)
                text = random.choice(story_comments)
                
                Comment.objects.create(
                    user=user,
                    content_type='STORY',
                    object_id=story.id,
                    content_type_field=ContentType.objects.get_for_model(MythStory),
                    text=text,
                    created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                )
                comments_created += 1
        
        self.stdout.write(f'-> {comments_created} commentaires créés')
        
        # Générer des notations
        ratings_created = 0
        
        # Notations pour les mythologies
        for mythology in mythologies:
            # 3-8 notations par mythologie
            num_ratings = random.randint(3, 8)
            users_sampled = random.sample(demo_users, min(num_ratings, len(demo_users)))
            for user in users_sampled:
                score = random.randint(3, 5)  # Tendance positive
                
                rating, created = Rating.objects.get_or_create(
                    user=user,
                    content_type='MYTHOLOGY',
                    object_id=mythology.id,
                    content_type_field=ContentType.objects.get_for_model(Mythology),
                    defaults={
                        'score': score,
                        'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                    }
                )
                if created:
                    ratings_created += 1
        
        # Notations pour les personnages
        for character in characters:
            # 2-6 notations par personnage
            num_ratings = random.randint(2, 6)
            users_sampled = random.sample(demo_users, min(num_ratings, len(demo_users)))
            for user in users_sampled:
                score = random.randint(3, 5)  # Tendance positive
                
                rating, created = Rating.objects.get_or_create(
                    user=user,
                    content_type='CHARACTER',
                    object_id=character.id,
                    content_type_field=ContentType.objects.get_for_model(Character),
                    defaults={
                        'score': score,
                        'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                    }
                )
                if created:
                    ratings_created += 1
        
        # Notations pour les histoires
        for story in stories:
            # 3-7 notations par histoire
            num_ratings = random.randint(3, 7)
            users_sampled = random.sample(demo_users, min(num_ratings, len(demo_users)))
            for user in users_sampled:
                score = random.randint(3, 5)  # Tendance positive
                
                rating, created = Rating.objects.get_or_create(
                    user=user,
                    content_type='STORY',
                    object_id=story.id,
                    content_type_field=ContentType.objects.get_for_model(MythStory),
                    defaults={
                        'score': score,
                        'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                    }
                )
                if created:
                    ratings_created += 1
        
        self.stdout.write(f'-> {ratings_created} notations créées')
        
        self.stdout.write(self.style.SUCCESS('Génération d\'interactions terminée avec succès !'))
        self.stdout.write('Utilisateurs de démonstration créés (mot de passe: demo123):')
        for user in demo_users:
            self.stdout.write(f'  - {user.username} ({user.email})')