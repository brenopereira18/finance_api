from rest_framework import viewsets
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.db import transaction
from userPlan.models import UserPlan


class RegisterUserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()  
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

  def perform_create(self, serializer):    
    serializer.save()

        