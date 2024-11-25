from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError


class UpdatePlanViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]

  @action(detail=False, methods=['patch'])
  def update_plan(self, request, *args, **kwargs):
    user_plan = request.user.user_plan
    new_plan = request.data.get('plan')

    if new_plan not in ['FREE', 'PREMIUM']:  
      raise ValidationError({"error": "Plano inválido."})

    user_plan.plan = new_plan
    user_plan.save()

    return Response({"menssage": f"Plano atualizado para {new_plan}"})

