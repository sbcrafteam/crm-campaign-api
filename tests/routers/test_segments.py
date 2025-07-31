import pytest
from app.main import app
from app.dependencies.segments import get_segment_service
from app.models.user import User


@pytest.fixture(autouse=True)
def patch_segment_service(mocker):
    mock_service = mocker.Mock()
    mocker.patch("app.routers.segments.get_segment_service", return_value=mock_service)
    app.dependency_overrides[get_segment_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.pop(get_segment_service, None)


def test_get_users_by_segment_success(client, patch_segment_service):
    mock_users = [
        User(user_id=1, name="Alice", email="alice@example.com", segment_id=101),
        User(user_id=2, name="Bob", email="bob@example.com", segment_id=101),
    ]
    patch_segment_service.get_users_by_segment.return_value = mock_users

    response = client.get("/segments/101/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(user["segment_id"] == 101 for user in data)


def test_get_users_by_segment_not_found(client, patch_segment_service):
    patch_segment_service.get_users_by_segment.return_value = []

    response = client.get("/segments/999/users")
    assert response.status_code == 404

    error = response.json()
    assert error["code"] == 404
    assert error["message"] == "HTTP Error"
    assert "Segment ID 999 returned no results" in error["detail"]
