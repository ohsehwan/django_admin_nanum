# Generated by Django 2.1.5 on 2019-02-01 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0015_guardian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardian',
            name='h_addr',
            field=models.CharField(max_length=20, verbose_name='집주소'),
        ),
    ]