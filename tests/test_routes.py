import os
import pytest
from app import app, db
from app.models import Post, User  # Import models from app.models

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

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Blog Posts' in response.data

def test_add_post(client):
    response = client.post('/add-post', data={
        'title': 'Test Title',
        'content': 'Test Content'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Title' in response.data