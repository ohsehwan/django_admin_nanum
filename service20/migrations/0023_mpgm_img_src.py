# Generated by Django 2.1.5 on 2019-02-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0022_auto_20190208_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpgm',
            name='img_src',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='이미지경로'),
        ),
    ]