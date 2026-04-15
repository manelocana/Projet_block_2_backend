

import time
from controllers.user_controller import UserController


""" verifier que email c'est unique """
def unique_email():
    return f"test_{int(time.time() * 1000)}@test.com"



""" register """
def test_register_success():
    body = {
        "username": "testuser",
        "email": unique_email(),
        "password": "1234"
    }

    response, status = UserController.register(body)

    assert status == 201
    assert "user" in response
    assert response["user"]["email"] == body["email"]



def test_register_missing_fields():
    body = {
        "email": unique_email()
    }

    response, status = UserController.register(body)

    assert status == 400
    assert "error" in response


def test_register_duplicate_email():
    email = unique_email()

    body = {
        "username": "test",
        "email": email,
        "password": "1234"
    }

    UserController.register(body)
    response, status = UserController.register(body)

    assert status == 400


""" login """
def test_login_success():
    email = unique_email()

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
    assert "user" in response



def test_login_wrong_password():
    email = unique_email()

    UserController.register({
        "username": "test",
        "email": email,
        "password": "1234"
    })

    response, status = UserController.login({
        "email": email,
        "password": "wrong"
    })

    assert status == 401



def test_login_user_not_found():
    response, status = UserController.login({
        "email": unique_email(),
        "password": "1234"
    })

    assert status == 404



""" update """
def test_update_user():
    email = unique_email()

    res, _ = UserController.register({
        "username": "old",
        "email": email,
        "password": "1234"
    })

    user_id = res["user"]["id"]

    new_email = unique_email()

    response, status = UserController.update(user_id, {
        "username": "newname",
        "email": new_email,
        "password": "9999"
    })

    assert status == 200
    assert response["user"]["username"] == "newname"
    assert response["user"]["email"] == new_email