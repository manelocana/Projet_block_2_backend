

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from controllers.user_controller import UserController
from controllers.artwork_controller import ArtworkController
from controllers.biography_controller import BiographyController
from controllers.message_controller import MessageController



""" pour envoyer responses json """
""" pour pas repeter json.dumps et headers dans chaque endpoint """
class Response:

    def __init__(self, handler):
        """ handler = objet pour gerer des HTTP (BaseHTTPRequestHandler) """
        self.handler = handler


    def json(self, payload, status=200):
        """ Convert dict → JSON → bytes (bytes pour HTTP) """
        body = json.dumps(payload, default=str).encode("utf-8")

        """ Code HTTP (200, 404, etc.) """
        self.handler.send_response(status)

        """ Headers basics """
        self.handler.send_header("Content-Type", "application/json; charset=utf-8")

        """ pour les requetes http """
        self.handler.send_header("Content-Length", str(len(body)))

        self.handler.end_headers()

        """ write-file in body les header """
        self.handler.wfile.write(body)



""" gestioner les requetes http """
class Handler(BaseHTTPRequestHandler):

    """ lire le body de la requete (JSON) et convert a dict """
    def parse_body(self):
        length = int(self.headers.get("Content-Length", 0))

        """ si y a pas body: """
        if length == 0:
            return {}

        try:
            raw = self.rfile.read(length)   # lire bytes
            return json.loads(raw)          # bytes → dict
                                       
        except json.JSONDecodeError:
            return {}


    """ unifier le path, eviter problemes """
    def get_path(self):
        return urlparse(self.path).path
    


    """ separer la ID de la URL  (/api/users/5 → 5) """
    def get_id(self):
        try:
            path = self.get_path()
            return int(path.rstrip("/").split("/")[-1])
        except ValueError:
            return None


    """ l'utilisateur c'est admin ?  """
    def is_admin(self):
        return self.headers.get("Role") == "admin"


   
    """ post = creer-ajouter """
    def do_POST(self):
        """ res, variable pour la response """
        res = Response(self)    
        """ body, pour envoyer les données """  
        body = self.parse_body()  
        path = self.get_path()



        if path == "/api/register":
            response, status = UserController.register(body)
            return res.json(response, status)


        if path == "/api/login":
            response, status = UserController.login(body)
            return res.json(response, status)


        if path == "/api/artworks":
            if not self.is_admin():
                return res.json({"error": "user-id requis"}, 400)
            
            response, status = ArtworkController.create(body)
            return res.json(response, status)


        if path == "/api/contact":
            response, status = MessageController.create(body)
            return res.json(response, status)


        """ si y a pas des routes, montrer erreur """
        return res.json({"error": "Not found"}, 404)



    """ get = regarder-lire """
    def do_GET(self):
        res = Response(self)
        path =  self.get_path()


        if path == "/":
            return res.json({"message": "API simple sans framework, depuis scratch"})


        if path == "/api/artworks":
            response, status = ArtworkController.get_all()
            return res.json(response, status)


        if path == "/api/users":
            if not self.is_admin():
                return res.json({"error": "Non autorisé"}, 403)

            response, status = UserController.get_all_users()
            return res.json(response, status)


        if path == "/api/biography":
            if not self.headers.get("User-Id"):
                return res.json({"error": "user-id requis"}, 400)

            response, status = BiographyController.get(self.headers)
            return res.json(response, status)


        if path == "/api/messages":
            if not self.is_admin():
                return res.json({"error": "Non autorisé"}, 403)

            response, status = MessageController.get_all()
            return res.json(response, status)


        return res.json({"error": "Not found"}, 404)


    """ put = mise a jour-actualiser """
    def do_PUT(self):
        res = Response(self)
        body = self.parse_body()
        resource_id = self.get_id()
        path = self.get_path()


        if path.startswith("/api/artworks/"):
            if not resource_id:
                return res.json({"error": "ID incorrect"}, 400)

            response, status = ArtworkController.update(body, resource_id)
            return res.json(response, status)


        if path == "/api/biography":
            if not self.headers.get("User-Id"):
                return res.json({"error": "Non autorisé"}, 403)

            response, status = BiographyController.update(body, self.headers)
            return res.json(response, status)

        
        if path.startswith("/api/users/"):
            if not resource_id:
                return res.json({"error": "ID incorrect"}, 400)

            response, status = UserController.update(resource_id, body)
            return res.json(response, status)


        return res.json({"error": "Not found"}, 404)




    """ delete = supprimer-eliminer """
    def do_DELETE(self):
        res = Response(self)
        resource_id = self.get_id()
        path = self.get_path()


        if path.startswith("/api/artworks/"):
            if not resource_id:
                return res.json({"error": "ID incorrect"}, 400)

            response, status = ArtworkController.delete(resource_id)
            return res.json(response, status)

        return res.json({"error": "Not found"}, 404)



""" lancer le server """
if __name__ == "__main__":
    print("Server lancé sur http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()