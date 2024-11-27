from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('finance_api/(?P<version>(v1|v2))/', include('transactions.urls')),
    re_path('finance_api/(?P<version>(v1|v2))/', include('StripeUpdatePlan.urls')),
    re_path('finance_api/(?P<version>(v1|v2))/', include('StripeSubscription.urls')),
    re_path('finance_api/(?P<version>(v1|v2))/', include('user.urls')),
    re_path('finance_api/(?P<version>(v1|v2))/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('finance_api/(?P<version>(v1|v2))/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
