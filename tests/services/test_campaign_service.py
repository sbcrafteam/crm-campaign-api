import pytest
from app.services.campaign_service import CampaignService
from app.models.campaign import Campaign

@pytest.fixture
def campaign_service():
    return CampaignService()

def test_create_campaign(mocker, campaign_service):
    mock_campaigns = []
    mocker.patch("app.storage.db.campaigns", mock_campaigns)

    campaign = Campaign(
        name="Test Campaign",
        start_date="2025-07-01",
        end_date="2025-07-10"
    )
    result = campaign_service.create_campaign(campaign)

    assert result == campaign
    assert len(mock_campaigns) == 1
    assert mock_campaigns[0] == campaign

def test_list_campaigns(mocker, campaign_service):
    mock_campaigns = [
        Campaign(name="C1", start_date="2025-07-01", end_date="2025-07-05"),
        Campaign(name="C2", start_date="2025-07-10", end_date="2025-07-15"),
    ]
    mocker.patch("app.storage.db.campaigns", mock_campaigns)

    campaigns = campaign_service.list_campaigns()

    assert campaigns == mock_campaigns

def test_get_campaign_found(mocker, campaign_service):
    c1 = Campaign(name="FindMe", start_date="2025-08-01", end_date="2025-08-10")
    mock_campaigns = [c1]
    mocker.patch("app.storage.db.campaigns", mock_campaigns)

    found = campaign_service.get_campaign(c1.id)

    assert found == c1

def test_get_campaign_not_found(mocker, campaign_service):
    mocker.patch("app.storage.db.campaigns", [])

    found = campaign_service.get_campaign("non-existent-id")

    assert found is None
