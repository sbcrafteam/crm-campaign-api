import pytest
from app.services.segment_service import SegmentService
from app.models.user import User

@pytest.fixture
def segment_service():
    return SegmentService()

def test_get_users_by_segment_found(mocker, segment_service):
    mock_users = [
        User(user_id=1, name="Alice", email="alice@example.com", segment_id=100),
        User(user_id=2, name="Bob", email="bob@example.com", segment_id=100),
        User(user_id=3, name="Eve", email="eve@example.com", segment_id=200),
    ]
    mocker.patch("app.storage.db.users", mock_users)

    users_100 = segment_service.get_users_by_segment(100)
    assert len(users_100) == 2
    assert all(u.segment_id == 100 for u in users_100)

def test_get_users_by_segment_empty(mocker, segment_service):
    mocker.patch("app.storage.db.users", [])

    users = segment_service.get_users_by_segment(999)
    assert users == []
