# Generated by Django 4.2 on 2023-04-07 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_alter_product_price_delete_inbound'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='수량')),
                ('inbound_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField(verbose_name='상품가격')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.product')),
            ],
            options={
                'verbose_name': '입고',
                'db_table': 'inbound',
            },
        ),
    ]