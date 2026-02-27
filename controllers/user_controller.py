


import json
from models.user import User
import hashlib




class UserController:

    @staticmethod
    def register(request_handler):
        length = int(request_handler.headers.get("Content-Length", 0))
        raw = request_handler.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "Missing fields"}, 400

        if User.find_by_email(email):
            return {"error": "Email already exists"}, 400

        user_id = User.create(username, email, password)

        return {"message": "User created", "user_id": user_id}, 201



    @staticmethod
    def login(body):

        if not body:
            return {"error": "Body vacío"}, 400

        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return {"error": "Faltan datos"}, 400

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = User.find_by_email(email)

        if not user:
            return {"error": "Usuario no encontrado"}, 404

        if user.password != hashed_password:
            return {"error": "Contraseña incorrecta"}, 401

        return {
            "message": "Login correcto",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }, 200
    


    @staticmethod
    def get_all_users(role):

        if role != "admin":
            return {"error": "No autorizado"}, 403

        users = User.get_all_users()
        return users, 200
    


    @staticmethod
    def update(user_id, body):

        if not body:
            return {"error": "Body vacío"}, 400

        username = body.get("username")
        email = body.get("email")

        if not username or not email:
            return {"error": "Faltan datos"}, 400

        User.update_user(user_id, username, email)

        return {"message": "User updated"}, 200