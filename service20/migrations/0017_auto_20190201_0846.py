# Generated by Django 2.1.5 on 2019-02-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0016_auto_20190201_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardian',
            name='h_addr',
            field=models.CharField(max_length=200, verbose_name='집주소'),
        ),
        migrations.AlterField(
            model_name='mpgm',
            name='base_div',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='기준 프로그램 여부'),
        ),
    ]
