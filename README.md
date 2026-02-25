

# 📘 BLOC 2 – Backend sans framework (Python + MySQL)



## 🎯 Objectif

### Développer un backend **from scratch** :

- Sans framework (pas de Flask)

- Architecture MVC manuelle

- Programmation orientée objet (POO)

- Utilisation de MySQL

- Exposition d’endpoints REST

- Gestion des utilisateurs, rôles et artworks


⚠️ Le backend est une API JSON, pas une application web HTML.
Le navigateur affichera du JSON… ou une 404 si la route n’existe pas.

---

## 1️⃣ Architecture générale

### Structure du projet

    backend/
    │
    ├── main.py              → Serveur HTTP et routing
    ├── db_config.py         → Connexion MySQL
    │
    ├── models/              → Logique base de données
    │   ├── user.py
    │   ├── artwork.py
    │
    ├── controllers/         → Logique métier
    │   ├── user_controller.py
    │   ├── artwork_controller.py
    │
    └── database.sql         → Script de création des tables


---

### Responsabilités

- main.py → Reçoit les requêtes HTTP et gère le routing manuel

- controllers/ → Valide les données et appelle les modèles

- models/ → Exécute les requêtes SQL

- database.sql → Définit la structure de la base de données


### Architecture MVC :

    Modèle → Controller → Vue (JSON)

La fonction _send_json() joue le rôle de “vue”.


---

## 2️⃣ Serveur HTTP manuel

Nous utilisons :

    from http.server import HTTPServer, BaseHTTPRequestHandler



Méthodes implémentées :

- do_GET()

- do_POST()

- do_PUT()

- do_DELETE()


Routing manuel :

    if self.path.startswith("/api/artworks"):

⚠️ Toujours utiliser la barre initiale /.
Sans elle, la route ne correspond pas → 404.


---


## 3️⃣ _send_json() – Envoi de réponse

### Fonction dans le Handler :

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)



### Responsabilités :

- Sérialisation JSON

- Envoi des headers corrects

- Prévention des erreurs AttributeError


---


## 4️⃣ _parse_body() – Lecture du body JSON

### Fonction utilisée pour POST et PUT :

    def _parse_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            try:
                return json.loads(raw_body)
            except json.JSONDecodeError:
                return None
        return {}



Permet :

- D’éviter la duplication de code

- De gérer les JSON invalides proprement


---

## 5️⃣ Modèle (POO)

### Chaque entité possède sa classe :

- User

- Artwork

- Méthodes typiques :

- create()

- find_by_email()

- update()

- delete()



### Le modèle :

- Interagit uniquement avec MySQL

- Ne connaît rien du HTTP


### Séparation claire :

    Modèle = Base de données
    Controller = Logique métier
    main.py = HTTP


---

## 6️⃣ Controller (logique métier)

### Exemple user_controller.py :

- Reçoit les données de la requête

- Valide les champs

- Appelle le modèle

- Retourne (response, status)


Exemple :

    return {"message": "User created"}, 201


Le controller :

- N’exécute pas de SQL directement

- N’envoie pas de headers HTTP


---


## 7️⃣ main.py – Router et flux complet

Exemple do_POST() :

    if self.path == "/api/register":
        response, status = UserController.register(body)
        return self._send_json(response, status)



### Flux complet MVC manuel :

    Client → main.py → Controller → Modèle → MySQL
            → Controller → _send_json() → Client



### Points importants :

-  do_GET, do_POST, do_PUT, do_DELETE fonctionnent de la même manière

- La barre / initiale est obligatoire

- _send_json() évite les erreurs de socket


---


## 8️⃣ CRUD des Artworks

    Méthode	Route	Action
    GET	/api/artworks	Récupérer tous les artworks
    POST	/api/artworks	Créer un artwork
    PUT	/api/artworks/{id}	Mettre à jour un artwork
    DELETE	/api/artworks/{id}	Supprimer un artwork



Notes :

- do_PUT et do_DELETE valident que l’ID est numérique → sinon 400

- do_DELETE est correctement indenté au même niveau que les autres méthodes


---

## 9️⃣ Base de données

### Défini dans database.sql :

- users

- artworks

- biography (à implémenter)

- messages (à implémenter)

- db_start.py :

Crée automatiquement la base et les tables

⚠️ Ne jamais mettre CREATE TABLE dans un modèle.
Le modèle ne fait que des opérations CRUD.


---

## 🔟 Sécurité basique

Hash des mots de passe :

    hashlib.sha256(password.encode()).hexdigest()

Aucun mot de passe en texte clair

Niveau académique correct


--- 

## 1️⃣1️⃣ Testing

⚠️ Ne pas attendre du HTML dans le navigateur.
C’est une API JSON.

Utiliser :

    curl http://localhost:8000/api/artworks
    curl -X POST http://localhost:8000/api/register \
    -d '{"username":"juan","email":"juan@example.com","password":"1234"}' \
    -H "Content-Type: application/json"



Debug utile :

    print("GET reçu :", repr(self.path))

_send_json() évite les erreurs de connexion interrompue.


---

🧠 État actuel du projet

✔ Backend sans framework
✔ MVC manuel fonctionnel
✔ _send_json() et _parse_body()
✔ CRUD complet des artworks
✔ Enregistrement / login basique
✔ Connexion MySQL modulaire
✔ db_start.py et database.sql opérationnels
✔ Tests avec Postman / curl
✔ Erreurs classiques corrigées (/, indentation, AttributeError)