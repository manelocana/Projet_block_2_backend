Backend Python from Scratch (Block 2)
# 🟦 BLOCK 2 — API Backend en Python pur (sans framework)

## 📌 Introduction

Ce projet consiste en la réalisation d’une API backend complète développée en **Python pur**, sans l’utilisation de frameworks tels que Flask ou Django.

L’objectif principal est de comprendre en profondeur le fonctionnement interne d’un backend web, notamment :
- la gestion des requêtes HTTP,
- le routage manuel,
- la séparation des responsabilités,
- l’accès à une base de données relationnelle,
- la gestion des réponses JSON.

Ce projet reproduit de manière simplifiée le comportement interne d’un framework web.


---


## 🚀 Lancement du projet

### ▶️ Démarrer le serveur

<!-- bash -->
    python main.py


---


## 🌐 Accès à l’API

L’API est disponible en local à l’adresse :

    http://localhost:8000


Le serveur utilise le module natif http.server de Python.


---


## 🧱 Architecture générale

Le projet suit une architecture inspirée du modèle MVC simplifié :

Requête HTTP → Handler → Controller → Model → Base de données → Réponse JSON


---



## 📁 Structure du projet

project/
│
├── main.py                  # Point d’entrée du serveur HTTP
├── db_config.py             # Configuration de la connexion base de données
│
├── controllers/             # Logique métier (business logic)
│   ├── user_controller.py
│   ├── artwork_controller.py
│   ├── biography_controller.py
│   └── message_controller.py
│
├── models/                  # Accès et manipulation de la base de données
│   ├── user.py
│   ├── artwork.py
│   ├── biography.py
│   └── message.py
│
├── tests/                   # Tests unitaires avec pytest
│
└── README.md


---


## ⚙️ Technologies utilisées

- Python 3.11
- http.server (BaseHTTPRequestHandler)
- JSON (format d’échange de données)
- MySQL / SQLite (base de données relationnelle)
- Pytest (tests unitaires)
- Thunder Client (tests API)


---


## 🔄 Fonctionnement global

Chaque requête HTTP suit le flux suivant :

### Client → Handler → Controller → Model → Base de données → Response


## Description des étapes :

### 1. Handler

Le Handler hérite de BaseHTTPRequestHandler.

Il est responsable de :

- recevoir les requêtes HTTP,
- analyser la route (URL),
- extraire les données (body, headers),
- rediriger vers le bon contrôleur.

Il gère les méthodes :

- GET
- POST
- PUT
- DELETE


### 2. Controllers

Les contrôleurs contiennent la logique métier.

Ils sont responsables de :

- valider les données reçues,
- appliquer les règles métier,
- appeler les modèles,
- formater la réponse.

Chaque entité possède son contrôleur :

- UserController
- ArtworkController
- BiographyController
- MessageController


### 3. Models

Les modèles gèrent directement l’accès à la base de données.

Ils contiennent les requêtes SQL :

- SELECT
- INSERT
- UPDATE
- DELETE

Chaque modèle correspond à une table de la base de données.


---


## 📦 Système de réponse

Une classe Response a été créée pour centraliser la gestion des réponses HTTP.

Elle permet :

- la conversion des dictionnaires Python en JSON,
- l’ajout des headers HTTP,
- la gestion des codes de statut (200, 400, 404, etc.),
- la gestion du CORS.


---



## 🌐 Endpoints de l’API


🔐 Authentification
| Méthode | Route         | Description               |
| ------- | ------------- | ------------------------- |
| POST    | /api/register | Création d’un utilisateur |
| POST    | /api/login    | Connexion utilisateur     |


🎨 Artworks
| Méthode | Route             | Description                 |
| ------- | ----------------- | --------------------------- |
| GET     | /api/artworks     | Récupérer tous les artworks |
| POST    | /api/artworks     | Créer un artwork            |
| PUT     | /api/artworks/:id | Modifier un artwork         |
| DELETE  | /api/artworks/:id | Supprimer un artwork        |


👤 Utilisateurs
| Méthode | Route      | Description                               |
| ------- | ---------- | ----------------------------------------- |
| GET     | /api/users | Liste des utilisateurs (admin uniquement) |


📖 Biographie
| Méthode | Route          | Description                 |
| ------- | -------------- | --------------------------- |
| GET     | /api/biography | Récupérer la biographie     |
| PUT     | /api/biography | Mettre à jour la biographie |


💬 Messages
| Méthode | Route         | Description                          |
| ------- | ------------- | ------------------------------------ |
| POST    | /api/contact  | Envoyer un message                   |
| GET     | /api/messages | Voir les messages (admin uniquement) |


---



## 🔐 Authentification et autorisation

Le système de sécurité est simplifié et repose sur les headers HTTP :

Headers utilisés :
- Role: admin
- User-Id: 1
- Logique :
- Les routes protégées vérifient le rôle admin

Certaines routes utilisent User-Id pour identifier l’utilisateur


---


## 🗄️ Base de données

La base de données est relationnelle et contient les tables suivantes :

- users
- artworks
- biography
- messages

Chaque modèle contient les opérations CRUD :

- Create
- Read
- Update
- Delete



---


## 🧪 Tests

Les tests ont été réalisés avec pytest.

Ils permettent de vérifier :

- la validation des données,
- la logique des contrôleurs,
- le comportement des routes.

Les tests utilisent également des mocks afin d’éviter l’accès réel à la base de données.


---


## 🔧 Gestion des erreurs

L’API gère plusieurs types d’erreurs :

- Données manquantes (400)
- Accès non autorisé (403)
- Ressource introuvable (404)
- Erreurs de validation

Toutes les erreurs sont retournées au format JSON.


---


## 🧠 Choix techniques

Ce projet a été réalisé sans framework afin de :

- comprendre le fonctionnement interne d’un serveur HTTP,
- maîtriser la gestion des requêtes sans abstraction,
- comprendre la séparation MVC,
- apprendre le fonctionnement réel d’un backend.


---



## 🎯 Conclusion

Ce projet démontre la création complète d’une API backend en Python pur.

Il reproduit le fonctionnement interne des frameworks modernes tout en gardant un contrôle total sur chaque couche de l’application.

Ce travail permet de comprendre en profondeur les concepts fondamentaux du développement backend.