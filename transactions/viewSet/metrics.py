from django.db.models import Sum, DecimalField, F, ExpressionWrapper
    
def validate_transactions(transactions):
  """Verifica se há transações e se o total não é zero."""
  total_transaction_amount = transactions.aggregate(total=Sum('amount'))['total']
  if not total_transaction_amount or total_transaction_amount == 0:
    return False, None
  return True, total_transaction_amount
    
def calculate_amount_and_percentage(transactions, total_transaction_amount, group_by_field):
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

