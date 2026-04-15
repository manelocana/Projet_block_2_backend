


from controllers.artwork_controller import ArtworkController


def test_create_artwork_success():
    body = {
        "user_id": "1",
        "title": "Test artwork",
        "description": "test",
        "category": "art"
    }

    response, status = ArtworkController.create(body)

    assert status == 201
    assert "message" in response



def test_get_all_artworks():
    response, status = ArtworkController.get_all()

    assert status == 200
    assert isinstance(response, list)



def test_create_artwork_missing_title():
    body = {}

    response, status = ArtworkController.create(body)

    assert status == 400




def test_update_artwork():
    # crear primero
    body = {
        "user_id": "1",
        "title": "Old",
        "description": "desc",
        "category": "art"
    }

    res, _ = ArtworkController.create(body)
    artwork_id = res["artwork"]["id"]

    # actualizar
    response, status = ArtworkController.update(
        {"title": "New"},
        artwork_id
    )

    assert status == 200
    assert response["artwork"]["title"] == "New"




def test_delete_artwork():
    body = {
        "user_id": "1",
        "title": "To delete",
        "description": "desc",
        "category": "art"
    }

    res, _ = ArtworkController.create(body)
    artwork_id = res["artwork"]["id"]

    response, status = ArtworkController.delete(artwork_id)

    assert status == 200