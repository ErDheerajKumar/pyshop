# Generated by Django 2.2.6 on 2019-11-18 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_order_billing_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='state',
            field=models.CharField(default='RJ', max_length=20),
            preserve_default=False,
        ),
    ]
