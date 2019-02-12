# Generated by Django 2.1.5 on 2019-02-10 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0026_auto_20190210_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='com_cdh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std_grp_code', models.CharField(max_length=6, verbose_name='그룹코드')),
                ('lang_key', models.CharField(max_length=2, verbose_name='언어')),
                ('std_grp_code_nm', models.CharField(blank=True, max_length=50, null=True, verbose_name='그룹코드명')),
                ('rmrk', models.CharField(blank=True, max_length=255, null=True, verbose_name='비고')),
                ('use_indc', models.CharField(default='Y', max_length=1, verbose_name='사용여부')),
                ('cls_date', models.CharField(default='99991231', max_length=8, verbose_name='사용 종료일')),
                ('sys_id', models.CharField(blank=True, max_length=12, null=True, verbose_name='시스템ID')),
                ('grp_type', models.CharField(blank=True, max_length=2, null=True, verbose_name='그룹유형 - 시스템,사용자 → 수정가능')),
                ('ins_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='입력자ID')),
                ('ins_ip', models.CharField(blank=True, max_length=20, null=True, verbose_name='입력자IP')),
                ('ins_dt', models.DateTimeField(blank=True, null=True, verbose_name='입력일시')),
                ('ins_pgm', models.CharField(blank=True, max_length=20, null=True, verbose_name='입력프로그램ID')),
                ('upd_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='수정자ID')),
                ('upd_ip', models.CharField(blank=True, max_length=20, null=True, verbose_name='수정자IP')),
                ('upd_dt', models.DateTimeField(blank=True, null=True, verbose_name='수정일시')),
                ('upd_pgm', models.CharField(blank=True, max_length=20, null=True, verbose_name='수정프로그램ID')),
            ],
            options={
                'verbose_name': 'Common Code Master Head',
                'verbose_name_plural': 'Common Code Master Head',
            },
        ),
        migrations.AlterField(
            model_name='ms_sub',
            name='att_id',
            field=models.ForeignKey(blank=True, limit_choices_to={'std_grp_code': 'MS0010'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='service20.com_cdh', verbose_name='속성ID'),
        ),
        migrations.AlterField(
            model_name='ms_sub',
            name='ms_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service20.msch', verbose_name='멘토스쿨ID'),
        ),
        migrations.AlterUniqueTogether(
            name='com_cdh',
            unique_together={('std_grp_code', 'lang_key')},
        ),
    ]