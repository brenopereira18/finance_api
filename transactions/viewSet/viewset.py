from datetime import datetime
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from .metrics import (calculate_amount_and_percentage, validate_transactions)
from rest_framework.permissions import IsAuthenticated


class TransactionViewSet(viewsets.ModelViewSet):  
  serializer_class = TransactionSerializer 
  permission_classes = [IsAuthenticated] 

  def get_queryset(self):
    return Transaction.objects.filter(user=self.request.user)
  
  def perform_create(self, serializer):
    """ Garante que o usuário autenticado seja atribuído na transação. """
    serializer.save(user=self.request.user)
  
  def process_calculate(self, group_by_field, month=None, year=None, filter_by_type=None):
    """ Pega o mês e ano atual se não for passado. """
    if not month or not year:
      current_date = datetime.now()
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
        
    return Response(result)
    
  @action(detail=False, methods=['get'])
  def transaction_by_type(self, request, *args, **kwargs):
    """ Recupera mês e ano da query. """ 
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)

    return self.process_calculate('type', month, year)    
  
  @action(detail=False, methods=['get'])
  def transaction_by_category(self, request, *args, **kwargs):    
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)

    return self.process_calculate('category', month, year, filter_by_type='EXPENSE')
  
  @action(detail=False, methods=['get'])
  def last_transactions(self, request, *args, **kwargs):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)

    if not month or not year:
      current_date = datetime.now()
      month = current_date.month
      year = current_date.year

    last_transactions = get_transactions_for_month(month, year)
    response_last_transactions = last_transactions.order_by('-updatedAt')[:10]
    
    serializer = self.get_serializer(response_last_transactions, many=True)

    return Response(serializer.data)
        
    