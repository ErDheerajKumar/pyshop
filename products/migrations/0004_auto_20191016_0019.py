# Generated by Django 2.2.6 on 2019-10-15 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20191015_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=2, verbose_name=(('S', 'Shirt'), ('SW', 'Sport wear'), ('OW', 'Outwear'))),
        ),
        migrations.AlterField(
            model_name='product',
            name='label',
            field=models.CharField(max_length=1, verbose_name=(('P', 'primary'), ('S', 'secondary'), ('D', 'danger'))),
        ),
    ]