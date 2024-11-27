import stripe
import os
from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userPlan.models import UserPlan
import logging

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

logger = logging.getLogger(__name__)


class StripeSubscriptionViewSet(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  """ Retorna  a url para pagamento da assinatura. """
  def create(self, request, *args, **kwargs):
    user = request.user
    user_plan = get_object_or_404(UserPlan, user=user)

    if user_plan.plan == 'PREMIUM':
      return Response(
        {"detail": "O usuário já possui um plano PREMIUM."},
        status=status.HTTP_400_BAD_REQUEST,
      )

    try:
      price_id = os.getenv('STRIPE_PREMIUM_PLAN_PRICE_ID')

      """ Cria sessão de pagamento no Stripe. """
      checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
          'price': price_id,
          'quantity': 1,
        }],
        metadata={'user_id': user.id},
      )
      logger.info(f"Stripe checkout session created for user {user.id}")
      return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)
    except Exception as e:
      logger.error(f"Error creating Stripe checkout session: {str(e)}")
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)