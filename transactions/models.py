from django.db import models
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth.models import User

TRANSACTION_TYPE_CHOICES = [
    ("DEPOSIT", _("Depósito")),  
    ("EXPENSE", _("Despesa")),
    ("INVESTMENT", _("Investimento")),
]

TRANSACTION_CATEGORY_CHOICES = [
    ("HOUSING", _("Moradia")),  
    ("TRANSPORTATION", _("Transporte")),
    ("FOOD", _("Alimentação")),
    ("ENTERTAINMENT", _("Entretenimento")),
    ("HEALTH", _("Saúde")),
    ("UTILITY", _("Utilidades")),
    ("SALARY", _("Salário")),
    ("EDUCATION", _("Educação")),
    ("OTHER", _("Outro")),
]

PAYMENT_METHOD_CHOICES = [
    ("CREDIT_CARD", _("Cartão de Crédito")),
    ("DEBIT_CARD", _("Cartão de Débito")),
    ("BANK_TRANSFER", _("Transferência Bancária")),
    ("BANK_SLIP", _("Boleto Bancário")),
    ("CASH", _("Dinheiro")),
    ("PIX", _("PIX")),
    ("OTHER", _("Outro")),
]


class Transaction(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transaction")  
    name = models.CharField(max_length=50, verbose_name=_("Nome"))  
    type = models.CharField(max_length=25, choices=TRANSACTION_TYPE_CHOICES, verbose_name=_("Tipo"))
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Valor"))
    category = models.CharField(max_length=25, choices=TRANSACTION_CATEGORY_CHOICES, verbose_name=_("Categoria"))
    paymentMethod = models.CharField(max_length=25, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Método de Pagamento"))
    date = models.DateField(verbose_name=_("Data"))
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    updatedAt = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        ordering = ["-updatedAt"]  
        verbose_name = _("Transação")
        verbose_name_plural = _("Transações")

    def __str__(self):
        return self.name
