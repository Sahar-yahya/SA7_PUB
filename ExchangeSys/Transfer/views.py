"""API endpoint classes for Transfer app"""
import uuid
from django.db import transaction
from bulk_update.helper import bulk_update

from rest_framework.viewsets import ModelViewSet

from Transfer import serializers as Transfer_serializers
from Transfer import exceptions
from Transfer import models as Transfer_models
from account import models as account_models


class Transfer(ModelViewSet):
    """Endpoint class for Transfer"""
    queryset = Transfer_models.Transfer.objects.select_related()
    serializer_class = Transfer_serializers.TransferSer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        """Make transaction"""
        data = serializer.data
        with transaction.atomic():
            accounts = {
                acc.id : acc for acc in account_models.Account.objects.select_for_update().filter(
                    id__in=(data['account'], data['to_account'])
                )
            }
            if len(accounts) != 2:
                raise exceptions.InvalidAccounts

            account = accounts[data['account']]
            to_account = accounts[data['to_account']]

            if account.currency != to_account.currency:
                raise exceptions.CurrenciesNotMatched

            tr_hash = uuid.uuid4()
            Transfer_models.Transfer.objects.bulk_create([
                Transfer_models.Transfer(
                    account=account,
                    amount=data['amount'],
                    to_account=to_account,
                    direction=Transfer_models.Transfer.SEND,
                    tr_hash=tr_hash
                ),
                Transfer_models.Transfer(
                    account=to_account,
                    amount=data['amount'],
                    to_account=account,
                    direction=Transfer_models.Transfer.RECEIVE,
                    tr_hash=tr_hash
                )
            ])

            account.balance = Transfer_models.Transfer.recalc_account_balance(account.id)
            to_account.balance = Transfer_models.Transfer.recalc_account_balance(to_account.id)

            if account.balance < 0:
                raise exceptions.NotEnoughMoney

            bulk_update([account, to_account])
