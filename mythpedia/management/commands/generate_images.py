from django.core.management.base import BaseCommand
from mythpedia.models import Character, MythStory
import random

class Command(BaseCommand):
    help = 'Génère des images de meilleure qualité pour les personnages et les histoires'

    def handle(self, *args, **options):
        self.stdout.write('Génération d\'images de qualité...')
        
        # Styles d'images pour différents types de mythologies
        image_styles = {
            'grecque': ['https://i.imgur.com/8X2y0Jl.jpg', 'https://i.imgur.com/9Y3nK7m.jpg', 'https://i.imgur.com/7Lm4pQ2.jpg'],
            'nordique': ['https://i.imgur.com/9Ml3X8N.jpg', 'https://i.imgur.com/4Kn7Y2P.jpg', 'https://i.imgur.com/8Lm4X9Q.jpg'],
            'égyptienne': ['https://i.imgur.com/9Mm8X8C.jpg', 'https://i.imgur.com/4Nn9Y7D.jpg', 'https://i.imgur.com/8Ll9X6E.jpg'],
            'romaine': ['https://i.imgur.com/9Mm9X9P.jpg', 'https://i.imgur.com/4Nn8Y8Q.jpg', 'https://i.imgur.com/8Ll9X7R.jpg'],
            'japonaise': ['https://i.imgur.com/9Mm9X9E.jpg', 'https://i.imgur.com/4Nn8Y8F.jpg', 'https://i.imgur.com/8Ll9X7G.jpg'],
            'hindoue': ['https://i.imgur.com/9Mm9X9R.jpg', 'https://i.imgur.com/4Nn8Y8S.jpg', 'https://i.imgur.com/8Ll9X7T.jpg'],
            'chinoise': ['https://i.imgur.com/9Mm9X9G.jpg', 'https://i.imgur.com/4Nn8Y8H.jpg', 'https://i.imgur.com/8Ll9X7I.jpg'],
            'celtique': ['https://i.imgur.com/9Mm9X9V.jpg', 'https://i.imgur.com/4Nn8Y8W.jpg', 'https://i.imgur.com/8Ll9X7X.jpg'],
            'aztèque': ['https://i.imgur.com/9Mm9X9I.jpg', 'https://i.imgur.com/4Nn8Y8J.jpg', 'https://i.imgur.com/8Ll9X7K.jpg'],
            'aborigène': ['https://i.imgur.com/9Mm9X9V.jpg', 'https://i.imgur.com/4Nn8Y8W.jpg', 'https://i.imgur.com/8Ll9X7X.jpg']
        }
        
        # Générer des URLs d'images uniques pour chaque personnage
        characters = Character.objects.all()
        updated_chars = 0
        
        for character in characters:
            # Déterminer le style en fonction de la mythologie
            mythology_name = character.mythology.title.lower()
            style_key = None
            
            for key in image_styles.keys():
                if key in mythology_name:
                    style_key = key
                    break
            
            if not style_key:
                style_key = random.choice(list(image_styles.keys()))
            
            # Générer une URL unique avec un hash basé sur le nom du personnage
            hash_value = abs(hash(character.name)) % 1000
            image_url = f"https://picsum.photos/seed/{character.name.replace(' ', '')}{hash_value}/400/500.jpg"
            
            # Mettre à jour l'image du personnage
            character.image_url = image_url
            character.save()
            updated_chars += 1
        
        self.stdout.write(f'-> {updated_chars} personnages mis à jour avec de nouvelles images')
        
        # Mettre à jour les images des histoires
        stories = MythStory.objects.all()
        updated_stories = 0
        
        for story in stories:
            # Générer une URL unique pour chaque histoire
            hash_value = abs(hash(story.title)) % 1000
            image_url = f"https://picsum.photos/seed/{story.title.replace(' ', '')}{hash_value}/800/400.jpg"
            
            # Mettre à jour l'image de l'histoire
            story.image_url = image_url
            story.save()
            updated_stories += 1
        
        self.stdout.write(f'-> {updated_stories} histoires mises à jour avec de nouvelles images')
        
        self.stdout.write(self.style.SUCCESS('Génération d\'images terminée avec succès !'))