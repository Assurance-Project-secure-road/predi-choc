from operator import index
from pandas.core.frame import DataFrame
from pandas._testing import assert_frame_equal
from app.helpers import (
    format_data_caracteristiques,
    format_data_lieux,
    format_data_usagers,
    format_data_vehicules,
)
import pytest
import pandas as pd
from app import create_app
from app.db import db
from app.models import (
    Caracteristique,
    Lieux,
    Usager,
    User,
    UserRole,
    Vehicule,
)


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,
            "SERVER_NAME": "exemple.com",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": "test",
        }
    )
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    db.create_all()
    yield client


def test_db_schema(client):
    """Check if tables have successfully been added to the db"""
    table_names = [
        "Caracteristique",
        "Vehicule",
        "Usager",
        "Lieux",
        "user",
        "user_role",
    ]
    with db.engine.connect() as connexion:
        for table_name in table_names:
            assert db.engine.dialect.has_table(connexion, table_name) == True
