# Generated by Django 3.2.9 on 2022-03-20 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_products_ownerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='owner',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='products',
            name='ownerId',
            field=models.IntegerField(default=''),
        ),
    ]
