from app.dependencies.campaigns import get_campaign_service
from app.services.campaign_service import CampaignService

def test_get_campaign_service_instance():
    service = get_campaign_service()
    assert isinstance(service, CampaignService)
