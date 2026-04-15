

from controllers.biography_controller import BiographyController



def test_update_biography():
    headers = {
        "User-Id": "1",
        "Role": "artist"
    }

    body = {
        "content": "My bio"
    }

    response, status = BiographyController.update(body, headers)

    assert status == 200
    assert "biography" in response