from rest_framework.routers import DefaultRouter
from user.viewSet import RegisterUserViewSet

router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='user')
urlpatterns = router.urls