

from models.biography import Biography



class BiographyController:

    @classmethod
    def get(clase, headers):

        user_id = headers.get("User-Id")

        if not user_id:
            return {"error": "user id non autorisé"}, 400

        """ instance del object """
        bio = Biography.get_by_user_id(user_id)

        if not bio:
            return {"message": "Y a pas biography"}, 404

        """ return un dict-json """
        return bio.to_dict(), 200




    @classmethod
    def update(clase, body, headers):

        role = headers.get("Role")
        user_id = headers.get("User-Id")

        if role not in ["admin", "artist"]:
            return {"error": "Non autorisé"}, 403

        if not user_id:
            return {"error": "User ID non valide"}, 400

        content = body.get("content")

        if not content:
            return {"error": "Content required"}, 400

        """ voir si dejà existe """
        bio = Biography.get_by_user_id(user_id)

        if not bio:
            bio = Biography(None, user_id, content)
        else:
            bio.content = content

        bio.save()

        return {
            "message": "Biography mise a jour",
            "biography": bio.to_dict()
        }, 200