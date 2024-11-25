from rest_framework.routers import DefaultRouter
from userPlan.views import UpdatePlanViewSet

router = DefaultRouter()
router.register(r'user-plan', UpdatePlanViewSet, basename='user-plan')
urlpatterns = router.urls