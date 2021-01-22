import os
import random
import datetime
from celery import shared_task, task
from kombu.utils import json
from paying.models import PayingBill
from rest_framework import serializers



os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


@shared_task(name="sum")
def add(x, y):
    return x + y


class PayingBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayingBill
        fields = "__all__"

@shared_task(name='multi')
def mul(x, y):
    number_1 = x
    number_2 = x * (y * random.randint(3, 100))
    total = number_1 * number_2
    new_obj = PayingBill.objects.create(
        item_name='some item',
        number_1=number_1,
        number_2=number_2,
        total=total,
        timestamp=datetime.datetime.now
    )
    return PayingBillSerializer(new_obj).data


@shared_task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)
