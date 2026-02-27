


from models.biography import Biography




class BiographyController:

    @staticmethod
    def get():
        bio = Biography.get()
        if not bio:
            return {"message": "No biography set"}, 404
        return bio, 200



    @staticmethod
    def update(body, role):
        if role != "admin" and role != "artist":
            return {"error": "No autorizado"}, 403

        content = body.get("content")
        if not content:
            return {"error": "Content required"}, 400

        Biography.create_or_update(content)
        return {"message": "Biography updated"}, 200