

from controllers.user_controller import UserController



def test_register_success(monkeypatch):

    """ faux user pour pas toucher la db reel """
    class FakeUser:
        @staticmethod
        def find_by_email(email):
            return None

        @staticmethod
        def create(username, email, password):
            return 1

    monkeypatch.setattr("controllers.user_controller.User", FakeUser)

    response, status = UserController.register({
        "username": "test",
        "email": "test@mail.com",
        "password": "1234"
    })

    assert status == 201
    assert response["message"] == "User created"