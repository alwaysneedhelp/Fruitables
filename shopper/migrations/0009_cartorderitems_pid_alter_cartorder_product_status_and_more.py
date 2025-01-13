# Generated by Django 5.0.6 on 2024-08-09 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopper', '0008_alter_cartorder_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='pid',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=10),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1.99', max_digits=99999),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=10),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.DecimalField(decimal_places=2, default='1.99', max_digits=99999),
        ),
    ]