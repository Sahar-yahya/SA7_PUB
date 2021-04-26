"""Models Transfer"""
import uuid
from django.db import models
from account.models import Account
from ExchangeSys import settings



class Transfer(models.Model):
    SEND = -1
    RECEIVE = 1

    Directions = ((SEND, 'send'),(RECEIVE, 'recieve'),)
    ExpressNo = models.AutoField(primary_key=True)
    SenderName = models.CharField(max_length=100, null = True, blank = True)
    ReceiverName = models.CharField(max_length=100, null = True, blank = True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounts')
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    commission = models.DecimalField(max_digits=100, decimal_places=2)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_accounts')
    direction = models.IntegerField(choices=Directions)
    Date = models.DateField(null = True, blank = True)
    Region = models.CharField(max_length=100, null = True, blank = True)
    Purpose = models.CharField(max_length=200, null = True, blank = True)




    @classmethod
    def recalc_account_balance(cls, account_id):
        """Recount balance of account"""
        amounts = cls.objects.filter(
            account=account_id,
        ).aggregate(
            _in=models.Sum('amount', filter=models.Q(direction=cls.RECEIVE)),
            _out=models.Sum('amount', filter=models.Q(direction=cls.SEND))
        )
        return (amounts['_in'] or 0) - (amounts['_out'] or 0)
