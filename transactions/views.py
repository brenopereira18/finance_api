from datetime import datetime
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from django.db.models import Sum, DecimalField, F, ExpressionWrapper


class TransactionViewSet(viewsets.ModelViewSet):
  queryset = Transaction.objects.all()
  serializer_class = TransactionSerializer  

  def get_transactions_for_month(self, month, year):
    """Filtra as transações para o mês e ano passado."""
    return self.queryset.filter(date__month=month, date__year=year)
    
  def validate_transactions(self, transactions):
    """Verifica se há transações e se o total não é zero."""
    total_transaction_amount = transactions.aggregate(total=Sum('amount'))['total']
    if not total_transaction_amount or total_transaction_amount == 0:
      return False, None
    return True, total_transaction_amount
    
  def calculate_amount_and_percentage(self, transactions, total_transaction_amount, group_by_field):
    """Calcula o total e a porcentagem por tipo de transação."""
    transaction_data = (
      transactions.values(group_by_field)  
      .annotate(type_total=Sum('amount'))  
      .annotate(
        percentage=ExpressionWrapper(
          F('type_total') * 100.0 / total_transaction_amount,
          output_field=DecimalField()
        )
      )
    )
        
    result = {
      item[group_by_field]: {
        'total': item['type_total'],
        'percentage': round(item['percentage'], 2)  
      }
      for item in transaction_data
    }
        
    return result
  
  def process_calculate(self, group_by_field, month=None, year=None, filter_by_type=None):
    """ Pega o mês e ano atual se não for passado. """
    if not month or not year:
      current_date = datetime.now()
      month = current_date.month
      year = current_date.year
      
    """ Obtem as transações para o mês e ano específico. """ 
    transactions_for_month = self.get_transactions_for_month(month, year)

    """ Filtra por transações do tipo EXPENSE. """
    if filter_by_type:
      transactions_for_month = transactions_for_month.filter(type=filter_by_type)
        
    """ Valida as transações. """ 
    is_valid, total_transaction_amount = self.validate_transactions(transactions_for_month)
        
    if not is_valid:
      return Response(
        {'error': 'No transactions or total amount is zero for this month.'},
        status=400
      )
        
    """ Calcula o total e as porcentagens de trasações. """ 
    result = self.calculate_amount_and_percentage(transactions_for_month, total_transaction_amount, group_by_field)
        
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
        
    