

from models.artwork import Artwork


""" les controller c'est la conexion des models avec http """
class ArtworkController:

    @classmethod
    def get_all(clase):
        artworks = Artwork.get_all()

        """ convert object a dict """
        data = [artwork.to_dict() for artwork in artworks]

        return data, 200



    @classmethod
    def create(clase, body):

        user_id = body.get("user_id")
        title = body.get("title")
        description = body.get("description")
        category = body.get("category")

        if not title:
            return {"error": "Title required"}, 400

        if not user_id:
            return {"error": "user_id required"}, 400

        """ object artwork """
        artwork = Artwork.create(user_id, title, description, category)

        return {
            "message": "Artwork crée",
            "artwork": artwork.to_dict()
        }, 201



    @classmethod
    def update(clase, body, artwork_id):

        artwork = Artwork.get_by_id(artwork_id)

        if not artwork:
            return {"error": "Artwork non disponible"}, 404

        title = body.get("title", artwork.title)
        description = body.get("description", artwork.description)
        category = body.get("category", artwork.category)

        artwork.update(title, description, category)

        return {
            "message": "Artwork mise ajour",
            "artwork": artwork.to_dict()
        }, 200



    @classmethod
    def delete(clase, artwork_id):

        artwork = Artwork.get_by_id(artwork_id)

        if not artwork:
            return {"error": "Artwork non disponible"}, 404

        artwork.delete()

        return {"message": "Artwork supprimé"}, 200