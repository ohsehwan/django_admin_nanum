# Generated by Django 2.1.5 on 2019-01-31 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post2.Post2')),
            ],
        ),
    ]
