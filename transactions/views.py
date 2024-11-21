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
    
  def calculate_percentage(self, transactions, total_transaction_amount):
    """Calcula a porcentagem por tipo de transação."""
    transaction_data = (
      transactions.values('type')  
      .annotate(type_total=Sum('amount'))  
      .annotate(
        percentage=ExpressionWrapper(
          F('type_total') * 100.0 / total_transaction_amount,
          output_field=DecimalField()
        )
      )
    )
        
    result = {
      item['type']: {
        'total': item['type_total'],
        'percentage': round(item['percentage'], 2)  
      }
      for item in transaction_data
    }
        
    return result
    
  @action(detail=False, methods=['get'])
  def amount_and_percentage_by_type(self, request, *args, **kwargs):
    # Recupera mês e ano da query ou o mês e ano atual, se não for passado.
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
        
    if not month or not year:
      current_date = datetime.now()
      month = current_date.month
      year = current_date.year
      
    # Obtem as transações para o mês e ano específico.
    transactions_for_month = self.get_transactions_for_month(month, year)
        
    # Valida as transações.
    is_valid, total_transaction_amount = self.validate_transactions(transactions_for_month)
        
    if not is_valid:
      return Response(
        {'error': 'No transactions or total amount is zero for this month.'},
        status=400
      )
        
    # Calcula as porcentagens de trasações por tipo
    result = self.calculate_percentage(transactions_for_month, total_transaction_amount)
        
    return Response(result)
    