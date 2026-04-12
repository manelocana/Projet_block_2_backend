


from controllers.biography_controller import BiographyController




def test_biography_missing_user():
    response, status = BiographyController.get({})

    assert status == 400