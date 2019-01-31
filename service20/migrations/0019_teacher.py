# Generated by Django 2.1.5 on 2019-02-01 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0018_auto_20190201_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('tchr_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='교사 ID(학교별 부여)')),
                ('tchr_nm', models.CharField(max_length=20, verbose_name='교사명')),
                ('tchr_nm_e', models.CharField(max_length=20, verbose_name='교사 영문명')),
                ('sch_grd', models.CharField(max_length=1, verbose_name='학교구분')),
                ('sch_cd', models.CharField(max_length=10, verbose_name='학교')),
                ('sch_nm', models.CharField(max_length=30, verbose_name='학교명')),
                ('mob_no', models.CharField(blank=True, max_length=12, null=True, verbose_name='휴대전화')),
                ('tel_no', models.CharField(blank=True, max_length=12, null=True, verbose_name='사무실전화')),
                ('area_city', models.CharField(max_length=10, verbose_name='시/도')),
                ('area_gu', models.CharField(max_length=10, verbose_name='지역구(시/군)')),
                ('h_addr', models.CharField(max_length=200, verbose_name='집주소')),
                ('h_post_no', models.CharField(blank=True, max_length=6, null=True, verbose_name='우편번호')),
                ('s_addr', models.CharField(max_length=200, verbose_name='학교주소')),
                ('s_post_no', models.CharField(blank=True, max_length=6, null=True, verbose_name='우편번호')),
                ('email_addr', models.CharField(max_length=50, verbose_name='이메일 주소')),
                ('ins_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='입력자ID')),
                ('ins_ip', models.CharField(blank=True, max_length=20, null=True, verbose_name='입력자IP')),
                ('ins_dt', models.DateTimeField(blank=True, null=True, verbose_name='입력일시')),
                ('ins_pgm', models.CharField(blank=True, max_length=20, null=True, verbose_name='입력프로그램ID')),
                ('upd_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='수정자ID')),
                ('upd_ip', models.CharField(blank=True, max_length=20, null=True, verbose_name='수정자IP')),
                ('upd_dt', models.DateTimeField(blank=True, null=True, verbose_name='수정일시')),
                ('upd_pgm', models.CharField(blank=True, max_length=20, null=True, verbose_name='수정프로그램ID')),
            ],
        ),
    ]
