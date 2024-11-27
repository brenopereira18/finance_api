import stripe
import os
from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userPlan.models import UserPlan
import logging

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY') 

logger = logging.getLogger(__name__)


class StripeUpdatePlanWebhookViewSet(viewsets.ViewSet):
  permission_classes = [AllowAny]    

  def create(self, request, *args, **kwargs):
    payload = request.body    
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
      event = stripe.Webhook.construct_event(
        payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
      )
    except ValueError:
      return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
      return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
    
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
      user_id = payment_intent.get('metadata', {}).get('user_id')

      if user_id:
        user_plan = get_object_or_404(UserPlan, user__id=user_id)
        if user_plan.plan == 'FREE':
          user_plan.plan = 'PREMIUM'
          user_plan.save()
          logger.info(f"User {user_id} plan updated to PREMIUM")
        else:
          logger.info(f"User {user_id} already has a PREMIUM plan")

    elif event['type'] == 'customer.subscription.deleted':
      subscription = event['data']['object']
      user_id = subscription.get('metadata', {}).get('user_id')

      if user_id:
        user_plan = get_object_or_404(UserPlan, user__id=user_id)
        if user_plan.plan != 'FREE':
          user_plan.plan = 'FREE'
          user_plan.save()
          logger.info(f"User {user_id} plan reverted to FREE")
        else:
          logger.info(f"User {user_id} already has a FREE plan")

    else:
      logger.info(f"Unhandled event type: {event['type']}")

    return Response({'status': 'success'}, status=status.HTTP_200_OK)