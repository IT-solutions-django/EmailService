# Generated by Django 5.1.3 on 2024-12-01 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_ipaddress_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='host',
            field=models.CharField(max_length=100, verbose_name='host'),
        ),
    ]
