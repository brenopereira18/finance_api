from django.db import models
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth.models import User

PLAN_CHOICES = [
  ('FREE', _('gratuito')),
  ('PREMIUM', _('premium')),
]

class UserPlan(models.models):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_plan')
  plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='FREE')

  def month_transaction_limit(self):
    return 10 if self.plan == 'FREE' else float('inf')