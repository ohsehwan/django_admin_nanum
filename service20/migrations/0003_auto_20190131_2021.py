# Generated by Django 2.1.5 on 2019-01-31 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0002_msch_img_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_apl',
            name='apl_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Member', verbose_name='지원자ID(학번)'),
        ),
    ]
