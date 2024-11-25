from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from userPlan.models import UserPlan

@receiver(post_save, sender=User)
def create_user_plan(sender, instance, created, **kwargs):
  if created:
    UserPlan.objects.create(user=instance)