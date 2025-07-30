import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import db
from app.models.user import User
from app.core.auth import validate_api_key, API_KEY

# Override API key dependency globally so tests don't need to provide header
app.dependency_overrides[validate_api_key] = lambda: API_KEY

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Clear and reinitialize in-memory storage before each test
    db.campaigns.clear()
    db.users.clear()
    db.users.extend([
        User(user_id=1, name="Alice", email="alice@example.com", segment_id=100),
        User(user_id=2, name="Bob", email="bob@example.com", segment_id=100),
        User(user_id=3, name="Eve", email="eve@example.com", segment_id=200),
    ])
    yield
    db.campaigns.clear()
    db.users.clear()
