from app.models.campaign import Campaign
from app.storage.db import campaigns


class CampaignService:
    """
    Service responsible for managing campaign operations.
    """

    def create_campaign(self, campaign: Campaign) -> Campaign:
        """
        Create and store a new campaign.

        Args:
            campaign (Campaign): The campaign data without ID.

        Returns:
            Campaign: The stored campaign with generated ID.
        """
        campaigns.append(campaign)
        return campaign

    def list_campaigns(self) -> list[Campaign]:
        """
        Retrieve all stored campaigns.

        Returns:
            list[Campaign]: List of all campaigns.
        """
        return campaigns

    def get_campaign(self, campaign_id: str) -> Campaign | None:
        """
        Retrieve a specific campaign by its ID.

        Args:
            campaign_id (str): Unique identifier of the campaign.

        Returns:
            Campaign | None: The campaign if found, otherwise None.
        """
        return next((c for c in campaigns if c.id == campaign_id), None)
