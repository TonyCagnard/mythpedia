# mythpedia/management/commands/seed_stories.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from mythpedia.models import MythStory, Mythology, Character
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample mythological stories'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting stories seeding...'))

        # Récupérer toutes les mythologies et personnages existants
        mythologies = list(Mythology.objects.all())
        characters = list(Character.objects.all())
        
        if not mythologies:
            self.stdout.write(self.style.ERROR('No mythologies found. Please run seed_mythologies first.'))
            return
            
        if not characters:
            self.stdout.write(self.style.WARNING('No characters found. Stories will be created without characters.'))

        # Données d'exemple pour les histoires
        STORIES_DATA = [
            {
                'title': "La Création du Monde selon les Chinois",
                'summary': "Le mythe de Pangu séparant le ciel et la terre",
                'full_text': "Au commencement, il n'y avait que le chaos sous forme d'un œuf cosmique. Pangu, un géant né de cet œuf, dorma pendant dix-huit mille ans. En se réveillant, il se sentit à l'étroit et décida de briser sa prison. D'un coup de hache puissante, il fendit l'œuf en deux : la partie supérieure devint le ciel et la partie inférieure devint la terre. Pour séparer définitivement les deux éléments, Pangu se tint entre eux, les poussant sans cesse. Pendant des milliers d'années, il maintint cette position jusqu'à ce que le ciel et la terre soient à leur distance actuelle. Épuisé par cet effort, Pangu s'effondra et son corps se transformera en éléments de notre monde : son souffle devint le vent, sa voix le tonnerre, ses yeux le soleil et la lune, et son sang les rivières et les océans.",
                'themes': "Création, Cosmogonie, Origine du monde",
                'mythology_slug': 'chinese',
                'character_slugs': ['pangu', 'nuwa']
            },
            {
                'title': "Le Ragnarök",
                'summary': "La fin prophétisée du monde dans la mythologie nordique",
                'full_text': "Le Ragnarök, ou 'destinée des dieux', est la bataille prophétisée qui mettra fin au monde actuel. Selon les mythes, cette apocalypse sera précédée de trois hivers successifs, connus sous le nom de 'Fimbulvetr'. Pendant cette période de troubles, les liens familiaux se briseront et la morale s'effondrera. Le loup Fenrir, enchaîné par les dieux, se libérera et parcourra le monde, dévorant le soleil et la lune. Les monstres du chaos, menés par Loki et sa fille Hel, envahiront les neuf mondes. Sur le champ de Vígríðr, les dieux Ases affronteront les dieux Vanir, menés par Loki et ses enfants. Thor affrontera le serpent Jörmungandr et ils s'entretueront mutuellement. Odin sera dévoré par Fenrir, Thor par le serpent Jörmungandr, et Freyr par le géant de feu Surtr. Finalement, Surtr consumera le monde de flammes, ne laissant que quelques terres stériles d'où une nouvelle humanité émergera, menée par les seuls survivants : Líf et Lífþrasir.",
                'themes': "Apocalypse, Prophétie, Fin du monde, Bataille",
                'mythology_slug': 'nordic',
                'character_slugs': ['odin', 'thor', 'loki', 'freyr']
            },
            {
                'title': "Le Jugement d'Osiris",
                'summary': "Le mythe de la résurrection et de la justice dans l'au-delà",
                'full_text': "Osiris, bienveillant roi d'Égypte, fut assassiné par son frère jaloux Seth qui le démemvra et dispersa les morceaux à travers le pays. Isis, épouse dévouée d'Osiris, parcourut le pays pour retrouver les fragments de son mari. Avec l'aide d'Anubis, elle réussit à reconstituer le corps d'Osiris, à l'exception de son phallus, avalé par un poisson. Par sa magie puissante, elle le ramena à la vie, devenant ainsi la première momie et inaugurant la pratique de l'embaumement. Osiris, désormais incapable de régner sur le monde des vivants, devint le juge des âmes dans l'au-delà, où les cœurs étaient pesés contre la plume de Maât (la vérité et la justice). Ce mythe explique l'importance de la justice, de la vérité et de l'équilibre dans la culture égyptienne, ainsi que l'origine des rituels funéraires complexes qui caractérisent cette civilisation.",
                'themes': "Mort, Résurrection, Justice, Au-delà, Magie",
                'mythology_slug': 'egyptian',
                'character_slugs': ['osiris', 'isis', 'anubis', 'seth']
            },
            {
                'title': "La Guerre de Troie",
                'summary': "Le conflit légendaire qui mena à la chute de la grande cité",
                'full_text': "La guerre de Troie, l'un des plus grands conflits de l'Antiquité, débuta par une dispute entre déesses. Éris, déesse de la discorde, jeta une pomme d'or marquée 'Pour la plus belle' lors du mariage de Pélée et Thétis. Hera, Athéna et Aphrodite se disputèrent la pomme, et Zeus ordonna à Paris de la trancher. Paris choisit Aphrodite, qui lui promit l'amour d'Hélène, la plus belle mortelle. Mais Hélène était déjà mariée à Ménélas, roi de Sparte. Paris l'enleva, emmenant Hélène à Troie. Les Grecs, liés par serment, unirent leurs forces pour récupérer Hélène. La guerre dura dix ans, marquée par des exploits légendaires : la ruse d'Ulysse avec le cheval de Troie, la force d'Achille, la courage d'Hector, et la sagesse de Nestor. Finalement, grâce à la ruse d'Ulysse, les Grecs pénétrèrent dans Troie et la incendièrent, mettant fin à la guerre et à une époque glorieuse de l'histoire grecque.",
                'themes': "Guerre, Amour, Trahison, Héros, Destin",
                'mythology_slug': 'greek',
                'character_slugs': ['hercules', 'achille', 'hector', 'odysseus', 'paris']
            },
            {
                'title': "Le Voyage d'Inari au Pays des Morts",
                'summary': "Un voyage spirituel dans les royaumes souterrains japonais",
                'full_text': "Inari, kami des riz, des renards et de la prospérité, entreprit un jour dans les royaumes souterrains (Yomi) pour sauver son épouse et les âmes perdues. Accompagné de ses messagers renards (kitsune), Inari traversa les huit couches de l'enfer, faisant face à des démons et esprits malveillants. À chaque couche, il dut résoudre une épreuve ou un puzzle, utilisant sa sagesse et sa ruse pour surmonter les obstacles. Dans la couche la plus profonde, il trouva les âmes des innocents retenues prisonnières par des démons. Avec l'aide de ses renards, qui pouvaient se transformer et créer des illusions, Inari distrait les gardiens et libéra les âmes. Ce voyage symbolise le courage de faire face à l'adversité pour le bien des autres, et représente l'importance du riz comme nourriture spirituelle et physique dans la culture japonaise.",
                'themes': "Voyage, Au-delà, Courage, Sauvetage, Spiritualité",
                'mythology_slug': 'japanese',
                'character_slugs': ['inari', 'izanagi', 'izanami']
            }
        ]

        # Créer les histoires
        created_count = 0
        for story_data in STORIES_DATA:
            # Trouver la mythologie correspondante
            mythology = None
            for myth in mythologies:
                if myth.slug == story_data['mythology_slug']:
                    mythology = myth
                    break
            
            if not mythology:
                self.stdout.write(self.style.WARNING(f"Mythology with slug '{story_data['mythology_slug']}' not found. Skipping story '{story_data['title']}'"))
                continue
            
            # Créer l'histoire
            story = MythStory.objects.create(
                mythology=mythology,
                title=story_data['title'],
                slug=slugify(story_data['title']),
                summary=story_data['summary'],
                full_text=story_data['full_text'],
                themes=story_data['themes'],
                image_url=f"https://picsum.photos/seed/{story_data['title'].replace(' ', '')}/800/400.jpg"
            )
            
            # Ajouter les personnages associés
            for char_slug in story_data.get('character_slugs', []):
                for character in characters:
                    if character.slug == char_slug and character.mythology == mythology:
                        story.characters.add(character)
                        break
            
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created Story: {story.title} for {mythology.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'Stories seeding complete! Created {created_count} stories.'))