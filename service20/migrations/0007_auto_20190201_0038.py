# Generated by Django 2.1.5 on 2019-02-01 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0006_auto_20190201_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_apl',
            name='gen',
            field=models.CharField(choices=[('M', '남자'), ('W', '여자')], max_length=1, verbose_name='성별'),
        ),
    ]