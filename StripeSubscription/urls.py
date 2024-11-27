from rest_framework.routers import DefaultRouter
from StripeSubscription.viewSet import StripeSubscriptionViewSet


router = DefaultRouter()
router.register(r'stripe-subscription', StripeSubscriptionViewSet, basename='stripe-subscription')
urlpatterns = router.urls