from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, BedViewSet,
    AdmissionViewSet, BillViewSet,
    PaymentViewSet, StaffViewSet,
    StaffAssignmentViewSet
)

router = DefaultRouter()

router.register('rooms', RoomViewSet)
router.register('beds', BedViewSet)
router.register('admissions', AdmissionViewSet)
router.register('bills', BillViewSet)
router.register('payments', PaymentViewSet)
router.register('staff', StaffViewSet)
router.register('staff-assignments', StaffAssignmentViewSet)

urlpatterns = router.urls