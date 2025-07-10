# Structure du Module Library

## 📁 Organisation des vues

### `/views/api/` - Vues API

- **`books_api_view.xml`** - Template pour la liste des livres via API
- **`book_detail_view.xml`** - Template pour les détails d'un livre via API
- **`error_view.xml`** - Template pour les pages d'erreur API
- **`modern_interface_view.xml`** - Interface moderne avec JavaScript

### `/views/web/` - Vues web classiques Odoo

- **`book_view.xml`** - Vues formulaire, liste et recherche pour les livres
- **`author_view.xml`** - Vues pour les auteurs
- **`publisher_view.xml`** - Vues pour les éditeurs
- **`category_view.xml`** - Vues pour les catégories

### `/views/menus/` - Menus

- **`library_menu.xml`** - Menu principal et sous-menus de la bibliothèque

## 🚀 Routes API disponibles

### Routes principales

- **`GET /api/test`** - Page de diagnostic et test
- **`GET /api/books`** - Liste de tous les livres
- **`GET /api/books/<id>`** - Détails d'un livre spécifique
- **`GET /api/books/search?q=<terme>`** - Recherche de livres

### Templates utilisés

- **`library.books_list_template`** - Affichage de la liste des livres
- **`library.book_detail_template`** - Affichage des détails d'un livre
- **`library.error_template`** - Affichage des erreurs
- **`modern_books_interface`** - Interface moderne avec JavaScript

## 🎯 Fonctionnalités

### Interface API

- ✅ Design responsive avec Bootstrap
- ✅ Recherche en temps réel
- ✅ Navigation intuitive
- ✅ Gestion d'erreurs robuste
- ✅ Badges d'état colorés

### Interface moderne

- ✅ Statistiques en temps réel
- ✅ Filtres avancés avec animations
- ✅ Modal pour les détails
- ✅ Pagination dynamique
- ✅ JavaScript moderne (ES6)

### Interface web classique

- ✅ Vues formulaire complètes
- ✅ Vues liste avec filtres
- ✅ Recherche avancée
- ✅ Groupement par auteurs

## 🔧 Installation

1. **Mettre à jour le module** :

   ```bash
   python3 -m odoo -d your_database -u library --stop-after-init
   ```

2. **Tester les routes** :
   - Diagnostic : `http://localhost:8069/api/test`
   - Liste des livres : `http://localhost:8069/api/books`
   - Recherche : `http://localhost:8069/api/books/search?q=python`

## 📋 Structure des données

### Modèles disponibles

- **`library.book`** - Livres avec tous les détails
- **`library.author`** - Auteurs des livres
- **`library.publisher`** - Éditeurs
- **`library.book.category`** - Catégories de livres

### Champs principaux des livres

- `name` - Titre du livre
- `description` - Description
- `isbn` - Numéro ISBN
- `state` - État (available/borrowed/lost)
- `publication_date` - Date de publication
- `publisher_id` - Éditeur (relation)
- `author_ids` - Auteurs (relation multiple)
- `category_id` - Catégorie (relation)

## 🎨 Interfaces disponibles

### Interface classique

- **URL** : `/api/books`
- **Caractéristiques** :
  - Design simple et efficace
  - Navigation basique
  - Recherche par formulaire

### Interface moderne

- **URL** : Accessible via menu "Interface Moderne"
- **Caractéristiques** :
  - Design moderne avec animations
  - Statistiques en temps réel
  - Filtres avancés
  - Interface JavaScript interactive
  - Modal pour les détails

### Interface web Odoo

- **URL** : Via menu "Library" > "Books"
- **Caractéristiques** :
  - Formulaires Odoo classiques
  - Vues liste et recherche
  - Intégration complète avec Odoo

## 📊 Données retournées

### Structure d'un livre

```json
{
  "id": 1,
  "name": "Titre du livre",
  "description": "Description du livre",
  "publication_date": "2024-01-01",
  "isbn": "978-1234567890",
  "state": "available",
  "reference": "REF001",
  "publisher": {
    "id": 1,
    "name": "Nom de l'éditeur"
  },
  "authors": [
    {
      "id": 1,
      "name": "Nom de l'auteur"
    }
  ],
  "category": {
    "id": 1,
    "name": "Nom de la catégorie"
  }
}
```

### États des livres

- `available` : Disponible
- `borrowed` : Emprunté
- `lost` : Perdu

## 🔧 Configuration

### Templates utilisés

- `library.books_list_template` : Liste des livres
- `library.book_detail_template` : Détails d'un livre
- `library.error_template` : Pages d'erreur
- `modern_books_interface` : Interface moderne

### Gestion d'erreurs

- Modèle non disponible
- Livre non trouvé
- Erreur de recherche
- Erreur de connexion

## 🎯 Exemples d'utilisation

### Recherche de livres

```bash
# Recherche par titre
GET /api/books/search?q=python

# Recherche par auteur
GET /api/books/search?q=Victor Hugo

# Recherche par catégorie
GET /api/books/search?q=roman
```

### Accès aux détails

```bash
# Détails du livre avec ID 1
GET /api/books/1
```

## 🚀 Installation et test

1. **Installer le module** :

   ```bash
   python3 -m odoo -d your_database -u library --stop-after-init
   ```

2. **Tester les routes** :

   - Diagnostic : `http://localhost:8069/api/test`
   - Liste des livres : `http://localhost:8069/api/books`
   - Recherche : `http://localhost:8069/api/books/search?q=python`

3. **Interface moderne** :
   - Accès via le menu "Library" > "Interface Moderne"

## 📝 Notes techniques

- **Authentification** : `auth='public'` (pas d'authentification requise)
- **CSRF** : Désactivé pour les routes API
- **Méthodes** : GET uniquement
- **Format de retour** : HTML avec templates QWeb
- **Gestion d'erreurs** : Templates d'erreur centralisés

## 🎨 Avantages de la structure

- **Organisation claire** - Chaque type de vue dans son dossier
- **Maintenance facile** - Séparation des responsabilités
- **Évolutivité** - Facile d'ajouter de nouvelles vues
- **Réutilisabilité** - Templates modulaires
- **Documentation** - Structure bien documentée
