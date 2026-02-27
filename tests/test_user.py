

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.user_controller import UserController



def test_register_missing_fields():
    body = {
        "email": "test@test.com"
    }
    response, status = UserController.register(body)
    assert status == 400
    assert "error" in response



def test_login_body_empty():
    response, status = UserController.login(None)
    assert status == 400



def test_login_user_not_found():
    body = {
        "email": "fake@email.com",
        "password": "1234"
    }
    response, status = UserController.login(body)
    assert status == 404