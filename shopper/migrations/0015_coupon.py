# Generated by Django 5.0.6 on 2024-08-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopper', '0014_alter_cartorder_oid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('discount', models.DecimalField(decimal_places=2, default='1.99', max_digits=99999)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]