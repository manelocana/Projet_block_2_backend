


from controllers.user_controller import UserController




def test_login_success(monkeypatch):

    class FakeUser:
        id = 1
        username = "test"
        role = "artist"
        password = "hashed123"

        @staticmethod
        def find_by_email(email):
            return FakeUser()

        @staticmethod
        def hash_password(p):
            return "hashed123"

    monkeypatch.setattr("controllers.user_controller.User", FakeUser)

    response, status = UserController.login({
        "email": "test@mail.com",
        "password": "1234"
    })

    assert status == 200
    assert "user" in response