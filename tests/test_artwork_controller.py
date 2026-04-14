


from controllers.artwork_controller import ArtworkController


def test_create_artwork_success():
    body = {
        "title": "Test artwork"
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