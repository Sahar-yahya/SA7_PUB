"""Admin interface for creating/deleting/updating Transfers for test"""
from django.contrib import admin
from Transfer.models import Transfer

class TransferAdmin(admin.ModelAdmin):
    """Accounts admin custom class"""
    list_display = (
        # 'id',
        'ExpressNo',
        'SenderName',
        'ReceiverName',
        'account',
        'amount',
        'to_account',
        'direction',
        'Date',
        'Region',
        'Purpose',
    )
    search_fields = ('id', 'account__id', 'to_account__id', 'ExpressNo',)

admin.site.register(Transfer, TransferAdmin)
