from rest_framework.routers import DefaultRouter
from StripeUpdatePlan.viewSet import StripeUpdatePlanWebhookViewSet

router = DefaultRouter()
router.register(r'stripe-update-plan-webhook', StripeUpdatePlanWebhookViewSet, basename='stripe-update-plan-webhook')
urlpatterns = router.urls