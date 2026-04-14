

from models.artwork import Artwork


""" les controller c'est la conexion des models avec http """
class ArtworkController:

    @classmethod
    def get_all(cls):
        try:
            artworks = Artwork.get_all()
            """ convert object a dict """
            return [artwork.to_dict() for artwork in artworks], 200
        
        except Exception as e:
            return {"error": f"error {str(e)}"}, 500


    @classmethod
    def create(cls, body):

        user_id = body.get("user_id")
        title = body.get("title")
        description = body.get("description")
        category = body.get("category")

        if not user_id:
            return {"error": "user_id requis"}, 400
        
        if not title:
            return {"error": "Title required"}, 400

        try:
            """ object artwork """
            artwork = Artwork.create(user_id, title, description, category)
            return {"message": "Artwork crée", "artwork": artwork.to_dict()}, 201
        
        except Exception as e:
            return {"error": f"error {str(e)}"}



    @classmethod
    def update(cls, body, artwork_id):

        try:
            artwork = Artwork.get_by_id(artwork_id)
        except Exception as e:
            return {"error": f"error {str(e)}"}, 500

        if not artwork:
            return {"error": "Artwork non disponible"}, 404

        """ si on actualise pas, reste le parametre actuel """
        title = body.get("title", artwork.title)
        description = body.get("description", artwork.description)
        category = body.get("category", artwork.category)

        try:
            artwork.update(title, description, category)
            return {"message": "Artwork mise ajour", "artwork": artwork.to_dict()}, 200
        
        except Exception as e:
            return {"error": f"error {str(e)}"}, 500



    @classmethod
    def delete(cls, artwork_id):

        try:
            artwork = Artwork.get_by_id(artwork_id)

        except Exception as e:
            return {"error":f"error {str(e)}"}, 500
        

        if not artwork:
            return {"error": "Artwork non disponible"}, 404

        try:
            artwork.delete()
            return {"message": "Artwork supprimé"}, 200
        
        except Exception as e:
            return {"error": f"error {str(e)}"}, 500