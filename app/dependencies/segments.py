from app.services.segment_service import SegmentService

def get_segment_service() -> SegmentService:
    """Provides a SegmentService instance."""
    return SegmentService()
