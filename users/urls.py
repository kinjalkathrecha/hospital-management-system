from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorViewSet, PatientViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('doctors', DoctorViewSet)
router.register('patients', PatientViewSet)

urlpatterns = router.urls