import pytest
from app.models.campaign import Campaign
from datetime import date

@pytest.fixture(autouse=True)
def patch_campaign_service(mocker):
    mock_service = mocker.Mock()
    mocker.patch("app.dependencies.campaigns.get_campaign_service", return_value=mock_service)
    return mock_service

def test_create_campaign_success(client, patch_campaign_service):
    campaign_data = {
        "name": "Test",
        "start_date": "2025-08-01",
        "end_date": "2025-08-15",
        "segment_id": 101
    }
    mock_campaign = Campaign(**campaign_data)
    patch_campaign_service.create_campaign.return_value = mock_campaign

    response = client.post("/campaigns", json=campaign_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
    patch_campaign_service.create_campaign.assert_called_once()

def test_create_campaign_empty_name(client):
    response = client.post("/campaigns", json={
        "name": " ",
        "start_date": "2025-08-01",
        "end_date": "2025-08-10"
    })
    assert response.status_code == 400
    assert "Name must not be empty" in response.text

def test_create_campaign_invalid_date_range(client):
    response = client.post("/campaigns", json={
        "name": "Test Campaign",
        "start_date": "2025-08-15",
        "end_date": "2025-08-01"
    })
    assert response.status_code == 400
    assert "end_date must be after start_date" in response.text

def test_get_campaign_by_id_success(client, patch_campaign_service):
    campaign = Campaign(
        name="Existing Campaign",
        start_date=date(2025, 8, 1),
        end_date=date(2025, 8, 15),
        segment_id=101
    )
    patch_campaign_service.get_campaign.return_value = campaign

    response = client.get(f"/campaigns/{campaign.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Existing Campaign"

def test_get_campaign_not_found(client, patch_campaign_service):
    patch_campaign_service.get_campaign.return_value = None

    response = client.get("/campaigns/nonexistent-id")
    assert response.status_code == 404
    assert "Campaign not found" in response.text

def test_list_campaigns(client, patch_campaign_service):
    campaigns = [
        Campaign(
            name="Campagne 1",
            start_date="2025-07-01",
            end_date="2025-07-10",
            segment_id=101
        ),
        Campaign(
            name="Campagne 2",
            start_date="2025-08-01",
            end_date="2025-08-15",
            segment_id=102
        ),
    ]
    patch_campaign_service.list_campaigns.return_value = campaigns

    response = client.get("/campaigns")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Campagne 1"
    assert data[1]["segment_id"] == 102
