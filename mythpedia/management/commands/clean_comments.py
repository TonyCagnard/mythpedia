from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mythpedia.models import Comment, Rating

class Command(BaseCommand):
    help = 'Supprime les commentaires et notations des utilisateurs de démonstration'

    def handle(self, *args, **options):
        self.stdout.write('Nettoyage des commentaires et notations des utilisateurs de démonstration...')
        
        # Liste des utilisateurs de démonstration à supprimer
        demo_usernames = ['zeus_fan', 'odin_lover', 'ra_worshipper', 'thor_follower', 'athena_scholar']
        
        # Supprimer les commentaires des utilisateurs de démonstration
        comments_deleted = 0
        for username in demo_usernames:
            try:
                user = User.objects.get(username=username)
                user_comments = Comment.objects.filter(user=user)
                count = user_comments.count()
                user_comments.delete()
                comments_deleted += count
                self.stdout.write(f'  - {count} commentaires supprimés pour {username}')
            except User.DoesNotExist:
                self.stdout.write(f'  - Utilisateur {username} non trouvé')
        
        # Supprimer les notations des utilisateurs de démonstration
        ratings_deleted = 0
        for username in demo_usernames:
            try:
                user = User.objects.get(username=username)
                user_ratings = Rating.objects.filter(user=user)
                count = user_ratings.count()
                user_ratings.delete()
                ratings_deleted += count
                self.stdout.write(f'  - {count} notations supprimées pour {username}')
            except User.DoesNotExist:
                pass  # Déjà géré ci-dessus
        
        self.stdout.write(self.style.SUCCESS(f'Nettoyage terminé ! {comments_deleted} commentaires et {ratings_deleted} notations supprimés.'))