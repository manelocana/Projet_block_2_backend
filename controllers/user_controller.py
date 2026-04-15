


from models.user import User




class UserController:

    @classmethod
    def register(clase, body):

        if not body:
            return {"error": "body vide"}, 400

        
        username = body.get("username")
        email = body.get("email")
        password = body.get("password")

        if not username or not email or not password:
            return {"error": "manque des parametres"}, 400

        if User.find_by_email(email):
            return {"error": "email déjà enregistré"}, 400

        try:
            """ instancier object user """
            user = User.create(username, email, password)

            return {
                "message": "User enregistré",
                "user": user.to_dict()
            }, 201
        
        except Exception as e:
            return {"error": str(e)}, 500




    @classmethod
    def login(clase, body):

        if not body:
            return {"error": "Body vide"}, 400

        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return {"error": "non autorisé"}, 400

        user = User.find_by_email(email)

        if not user:
            return {"error": "non autorisé"}, 404

        hashed_password = User.hash_password(password)

        if user.password != hashed_password:
            return {"error": "non autorisé"}, 401

        try:
            return {
                "message": "Login correct",
                "user": user.to_dict()
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500



    @classmethod
    def get_all_users(clase):

        try:
            users = User.get_all()

            """ convert object data a dict-json """
            data = [user.to_dict() for user in users]

            return data, 200
        
        except Exception as e:
            return {"error": str(e)}, 500



    @classmethod
    def update(clase, user_id, body):

        if not body:
            return {"error": "Body vide"}, 400

        user = User.find_by_id(user_id)

        if not user:
            return {"error": "User not found"}, 404

        username = body.get("username")
        email = body.get("email")
        password = body.get("password")

        if not username or not email:
            return {"error": "remplir username o email"}, 400

        try:
            user.update(username, email, password)

            return {
                "message": "utilisateur mise a jour",
                "user": user.to_dict()
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500