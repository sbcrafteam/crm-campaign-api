from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.user import User
from app.models.error import ErrorResponse
from app.services.segment_service import SegmentService
from app.dependencies.segments import get_segment_service

router = APIRouter(prefix="/segments", tags=["Segments"])


@router.get("/{segment_id}/users", response_model=List[User])
def get_users_by_segment(
    segment_id: int, service: SegmentService = Depends(get_segment_service)
) -> List[User]:
    """
    Retrieve all users for a specific segment.

    Args:
        segment_id (int): ID of the segment.
        service (SegmentService): The injected segment service.

    Returns:
        List[User]: List of users belonging to the segment.
    """
    users = service.get_users_by_segment(segment_id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                code=404,
                message="No users found for segment",
                detail=f"Segment ID {segment_id} returned no results",
            ).model_dump(),
        )
    return users
