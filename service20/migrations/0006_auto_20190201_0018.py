# Generated by Django 2.1.5 on 2019-02-01 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0005_auto_20190201_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_apl',
            name='ms_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service20.msch', verbose_name='멘토스쿨ID'),
        ),
    ]
