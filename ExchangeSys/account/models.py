"""Models account"""
from django.db import models
from django.utils.translation import gettext_lazy as _

class Account(models.Model):
    """Model account"""
    USD = 'USD'
    YER = 'YER'

    Currencies = (
        (USD, 'United States Dollar'),
        (YER, 'Yemeni Riyal'),
    )



    
    id = models.CharField(max_length=100, primary_key=True)
    AccountType = models.CharField(max_length=20, choices=[
        ('fund_accounts', ('FundAccounts')),
        ('tranfer_accounts', ('TranferAccount')),
        ('commission_accounts', ('CommissionAccounts'))],
        default='fund_accounts')
 

    balance = models.DecimalField(max_digits=100, decimal_places=2)
    currency = models.CharField(max_length=10, choices=Currencies)

    def __str__(self):
        return '{}: {} {}'.format(self.id, self.balance, self.currency)
