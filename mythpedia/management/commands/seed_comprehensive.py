from django.core.management.base import BaseCommand
from django.utils.text import slugify
from mythpedia.models import Mythology, Character, MythStory
import random

class Command(BaseCommand):
    help = 'Peuple la base de données avec un contenu mythologique complet et diversifié'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Début du peuplement complet de la base de données...'))
        
        # Supprimer les données existantes
        MythStory.objects.all().delete()
        Character.objects.all().delete()
        Mythology.objects.all().delete()
        
        # Données complètes des mythologies
        mythologies_data = [
            {
                'title': 'Mythologie Grecque',
                'icon_class': 'fa-landmark',
                'color_from': 'from-blue-500',
                'color_to': 'to-cyan-400',
                'description': 'La mythologie grecque est l\'ensemble des mythes et des légendes appartenant à la religion des anciens Grecs. Ces mythes racontent l\'histoire des dieux, des héros, et de l\'univers, expliquant l\'origine du monde et les traditions religieuses.',
                'card_summary': 'Dieux de l\'Olympe, héros légendaires et créatures mythiques',
                'characters': [
                    {'name': 'Zeus', 'role': 'Roi des dieux', 'description': 'Maître du ciel et de la foudre, Zeus règne sur l\'Olympe et supervise les affaires des dieux et des mortels.', 'image': 'https://i.imgur.com/8X2y0Jl.jpg'},
                    {'name': 'Héra', 'role': 'Reine des dieux', 'description': 'Déesse du mariage et de la famille, sœur et épouse de Zeus.', 'image': 'https://i.imgur.com/9Y3nK7m.jpg'},
                    {'name': 'Poséidon', 'role': 'Dieu de la mer', 'description': 'Maître des océans et des tremblements de terre, frère de Zeus.', 'image': 'https://i.imgur.com/7Lm4pQ2.jpg'},
                    {'name': 'Athéna', 'role': 'Déesse de la sagesse', 'description': 'Déesse de la stratégie guerrière, de la sagesse et des arts.', 'image': 'https://i.imgur.com/5R9oT3L.jpg'},
                    {'name': 'Apollon', 'role': 'Dieu du soleil', 'description': 'Dieu de la musique, de la poésie, de la prophétie et de la lumière.', 'image': 'https://i.imgur.com/3Nq8V7X.jpg'},
                    {'name': 'Artémis', 'role': 'Déesse de la chasse', 'description': 'Déesse de la nature sauvage, de la chasse et de la lune.', 'image': 'https://i.imgur.com/6Pm4W9Y.jpg'},
                    {'name': 'Arès', 'role': 'Dieu de la guerre', 'description': 'Dieu de la violence et de la guerre brute.', 'image': 'https://i.imgur.com/2Kj7F5G.jpg'},
                    {'name': 'Aphrodite', 'role': 'Déesse de l\'amour', 'description': 'Déesse de la beauté, de l\'amour et du désir.', 'image': 'https://i.imgur.com/4Hm6R8Z.jpg'},
                    {'name': 'Héphaïstos', 'role': 'Dieu du feu', 'description': 'Dieu de la forge, du feu et de la métallurgie.', 'image': 'https://i.imgur.com/8Nq5T3U.jpg'},
                    {'name': 'Déméter', 'role': 'Déesse de l\'agriculture', 'description': 'Déesse des récoltes, de l\'agriculture et de la fertilité.', 'image': 'https://i.imgur.com/1Lm9X7V.jpg'},
                    {'name': 'Hermès', 'role': 'Messager des dieux', 'description': 'Messager des dieux, protecteur des voyageurs et des voleurs.', 'image': 'https://i.imgur.com/7Rn4Y2W.jpg'},
                    {'name': 'Hadès', 'role': 'Dieu des enfers', 'description': 'Roi du monde souterrain et des morts.', 'image': 'https://i.imgur.com/3Kp8T1Q.jpg'},
                    {'name': 'Héraclès', 'role': 'Héros demi-dieu', 'description': 'Fils de Zeus, célèbre pour ses douze travaux.', 'image': 'https://i.imgur.com/5Mj7R2X.jpg'},
                    {'name': 'Achille', 'role': 'Guerrier légendaire', 'description': 'Héros de la guerre de Troie, invulnérable sauf au talon.', 'image': 'https://i.imgur.com/9Lm3X6Y.jpg'},
                    {'name': 'Ulysse', 'role': 'Roi d\'Ithaque', 'description': 'Héros de l\'Odyssée, connu pour son intelligence et sa ruse.', 'image': 'https://i.imgur.com/2Nk8V4Z.jpg'},
                ],
                'stories': [
                    {'title': 'La Guerre de Troie', 'summary': 'Le conflit légendaire entre Grecs et Troyens', 'full_text': 'La guerre de Troie est un conflit mythique qui a opposé les Achéens aux Troyens. Elle a été déclenchée par l\'enlèvement d\'Hélène, épouse du roi Ménélas, par Pâris, prince de Troie. La guerre a duré dix ans et s\'est terminée par la chute de Troie grâce à la ruse du cheval de Troie.', 'themes': 'Guerre, Amour, Trahison, Héroïsme', 'image': 'https://i.imgur.com/8Lm3X7K.jpg'},
                    {'title': 'Les Douze Travaux d\'Héraclès', 'summary': 'Les exploits légendaires du plus grand des héros grecs', 'full_text': 'Pour expier un crime terrible, Héraclès doit accomplir douze travaux impossibles : tuer le lion de Némée, décapiter l\'hydre de Lerne, capturer la biche de Cérynie, etc. Chaque travail teste sa force, son courage et son ingéniosité.', 'themes': 'Rédemption, Courage, Force, Épreuves', 'image': 'https://i.imgur.com/3Km9X5L.jpg'},
                    {'title': 'Le Mythe de Prométhée', 'summary': 'Le Titan qui a volé le feu pour l\'humanité', 'full_text': 'Prométhée, Titan ami des humains, a volé le feu sacré de l\'Olympe pour le donner aux mortels. Pour punir cette audace, Zeus l\'a enchaîné à un rocher où un aigle dévorait chaque jour son foie, qui repoussait la nuit.', 'themes': 'Sacrifice, Connaissance, Rébellion, Punition', 'image': 'https://i.imgur.com/7Ln4Y3M.jpg'},
                ]
            },
            {
                'title': 'Mythologie Nordique',
                'icon_class': 'fa-hammer',
                'color_from': 'from-gray-700',
                'color_to': 'to-blue-400',
                'description': 'La mythologie nordique est l\'ensemble des mythes des peuples germaniques du Nord de l\'Europe. Elle met en scène des dieux guerriers, des géants, des nains et des monstres, dans un univers marqué par la fatalité et la préparation du Ragnarök.',
                'card_summary': 'Dieux guerriers, géants et la fin du monde prophétique',
                'characters': [
                    {'name': 'Odin', 'role': 'Père des dieux', 'description': 'Dieu de la sagesse, de la guerre et de la mort, il a sacrifié un œil pour boire à la source de la connaissance.', 'image': 'https://i.imgur.com/9Ml3X8N.jpg'},
                    {'name': 'Thor', 'role': 'Dieu du tonnerre', 'description': 'Fils d\'Odin, dieu de la force et du tonnerre, il possède le marteau Mjöllnir.', 'image': 'https://i.imgur.com/4Kn7Y2P.jpg'},
                    {'name': 'Loki', 'role': 'Dieu de la tromperie', 'description': 'Dieu du feu et de la malice, maître des transformations et des ruses.', 'image': 'https://i.imgur.com/8Lm4X9Q.jpg'},
                    {'name': 'Freyja', 'role': 'Déesse de l\'amour', 'description': 'Déesse de l\'amour, de la beauté et de la fertilité.', 'image': 'https://i.imgur.com/3Nn5V6R.jpg'},
                    {'name': 'Baldr', 'role': 'Dieu de la lumière', 'description': 'Fils d\'Odin, dieu de la beauté et de la pureté.', 'image': 'https://i.imgur.com/7Ml6Y3S.jpg'},
                    {'name': 'Tyr', 'role': 'Dieu de la justice', 'description': 'Dieu de la guerre et de la justice, il a sacrifié sa main pour enchaîner Fenrir.', 'image': 'https://i.imgur.com/2Kk4V5T.jpg'},
                    {'name': 'Freyr', 'role': 'Dieu de la fertilité', 'description': 'Dieu de la prospérité, de la paix et des récoltes.', 'image': 'https://i.imgur.com/9Ll7X4U.jpg'},
                    {'name': 'Heimdall', 'role': 'Gardien des dieux', 'description': 'Gardien du pont Bifröst, il peut entendre l\'herbe pousser.', 'image': 'https://i.imgur.com/5Mm8Y6V.jpg'},
                    {'name': 'Fenrir', 'role': 'Loup géant', 'description': 'Fils de Loki, loup monstrueux destiné à tuer Odin lors du Ragnarök.', 'image': 'https://i.imgur.com/6Nn9Y7W.jpg'},
                    {'name': 'Jörmungand', 'role': 'Serpent mondial', 'description': 'Serpent de mer géant qui entoure le monde.', 'image': 'https://i.imgur.com/3Ll5X8X.jpg'},
                ],
                'stories': [
                    {'title': 'Le Ragnarök', 'summary': 'La fin du monde dans la mythologie nordique', 'full_text': 'Le Ragnarök est la bataille prophétique qui marque la fin du monde. Les dieux affronteront les géants et les monstres. Odin sera tué par Fenrir, Thor par Jörmungand, et le monde sera détruit par le feu avant de renaître.', 'themes': 'Apocalypse, Destin, Destruction, Renaissance', 'image': 'https://i.imgur.com/8Mm9Y7Z.jpg'},
                    {'title': 'L\'Enlèvement d\'Idunn', 'summary': 'Le vol des pommes d\'or de la jeunesse', 'full_text': 'Le géant Thjazi a enlevé Idunn, gardienne des pommes d\'or qui maintiennent les dieux jeunes. Loki a dû la sauver pour empêcher les dieux de vieillir et mourir.', 'themes': 'Tromperie, Sauvetage, Immortalité, Ruse', 'image': 'https://i.imgur.com/4Nn8Y6A.jpg'},
                    {'title': 'La Mort de Baldr', 'summary': 'Le début de la fin pour les dieux nordiques', 'full_text': 'Baldr, le plus aimé des dieux, a été tué par une fléchette de gui, son unique faiblesse. Sa mort est le premier signe du Ragnarök approchant.', 'themes': 'Tragédie, Fatalité, Mort, Prémonition', 'image': 'https://i.imgur.com/7Ll7X5B.jpg'},
                ]
            },
            {
                'title': 'Mythologie Égyptienne',
                'icon_class': 'fa-ankh',
                'color_from': 'from-yellow-500',
                'color_to': 'to-orange-400',
                'description': 'La mythologie égyptienne est l\'ensemble des croyances religieuses de l\'Égypte antique. Elle met en scène des dieux hybrides, des pharaons divinisés et des rituels complexes liés à la mort et à la résurrection.',
                'card_summary': 'Dieux à tête d\'animal, pharaons divins et voyage dans l\'au-delà',
                'characters': [
                    {'name': 'Râ', 'role': 'Dieu du soleil', 'description': 'Dieu créateur, maître du soleil qui traverse le ciel chaque jour.', 'image': 'https://i.imgur.com/9Mm8X8C.jpg'},
                    {'name': 'Osiris', 'role': 'Dieu des morts', 'description': 'Seigneur de l\'au-delà, juge des âmes.', 'image': 'https://i.imgur.com/4Nn9Y7D.jpg'},
                    {'name': 'Isis', 'role': 'Déesse mère', 'description': 'Déesse de la magie, de la maternité et de la résurrection.', 'image': 'https://i.imgur.com/8Ll9X6E.jpg'},
                    {'name': 'Horus', 'role': 'Dieu du ciel', 'description': 'Fils d\'Isis et Osiris, dieu faucon protecteur des pharaons.', 'image': 'https://i.imgur.com/3Mm7Y5F.jpg'},
                    {'name': 'Anubis', 'role': 'Dieu des momies', 'description': 'Dieu à tête de chacal, gardien des tombes.', 'image': 'https://i.imgur.com/7Nn8X6G.jpg'},
                    {'name': 'Thot', 'role': 'Dieu de la sagesse', 'description': 'Dieu ibis de l\'écriture, de la connaissance et du temps.', 'image': 'https://i.imgur.com/2Ll6Y4H.jpg'},
                    {'name': 'Seth', 'role': 'Dieu du chaos', 'description': 'Dieu du désert, des orages et de la violence.', 'image': 'https://i.imgur.com/9Kl7X5I.jpg'},
                    {'name': 'Bastet', 'role': 'Déesse chatte', 'description': 'Déesse protectrice, maîtresse de la joie et de la danse.', 'image': 'https://i.imgur.com/5Ll8Y7J.jpg'},
                    {'name': 'Ptah', 'role': 'Dieu créateur', 'description': 'Dieu de Memphis, créateur du monde par la pensée et la parole.', 'image': 'https://i.imgur.com/6Mm9X8K.jpg'},
                    {'name': 'Sekhmet', 'role': 'Déesse guerrière', 'description': 'Déesse lionne, destructrice et guérisseuse.', 'image': 'https://i.imgur.com/3Nn7Y6L.jpg'},
                ],
                'stories': [
                    {'title': 'Le Mythe d\'Osiris et Isis', 'summary': 'L\'histoire d\'amour, de trahison et de résurrection', 'full_text': 'Osiris, roi bienfaiteur, est tué et démembré par son frère Seth. Isis, son épouse, retrouve tous les morceaux de son corps sauf un, le ressuscite et conçoit Horus qui vengera son père.', 'themes': 'Amour, Mort, Résurrection, Vengeance', 'image': 'https://i.imgur.com/8Ll8X9M.jpg'},
                    {'title': 'Le Voyage du Soleil', 'summary': 'Le parcours nocturne de Râ dans l\'au-delà', 'full_text': 'Chaque nuit, Râ traverse le monde souterrain dans sa barque solaire, affrontant les forces du chaos avant de renaître à l\'aube.', 'themes': 'Cycle, Éternité, Combat, Renaissance', 'image': 'https://i.imgur.com/4Mm9Y7N.jpg'},
                    {'title': 'Le Jugement de l\'Âme', 'summary': 'La pesée du cœur dans la salle des deux vérités', 'full_text': 'Les morts doivent passer le jugement : leur cœur est pesé contre la plume de Maât. Seuls les cœurs légers peuvent accéder à l\'au-delà.', 'themes': 'Justice, Mort, Morale, Éternité', 'image': 'https://i.imgur.com/7Nn9X8O.jpg'},
                ]
            },
            {
                'title': 'Mythologie Romaine',
                'icon_class': 'fa-shield-alt',
                'color_from': 'from-red-600',
                'color_to': 'to-purple-500',
                'description': 'La mythologie romaine s\'est développée à partir de la mythologie grecque mais avec des caractéristiques propres. Elle met en scène des dieux et des héros qui reflètent les valeurs romaines : la discipline, le courage et la piété.',
                'card_summary': 'Dieux guerriers, empereurs divinisés et fondation de Rome',
                'characters': [
                    {'name': 'Jupiter', 'role': 'Roi des dieux', 'description': 'Équivalent romain de Zeus, dieu du ciel et de la foudre.', 'image': 'https://i.imgur.com/9Mm9X9P.jpg'},
                    {'name': 'Junon', 'role': 'Reine des dieux', 'description': 'Équivalente d\'Héra, protectrice des femmes et du mariage.', 'image': 'https://i.imgur.com/4Nn8Y8Q.jpg'},
                    {'name': 'Mars', 'role': 'Dieu de la guerre', 'description': 'Père fondateur de Rome, dieu protecteur de l\'armée.', 'image': 'https://i.imgur.com/8Ll9X7R.jpg'},
                    {'name': 'Vénus', 'role': 'Déesse de l\'amour', 'description': 'Équivalente d\'Aphrodite, mère d\'Énée.', 'image': 'https://i.imgur.com/3Mm8Y6S.jpg'},
                    {'name': 'Minerve', 'role': 'Déesse de la sagesse', 'description': 'Équivalente d\'Athéna, protectrice des artisans.', 'image': 'https://i.imgur.com/7Nn7Y5T.jpg'},
                    {'name': 'Diane', 'role': 'Déesse de la chasse', 'description': 'Équivalente d\'Artémis, protectrice de la nature.', 'image': 'https://i.imgur.com/2Ll6Y4U.jpg'},
                    {'name': 'Vulcain', 'role': 'Dieu du feu', 'description': 'Équivalent d\'Héphaïstos, forgeron des dieux.', 'image': 'https://i.imgur.com/9Kl8X7V.jpg'},
                    {'name': 'Mercure', 'role': 'Messager des dieux', 'description': 'Équivalent d\'Hermès, protecteur des commerçants.', 'image': 'https://i.imgur.com/5Ll9Y8W.jpg'},
                    {'name': 'Pluton', 'role': 'Dieu des enfers', 'description': 'Équivalent d\'Hadès, roi du monde souterrain.', 'image': 'https://i.imgur.com/6Mm7X9X.jpg'},
                    {'name': 'Cérès', 'role': 'Déesse de l\'agriculture', 'description': 'Équivalente de Déméter, protectrice des récoltes.', 'image': 'https://i.imgur.com/3Nn8Y7Y.jpg'},
                    {'name': 'Romulus', 'role': 'Fondateur de Rome', 'description': 'Fils de Mars, premier roi de Rome.', 'image': 'https://i.imgur.com/7Ll9X6Z.jpg'},
                    {'name': 'Énée', 'role': 'Héros troyen', 'description': 'Fils de Vénus, ancêtre des Romains.', 'image': 'https://i.imgur.com/2Mm7Y5A.jpg'},
                ],
                'stories': [
                    {'title': 'La Fondation de Rome', 'summary': 'Romulus et Rémus, les jumeaux divins', 'full_text': 'Romulus et Rémus, fils du dieu Mars et de la vestale Rhéa Silvia, sont abandonnés et allaités par une louve. Adultes, ils fondent Rome mais Romulus tue Rémus lors d\'une dispute.', 'themes': 'Fondation, Fratricide, Destin, Divinité', 'image': 'https://i.imgur.com/8Ll8X7B.jpg'},
                    {'title': 'L\'Enlèvement des Sabines', 'summary': 'Le début de la population de Rome', 'full_text': 'Pour peupler sa nouvelle ville, Romulus organise des jeux et invite les peuples voisins. Ses hommes enlèvent les jeunes femmes sabines qui deviendront les mères des premiers Romains.', 'themes': 'Violence, Union, Fondation, Paix', 'image': 'https://i.imgur.com/4Mm9Y8C.jpg'},
                    {'title': 'L\'Énéide', 'summary': 'Le voyage d\'Énée vers l\'Italie', 'full_text': 'Après la chute de Troie, Énée fuit avec son père et son fils. Après un long périple rempli d\'épreuves, il atteint l\'Italie où ses descendants fonderont Rome.', 'themes': 'Exil, Destin, Courage, Fondation', 'image': 'https://i.imgur.com/9Nn9X9D.jpg'},
                ]
            },
            {
                'title': 'Mythologie Japonaise',
                'icon_class': 'fa-torii-gate',
                'color_from': 'from-pink-500',
                'color_to': 'to-red-400',
                'description': 'La mythologie japonaise est un ensemble complexe de traditions et de croyances qui mêlent divinités, esprits et créatures légendaires. Elle explique la création du Japon et l\'origine de la famille impériale.',
                'card_summary': 'Kamis, esprits naturels et créatures surnaturelles',
                'characters': [
                    {'name': 'Amaterasu', 'role': 'Déesse du soleil', 'description': 'Déesse principale, ancêtre de la famille impériale.', 'image': 'https://i.imgur.com/9Mm9X9E.jpg'},
                    {'name': 'Susanoo', 'role': 'Dieu de la mer', 'description': 'Dieu des tempêtes et des océans, frère d\'Amaterasu.', 'image': 'https://i.imgur.com/4Nn8Y8F.jpg'},
                    {'name': 'Tsukuyomi', 'role': 'Dieu de la lune', 'description': 'Dieu de la nuit et des cycles lunaires.', 'image': 'https://i.imgur.com/8Ll9X7G.jpg'},
                    {'name': 'Izanagi', 'role': 'Créateur', 'description': 'Dieu créateur, père des kamis principaux.', 'image': 'https://i.imgur.com/3Mm8Y6H.jpg'},
                    {'name': 'Izanami', 'role': 'Créatrice', 'description': 'Déesse créatrice, mère des kamis principaux.', 'image': 'https://i.imgur.com/7Nn7Y5I.jpg'},
                    {'name': 'Raijin', 'role': 'Dieu du tonnerre', 'description': 'Dieu démoniaque de la foudre et des orages.', 'image': 'https://i.imgur.com/2Ll6Y4J.jpg'},
                    {'name': 'Fujin', 'role': 'Dieu du vent', 'description': 'Dieu démoniaque qui contrôle les vents.', 'image': 'https://i.imgur.com/9Kl8X7K.jpg'},
                    {'name': 'Hachiman', 'role': 'Dieu de la guerre', 'description': 'Protecteur du Japon et des guerriers.', 'image': 'https://i.imgur.com/5Ll9Y8L.jpg'},
                    {'name': 'Inari', 'role': 'Déesse du riz', 'description': 'Déesse de la prospérité et des récoltes.', 'image': 'https://i.imgur.com/6Mm7X9M.jpg'},
                    {'name': 'Benzaiten', 'role': 'Déesse de la musique', 'description': 'Déesse de la musique, de l\'art et de la connaissance.', 'image': 'https://i.imgur.com/3Nn8Y7N.jpg'},
                ],
                'stories': [
                    {'title': 'La Création du Japon', 'summary': 'Izanagi et Izanami forment les îles', 'full_text': 'Les dieux créateurs Izanagi et Izanami agitent leur lance dans l\'océan primordial. Les gouttes qui tombent forment les premières îles du Japon.', 'themes': 'Création, Amour, Naissance, Sacré', 'image': 'https://i.imgur.com/8Ll8X8O.jpg'},
                    {'title': 'Amaterasu dans la Grotte', 'summary': 'Le monde sans soleil', 'full_text': 'Fâchée contre son frère Susanoo, Amaterasu se cache dans une grotte, plongeant le monde dans l\'obscurité. Les autres dieux doivent la faire sortir avec des ruses.', 'themes': 'Conflit, Obscurité, Ruse, Renaissance', 'image': 'https://i.imgur.com/4Mm9Y9P.jpg'},
                    {'title': 'Le Combat de Susanoo', 'summary': 'Le dieu affronte le dragon Yamata', 'full_text': 'Susanoo combat le dragon à huit têtes Yamata no Orochi, le tue et trouve dans son corps l\'épée sacrée Kusanagi, un des trésors impériaux.', 'themes': 'Combat, Courage, Monstres, Trésors', 'image': 'https://i.imgur.com/9Nn9X9Q.jpg'},
                ]
            },
            {
                'title': 'Mythologie Hindoue',
                'icon_class': 'fa-om',
                'color_from': 'from-orange-500',
                'color_to': 'to-red-600',
                'description': 'La mythologie hindoue est l\'une des plus riches et complexes au monde. Elle met en scène des milliers de divinités, des cycles cosmiques et des philosophies profondes qui expliquent la création, la préservation et la destruction de l\'univers.',
                'card_summary': 'Dieux multiples, cycles cosmiques et philosophie profonde',
                'characters': [
                    {'name': 'Brahma', 'role': 'Créateur', 'description': 'Dieu créateur de l\'univers, à quatre têtes.', 'image': 'https://i.imgur.com/9Mm9X9R.jpg'},
                    {'name': 'Vishnou', 'role': 'Préserveur', 'description': 'Dieu qui préserve l\'univers, a dix avatars.', 'image': 'https://i.imgur.com/4Nn8Y8S.jpg'},
                    {'name': 'Shiva', 'role': 'Destructeur', 'description': 'Dieu qui détruit pour régénérer, maître du yoga.', 'image': 'https://i.imgur.com/8Ll9X7T.jpg'},
                    {'name': 'Lakshmi', 'role': 'Déesse de la richesse', 'description': 'Épouse de Vishnou, déesse de la prospérité.', 'image': 'https://i.imgur.com/3Mm8Y6U.jpg'},
                    {'name': 'Parvati', 'role': 'Déesse mère', 'description': 'Épouse de Shiva, mère de Ganesh.', 'image': 'https://i.imgur.com/7Nn7Y5V.jpg'},
                    {'name': 'Ganesh', 'role': 'Dieu à tête d\'éléphant', 'description': 'Fils de Shiva, dieu qui élimine les obstacles.', 'image': 'https://i.imgur.com/2Ll6Y4W.jpg'},
                    {'name': 'Krishna', 'role': 'Avatar de Vishnou', 'description': 'Héros divin, conseiller dans la Bhagavad Gita.', 'image': 'https://i.imgur.com/9Kl8X7X.jpg'},
                    {'name': 'Rama', 'role': 'Avatar de Vishnou', 'description': 'Héros du Ramayana, modèle de vertu.', 'image': 'https://i.imgur.com/5Ll9Y8Y.jpg'},
                    {'name': 'Durga', 'role': 'Déesse guerrière', 'description': 'Aspect guerrier de Parvati, combat les démons.', 'image': 'https://i.imgur.com/6Mm7X9Z.jpg'},
                    {'name': 'Kali', 'role': 'Déesse de la destruction', 'description': 'Aspect destructeur de Parvati, déesse du temps.', 'image': 'https://i.imgur.com/3Nn8Y7A.jpg'},
                    {'name': 'Hanuman', 'role': 'Dieu-singe', 'description': 'Dévot de Rama, dieu de la force et du dévouement.', 'image': 'https://i.imgur.com/7Nn7Y6B.jpg'},
                    {'name': 'Saraswati', 'role': 'Déesse du savoir', 'description': 'Déesse de la connaissance, de la musique et des arts.', 'image': 'https://i.imgur.com/2Ll6Y5C.jpg'},
                ],
                'stories': [
                    {'title': 'Le Ramayana', 'summary': 'L\'épopée de Rama et Sita', 'full_text': 'Rama, prince vertueux, est exilé avec sa femme Sita. Lorsque le démon Ravana enlève Sita, Rama avec l\'aide de Hanuman et de son frère Lakshmana livre une guerre épique pour la délivrer.', 'themes': 'Amour, Devoir, Combat, Vertu', 'image': 'https://i.imgur.com/8Ll8X8D.jpg'},
                    {'title': 'Le Mahabharata', 'summary': 'La guerre des cousins Pandavas et Kauravas', 'full_text': 'Le plus long poème jamais composé, racontant la guerre entre les cousins Pandavas et Kauravas pour le contrôle du trône. La Bhagavad Gita en fait partie.', 'themes': 'Guerre, Devoir, Philosophie, Destin', 'image': 'https://i.imgur.com/4Mm9Y9E.jpg'},
                    {'title': 'Le Danse Cosmique de Shiva', 'summary': 'La création et la destruction universelles', 'full_text': 'Shiva danse la Tandava, sa danse cosmique qui crée, préserve et détruit l\'univers dans un cycle éternel.', 'themes': 'Cycle, Destruction, Création, Éternité', 'image': 'https://i.imgur.com/9Nn9X9F.jpg'},
                ]
            },
            {
                'title': 'Mythologie Chinoise',
                'icon_class': 'fa-yin-yang',
                'color_from': 'from-red-600',
                'color_to': 'to-yellow-500',
                'description': 'La mythologie chinoise est un ensemble de légendes et de mythes transmis depuis des millénaires. Elle mélange histoire, religion et folklore, avec des dragons, des empereurs divins et des sages légendaires.',
                'card_summary': 'Dragons, empereurs divins et philosophie taoïste',
                'characters': [
                    {'name': 'Yu Di', 'role': 'Empereur de Jade', 'description': 'Souverain des cieux, maître des dieux et des mortels.', 'image': 'https://i.imgur.com/9Mm9X9G.jpg'},
                    {'name': 'Long Wang', 'role': 'Roi Dragon', 'description': 'Maître des mers et des pluies, contrôleur des éléments.', 'image': 'https://i.imgur.com/4Nn8Y8H.jpg'},
                    {'name': 'Nuwa', 'role': 'Déesse créatrice', 'description': 'Déesse qui a créé l\'humanité avec de l\'argile.', 'image': 'https://i.imgur.com/8Ll9X7I.jpg'},
                    {'name': 'Fuxi', 'role': 'Souverain primordial', 'description': 'Premier empereur, inventeur de l\'écriture et de la musique.', 'image': 'https://i.imgur.com/3Mm8Y6J.jpg'},
                    {'name': 'Shennong', 'role': 'Empereur agriculteur', 'description': 'Divinité de l\'agriculture et de la médecine.', 'image': 'https://i.imgur.com/7Nn7Y5K.jpg'},
                    {'name': 'Huang Di', 'role': 'Empereur Jaune', 'description': 'Ancêtre mythique du peuple chinois.', 'image': 'https://i.imgur.com/2Ll6Y4L.jpg'},
                    {'name': 'Chang\'e', 'role': 'Déesse lunaire', 'description': 'Déesse qui vit sur la lune avec un lapin.', 'image': 'https://i.imgur.com/9Kl8X7M.jpg'},
                    {'name': 'Hou Yi', 'role': 'Archer divin', 'description': 'Héros qui a abattu neuf soleils supplémentaires.', 'image': 'https://i.imgur.com/5Ll9Y8N.jpg'},
                    {'name': 'Nezha', 'role': 'Dieu guerrier', 'description': 'Jeune divinité combattante, protecteur des enfants.', 'image': 'https://i.imgur.com/6Mm7X9O.jpg'},
                    {'name': 'Sun Wukong', 'role': 'Roi Singe', 'description': 'Singe immortel doté de pouvoirs magiques extraordinaires.', 'image': 'https://i.imgur.com/3Nn8Y7P.jpg'},
                    {'name': 'Guanyin', 'role': 'Déesse de miséricorde', 'description': 'Bodhisattva de la compassion et de la bonté.', 'image': 'https://i.imgur.com/7Nn7Y6Q.jpg'},
                    {'name': 'Zhu Bajie', 'role': 'Cochon divin', 'description': 'Compagnon de Sun Wukong, demi-homme demi-cochon.', 'image': 'https://i.imgur.com/2Ll6Y5R.jpg'},
                ],
                'stories': [
                    {'title': 'Le Voyage en Occident', 'summary': 'Le périple du moine Tripitaka et ses compagnons', 'full_text': 'Le moine bouddhiste Tripitaka voyage vers l\'Inde avec Sun Wukong le roi singe, Zhu Bajie le cochon et Sha Wujing le sable pour rapporter des écritures sacrées.', 'themes': 'Voyage, Spiritualité, Épreuves, Illumination', 'image': 'https://i.imgur.com/8Ll8X8S.jpg'},
                    {'title': 'La Création du Monde', 'summary': 'Le géant Pangu sépare le ciel et la terre', 'full_text': 'Pangu émerge d\'un œuf cosmique et sépare le ciel et la terre. Après sa mort, son corps devient les éléments du monde : ses yeux le soleil et la lune, son sang les rivières, etc.', 'themes': 'Création, Sacrifice, Cosmos, Transformation', 'image': 'https://i.imgur.com/4Mm9Y9T.jpg'},
                    {'title': 'Le Grand Déluge', 'summary': 'Nuwa répare le ciel', 'full_text': 'Après une bataille catastrophique, le ciel se déchire et des eaux dévastatrices inondent la terre. La déesse Nuwa répare le ciel avec des pierres de cinq couleurs.', 'themes': 'Destruction, Sauvetage, Réparation, Nature', 'image': 'https://i.imgur.com/9Nn9X9U.jpg'},
                ]
            },
            {
                'title': 'Mythologie Celtique',
                'icon_class': 'fa-clover',
                'color_from': 'from-green-600',
                'color_to': 'to-emerald-400',
                'description': 'La mythologie celtique est l\'ensemble des légendes des peuples celtes de l\'Europe occidentale. Elle met en scène des druides, des héros guerriers, des fées et des créatures magiques dans un monde où la nature est sacrée.',
                'card_summary': 'Druides, héros guerriers et créatures magiques',
                'characters': [
                    {'name': 'Lugh', 'role': 'Dieu suprême', 'description': 'Dieu des arts, des sciences et de la guerre.', 'image': 'https://i.imgur.com/9Mm9X9V.jpg'},
                    {'name': 'Dagda', 'role': 'Père des dieux', 'description': 'Dieu puissant, maître du temps et de l\'abondance.', 'image': 'https://i.imgur.com/4Nn8Y8W.jpg'},
                    {'name': 'Morrigan', 'role': 'Déesse de la guerre', 'description': 'Déesse triple de la guerre, de la mort et de la prophétie.', 'image': 'https://i.imgur.com/8Ll9X7X.jpg'},
                    {'name': 'Brigid', 'role': 'Déesse du feu', 'description': 'Déesse du feu, de la poésie et de la forge.', 'image': 'https://i.imgur.com/3Mm8Y6Y.jpg'},
                    {'name': 'Cernunnos', 'role': 'Dieu cornu', 'description': 'Dieu de la nature, des animaux et de la fertilité.', 'image': 'https://i.imgur.com/7Nn7Y5Z.jpg'},
                    {'name': 'Cú Chulainn', 'role': 'Héros guerrier', 'description': 'Plus grand héros d\'Irlande, guerrier surhumain.', 'image': 'https://i.imgur.com/2Ll6Y4A.jpg'},
                    {'name': 'Fionn mac Cumhaill', 'role': 'Chef guerrier', 'description': 'Chef des Fianna, chasseur et magicien.', 'image': 'https://i.imgur.com/9Kl8X7B.jpg'},
                    {'name': 'Mabon', 'role': 'Dieu de la chasse', 'description': 'Dieu de la chasse et de la nature sauvage.', 'image': 'https://i.imgur.com/5Ll9Y8C.jpg'},
                    {'name': 'Arawn', 'role': 'Roi de l\'au-delà', 'description': 'Souverain du monde souterrain gallois.', 'image': 'https://i.imgur.com/6Mm7X9D.jpg'},
                    {'name': 'Rhiannon', 'role': 'Déesse cheval', 'description': 'Déesse galloise des chevaux et de la fertilité.', 'image': 'https://i.imgur.com/3Nn8Y7E.jpg'},
                ],
                'stories': [
                    {'title': 'La Bataille de Mag Tuired', 'summary': 'La guerre entre les Tuatha Dé Danann et les Fomoires', 'full_text': 'Les dieux Tuatha Dé Danann combattent les géants Fomoires pour le contrôle de l\'Irlande. Lugh mène les dieux à la victoire contre le roi Balor.', 'themes': 'Guerre, Destin, Pouvoir, Sacrifice', 'image': 'https://i.imgur.com/8Ll8X8F.jpg'},
                    {'title': 'La Razzia des Vaches de Cooley', 'summary': 'L\'épopée de Cú Chulainn', 'full_text': 'La reine Medb envahit l\'Ulster pour voler le taureau brun de Cooley. Seul Cú Chulainn défend la province pendant que les guerriers sont paralysés par une malédiction.', 'themes': 'Guerre, Courage, Solitude, Honneur', 'image': 'https://i.imgur.com/4Mm9Y9G.jpg'},
                    {'title': 'La Poursuite de Diarmuid et Grainne', 'summary': 'Une histoire d\'amour tragique', 'full_text': 'Grainne, fiancée du vieux Fionn, s\'enfuit avec le jeune Diarmuid. Fionn les poursuit à travers toute l\'Irlande jusqu\'à la mort tragique de Diarmuid.', 'themes': 'Amour, Trahison, Poursuite, Tragédie', 'image': 'https://i.imgur.com/9Nn9X9H.jpg'},
                ]
            },
            {
                'title': 'Mythologie Aztèque',
                'icon_class': 'fa-sun',
                'color_from': 'from-yellow-600',
                'color_to': 'to-red-700',
                'description': 'La mythologie aztèque est un ensemble complexe de croyances qui explique la création du monde à travers cinq âges successifs. Elle met en scène des dieux exigeants qui nécessitent des sacrifices humains pour maintenir l\'équilibre cosmique.',
                'card_summary': 'Dieux du sang, sacrifices humains et calendrier cosmique',
                'characters': [
                    {'name': 'Huitzilopochtli', 'role': 'Dieu de la guerre', 'description': 'Dieu du soleil et de la guerre, protecteur des Aztèques.', 'image': 'https://i.imgur.com/9Mm9X9I.jpg'},
                    {'name': 'Quetzalcoatl', 'role': 'Dieu serpent à plumes', 'description': 'Dieu de la sagesse, du vent et de la création.', 'image': 'https://i.imgur.com/4Nn8Y8J.jpg'},
                    {'name': 'Tezcatlipoca', 'role': 'Dieu du miroir fumant', 'description': 'Dieu de la nuit, de la magie et du destin.', 'image': 'https://i.imgur.com/8Ll9X7K.jpg'},
                    {'name': 'Tlaloc', 'role': 'Dieu de la pluie', 'description': 'Dieu de l\'eau, des orages et de la fertilité.', 'image': 'https://i.imgur.com/3Mm8Y6L.jpg'},
                    {'name': 'Xipe Totec', 'role': 'Dieu écorché', 'description': 'Dieu du renouveau, de l\'agriculture et du printemps.', 'image': 'https://i.imgur.com/7Nn7Y5M.jpg'},
                    {'name': 'Coatlicue', 'role': 'Déesse mère', 'description': 'Mère des dieux, déesse de la terre et de la mort.', 'image': 'https://i.imgur.com/2Ll6Y4N.jpg'},
                    {'name': 'Coyolxauhqui', 'role': 'Déesse lunaire', 'description': 'Déesse de la lune, tuée par son frère Huitzilopochtli.', 'image': 'https://i.imgur.com/9Kl8X7O.jpg'},
                    {'name': 'Mictlantecuhtli', 'role': 'Dieu des morts', 'description': 'Seigneur de Mictlan, le monde souterrain.', 'image': 'https://i.imgur.com/5Ll9Y8P.jpg'},
                    {'name': 'Xochiquetzal', 'role': 'Déesse des fleurs', 'description': 'Déesse de l\'amour, de la beauté et des fleurs.', 'image': 'https://i.imgur.com/6Mm7X9Q.jpg'},
                    {'name': 'Tonatiuh', 'role': 'Dieu soleil', 'description': 'Cinquième soleil, nécessite des sacrifices humains.', 'image': 'https://i.imgur.com/3Nn8Y7R.jpg'},
                ],
                'stories': [
                    {'title': 'La Création du Cinquième Soleil', 'summary': 'Le sacrifice des dieux pour créer le monde', 'full_text': 'Après la destruction des quatre mondes précédents, les dieux se sacrifient à Teotihuacan pour créer le cinquième soleil. Nanahuatzin, le plus humble, devient le nouveau soleil.', 'themes': 'Création, Sacrifice, Destruction, Renaissance', 'image': 'https://i.imgur.com/8Ll8X8S.jpg'},
                    {'title': 'La Naissance de Huitzilopochtli', 'summary': 'Le dieu guerrier né déjà armé', 'full_text': 'Huitzilopochtli naît déjà adulte et armé de sa mère Coatlicue pour défendre sa sœur Coyolxauhqui et ses frères qui voulaient la tuer.', 'themes': 'Naissance, Guerre, Protection, Tragédie', 'image': 'https://i.imgur.com/4Mm9Y9T.jpg'},
                    {'title': 'Quetzalcoatl et le Maïs', 'summary': 'Le dieu qui offre le maïs aux humains', 'full_text': 'Quetzalcoatl vole les os précieux contenant le maïs dans le monde souterrain pour les offrir aux humains, leur permettant de cultiver et de survivre.', 'themes': 'Vol, Don, Survie, Agriculture', 'image': 'https://i.imgur.com/9Nn9X9U.jpg'},
                ]
            },
            {
                'title': 'Mythologie Aborigène',
                'icon_class': 'fa-leaf',
                'color_from': 'from-amber-700',
                'color_to': 'to-orange-600',
                'description': 'La mythologie aborigène australienne est l\'ensemble des croyances spirituelles des peuples indigènes d\'Australie. Elle explique la création du monde à travers le "Temps du Rêve", une époque mythique où les êtres ancestraux ont façonné le paysage.',
                'card_summary': 'Temps du Rêve, êtres ancestraux et paysage sacré',
                'characters': [
                    {'name': 'L\'Arc-en-ciel Serpent', 'role': 'Créateur suprême', 'description': 'Être ancestral qui a créé le paysage et les êtres vivants.', 'image': 'https://i.imgur.com/9Mm9X9V.jpg'},
                    {'name': 'Bunjil', 'role': 'Aigle créateur', 'description': 'Esprit créateur sous forme d\'aigle dans le sud-est.', 'image': 'https://i.imgur.com/4Nn8Y8W.jpg'},
                    {'name': 'Wagyl', 'role': 'Serpent d\'eau', 'description': 'Grand serpent qui a créé les rivières et lacs.', 'image': 'https://i.imgur.com/8Ll9X7X.jpg'},
                    {'name': 'Namarrgon', 'role': 'Homme-tonnerre', 'description': 'Esprit puissant qui crée les orages et éclairs.', 'image': 'https://i.imgur.com/3Mm8Y6Y.jpg'},
                    {'name': 'Wati Nyiru', 'role': 'Homme du soleil', 'description': 'Esprit qui poursuit les sœurs Kungkarangkalpa.', 'image': 'https://i.imgur.com/7Nn7Y5Z.jpg'},
                    {'name': 'Yurlungur', 'role': 'Grand serpent', 'description': 'Serpent arc-en-ciel du nord de l\'Australie.', 'image': 'https://i.imgur.com/2Ll6Y4A.jpg'},
                    {'name': 'Tiddalik', 'role': 'Grenouille géante', 'description': 'Grenouille qui a bu toute l\'eau du monde.', 'image': 'https://i.imgur.com/9Kl8X7B.jpg'},
                    {'name': 'Mimi', 'role': 'Esprits minces', 'description': 'Esprits fragiles qui vivent dans les rochers.', 'image': 'https://i.imgur.com/5Ll9Y8C.jpg'},
                    {'name': 'Julana', 'role': 'Homme rouge', 'description': 'Esprit joueur qui crée des tornades.', 'image': 'https://i.imgur.com/6Mm7X9D.jpg'},
                ],
                'stories': [
                    {'title': 'Le Temps du Rêve', 'summary': 'La création du monde par les êtres ancestraux', 'full_text': 'Pendant le Temps du Rêve, les êtres ancestraux ont émergé de la terre et ont créé le paysage, les animaux et les humains avant de retourner sous terre, laissant leur esprit dans les lieux sacrés.', 'themes': 'Création, Temps, Espace, Spiritualité', 'image': 'https://i.imgur.com/8Ll8X8E.jpg'},
                    {'title': 'Tiddalik la Grenouille Géante', 'summary': 'La grenouille qui a bu toute l\'eau', 'full_text': 'Tiddalik, grenouille géante, avale toute l\'eau du monde. Les animaux doivent le faire rire pour libérer l\'eau et sauver la planète de la sécheresse.', 'themes': 'Gourmandise, Sauvetage, Humour, Nature', 'image': 'https://i.imgur.com/4Mm9Y9F.jpg'},
                    {'title': 'Les Sept Sœurs', 'summary': 'La poursuite éternelle dans le ciel', 'full_text': 'Les sœurs Kungkarangkalpa sont poursuivies par Wati Nyiru à travers le désert. Elles s\'envolent dans le ciel pour devenir les Pléiades.', 'themes': 'Poursuite, Protection, Astronomie, Évasion', 'image': 'https://i.imgur.com/9Nn9X9G.jpg'},
                ]
            }
        ]
        
        # Créer les mythologies et leur contenu
        for myth_data in mythologies_data:
            # Créer la mythologie
            mythology = Mythology.objects.create(
                title=myth_data['title'],
                icon_class=myth_data['icon_class'],
                color_from=myth_data['color_from'],
                color_to=myth_data['color_to'],
                description=myth_data['description'],
                card_summary=myth_data['card_summary']
            )
            
            self.stdout.write(f'OK Créé: {mythology.title}')
            
            # Créer les personnages (limité à 6 par mythologie)
            characters = []
            max_characters = 6
            for i, char_data in enumerate(myth_data['characters'][:max_characters]):
                character = Character.objects.create(
                    mythology=mythology,
                    name=char_data['name'],
                    slug=slugify(char_data['name']),
                    role=char_data['role'],
                    description=char_data['description'],
                    image_url=char_data['image']
                )
                characters.append(character)
            
            self.stdout.write(f'   -> {len(characters)} personnages créés (limité à {max_characters})')
            
            # Créer les histoires
            for story_data in myth_data['stories']:
                story = MythStory.objects.create(
                    mythology=mythology,
                    title=story_data['title'],
                    slug=slugify(story_data['title']),
                    summary=story_data['summary'],
                    full_text=story_data['full_text'],
                    themes=story_data['themes'],
                    image_url=story_data['image']
                )
                
                # Ajouter quelques personnages aléatoires à chaque histoire
                if characters:
                    selected_chars = random.sample(characters, min(random.randint(2, 5), len(characters)))
                    story.characters.set(selected_chars)
            
            self.stdout.write(f'   -> {len(myth_data["stories"])} histoires créées')
        
        self.stdout.write(self.style.SUCCESS('Peuplement complet terminé avec succès !'))
        self.stdout.write(f'Statistiques:')
        self.stdout.write(f'   - {Mythology.objects.count()} mythologies créées')
        self.stdout.write(f'   - {Character.objects.count()} personnages créés')
        self.stdout.write(f'   - {MythStory.objects.count()} histoires créées')