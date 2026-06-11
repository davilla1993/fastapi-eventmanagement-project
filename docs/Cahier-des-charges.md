# Projets d'évaluation finale — APIs Web Flask & FastAPI

### Livrables attendus pour chaque projet

1. **Dépôt Git public** (GitHub/GitLab) avec historique de commits propre et atomiques.
2. **Code source** structuré, lisible, conforme aux bonnes pratiques (PEP 8, typage statique avec `mypy` ou `pyright` recommandé).
3. **README.md** complet : description, architecture, installation, lancement, exemples d'appels API (`curl` ou `httpie`), captures.
4. **Tests automatisés** (`pytest`) avec **couverture ≥ 70 %** mesurée via `pytest-cov`.
5. **Documentation OpenAPI/Swagger** fonctionnelle et exemples de requêtes/réponses documentés.
6. **Dockerfile + docker-compose.yml** permettant un lancement reproductible (`docker compose up`).
7. **Pipeline CI** minimal (GitHub Actions ou GitLab CI) : lint + tests + build de l'image Docker.
8. **Rapport technique** (5–10 pages, PDF) : choix d'architecture, difficultés rencontrées, métriques, perspectives.
9. **Démo vidéo** (3–5 min) ou **soutenance** de 15 minutes (à confirmer par l'enseignant).

### Barème commun (/20)

| Critère | Points |
|---|---|
| Qualité du code (structure, lisibilité, typage) | 4 |
| Fonctionnalités demandées (complétude) | 4 |
| Tests automatisés (couverture, qualité) | 3 |
| Sécurité (authentification, validation, secrets, CORS) | 3 |
| Documentation (README, OpenAPI, rapport) | 2 |
| Déploiement (Docker, CI, reproductibilité) | 2 |
| Originalité / dépassement du cahier des charges | 2 |

### Contraintes transverses

- **Python ≥ 3.11**, environnement virtuel `venv` ou `uv`.
- **Validation stricte** des entrées (Pydantic v2 pour FastAPI, Marshmallow ou WTForms pour Flask).
- **Aucun secret en clair** dans le dépôt : `.env` ignoré, exemple dans `.env.example`.
- **Gestion d'erreurs centralisée** : codes HTTP corrects, messages JSON cohérents.
- **Logs structurés** (JSON de préférence) avec niveaux appropriés.
- **Modèles ML** : si pertinent, versionner les poids via Git LFS, MLflow, ou DVC.

### Plagiat

Le plagiat (entre étudiants, depuis Internet, ou via génération brute par IA sans compréhension) entraîne **la note de 0/20** et un signalement administratif. L'usage d'IA assistante est autorisé **uniquement** si l'étudiant peut expliquer chaque ligne de son code en soutenance.

---

## Projet 10 — API publique avancée avec Pydantic v2 et types personnalisés (FastAPI)

**Stack imposée :** FastAPI, Pydantic v2, PostgreSQL, pytest, hypothesis (property-based testing).

**Contexte.** Plateforme publique de gestion d'événements culturels (concerts, théâtre, conférences). L'API doit exposer une validation extrêmement rigoureuse et auto-documentée, accessible à des développeurs tiers.

**Fonctionnalités exigées.**

- Modèles Pydantic v2 avec **types personnalisés** : `CodePostalFR`, `IBAN`, `TelephoneE164`, `Slug`, `URLImage` (avec vérification d'extension et de domaine autorisé).
- Validators et serializers personnalisés (e.g. dates au format ISO 8601 strict, fuseaux horaires explicites).
- Schémas distincts `Create`, `Update`, `Read`, `ReadDetail` selon le besoin.
- **Polymorphisme** : un événement peut être `Concert`, `Theatre`, `Conference`, chacun avec des champs spécifiques (discriminator field).
- Filtres avancés : `GET /evenements?ville=...&date_min=...&prix_max=...&tags=jazz,bebop`.
- Tests **property-based** avec Hypothesis : pour chaque type personnalisé, générer des valeurs aléatoires valides/invalides et vérifier le comportement.

**Difficulté supplémentaire.** L'OpenAPI généré doit afficher des exemples réalistes pour chaque modèle et chaque type personnalisé.

---


**Bon courage, et soignez votre rendu : ces projets sont la dernière brique de votre cursus avant l'industrie ou la recherche.**
