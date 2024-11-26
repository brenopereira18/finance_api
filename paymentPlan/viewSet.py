import stripe
import os
from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userPlan.models import UserPlan

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY') 


class StripeWebhookViewSet(viewsets.ViewSet):   

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

    return Response({'status': 'success'}, status=status.HTTP_200_OK)