


from models.artwork import Artwork





class ArtworkController:

    @staticmethod
    def get_all():
        artworks = Artwork.get_all()
        return artworks, 200



    @staticmethod
    def create(body):

        title = body.get("title")
        description = body.get("description")
        category = body.get("category")

        if not title:
            return {"error": "Title required"}, 400

        new_id = Artwork.create(title, description, category)

        return {"message": "Artwork created", "id": new_id}, 201



    @staticmethod
    def update(body, artwork_id):

        title = body.get("title")
        description = body.get("description")
        category = body.get("category")

        Artwork.update(artwork_id, title, description, category)

        return {"message": "Artwork updated"}, 200



    @staticmethod
    def delete(artwork_id):

        Artwork.delete(artwork_id)
        return {"message": "Artwork deleted"}, 200