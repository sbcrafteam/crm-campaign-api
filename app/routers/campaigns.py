from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.campaign import Campaign
from app.models.error import ErrorResponse
from app.services.campaign_service import CampaignService
from app.dependencies.campaigns import get_campaign_service

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("", response_model=Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: Campaign, service: CampaignService = Depends(get_campaign_service)
) -> Campaign:
    """
    Create a new campaign.

    Args:
        campaign (Campaign): The campaign data to create.
        service (CampaignService): The injected campaign service.

    Returns:
        Campaign: The created campaign object.
    """
    try:
        return service.create_campaign(campaign)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                code=400, message="Validation error", detail=str(e)
            ).model_dump(),
        )


@router.get("", response_model=List[Campaign])
def list_campaigns(
    service: CampaignService = Depends(get_campaign_service),
) -> List[Campaign]:
    """
    List all campaigns.

    Args:
        service (CampaignService): The injected campaign service.

    Returns:
        List[Campaign]: All stored campaigns.
    """
    return service.list_campaigns()


@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(
    campaign_id: str, service: CampaignService = Depends(get_campaign_service)
) -> Campaign:
    """
    Retrieve a campaign by its ID.

    Args:
        campaign_id (int): ID of the campaign to retrieve.
        service (CampaignService): The injected campaign service.

    Returns:
        Campaign: The campaign object if found.
    """
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                code=404,
                message="Campaign not found",
                detail=f"No campaign with ID {campaign_id}",
            ).model_dump(),
        )
    return campaign
