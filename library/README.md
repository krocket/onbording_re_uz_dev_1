# Module de Gestion de Bibliothèque

## Fonctionnalités

Ce module permet de gérer une bibliothèque avec les fonctionnalités suivantes :

- Gestion des livres avec titre, description, ISBN, etc.
- Gestion des auteurs, éditeurs et catégories
- Validation automatique des ISBN
- Génération de rapports PDF

## Rapport PDF

### Comment générer un rapport PDF

1. **Depuis la liste des livres :**

   - Allez dans le menu "Bibliothèque" > "Livres"
   - Sélectionnez un ou plusieurs livres
   - Cliquez sur "Action" > "Rapport des Livres"

2. **Depuis un livre individuel :**
   - Ouvrez un livre
   - Cliquez sur le bouton "Générer PDF" dans l'en-tête

### Contenu du rapport

Le rapport PDF inclut :

- Un en-tête avec le titre "Catalogue de la Bibliothèque"
- Des statistiques (total, disponibles, empruntés, perdus)
- Une liste détaillée de tous les livres avec :
  - Titre
  - ISBN
  - Auteurs
  - Éditeur
  - Catégorie
  - Date de publication
  - État (avec code couleur)
  - Référence
  - Description (si disponible)

### Installation

1. Assurez-vous que le module est installé dans Odoo
2. Les rapports sont automatiquement disponibles après l'installation
3. Redémarrez Odoo si nécessaire

### Personnalisation

Pour personnaliser le rapport :

- Modifiez le template dans `reports/library_book_report.xml`
- Ajustez la logique dans `reports/library_book_report.py`
- Ajoutez de nouveaux champs selon vos besoins
