from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Configure complètement le site avec tout le contenu et les interactions'

    def handle(self, *args, **options):
        self.stdout.write('Configuration complète de MythPedia en cours...')
        
        try:
            # 0. Nettoyage des faux commentaires
            self.stdout.write('0/4 - Nettoyage des faux commentaires...')
            call_command('clean_comments')
            
            # 1. Peuplement des mythologies
            self.stdout.write('1/4 - Peuplement des mythologies et contenu...')
            call_command('seed_comprehensive')
            
            # 2. Génération des images
            self.stdout.write('2/4 - Génération des images de qualité...')
            call_command('generate_images')
            
            # 3. Génération des interactions (désactivé pour éviter les faux commentaires)
            self.stdout.write('3/4 - Génération des commentaires et notations (désactivé)...')
            # call_command('generate_interactions')  # Désactivé pour éviter les faux commentaires
            
            self.stdout.write(self.style.SUCCESS('🎉 Configuration complète terminée avec succès !'))
            self.stdout.write('')
            self.stdout.write('📊 Résumé du contenu créé:')
            from mythpedia.models import Mythology, Character, MythStory, Comment, Rating
            self.stdout.write(f'   • {Mythology.objects.count()} mythologies')
            self.stdout.write(f'   • {Character.objects.count()} personnages')
            self.stdout.write(f'   • {MythStory.objects.count()} histoires')
            self.stdout.write(f'   • {Comment.objects.count()} commentaires')
            self.stdout.write(f'   • {Rating.objects.count()} notations')
            self.stdout.write('')
            self.stdout.write('🚀 Votre site est prêt !')
            self.stdout.write('   Lancez le serveur avec: python manage.py runserver')
            self.stdout.write('   Accédez au site: http://127.0.0.1:8000/')
            self.stdout.write('')
            self.stdout.write('👥 Utilisateurs de démonstration (mot de passe: demo123):')
            from django.contrib.auth.models import User
            demo_users = User.objects.filter(username__in=['zeus_fan', 'odin_lover', 'ra_worshipper', 'thor_follower', 'athena_scholar'])
            for user in demo_users:
                self.stdout.write(f'   • {user.username} ({user.email})')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la configuration: {e}'))
            raise