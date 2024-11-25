from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from .metrics import (calculate_amount_and_percentage, validate_transactions)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class TransactionViewSet(viewsets.ModelViewSet):  
  serializer_class = TransactionSerializer 
  permission_classes = [IsAuthenticated] 

  def get_queryset(self):
    return Transaction.objects.filter(user=self.request.user)
  
  def perform_create(self, serializer):
    user = self.request.user
    user_plan = user.user_plan

    if user_plan.plan == 'FREE':
      current_month = now().month
      current_year = now().year

      transactions_count = Transaction.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year
      ).count()

      if transactions_count >= user_plan.month_transaction_limit():
        raise ValidationError("Você atingiu o limite mensal de transações do plano gratuito.")  

    """ Garante que o usuário autenticado seja atribuído na transação. """
    serializer.save(user=user)
  
  def process_calculate(self, group_by_field, month=None, year=None, filter_by_type=None):
    """ Pega o mês e ano atual se não for passado. """
    if not month or not year:
      current_date = now()
      month = current_date.month
      year = current_date.year
      
    """ Obtem as transações para o mês e ano específico. """ 
    transactions_for_month = self.get_queryset().filter(date__month=month, date__year=year)

    """ Filtra por transações do tipo EXPENSE. """
    if filter_by_type:
      transactions_for_month = transactions_for_month.filter(type=filter_by_type)
        
    """ Valida as transações. """ 
    is_valid, total_transaction_amount = validate_transactions(transactions_for_month)
        
    if not is_valid:
      return Response(
        {'error': 'No transactions or total amount is zero for this month.'},
        status=400
      )
        
    """ Calcula o total e as porcentagens de trasações. """ 
    result = calculate_amount_and_percentage(transactions_for_month, total_transaction_amount, group_by_field)
        
    return result
    
  @action(detail=False, methods=['get'])
  def transaction_by_type(self, request, *args, **kwargs):
    """ Recupera mês e ano da query. """ 
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)

    transactions = self.process_calculate('type', month, year) 
    current_balance = transactions["DEPOSIT"]["total"] - transactions["EXPENSE"]["total"] - transactions["INVESTMENT"]["total"] 

    result = {
      "current_balance": current_balance,
      "transactions": transactions,
    }
    return Response(result)  
  
  @action(detail=False, methods=['get'])
  def transaction_by_category(self, request, *args, **kwargs):    
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    
    return Response(self.process_calculate('category', month, year, filter_by_type='EXPENSE'))
  
  @action(detail=False, methods=['get'])
  def last_transactions(self, request, *args, **kwargs):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)

    if not month or not year:
      current_date = datetime.now()
      month = current_date.month
      year = current_date.year

    last_transactions = self.get_queryset().filter(date__month=month, date__year=year)
    response_last_transactions = last_transactions.order_by('-updatedAt')[:10]
    
    serializer = self.get_serializer(response_last_transactions, many=True)

    return Response(serializer.data) 
  
    
        
    