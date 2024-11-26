from rest_framework.routers import DefaultRouter
from paymentPlan.viewSet import StripeWebhookViewSet

router = DefaultRouter()
router.register(r'stripe-webhook', StripeWebhookViewSet, basename='stripe-webhook')
urlpatterns = router.urls