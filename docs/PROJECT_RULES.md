# PROJECT_RULES.md

## Objectif

Ce document définit les règles de développement du projet.

L'architecture du projet n'est pas définie ici.

L'architecture officielle est décrite dans :

docs/ARCHITECTURE.md

Toutes les implémentations doivent respecter cette architecture.

# Priorité des documents

En cas de conflit, appliquer l'ordre suivant :

1. Cahier des charges
2. ARCHITECTURE.md
3. PROJECT_RULES.md
4. CLAUDE.md
5. SKILLS.md
6. TASKS.md

# Principes généraux

* Respecter strictement l'architecture définie dans ARCHITECTURE.md.
* Écrire du code simple, lisible et maintenable.
* Éviter toute duplication de logique métier.
* Respecter le principe de responsabilité unique.
* Favoriser la composition plutôt que l'héritage.
* Utiliser le typage Python partout où cela est pertinent.

# Conventions de nommage

## Fichiers

snake_case.py

Exemples :

event_repository.py
create_event_use_case.py
event_mapper.py

## Classes

PascalCase

Exemples :

Event
EventRepository
CreateEventUseCase

## Fonctions et variables

snake_case

Exemples :

create_event()
find_by_slug()

# Règles API

## Routes

Les routes FastAPI doivent être extrêmement légères.

Autorisé :

* Validation des entrées
* Injection des dépendances
* Appel des cas d'usage
* Retour des DTO

Interdit :

* Logique métier
* Accès direct à la base de données
* Transformations complexes

Exemple :

@app.post(...)
async def create_event(...):
return await use_case.execute(...)

# Cas d'usage

Les cas d'usage contiennent la logique applicative.

Chaque cas d'usage expose une méthode :

execute(...)

Exemples :

CreateEventUseCase
UpdateEventUseCase
DeleteEventUseCase
SearchEventsUseCase

Les cas d'usage orchestrent :

* Validation métier
* Transactions
* Appels aux repositories
* Appels aux services

# Repositories

Les repositories sont responsables uniquement :

* de la lecture
* de l'écriture
* de la suppression

Ils ne doivent jamais contenir :

* de logique métier
* de logique de validation

# Entités

Toutes les entités persistées doivent hériter de BaseEntity.

Champs obligatoires :

* id
* public_id
* created_at
* created_by
* updated_at
* updated_by
* deleted
* deleted_at
* deleted_by

Le soft delete est obligatoire.

# DTO et schémas

Pour chaque ressource :

* CreateSchema
* UpdateSchema
* ReadSchema
* ReadDetailSchema

Les schémas utilisent exclusivement Pydantic v2.

# Types personnalisés

Les types personnalisés doivent être implémentés dans le projet :

* Slug
* URLImage
* CodePostalFR
* TelephoneE164
* IBAN

## Slug

Contraintes :

* minuscules uniquement
* caractères alphanumériques
* tirets autorisés
* unique

Regex :

^[a-z0-9]+(?:-[a-z0-9]+)*$

## URLImage

Contraintes :

* HTTPS obligatoire
* extensions autorisées :

  * jpg
  * jpeg
  * png
  * webp
* validation du domaine autorisé

# Polymorphisme

Les événements utilisent un discriminant.

Types :

* Concert
* Theatre
* Conference

Les schémas Pydantic doivent utiliser les discriminated unions.

# Mapping

Les conversions Entity ↔ DTO doivent être centralisées dans des mappers.

Exemple :

EventMapper

Méthodes recommandées :

to_entity(...)
to_read_schema(...)
to_detail_schema(...)

# Gestion des erreurs

Créer des exceptions métier dédiées.

Exemples :

EventNotFoundException
CategoryNotFoundException
UnauthorizedActionException
DuplicateSlugException

Les exceptions doivent être converties en réponses HTTP appropriées.

# Sécurité

Authentification :

JWT Bearer Token

Rôles :

* ADMIN
* ORGANIZER
* USER

Les contrôles d'autorisation doivent être réalisés dans les cas d'usage ou services dédiés.

# Transactions

Toute opération d'écriture doit être transactionnelle.

Utiliser le Unit Of Work défini dans l'architecture.

# Logs

Interdictions :

* print()
* logging sauvage

Utiliser exclusivement le système de logging du projet.

Les logs doivent inclure :

* utilisateur
* opération
* date
* résultat

# Pagination

Toutes les listes doivent être paginées.

Format standard :

{
"items": [],
"page": 1,
"size": 20,
"total": 120
}

# Documentation OpenAPI

Chaque endpoint doit fournir :

* description
* exemples de requêtes
* exemples de réponses
* codes d'erreurs possibles

Le Swagger doit être exploitable sans documentation externe.

# Tests

Structure :

tests/
├── unit/
├── integration/
└── property/

Obligatoire :

* Pytest
* Hypothesis

Les règles métier critiques doivent être couvertes par des tests de propriété.

# Qualité

Outils obligatoires :

* Ruff
* Black
* MyPy
* Pytest

Objectif minimum :

80 % de couverture.

Aucun warning MyPy ne doit être ignoré sans justification.

# Règle finale

En cas d'hésitation :

1. Respecter le cahier des charges.
2. Respecter ARCHITECTURE.md.
3. Choisir la solution la plus simple.
4. Favoriser la lisibilité et la maintenabilité.
