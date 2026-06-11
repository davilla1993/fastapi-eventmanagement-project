# SKILLS.md

## Objectif

Ce document décrit les standards techniques obligatoires du projet.

Claude doit respecter ces règles lors de chaque génération de code.

---

# Technologies

## Backend

* Python 3.13+
* FastAPI
* Pydantic v2
* SQLAlchemy 2.x
* PostgreSQL
* Alembic

## Authentification

* JWT
* RBAC

## Qualité

* Ruff
* Black
* MyPy
* Pytest
* Hypothesis

## Conteneurisation

* Docker
* Docker Compose

---

# Architecture

Architecture DDD Lite inspirée des projets Spring Boot.

Aucune logique métier ne doit être placée dans :

* les routes
* les schémas Pydantic
* les repositories

La logique métier appartient exclusivement aux Use Cases.

---

# Structure des modules

Chaque module doit respecter la structure suivante :

modules/<module>/

* api/
* application/
* domain/
* infrastructure/

---

# API

Les routes FastAPI doivent :

* être fines
* déléguer aux Use Cases
* ne contenir aucune logique métier

Les routes doivent uniquement :

* recevoir la requête
* appeler un Use Case
* retourner la réponse

---

# Couche Application

La couche Application contient :

* les Use Cases
* les DTO
* les ports

Les Use Cases doivent être :

* simples
* testables
* indépendants du framework

---

# Couche Domaine

La couche Domaine contient :

* les entités métier
* les règles métier
* les Value Objects
* les exceptions métier

Le domaine ne doit jamais dépendre :

* de FastAPI
* de SQLAlchemy
* de PostgreSQL

---

# Couche Infrastructure

La couche Infrastructure contient :

* les repositories SQLAlchemy
* les adaptateurs externes
* la persistance

Aucune règle métier ne doit être implémentée ici.

---

# BaseEntity

Toutes les entités héritent de BaseEntity.

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

---

# Soft Delete

Suppression logique obligatoire.

Aucune suppression physique.

Les requêtes standard doivent exclure automatiquement les éléments supprimés.

---

# Audit

Toutes les modifications doivent être traçables.

Au minimum :

* créateur
* date de création
* modificateur
* date de modification

---

# Authentification

JWT obligatoire.

Endpoints protégés.

Gestion des rôles :

* ADMIN
* ORGANIZER
* USER

---

# Autorisations

ADMIN :

* accès complet

ORGANIZER :

* gestion de ses événements

USER :

* consultation publique

---

# Pydantic v2

Utiliser systématiquement :

* field_validator
* model_validator
* field_serializer

Éviter les anciennes API Pydantic v1.

---

# Types personnalisés

Créer les types suivants :

* Slug
* URLImage
* CodePostalFR
* TelephoneE164
* IBAN

Chaque type doit posséder :

* validation
* tests
* documentation

---

# Règles Slug

Format :

^[a-z0-9]+(?:-[a-z0-9]+)*$

Contraintes :

* minuscules
* sans accent
* sans espace
* unique

Possibilité de génération automatique depuis le titre.

---

# Règles URLImage

HTTPS obligatoire.

Extensions autorisées :

* jpg
* jpeg
* png
* webp

Validation du domaine obligatoire.

---

# Schémas API

Créer systématiquement :

* CreateSchema
* UpdateSchema
* ReadSchema
* ReadDetailSchema

Ne jamais exposer directement les entités SQLAlchemy.

---

# Polymorphisme

Implémenter les types :

* Concert
* Theatre
* Conference

Utiliser les discriminators Pydantic v2.

---

# Repository Pattern

Tous les accès aux données passent par des repositories.

Les Use Cases ne doivent jamais manipuler directement SQLAlchemy.

---

# Unit Of Work

Les transactions doivent être centralisées.

Les commits ne doivent pas être effectués dans les routes.

---

# Pagination

Toutes les listes doivent supporter :

* page
* size
* total

---

# Recherche

Prévoir :

* filtres
* tri
* pagination

sur les événements.

---

# Documentation OpenAPI

Chaque endpoint doit fournir :

* description
* exemples
* codes d'erreur

La documentation Swagger doit être exploitable sans lire le code.

---

# Logging

Logs structurés obligatoires.

Aucun print().

Utiliser le module logging.

---

# Tests

Chaque Use Case doit être testé.

Chaque Repository doit être testé.

Chaque endpoint critique doit être testé.

---

# Property Based Testing

Utiliser Hypothesis pour :

* Slug
* URLImage
* IBAN
* TelephoneE164
* CodePostalFR

---

# Couverture

Objectif minimal :

80 % de couverture.

---

# Qualité du code

Avant toute livraison :

* Ruff
* Black
* MyPy
* Pytest

doivent être exécutés avec succès.

---

# Interdictions

Ne jamais :

* mettre de logique métier dans les routes
* mettre de logique métier dans les repositories
* exposer directement les entités SQLAlchemy
* contourner les Use Cases
* ignorer les tests
* utiliser Any sans justification

---

# Priorité

Ordre de priorité :

1. Cahier des charges
2. PROJECT_RULES.md
3. CLAUDE.md
4. SKILLS.md
5. TASKS.md

En cas de conflit, respecter cet ordre.
