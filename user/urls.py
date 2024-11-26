from rest_framework.routers import DefaultRouter
from user.viewSet import RegisterUserViewSet

router = DefaultRouter()
router.register(r'register-user', RegisterUserViewSet, basename='register-user')
urlpatterns = router.urls