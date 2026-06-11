# Architecture du projet

/
├── app/
│   │
│   ├── modules/
│   │   │
│   │   ├── iam/
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   │
│   │   ├── events/
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   │
│   │   ├── organizers/
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   │
│   │   ├── venues/
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   │
│   │   └── categories/
│   │       ├── api/
│   │       ├── application/
│   │       ├── domain/
│   │       └── infrastructure/
│   │
│   ├── shared/
│   │   ├── domain/
│   │   ├── types/
│   │   ├── filters/
│   │   ├── pagination/
│   │   ├── exceptions/
│   │   └── utils/
│   │
│   ├── infrastructure/
│   │   ├── config/
│   │   ├── database/
│   │   ├── security/
│   │   ├── logging/
│   │   └── persistence/
│   │
│   ├── main.py
│   └── settings.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── property/
│
├── alembic/
│
├── docs/
│   ├── Cahier-des-charges.md
│   ├── ARCHITECTURE.md
│   ├── PROJECT_RULES.md
│   ├── SKILLS.md
│   └── TASKS.md
│
├── CLAUDE.md
├── pyproject.toml
├── alembic.ini
├── .env
└── docker-compose.yml


## Structure standard d'un module

Chaque module métier doit respecter la structure suivante :


module/
│
├── api/
│   ├── controllers/
│   └── dto/
│       ├── requests/
│       └── responses/
│
├── application/
│   ├── usecases/
│   ├── services/
│   └── mappers/
│
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── exceptions/
│
└── infrastructure/
    ├── repositories/
    └── persistence/

# Règles de dépendances

api
  ↓
application
  ↓
domain

infrastructure
  ↑
application

- domain ne dépend d'aucune autre couche
- application dépend du domain
- api dépend de l'application
- infrastructure implémente les contrats du domain