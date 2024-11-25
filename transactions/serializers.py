from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = '__all__'
    extra_kwargs = {
      'name': {'max_length': 50, 'required': True},
      'type': {'required': True},
      'amount': {'min_value': 0, 'required': True},
      'category': {'required': True},
      'paymentMethod': {'required': True},
      'date': {'required': True},
      'createdAt': {'read_only': True},  
      'updatedAt': {'read_only': True}, 
      'user': {'required': False},
    }