# Generated by Django 5.0.6 on 2024-08-11 19:25

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopper', '0013_cartorder_oid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=20, null=True, prefix=''),
        ),
    ]