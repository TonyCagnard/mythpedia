# MythPedia - Plateforme de Mythologies du Monde

Une application web Django complète pour explorer les mythologies du monde entier, avec des fonctionnalités sociales, une API REST et une interface moderne.

## 🌟 Fonctionnalités

### Système de Contenu Riche
- **10 mythologies** du monde entier (Grecque, Nordique, Égyptienne, Romaine, Japonaise, Hindoue, Chinoise, Celtique, Aztèque, Aborigène)
- **110+ personnages** avec descriptions détaillées et rôles
- **30+ histoires** et mythes avec textes complets
- **Images de qualité** pour tous les personnages et histoires

### Fonctionnalités Sociales
- **Système de commentaires** sur tous les contenus
- **Notations 5 étoiles** avec calcul de moyennes
- **Favoris personnels** pour les mythologies et personnages
- **Partage social** (Facebook, Twitter, LinkedIn, Email)

### Recherche Avancée
- **Recherche par mots-clés** dans tous les types de contenu
- **Filtres par type** (mythologies, personnages, histoires)
- **Filtre par mythologie** pour affiner les résultats
- **Résultats organisés** par catégorie

### Interface Utilisateur
- **Design moderne** avec Tailwind CSS et Font Awesome
- **Navigation responsive** adaptée mobile/desktop
- **Messages de notification** automatiques
- **Expérience utilisateur** optimisée

### API REST Complète
- **Endpoints pour toutes les ressources** (mythologies, personnages, histoires)
- **Système de filtrage** avancé avec Django Filter
- **Actions personnalisées** (ex: personnages d'une mythologie)
- **Statistiques des notations** via l'API

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8+
- Django 5.2+
- Pip (gestionnaire de paquets Python)

### Installation
1. Clonez ce repository
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration Automatique (Recommandé)
1. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```

2. **Configurez automatiquement TOUT le contenu** en une seule commande :
   ```bash
   python manage.py setup_complete
   ```
   *Cette commande inclut maintenant le nettoyage des faux commentaires et limite les personnages à 6 par mythologie*

3. Lancez le serveur de développement :
   ```bash
   python manage.py runserver
   ```

4. Accédez à l'application :
   - Site web : `http://127.0.0.1:8000/`
   - Administration : `http://127.0.0.1:8000/admin/`
   - API REST : `http://127.0.0.1:8000/api/`

## 📊 Contenu Inclus

La commande `setup_complete` crée automatiquement :

### Mythologies (10)
- Grecque, Nordique, Égyptienne, Romaine
- Japonaise, Hindoue, Chinoise, Celtique
- Aztèque, Aborigène

### Personnages (60+)
- **6 personnages par mythologie** pour une meilleure expérience utilisateur
- Dieux et déesses principaux
- Héros légendaires et créatures mythiques
- Descriptions détaillées et rôles spécifiques
- Images uniques pour chaque personnage
- **Affichage en défilement horizontal** pour éviter les pages trop longues

### Histoires (30+)
- Mythes fondateurs et épopées légendaires
- Récits complets avec thèmes identifiés
- Personnages associés automatiquement
- Images illustratives pour chaque histoire

### Interactions Sociales
- **Commentaires réels** (pas de faux commentaires de démonstration)
- **Notations** avec moyennes calculées
- **5 utilisateurs de démonstration** disponibles pour tester les fonctionnalités

## 👥 Utilisateurs de Démonstration

Pour tester les fonctionnalités sociales, utilisez ces comptes :
- **zeus_fan**@example.com (mot de passe: demo123)
- **odin_lover**@example.com (mot de passe: demo123)
- **ra_worshipper**@example.com (mot de passe: demo123)
- **thor_follower**@example.com (mot de passe: demo123)
- **athena_scholar**@example.com (mot de passe: demo123)

## 🔧 Commandes de Gestion

### Configuration Complète
```bash
# Configuration complète en UNE SEULE commande (recommandé)
python manage.py setup_complete
```

Cette commande exécute automatiquement :
1. `clean_comments` - Supprime les faux commentaires des utilisateurs de démonstration
2. `seed_comprehensive` - Crée toutes les mythologies (limité à 6 personnages par mythologie), personnages et histoires
3. `generate_images` - Génère des images de qualité pour tout le contenu
4. `generate_interactions` - Ajoute des commentaires et notations réalistes (désactivé par défaut)

### Commandes Individuelles
```bash
# Peuplement des mythologies uniquement
python manage.py seed_comprehensive

# Génération d'images
python manage.py generate_images

# Génération d'interactions sociales
python manage.py generate_interactions
```

### Administration Django
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

## 🌐 API REST

### Endpoints Principaux
- `GET /api/mythologies/` - Liste des mythologies
- `GET /api/characters/` - Liste des personnages
- `GET /api/stories/` - Liste des histoires
- `GET /api/comments/` - Commentaires et notations

### Filtres Disponibles
- `?search=terme` - Recherche par mots-clés
- `?mythology=id` - Filtrer par mythologie
- `?type=mythology|character|story` - Filtrer par type

## 🎨 Personnalisation

### Ajouter de Nouvelles Mythologies
1. Ajoutez des données dans `mythpedia/management/commands/seed_comprehensive.py`
2. Exécutez `python manage.py seed_comprehensive`
3. Les nouvelles mythologies seront automatiquement intégrées

### Modifier le Design
- Templates dans `mythpedia/templates/`
- Styles CSS avec Tailwind CSS
- Icônes Font Awesome intégrées

## 📝 Structure du Projet

```
mythology_project/
├── mythology_project/          # Configuration Django
├── mythpedia/                 # Application principale
│   ├── models.py             # Modèles de données
│   ├── views.py              # Logique des vues
│   ├── templates/            # Templates HTML
│   ├── management/commands/   # Scripts de gestion
│   └── api_views.py         # Vues de l'API REST
└── README.md                 # Ce fichier
```

## 🎯 Pour Commencer Immédiatement

Vous voulez un site complet **sans effort** ? Exécutez simplement :

```bash
# 1. Installez les dépendances
pip install -r requirements.txt

# 2. Appliquez les migrations
python manage.py migrate

# 3. Configurez TOUT en une seule commande
python manage.py setup_complete

# 4. Lancez le serveur
python manage.py runserver
```

**Voilà !** Votre site MythPedia est maintenant complet avec :
- 10 mythologies du monde entier
- 110+ personnages avec images
- 30+ histoires mythologiques
- 350+ commentaires et 600+ notations
- 5 utilisateurs de démonstration

Accédez à `http://127.0.0.1:8000/` et explorez !

## 🤝 Contribuer

1. Fork ce repository
2. Créez une branche de fonctionnalité
3. Commitez vos changements
4. Pushez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- Django Framework pour le backend robuste
- Tailwind CSS pour le design moderne
- Font Awesome pour les icônes
- Django REST Framework pour l'API

---

**MythPedia** - Explorez les mythologies du monde entier en un seul lieu ! 🌍✨

**Pas besoin de créer manuellement le contenu - tout est automatiquement configuré pour vous !** 🚀