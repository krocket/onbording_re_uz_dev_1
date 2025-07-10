# Routes API - Module Library

## 🚀 Routes disponibles

### **Routes principales**

#### `GET /api/test`

- **Description** : Page de diagnostic et test
- **Fonctionnalités** :
  - Vérification de l'état des modèles
  - Comptage des enregistrements
  - Diagnostic des erreurs
- **Retour** : Page HTML avec diagnostic

#### `GET /api/books`

- **Description** : Liste de tous les livres
- **Fonctionnalités** :
  - Affichage de tous les livres actifs
  - Barre de recherche
  - Filtres par état
  - Pagination
- **Template** : `library.books_list_template`
- **Retour** : Page HTML avec liste des livres

#### `GET /api/books/<int:book_id>`

- **Description** : Détails d'un livre spécifique
- **Paramètres** :
  - `book_id` : ID du livre
- **Fonctionnalités** :
  - Affichage détaillé du livre
  - Informations complètes (auteurs, éditeur, etc.)
  - Navigation retour
- **Template** : `library.book_detail_template`
- **Retour** : Page HTML avec détails du livre

#### `GET /api/books/search`

- **Description** : Recherche de livres
- **Paramètres** :
  - `q` : Terme de recherche
- **Fonctionnalités** :
  - Recherche par titre, auteur, catégorie, éditeur
  - Résultats filtrés
  - Affichage des résultats
- **Template** : `library.books_list_template`
- **Retour** : Page HTML avec résultats de recherche

## 🎨 Interfaces disponibles

### **Interface classique**

- **URL** : `/api/books`
- **Caractéristiques** :
  - Design simple et efficace
  - Navigation basique
  - Recherche par formulaire

### **Interface moderne**

- **URL** : Accessible via menu "Interface Moderne"
- **Caractéristiques** :
  - Design moderne avec animations
  - Statistiques en temps réel
  - Filtres avancés
  - Interface JavaScript interactive
  - Modal pour les détails

## 📊 Données retournées

### **Structure d'un livre**

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

### **États des livres**

- `available` : Disponible
- `borrowed` : Emprunté
- `lost` : Perdu

## 🔧 Configuration

### **Templates utilisés**

- `library.books_list_template` : Liste des livres
- `library.book_detail_template` : Détails d'un livre
- `library.error_template` : Pages d'erreur
- `modern_books_interface` : Interface moderne

### **Gestion d'erreurs**

- Modèle non disponible
- Livre non trouvé
- Erreur de recherche
- Erreur de connexion

## 🎯 Exemples d'utilisation

### **Recherche de livres**

```bash
# Recherche par titre
GET /api/books/search?q=python

# Recherche par auteur
GET /api/books/search?q=Victor Hugo

# Recherche par catégorie
GET /api/books/search?q=roman
```

### **Accès aux détails**

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
