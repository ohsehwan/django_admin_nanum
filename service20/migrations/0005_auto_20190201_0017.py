# Generated by Django 2.1.5 on 2019-02-01 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0004_auto_20190131_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_apl',
            name='ms_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service20.msch', verbose_name='지원자ID(학번)'),
        ),
    ]
