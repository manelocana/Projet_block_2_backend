


from models.message import Message





class MessageController:

    @staticmethod
    def create(body):
        if not body:
            return {"error": "Body vacío"}, 400

        name = body.get("name")
        email = body.get("email")
        message = body.get("message")

        if not name or not email or not message:
            return {"error": "Campos obligatorios"}, 400

        Message.create(name, email, message)

        return {"message": "Mensaje enviado correctamente"}, 201



    @staticmethod
    def get_all(role):
        if role != "admin":
            return {"error": "No autorizado"}, 403

        messages = Message.get_all()
        return messages, 200