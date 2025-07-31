from app.storage.db import users
from app.models.user import User


class SegmentService:
    """
    Service responsible for segment operations.
    """

    def get_users_by_segment(self, segment_id: int) -> list[User]:
        """
        Get users that belong to the specified segment.

        Args:
            segment_id (int): The segment ID to filter users by.

        Returns:
            list[User]: List of users in the specified segment.
        """
        return [u for u in users if u.segment_id == segment_id]
