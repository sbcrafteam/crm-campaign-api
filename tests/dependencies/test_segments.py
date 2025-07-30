from app.dependencies.segments import get_segment_service
from app.services.segment_service import SegmentService

def test_get_segment_service_instance():
    service = get_segment_service()
    assert isinstance(service, SegmentService)
