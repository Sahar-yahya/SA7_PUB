# Generated by Django 3.1.5 on 2021-02-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibManager', '0002_auto_20210202_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='media/book_image'),
        ),
    ]