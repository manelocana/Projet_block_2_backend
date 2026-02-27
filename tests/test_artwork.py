

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.artwork_controller import ArtworkController




def test_create_without_title():
    body = {
        "description": "desc",
        "category": "painting"
    }

    response, status = ArtworkController.create(body)

    assert status == 400