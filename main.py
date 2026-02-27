

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from controllers.user_controller import UserController
from controllers.artwork_controller import ArtworkController
from controllers.biography_controller import BiographyController
from controllers.message_controller import MessageController



class Handler(BaseHTTPRequestHandler):

    """ estructure envoi de reponse json """
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)



    """ lecture du body json """
    def _parse_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            try:
                return json.loads(raw_body)
            except json.JSONDecodeError:
                return None
        return {}



    def _is_admin(self):
        print("HEADERS COMPLETOS:", self.headers)
        role = self.headers.get("Role")
        print("ROLE HEADER RECIBIDO:", role)
        return role == "admin"



    def do_POST(self):

        body = self._parse_body()

        if self.path == "/api/register":
            response, status = UserController.register(body)
            return self._send_json(response, status)

        if self.path == "/api/login":
            response, status = UserController.login(body)
            return self._send_json(response, status)



        if self.path == "/api/artworks":
            response, status = ArtworkController.create(body)
            return self._send_json(response, status)
        

        if self.path == "/api/contact":
            response, status = MessageController.create(body)
            return self._send_json(response, status)


        self.send_response(404)
        self.end_headers()



    def do_GET(self):

        print("GET recibido:", self.path)

        if self.path == "/":
            return self._send_json({"message": "hola soy el server a pelo"}, 200)


        if self.path.startswith("/api/artworks"):
            response, status = ArtworkController.get_all()
            return self._send_json(response, status)
        

        if self.path == "/api/users":
            role = self.headers.get("Role")
            print("ROLE HEADER RECIBIDO:", role)

            if not self._is_admin():
                return self._send_json({"error": "No autorizado"}, 403)
            response, status = UserController.get_all_users(role)
            return self._send_json(response, status)
        

        if self.path == "/api/biography":
            response, status = BiographyController.get()
            return self._send_json(response, status)
        
        if self.path == "/api/messages":
            role = self.headers.get("Role")
            response, status = MessageController.get_all(role)
            return self._send_json(response, status)


        self.send_response(404)
        self.end_headers()



    def do_PUT(self):

        body = self._parse_body()

        if self.path.startswith("/api/artworks/"):
            try:
                artwork_id = int(self.path.split("/")[-1])
            except ValueError:
                return self._send_json({"error": "ID inválido"}, 400)
            response, status = ArtworkController.update(body, artwork_id)
            return self._send_json(response, status)
        


        if self.path == "/api/biography":
            role = self.headers.get("Role")
            response, status = BiographyController.update(body, role)
            return self._send_json(response, status)


        self.send_response(404)
        self.end_headers()



    def do_DELETE(self):

        if self.path.startswith("/api/artworks/"):
            try:
                artwork_id = int(self.path.split("/")[-1])
            except ValueError:
                return self._send_json({"error": "ID inválido"}, 400)

            response, status = ArtworkController.delete(artwork_id)
            return self._send_json(response, status)

        self.send_response(404)
        self.end_headers()




if __name__ == "__main__":
    print("Servidor corriendo en http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()