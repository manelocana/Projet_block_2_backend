


from controllers.artwork_controller import ArtworkController




def test_create_artwork_success(monkeypatch):

    class FakeArtwork:
        @staticmethod
        def create(user_id, title, description, category):
            return {"id": 1}

    monkeypatch.setattr("controllers.artwork_controller.Artwork", FakeArtwork)

    response, status = ArtworkController.create({
        "user_id": 1,
        "title": "Art",
        "description": "Desc",
        "category": "digital"
    })

    assert status == 201
    assert response["message"] == "Artwork created"