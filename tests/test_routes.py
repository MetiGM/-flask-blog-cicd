import os
import pytest
from app import app, db, Post, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Use environment variable for password
            user = User(username='testuser', password=os.getenv('TEST_USER_PASSWORD', 'testpass'))
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()