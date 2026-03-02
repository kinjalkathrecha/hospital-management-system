from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    LabReportViewSet,
    DepartmentViewSet,
    MedicalRecordViewSet
)

router = DefaultRouter()
router.register('appointments', AppointmentViewSet)
router.register('lab-reports', LabReportViewSet)
router.register('departments', DepartmentViewSet)
router.register('medical-records', MedicalRecordViewSet)

urlpatterns = router.urls

