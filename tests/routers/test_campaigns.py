import pytest
from datetime import date
from app.main import app
from app.dependencies.campaigns import get_campaign_service
from app.models.campaign import Campaign


@pytest.fixture(autouse=True)
def patch_campaign_service(mocker):
    mock_service = mocker.Mock()
    mocker.patch(
        "app.routers.campaigns.get_campaign_service", return_value=mock_service
    )
    app.dependency_overrides[get_campaign_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.pop(get_campaign_service, None)


def test_create_campaign_success(client, patch_campaign_service):
    data = {
        "name": "Test Campaign",
        "start_date": "2025-08-01",
        "end_date": "2025-08-15",
        "segment_id": 101,
    }
    expected = Campaign(**data)
    patch_campaign_service.create_campaign.return_value = expected

    response = client.post("/campaigns", json=data)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Test Campaign"
    patch_campaign_service.create_campaign.assert_called_once()


def test_create_campaign_empty_name(client):
    response = client.post(
        "/campaigns",
        json={"name": " ", "start_date": "2025-08-01", "end_date": "2025-08-10"},
    )
    assert response.status_code == 422
    assert "Name must not be empty" in response.text


def test_create_campaign_invalid_date_range(client):
    response = client.post(
        "/campaigns",
        json={
            "name": "Range Error",
            "start_date": "2025-08-15",
            "end_date": "2025-08-01",
        },
    )
    assert response.status_code == 422
    assert "end_date must be after start_date" in response.text


def test_get_campaign_by_id_success(client, patch_campaign_service):
    campaign = Campaign(
        name="Existing",
        start_date=date(2025, 8, 1),
        end_date=date(2025, 8, 15),
        segment_id=100,
    )
    patch_campaign_service.get_campaign.return_value = campaign

    response = client.get(f"/campaigns/{campaign.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Existing"


def test_get_campaign_not_found(client, patch_campaign_service):
    patch_campaign_service.get_campaign.return_value = None
    response = client.get("/campaigns/nonexistent-id")
    assert response.status_code == 404
    assert "Campaign not found" in response.text


def test_list_campaigns(client, patch_campaign_service):
    a = Campaign(name="C1", start_date="2025-07-01", end_date="2025-07-05")
    b = Campaign(name="C2", start_date="2025-08-01", end_date="2025-08-05")
    patch_campaign_service.list_campaigns.return_value = [a, b]

    response = client.get("/campaigns")
    assert response.status_code == 200
    arr = response.json()
    assert isinstance(arr, list) and len(arr) == 2
    assert arr[0]["name"] == "C1" and arr[1]["name"] == "C2"
