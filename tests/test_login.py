


from controllers.user_controller import UserController
import time


def test_login_flow():
    email = f"test_{int(time.time()*1000)}@test.com"

    UserController.register({
        "username": "test",
        "email": email,
        "password": "1234"
    })

    response, status = UserController.login({
        "email": email,
        "password": "1234"
    })

    assert status == 200