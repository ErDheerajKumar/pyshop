# Generated by Django 2.2.6 on 2019-12-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]