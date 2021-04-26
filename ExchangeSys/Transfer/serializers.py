"""Serializers Transfer"""
from rest_framework import serializers
from Transfer.models import Transfer


class TransferSer(serializers.ModelSerializer):
    """Serializer Transfer"""
    @staticmethod
    def validate_amount(value):
        """Additional checking amount"""
        if value < 0:
            raise serializers.ValidationError('Amount less than zero')
        return value

    class Meta:
        """Meta description"""
        model = Transfer
        fields = '__all__'
        read_only_fields = ('direction', 'tr_hash',)
