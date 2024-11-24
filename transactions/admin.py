from django.contrib import admin
from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'name', 'type', 'amount', 'category', 'paymentMethod', 'date',)
  fields = ('name', 'type', 'amount', 'category', 'paymentMethod', 'date',)
  search_fields =  ('name',)


admin.site.register(Transaction, TransactionAdmin)
