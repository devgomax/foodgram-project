# Generated by Django 3.2.4 on 2021-06-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210617_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество'),
        ),
    ]