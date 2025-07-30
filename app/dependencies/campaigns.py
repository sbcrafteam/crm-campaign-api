from app.services.campaign_service import CampaignService

def get_campaign_service() -> CampaignService:
    """Provides a CampaignService instance."""
    return CampaignService()
