# Generated by Django 2.1.5 on 2019-02-01 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0011_auto_20190201_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='mpgm',
            fields=[
                ('mp_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='멘토링 프로그램ID')),
                ('status', models.CharField(blank=True, max_length=2, null=True, verbose_name='상태')),
                ('mp_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='멘토링 프로그램 명')),
                ('mp_sname', models.CharField(blank=True, max_length=20, null=True, verbose_name='멘토링 프로그램 단명')),
                ('base_div', models.PositiveIntegerField(blank=True, max_length=1, null=True, verbose_name='기준 프로그램 여부')),
                ('mp_intro', models.CharField(blank=True, max_length=1000, null=True, verbose_name='프로그램 소개, CMS ID')),
                ('mng_area', models.CharField(blank=True, max_length=2, null=True, verbose_name='프로그램 관리자 영역')),
                ('mgr_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='프로그램 관리자 ID')),
                ('mgr_nm', models.CharField(blank=True, max_length=20, null=True, verbose_name='프로그램 관리자 명')),
                ('mng_org', models.CharField(blank=True, max_length=10, null=True, verbose_name='관리기관')),
                ('sup_org', models.CharField(blank=True, max_length=10, null=True, verbose_name='주관기관')),
                ('yr', models.CharField(blank=True, max_length=4, null=True, verbose_name='연도')),
                ('yr_seq', models.PositiveIntegerField(blank=True, null=True, verbose_name='차수')),
                ('apl_ntc_fr_dt', models.DateTimeField(blank=True, null=True, verbose_name='공지시작일')),
                ('apl_ntc_to_dt', models.DateTimeField(blank=True, null=True, verbose_name='공지종료일')),
                ('apl_term', models.CharField(blank=True, max_length=2, null=True, verbose_name='모집시기')),
                ('apl_fr_dt', models.DateTimeField(blank=True, null=True, verbose_name='모집기간-시작')),
                ('apl_to_dt', models.DateTimeField(blank=True, null=True, verbose_name='모집기간-종료')),
                ('mnt_term', models.CharField(blank=True, max_length=2, null=True, verbose_name='활동시기')),
                ('mnt_fr_dt', models.DateTimeField(blank=True, null=True, verbose_name='활동기간-시작')),
                ('mnt_to_dt', models.DateTimeField(blank=True, null=True, verbose_name='활동기간-시작')),
                ('tot_apl', models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격')),
                ('cnt_apl', models.PositiveIntegerField(default=0, verbose_name='지원인원')),
                ('cnt_doc_suc', models.PositiveIntegerField(default=0, verbose_name='서류전형 합격인원')),
                ('cnt_doc_res', models.PositiveIntegerField(default=0, verbose_name='서류전형 예비인원(실제 없음)')),
                ('cnt_intv_pl', models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 계획 인원')),
                ('cnt_intv_ac', models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 인원')),
                ('cnt_intv_suc', models.PositiveIntegerField(default=0, verbose_name='면접전형 합격인원')),
                ('cnt_iintv_res', models.PositiveIntegerField(default=0, verbose_name='면접전형 예비합격인원')),
                ('cnt_trn', models.PositiveIntegerField(default=0, verbose_name='교육인원')),
                ('cnt_mtr', models.PositiveIntegerField(default=0, verbose_name='최종합격 멘토인원')),
                ('doc_dt', models.DateTimeField(blank=True, null=True, verbose_name='서류전형일')),
                ('doc_mgr', models.CharField(blank=True, max_length=10, null=True, verbose_name='서류전형 수행자')),
                ('intv_dt', models.DateTimeField(blank=True, null=True, verbose_name='면접전형-입력-일')),
                ('intv_mgr', models.CharField(blank=True, max_length=10, null=True, verbose_name='면접전형-입력-자')),
                ('fin_dt', models.DateTimeField(blank=True, null=True, verbose_name='최종합격-입력-일')),
                ('fin_mgr', models.CharField(blank=True, max_length=10, null=True, verbose_name='최종합격-입력-자')),
                ('use_div', models.CharField(blank=True, max_length=1, null=True, verbose_name='사용 여부')),
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