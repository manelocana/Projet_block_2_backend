

from models.message import Message




class MessageController:

    @classmethod
    def create(clase, body):

        if not body:
            return {"error": "Body vide"}, 400
        
        name = body.get("name")
        email = body.get("email")
        content = body.get("message")

        if not name or not email or not content:
            return {"error": "il manque un parametre a remplir"}, 400

        try:
            message = Message.create(name, email, content)

            return {
                "message": "message envoi ok",
                "data": message.to_dict()
            }, 201
        
        except Exception as e:
            return {"error": str(e)}, 500




    @classmethod
    def get_all(clase):

        try:
            messages = Message.get_all()

            data = [msg.to_dict() for msg in messages]

            return data, 200
        
        except Exception as e:
            return {"error": str(e)}, 500