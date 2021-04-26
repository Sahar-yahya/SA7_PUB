# Generated by Django 2.2 on 2019-04-04 17:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('direction', models.IntegerField(choices=[(-1, 'SEND'), (1, 'RECEIVE')])),
                ('tr_hash', models.UUIDField(default=uuid.UUID('82d65f38-b5c3-40e7-a0fa-1c75f49a793d'))),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='account.Account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_accounts', to='account.Account')),
            ],
        ),
    ]
