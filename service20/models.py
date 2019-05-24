import uuid

import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from member.models import Member
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from collections import namedtuple
from collections  import OrderedDict

from django.db import connection

from decimal import Decimal
from pyfcm import FCMNotification

cursor = connection.cursor()

cursor.execute("select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001'")
MP0001_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0002'")
MP0002_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0059'")
MP0059_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0060'")
MP0060_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0063'")
MP0063_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0085'")
MP0085_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())



class mp_monh(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mon_no = models.PositiveIntegerField(null=False, verbose_name='모니터링 NO' )
  mon_sts = models.CharField(max_length=2, null=False, verbose_name='모니터링 상태(MP0075)' )
  mon_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='모니터링 구분(MP0083)' )
  mon_sdt = models.DateTimeField(null=True, blank=True, verbose_name='모니터링 시작 일시' )
  mon_edt = models.DateTimeField(null=True, blank=True, verbose_name='모니터링 종료 일시' )
  ast_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='모니터링 조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='모니터링 조교명' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 확인 일시' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '모니터링'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mon_no")


class mp_tmd(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mon_no = models.PositiveIntegerField(null=False, verbose_name='모니터링 NO' )
  mnte_no = models.PositiveIntegerField(null=False, verbose_name='멘티 지원 NO' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  mte_mon_sts = models.CharField(max_length=2, null=False, verbose_name='멘티 모니터링 상태(MP0075)' )
  mte_mon_sdt = models.DateTimeField(null=True, blank=True, verbose_name='멘티 모니터링 시작 일시' )
  mte_mon_edt = models.DateTimeField(null=True, blank=True, verbose_name='멘티 모니터링 종료 일시' )
  mtr_mon_sts = models.CharField(max_length=2, null=False, verbose_name='멘토 모니터링 상태(MP0075)' )
  mtr_mon_sdt = models.DateTimeField(null=True, blank=True, verbose_name='멘토 모니터링 시작 일시' )
  mtr_mon_edt = models.DateTimeField(null=True, blank=True, verbose_name='멘토 모니터링 종료 일시' )
  smon_div = models.CharField(max_length=1, default='N', verbose_name='현장 모니터링 필요여부' )
  mtr_mon = models.CharField(max_length=2000, null=True, blank=True, verbose_name='멘토 모니터링 내용' )
  mnte_mon = models.CharField(max_length=2000, null=True, blank=True, verbose_name='멘티 모니터링 내용' )
  mon_rmk = models.CharField(max_length=500, null=True, blank=True, verbose_name='비고' )
  ast_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='모니터링 조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='모니터링 조교명' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 확인 일시' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '전화 모니터링 상세(DETAIL)'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mon_no", "mnte_no")

    index_together = ["apl_no"]



class mp_smd(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mon_no = models.PositiveIntegerField(null=False, verbose_name='모니터링 NO' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  mon_sts = models.CharField(max_length=2, null=False, verbose_name='모니터링 상태(MP0075)' )
  mte_ast_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='모니터링 조교 ID' )
  mte_ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='모니터링 조교명' )
  mp_plc = models.CharField(max_length=1, null=True, blank=True, verbose_name='모니터링 장소 구분(MP0052)' )
  mp_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='모니터링 주소' )
  mon_sdt = models.DateTimeField(null=True, blank=True, verbose_name='모니터링 시작 일시' )
  mon_edt = models.DateTimeField(null=True, blank=True, verbose_name='모니터링 종료 일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 확인 일시' )
  eval_tot = models.PositiveIntegerField(null=True, blank=True, verbose_name='평가총점(100)' )
  mon_cmt = models.CharField(max_length=2000, null=True, blank=True, verbose_name='모니터링 의견' )
  mon_pic1 = models.CharField(max_length=200, null=True, blank=True, verbose_name='활동사진1(저장소URL)' )
  mon_pic2 = models.CharField(max_length=200, null=True, blank=True, verbose_name='활동사진2(저장소URL)' )
  mon_pic3 = models.CharField(max_length=200, null=True, blank=True, verbose_name='활동사진3(저장소URL)' )
  mon_pic4 = models.CharField(max_length=200, null=True, blank=True, verbose_name='활동사진4(저장소URL)' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '현장 모니터링(ON_SITE_MON_DETAIL)'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mon_no", "apl_no")

    index_together = ["apl_no"]



class mp_smm(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mon_no = models.PositiveIntegerField(null=False, verbose_name='모니터링 NO' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  evl_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  evl_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  evl_up_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='상위 속성 CODE HEADER' )
  evl_up_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='상위 속성 CODE' )
  evl_scr = models.PositiveIntegerField(default=1, verbose_name='평가점수(1~5)' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '현장 모니터링 채점 - MARK'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mon_no", "apl_no", "evl_cdh", "evl_cdd")

    index_together = ["apl_no"]




class oth_std(models.Model):
  std_id = models.CharField(max_length=16, null=False, verbose_name='타대생 ID(학교코드+학번)' )
  std_nm = models.CharField(max_length=50, null=False, verbose_name='타대생 명' )
  std_nm_e = models.CharField(max_length=50, null=True, blank=True, verbose_name='타대생 영문명' )
  ms_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='멘토스쿨ID' )
  apl_no = models.PositiveIntegerField(null=True, blank=True, verbose_name='지원 NO' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
  reg_dt = models.DateField(null=True, blank=True, verbose_name='등록일' )
  unv_cd = models.CharField(max_length=10, null=False, verbose_name='타대생 대학교 코드(MP0044)' )
  unv_nm = models.CharField(max_length=30, null=False, verbose_name='타대생 대학교 명' )
  cllg_cd = models.CharField(max_length=10, null=False, verbose_name='타대생 대학 코드' )
  cllg_nm = models.CharField(max_length=30, null=False, verbose_name='타대생 대학 명' )
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='타대생 학부/학과 코드' )
  dept_nm = models.CharField(max_length=30, null=False, verbose_name='타대생 학부/학과 명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
  gen = models.CharField(max_length=1, null=False, verbose_name='성별' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  exp_dt = models.DateField(null=True, blank=True, verbose_name='자격 박탈일' )
  exp_rsn = models.CharField(max_length=10, null=True, blank=True, verbose_name='박탈 사유' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  tel_no_g = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )
  h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
  post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  bank_acct = models.CharField(max_length=20, null=True, blank=True, verbose_name='은행 계좌 번호' )
  bank_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='은행 코드' )
  bank_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행 명' )
  bank_dpsr = models.CharField(max_length=20, null=True, blank=True, verbose_name='예금주' )
  cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
  cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
  cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
  cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
  inv_agr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='개인정보 동의 여부' )
  inv_agr_dt = models.DateTimeField(null=True, blank=True, verbose_name='개인정보 동의 일시' )
  dept_chr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 ID' )
  dept_chr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  ast_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='조교 명' )
  dept_appr_div = models.CharField(max_length=1, default='N', verbose_name='학과 승인 여부' )
  dept_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='학과 승인 날짜' )
  dept_retn_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='학과 반려 사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )
  pwd = models.CharField(max_length=128, default='1', verbose_name='비밀번호' )


  class Meta:
    verbose_name = '타대학생'
    verbose_name_plural =  verbose_name
    unique_together=("std_id", "unv_cd")



class oth_mgr(models.Model):
  mgr_id = models.CharField(max_length=16, null=False, verbose_name='관리자 ID(교직원 번호)' )
  mgr_nm = models.CharField(max_length=50, null=False, verbose_name='관리자 명' )
  mgr_nm_e = models.CharField(max_length=50, null=True, blank=True, verbose_name='관리자 영문명' )
  mng_area = models.CharField(max_length=2, null=True, blank=True, verbose_name='프로그램 관리 영역' )
  mgr_div = models.CharField(max_length=1, null=False, verbose_name='관리자구분' )
  org_div = models.CharField(max_length=1, null=False, verbose_name='기관구분' )
  org_cd = models.CharField(max_length=10, null=False, verbose_name='외부기관(대학교) 코드(MP0044)' )
  org_nm = models.CharField(max_length=30, null=False, verbose_name='외부기관(대학교) 명' )
  dept_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='부서코드' )
  dept_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='부서명' )
  ofc_lvl_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='직급코드' )
  ofc_lvl_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직급명' )
  func_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='직책코드' )
  func_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직책명' )
  status = models.CharField(max_length=1, default= '1', verbose_name='상태값' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='사무실전화' )
  h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pwd = models.CharField(max_length=128, default='1', verbose_name='비밀번호' )

  class Meta:
    verbose_name = '프로그램 관리자(타학교)'
    verbose_name_plural =  verbose_name
    unique_together=("mgr_id", "org_cd")
    


class com_cdh(models.Model):
  std_grp_code = models.CharField(max_length=6, null=False, verbose_name='그룹코드' )
  lang_key = models.CharField(max_length=2, null=False, verbose_name='언어' )
  std_grp_code_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='그룹코드명' )
  rmrk = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고' )
  use_indc = models.CharField(max_length=1, default= 'Y', verbose_name='사용여부' )
  cls_date = models.CharField(max_length=8, default= '99991231', verbose_name='사용 종료일' )
  sys_id = models.CharField(max_length=12, null=True, blank=True, verbose_name='시스템ID' )
  grp_type = models.CharField(max_length=2, null=True, blank=True, verbose_name='그룹유형 - 시스템,사용자 → 수정가능' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '공통코드관리(Master)'
    verbose_name_plural =  verbose_name
    unique_together=("std_grp_code", "lang_key")

  def __str__(self):
    return self.std_grp_code_nm   


class com_cdd(models.Model):
  std_grp_code = models.CharField(max_length=6, null=False, verbose_name='그룹코드' )
  #std_grp_code = models.ForeignKey(to='com_cdh',to_field='std_grp_code', on_delete=models.SET_NULL,null=True,blank=True,verbose_name='그룹코드')
  std_detl_code = models.CharField(max_length=10, null=False, verbose_name='공통코드' )
  lang_key = models.CharField(max_length=2, null=False, verbose_name='언어' )
  std_detl_code_nm = models.CharField(max_length=60, null=False, verbose_name='공통코드명' )
  rmrk = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고' )
  rmrk_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고2' )
  up_std_detl_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='상위공통코드' )
  use_indc = models.CharField(max_length=1, default= 'N', verbose_name='사용여부' )
  cls_date = models.CharField(max_length=8, default= '00000000', verbose_name='종료일' )
  sort_seq_no = models.CharField(max_length=10, default= '0000000000', verbose_name='순서' )
  co_code = models.CharField(max_length=4, null=True, blank=True, verbose_name='예비 코드' )
  plnt = models.CharField(max_length=4, null=True, blank=True, verbose_name='공장' )
  sys_id = models.CharField(max_length=12, null=True, blank=True, verbose_name='시스템ID' )
  text1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트1' )
  text2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트2' )
  text3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트3' )
  text4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트4' )
  text5 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트5' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '공통코드관리(디테일)'
    verbose_name_plural =  verbose_name
    unique_together=("std_grp_code", "std_detl_code", "lang_key")
    index_together = ["std_detl_code_nm", "std_detl_code"]

  def __str__(self):
    return self.std_detl_code_nm    




class mp_team_ans(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 번호' )
  team_id = models.CharField(max_length=16, null=False, verbose_name='팀 ID' )
  team_nm = models.CharField(max_length=50, null=False, verbose_name='팀명' )
  sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬' )
  ans_div = models.CharField(max_length=1, default='2', verbose_name='질문구분(CM0003)' )
  ans_t1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='선다형 답' )
  ans_t2 = models.CharField(max_length=1000, null=True, blank=True, verbose_name='수필형 답' )
  ans_t3 = models.CharField(max_length=10, null=True, blank=True, verbose_name='선택 답' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 팀 지원서 답변'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "team_no", "ques_no")



class mp_team_mrk(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)MP0039' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  item_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='채점항목코드-SEQ별' )
  item_nm = models.CharField(max_length=60, null=True, blank=True, verbose_name='채점항목명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mrk_cmt = models.CharField(max_length=500, null=True, blank=True, verbose_name='심사평' )

  class Meta:
    verbose_name = '프로그램 팀 지원서 채점'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "team_no", "mrk_seq", "mrk_no")



class mp_team_mrk_h(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)MP0039' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  tot_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='총점' )
  grade = models.CharField(max_length=1, null=True, blank=True, verbose_name='' )
  cov_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램 팀 지원서 채점 합계'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "team_no", "mrk_seq", "mrk_no")



class mp_team_chc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  chc_no = models.PositiveIntegerField(null=False, verbose_name='선택 NO' )
  att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
  att_cdh = models.CharField(max_length=6, null=False, verbose_name='속성 CODE HEADER' )
  att_cdd = models.CharField(max_length=10, null=False, verbose_name='선택 답변 코드' )
  chc_tp = models.CharField(max_length=1, null=True, blank=True, verbose_name='선택유형(MP0087:콤보,라디오,체크)' )
  chc_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='선택 답변 명' )
  chc_seq = models.PositiveIntegerField(null=False, verbose_name='선택 우선순위' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 순서' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 팀 지원서 선택형 답변'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "team_no", "chc_no")


class mp_team_atc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  atc_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ → PK 자동생성 시 필요없음' )
  atc_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  atc_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  atc_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첨부파일종류' )
  atc_file_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첨부파일명' )
  atc_file_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='파일경로' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 팀 지원자 첨부파일'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "team_no", "atc_seq")


class mp_team(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  team_no = models.PositiveIntegerField(null=False, verbose_name='팀 NO(지원 NO)' )
  team_nm = models.CharField(max_length=50, null=False, verbose_name='팀명' )
  team_id = models.CharField(max_length=16, null=False, verbose_name='팀 ID' )
  ldr_id = models.CharField(max_length=16, null=False, verbose_name='리더 ID(학번)' )
  pln_sdt = models.DateTimeField(null=True, blank=True, verbose_name='활동시작일(계획)' )
  pln_edt = models.DateTimeField(null=True, blank=True, verbose_name='활동종료일(계획)' )
  act_sdt = models.DateTimeField(null=True, blank=True, verbose_name='활동시작일(실적)' )
  act_edt = models.DateTimeField(null=True, blank=True, verbose_name='활동종료일(실적)' )
  act_area = models.CharField(max_length=50, null=True, blank=True, verbose_name='활동지역(국가)' )
  act_org = models.CharField(max_length=50, null=True, blank=True, verbose_name='방문기관' )
  act_dsc = models.CharField(max_length=100, null=True, blank=True, verbose_name='활동 내용' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='접수일(지원서 저장)' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0053)' )
  doc_cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
  doc_cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
  tot_doc = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='서류전형  총 점수' )
  doc_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='서류심사등수' )
  doc_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='서류심사결과' )
  intv_team = models.PositiveIntegerField(null=True, blank=True, verbose_name='면접팀' )
  intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접일' )
  intv_part_pl = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여계획' )
  intv_np_rsn_pl = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_pl_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여계획 입력일' )
  intv_part_ac = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여여부' )
  intv_np_rsn_ac = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_ac_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여 입력일' )
  intv_tot = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='면접점수' )
  intv_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접심사결과' )
  fnl_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='최종합격 여부' )
  score1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 석차' )
  score2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 총원' )
  score3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 학점' )
  score4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='봉사점수합계' )
  score5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='자격증 개수' )
  score6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 학점' )
  cscore1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수1-성적' )
  cscore2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수2-어학' )
  cscore3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수3-봉사' )
  cscore4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수4-지원서' )
  cscore5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수5-교직' )
  cscore6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수6-거주지' )
  ascore1 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점1' )
  ascore2 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점2' )
  ascore3 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점3' )
  ascore4 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점4' )
  ascore5 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점5' )
  ascore6 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점6' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 팀'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "team_no")


class mp_team_mem(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  team_id = models.CharField(max_length=16, null=False, verbose_name='팀 ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램 팀 멤버'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "team_id", "apl_no")






class ms_apl_lc(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  lc_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='성명' )
  license_large_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='대구분코드' )
  license_large_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='대구분코드명' )
  license_small_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='소구분코드' )
  license_small_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='소구분코드명' )
  license_cd = models.CharField(max_length=200, null=True, blank=True, verbose_name='자격증코드' )
  license_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='자격증명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 지원자(멘토) 자격증'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "apl_no", "lc_no")



class mp_mtr_lc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  lc_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='성명' )
  license_large_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='대구분코드' )
  license_large_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='대구분코드명' )
  license_small_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='소구분코드' )
  license_small_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='소구분코드명' )
  license_cd = models.CharField(max_length=200, null=True, blank=True, verbose_name='자격증코드' )
  license_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='자격증명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 지원자(멘토) 자격증'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "lc_no")



class vw_nanum_license(models.Model):
  apl_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='성명' )
  license_large_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='대구분코드' )
  license_large_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='대구분코드명' )
  license_small_cd = models.CharField(max_length=4, null=True, blank=True, verbose_name='소구분코드' )
  license_small_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='소구분코드명' )
  license_cd = models.CharField(max_length=200, null=True, blank=True, verbose_name='자격증코드' )
  license_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='자격증명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '학생 자격증 VIEW(임시)'
    verbose_name_plural =  verbose_name






class msch(models.Model):

  cursor = connection.cursor()
  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001'"
  cursor.execute(query)
  MP0001_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0002'")
  MP0002_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

  ms_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘토스쿨ID' )
  #status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MS0001)' )
  status = models.CharField(max_length=2, null=True, blank=True, choices=MP0001_CHOICES, verbose_name='상태(MP0001)' )
  ms_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='멘토스쿨 명' )
  ms_sname = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토스쿨 단명' )
  ms_intro = models.CharField(max_length=1000, null=True, blank=True, verbose_name='멘토스쿨 소개' )
  mng_area = models.CharField(max_length=2,  null=True, blank=True, verbose_name='멘토스쿨 관리 영역(MP0002)' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='멘토스쿨 관리자 ID' )
  mgr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토스쿨 관리자 명' )
  mng_org = models.CharField(max_length=10,  null=True, blank=True,  verbose_name='관리기관(MP0003)' )
  sup_org = models.CharField(max_length=10, null=True, blank=True, verbose_name='주관기관(MP0004)' )
  yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='연도' )
  yr_seq = models.PositiveIntegerField(null=True, blank=True, verbose_name='차수' )
  apl_ntc_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
  apl_ntc_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )
  apl_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='모집시기(MS0022)' )
  apl_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-시작' )
  apl_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-종료' )
  trn_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='교육시기(MS0022)' )
  trn_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='교육기간-시작' )
  trn_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='교육기간-종료' )
  tot_apl = models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격' )
  cnt_apl = models.PositiveIntegerField(default=0, verbose_name='지원인원' )
  cnt_doc_suc = models.PositiveIntegerField(default=0, verbose_name='서류전형 합격인원' )
  cnt_doc_res = models.PositiveIntegerField(default=0, verbose_name='서류전형 예비인원(실제 없음)' )
  cnt_intv_pl = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 계획 인원' )
  cnt_intv_ac = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 인원' )
  intv_dt = models.DateField(null=True, blank=True, verbose_name='면접일' )
  cnt_intv_suc = models.PositiveIntegerField(default=0, verbose_name='면접전형 합격인원' )
  cnt_iintv_res = models.PositiveIntegerField(default=0, verbose_name='면접전형 예비합격인원' )
  cnt_trn = models.PositiveIntegerField(default=0, verbose_name='교육인원' )
  cnt_mtr = models.PositiveIntegerField(default=0, verbose_name='최종합격 멘토인원' )
  doc_dt = models.DateTimeField(null=True, blank=True, verbose_name='서류전형예정일' )
  doc_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
  doc_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='면접전형-입력-자' )
  intv_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
  intv_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='면접전형-입력-자' )
  fin_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격 일' )
  fin_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격-입력-일' )
  fin_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='최종합격-입력-자' )
  use_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용 여부' )
  img_src = models.CharField(max_length=100, null=True, blank=True, verbose_name='소개 사진' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  def __str__(self):
    return self.ms_name

  class Meta:
    verbose_name = '멘토스쿨프로그램'
    verbose_name_plural =  verbose_name





class ms_sub(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
  att_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ → PK 자동생성 시 필요없음' )
  att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )
  att_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 단위' )
  use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
  sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '멘토스쿨 속성'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "att_id", "att_seq")



class ms_apl(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='지원자 명' )
  apl_nm_e = models.CharField(max_length=50, null=False, verbose_name='멘토 영문명' )
  unv_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학교 코드' )
  unv_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 대학교 명' )
  cllg_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학 코드' )
  cllg_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 대학 명' )
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 학부/학과 코드' )
  dept_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 학부/학과 명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
  gen = models.CharField(max_length=1, null=False, verbose_name='성별' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  mob_no = models.CharField(max_length=20, null=False, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  tel_no_g = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='접수일(지원서 저장)' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MS0024)' )
  doc_cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
  doc_cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
  tot_doc = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='서류전형  총 점수' )
  score1 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수1(성적,봉사,외국어,지원서)' )
  score2 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수2' )
  score3 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수3' )
  score4 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수4' )
  score5 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수5' )
  score6 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='원점수6' )
  cscore1 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수1' )
  cscore2 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수2' )
  cscore3 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수3' )
  cscore4 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수4' )
  cscore5 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수5' )
  cscore6 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='변환점수6' )
  doc_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='서류심사등수' )
  #doc_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='서류심사결과' )
  doc_rslt = models.CharField(max_length=1, null=True, blank=True, choices=(('P','합격'),('N','불합격')), verbose_name='서류심사결과', )
  intv_team = models.PositiveIntegerField(null=True, blank=True, verbose_name='면접팀' )
  intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접일' )
  intv_part_pl = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여계획' )
  intv_np_rsn_pl = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_pl_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여계획 입력일' )
  intv_part_ac = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여여부' )
  intv_np_rsn_ac = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_ac_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여 입력일' )
  intv_tot = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='면접점수' )
  intv_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접심사결과' )
  ms_trn_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='멘토스쿨 이수여부' )
  fnl_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='최종합격 여부' )
  mntr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='멘토ID' )
  mntr_dt = models.DateField(null=True, blank=True, verbose_name='멘토 자격 부여일' )
  sms_send_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='문자발송번호' )
  inv_agr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='개인정보 동의 여부' )
  inv_agr_dt = models.DateTimeField(null=True, blank=True, verbose_name='개인정보 동의 일시' )
  dept_chr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 ID' )
  dept_chr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  ast_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='조교 명' )
  dept_appr_div = models.CharField(max_length=1, default='N', choices=(('Y','승인'),('N','비승인')), verbose_name='학과 승인 여부' )
  #dept_appr_dt = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과 승인 날짜' )
  dept_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='학과 승인 날짜' )
  dept_retn_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='학과 반려 사유' )
  id_pic = models.CharField(max_length=100, null=True, blank=True, verbose_name='증명사진 위치' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pr_yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='직전 학년도' )
  pr_sch_yr = models.CharField(max_length=1, null=True, blank=True, verbose_name='직전 학년' )
  pr_term_div = models.CharField(max_length=2, null=True, blank=True, verbose_name='직전학기코드' )
  cmp_term = models.PositiveIntegerField(null=True, blank=True, verbose_name='현재기준 이수학기' )
  ascore1 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점1' )
  ascore2 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점2' )
  ascore3 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점3' )
  ascore4 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점4' )
  ascore5 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점5' )
  ascore6 = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='가산점6' )
  file_job_fav = models.CharField(max_length=100, null=True, blank=True, verbose_name='직업선호도 조사지 파일 경로' )
  intv_cmt = models.CharField(max_length=500, null=True, blank=True, verbose_name='면접심사평' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )


  class Meta:
    verbose_name = '멘토스쿨 지원자 및 사정'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "apl_no")

    index_together = ["apl_id"]
    index_together = ["apl_nm"]





class ms_ans(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 번호' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
  apl_nm = models.CharField(max_length=20, null=False, verbose_name='지원자 명' )
  sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬' )
  ans_t1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='선다형 답' )
  ans_t2 = models.CharField(max_length=1000, null=True, blank=True, verbose_name='수필형 답' )
  ans_t3 = models.CharField(max_length=2, null=True, blank=True, verbose_name='선택 답' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  class Meta:
    verbose_name = '지원서 답변'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "test_div", "apl_no", "ques_no")

class ms_mrk(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  item_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='채점항목코드-SEQ별' )
  item_nm = models.CharField(max_length=60, null=True, blank=True, verbose_name='채점항목명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mrk_cmt = models.CharField(max_length=500, null=True, blank=True, verbose_name='심사평' )


  class Meta:
    verbose_name = '지원서 채점'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "test_div", "apl_no", "mrk_seq", "mrk_no")


class ms_mrk_h(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)MP0039' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  tot_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='총점' )
  grade = models.CharField(max_length=1, null=True, blank=True, verbose_name='' )
  cov_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '멘토스쿨 지원서 채점 합계'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "test_div", "apl_no", "mrk_seq", "mrk_no")



class mentor(models.Model):
  cursor = connection.cursor()
  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0012'"
  cursor.execute(query)
  MS0012_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  mntr_id = models.CharField(max_length=16, primary_key=True, verbose_name='멘토ID' )
  mntr_nm = models.CharField(max_length=50, null=False, verbose_name='멘토 명' )
  mntr_nm_e = models.CharField(max_length=50, null=False, verbose_name='멘토 영문명' )
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
  mntr_dt = models.DateField(null=False, verbose_name='멘토 자격 부여일' )
  unv_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 대학교 코드' )
  unv_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 대학교 명' )
  cllg_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 대학 코드' )
  cllg_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 대학 명' )
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 학부/학과 코드' )
  dept_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 학부/학과 명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
  gen = models.CharField(max_length=1, null=False, choices=MS0012_CHOICES, verbose_name='성별' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  exp_dt = models.DateField(null=True, blank=True, verbose_name='멘토 자격 박탈일' )
  exp_rsn = models.CharField(max_length=10, null=True, blank=True, verbose_name='자격박탈 사유' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  tel_no_g = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )
  h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
  post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  bank_acct = models.CharField(max_length=20, null=True, blank=True, verbose_name='은행 계좌 번호' )
  bank_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='은행 코드' )
  bank_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행 명' )
  bank_dpsr = models.CharField(max_length=20, null=True, blank=True, verbose_name='예금주' )
  cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
  cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
  cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
  cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
  inv_agr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='개인정보 동의 여부' )
  inv_agr_dt = models.DateTimeField(null=True, blank=True, verbose_name='개인정보 동의 일시' )
  dept_chr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 ID' )
  dept_chr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  ast_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='조교 명' )
  dept_appr_div = models.CharField(max_length=1, default='N', verbose_name='학과 승인 여부' )
  #dept_appr_dt = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과 승인 날짜' )
  dept_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='학과 승인 날짜' )

  dept_retn_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='학과 반려 사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )


  class Meta:
    verbose_name = '멘토'
    verbose_name_plural =  verbose_name


class mentee(models.Model):
  mnte_id = models.CharField(max_length=16, primary_key=True, verbose_name='멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=False, verbose_name='멘티 명' )
  mnte_nm_e = models.CharField(max_length=50, null=False, verbose_name='멘티 영문명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일(+ 멘티명 → 동일인 찾기)' )
  sch_grd = models.CharField(max_length=1, null=False, verbose_name='학교구분' )
  sch_cd = models.CharField(max_length=10, null=False, verbose_name='학교' )
  sch_nm = models.CharField(max_length=30, null=False, verbose_name='학교명' )
  gen = models.CharField(max_length=1, null=False, verbose_name='성별' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자명' )
  grd_tel = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )



  cursor = connection.cursor()
  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0047'"
  cursor.execute(query)
  MP0047_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())  

  grd_rel = models.CharField(max_length=2, null=True, blank=True, choices=MP0047_CHOICES, verbose_name='보호자 관계(MP0047)' )
  prnt_nat_cd = models.CharField(max_length=10, null=False, verbose_name='부모출신국가코드' )
  prnt_nat_nm = models.CharField(max_length=20, null=False, verbose_name='부모출신국가명' )
  tchr_id = models.CharField(max_length=16, null=False, verbose_name='지도교사 ID' )
  tchr_nm = models.CharField(max_length=20, null=False, verbose_name='지도교사 명' )
  tchr_tel = models.CharField(max_length=20, null=False, verbose_name='지도교사 전화번호' )
  area_city = models.CharField(max_length=10, null=False, verbose_name='시/도' )
  area_gu = models.CharField(max_length=10, null=False, verbose_name='지역구(시/군)' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  s_addr = models.CharField(max_length=200, null=False, verbose_name='학교주소' )
  s_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
  mp_id = models.CharField(max_length=10, null=False, verbose_name='첫 지원 멘토링 프로그램ID' )
  mp_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첫 지원 멘토링 프로그램 명' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='첫 지원 멘토링 지원 NO' )
  mp_dt = models.CharField(max_length=8, null=False, verbose_name='첫 멘토링 시작일' )
  cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
  cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
  cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
  cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pwd = models.CharField(max_length=128, default='1', verbose_name='비밀번호' )



  class Meta:
    verbose_name = '멘티'
    verbose_name_plural =  verbose_name




class guardian(models.Model):
  grdn_id = models.CharField(max_length=16, primary_key=True, verbose_name='보호자ID' )
  grdn_nm = models.CharField(max_length=50, null=False, verbose_name='보호자명' )
  grdn_nm_e = models.CharField(max_length=50, null=False, verbose_name='보호자 영문명' )
  rel_tp = models.CharField(max_length=2, null=True, blank=True, verbose_name='관계(MP0047)' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일(+ 멘티명 → 동일인 찾기)' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  moth_nat_cd = models.CharField(max_length=10, null=False, verbose_name='출신국가코드' )
  moth_nat_nm = models.CharField(max_length=20, null=False, verbose_name='출신국가명' )
  tch_id = models.CharField(max_length=16, null=False, verbose_name='지도교사 ID' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pwd = models.CharField(max_length=128, default='2', verbose_name='비밀번호' )


  class Meta:
    verbose_name = '학부모(보호자 Gardian)'
    verbose_name_plural =  verbose_name





def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class mpgm(models.Model):
  

  cursor = connection.cursor()
  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001'"
  cursor.execute(query)
  MP0001_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0002'")
  MP0002_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

  cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0003'")
  MP0003_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

  cursor.execute("select * from service20_com_cdd where std_grp_code = 'MP0004'")
  MP0004_CHOICES = tuple((c[2], c[4]) for c in cursor.fetchall())

  mp_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘토링 프로그램ID' )
  status = models.CharField(max_length=3, null=True, blank=True, choices=MP0001_CHOICES, verbose_name='상태(MP0001)' )
  mp_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='멘토링 프로그램 명' )
  mp_sname = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토링 프로그램 단명' )
  base_div = models.PositiveIntegerField(null=True, blank=True, verbose_name='기준 프로그램 여부' )
  mp_intro = models.CharField(max_length=1000, null=True, blank=True, verbose_name='프로그램 소개, CMS ID' )
  mng_area = models.CharField(max_length=2, null=True, blank=True,choices=MP0002_CHOICES , verbose_name='프로그램 관리자 영역(MP0002)' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='프로그램 관리자 ID' )
  mgr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='프로그램 관리자 명' )
  mng_org = models.CharField(max_length=10, null=True, blank=True, choices=MP0003_CHOICES, verbose_name='관리기관(MP0003)' )

  sup_org = models.CharField(max_length=10, null=True, blank=True, choices=MP0004_CHOICES, verbose_name='주관기관(MP0004)' )
  yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='연도' )
  yr_seq = models.PositiveIntegerField(null=True, blank=True, verbose_name='차수' )
  apl_ntc_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
  apl_ntc_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )
  apl_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='모집시기' )
  apl_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-시작' )
  apl_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-종료' )
  mnt_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='활동시기' )
  mnt_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
  mnt_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
  tot_apl = models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격' )
  cnt_apl = models.PositiveIntegerField(default=0, verbose_name='지원인원' )
  cnt_doc_suc = models.PositiveIntegerField(default=0, verbose_name='서류전형 합격인원' )
  cnt_doc_res = models.PositiveIntegerField(default=0, verbose_name='서류전형 예비인원(실제 없음)' )
  cnt_intv_pl = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 계획 인원' )
  cnt_intv_ac = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 인원' )
  intv_dt = models.DateField(null=True, blank=True, verbose_name='면접일' )
  cnt_intv_suc = models.PositiveIntegerField(default=0, verbose_name='면접전형 합격인원' )
  cnt_iintv_res = models.PositiveIntegerField(default=0, verbose_name='면접전형 예비합격인원' )
  cnt_trn = models.PositiveIntegerField(default=0, verbose_name='교육인원' )
  cnt_mtr = models.PositiveIntegerField(default=0, verbose_name='최종합격 멘토인원' )
  doc_dt = models.DateTimeField(null=True, blank=True, verbose_name='서류전형예정일' )
  doc_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
  doc_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='면접전형-입력-자' )
  intv_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
  intv_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='면접전형-입력-자' )
  fin_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격 일' )
  fin_in_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격-입력-일' )
  fin_in_mgr = models.CharField(max_length=16, null=True, blank=True, verbose_name='최종합격-입력-자' )
  use_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용 여부' )
  img_src = models.CharField(max_length=100, null=True, blank=True, verbose_name='소개 사진' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  indv_div = models.CharField(max_length=1, default='N', verbose_name='개인/팀여부(MP0057)' )
  mem_cnt = models.PositiveIntegerField(default=1, verbose_name='팀원수(팀인 경우)' )
  mem_min = models.PositiveIntegerField(default=1, verbose_name='팀원수(팀인 경우)-최소' )

  class Meta:
    verbose_name = '교육기부프로그램'
    verbose_name_plural =  verbose_name







class mp_sub(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
  att_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ' )
  att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )
  att_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 단위' )
  use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
  sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta: 
    verbose_name = '교육기부프로그램속성'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "att_id", "att_seq")


class mp_mtr(models.Model):
  cursor = connection.cursor()
  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0012'"
  cursor.execute(query)
  MS0012_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0022'"
  cursor.execute(query)
  MS0022_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())


  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0053'"
  cursor.execute(query)
  MS0053_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())



  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  mntr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='멘토ID' )
  indv_div = models.CharField(max_length=1, null=False, verbose_name='개인/팀여부' )
  team_id = models.CharField(max_length=16, null=False, verbose_name='팀 ID' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자(멘토,학생) 학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='지원자(멘토,학생) 명' )
  apl_nm_e = models.CharField(max_length=50, null=False, verbose_name='지원자(멘토,학생) 영문명' )
  unv_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학교 코드' )
  unv_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 대학교 명' )
  cllg_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학 코드' )
  cllg_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 대학 명' )
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 학부/학과 코드' )
  dept_nm = models.CharField(max_length=30, null=False, verbose_name='지원자 학부/학과 명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
  gen = models.CharField(max_length=1, null=False, choices=MS0012_CHOICES, verbose_name='성별' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, choices=MS0022_CHOICES, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='집전화' )
  tel_no_g = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )
  h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
  post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  bank_acct = models.CharField(max_length=20, null=True, blank=True, verbose_name='은행 계좌 번호' )
  bank_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='은행 코드' )
  bank_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행 명' )
  bank_dpsr = models.CharField(max_length=20, null=True, blank=True, verbose_name='예금주' )
  cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
  cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
  cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
  cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='접수일(지원서 저장)' )
  status = models.CharField(max_length=2, choices=MS0053_CHOICES, null=True, blank=True, verbose_name='상태(MP0053)' )
  doc_cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
  doc_cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
  tot_doc = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='서류전형  총 점수' )
  score1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 석차' )
  score2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 총원' )
  score3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 학점' )
  score4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='봉사점수합계' )
  score5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='자격증 개수' )
  score6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='직전학기 학점' )
  cscore1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수1-성적' )
  cscore2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수2-어학' )
  cscore3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수3-봉사' )
  cscore4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수4-지원서' )
  cscore5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수5-교직' )
  cscore6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수6-거주지' )
  cscore7 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수7-자격증' )
  doc_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='서류심사등수' )
  doc_rslt = models.CharField(max_length=1, null=True, blank=True, choices=(('P','합격'),('N','불합격')), verbose_name='서류심사결과', )
  intv_team = models.PositiveIntegerField(null=True, blank=True, verbose_name='면접팀' )
  intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접일' )
  intv_part_pl = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여계획' )
  intv_np_rsn_pl = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_pl_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여계획 입력일' )
  intv_part_ac = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여여부' )
  intv_np_rsn_ac = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
  intv_part_ac_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여 입력일' )
  intv_tot = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='면접점수' )
  intv_rslt = models.CharField(max_length=1, null=True, blank=True,choices=(('P','합격'),(None,'')), verbose_name='면접심사결과' )
  ms_trn_yn = models.CharField(max_length=1, null=True, blank=True,choices=(('Y','이수'),(None,'')), verbose_name='멘토스쿨 이수여부' )
  fnl_rslt = models.CharField(max_length=1, null=True, blank=True, choices=(('P','합격'),(None,'')), verbose_name='최종합격 여부' )
  mntr_dt = models.DateField(null=True, blank=True, verbose_name='멘토 자격 부여일' )
  acpt_dt = models.DateTimeField(null=True, blank=True, verbose_name='수락일' )
  acpt_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='수락여부' )
  acpt_cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='수락취소 사유(MS0004)' )
  sms_send_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='문자발송번호' )
  inv_agr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='개인정보 동의 여부' )
  inv_agr_dt = models.DateTimeField(null=True, blank=True, verbose_name='개인정보 동의 일시' )
  dept_chr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 ID' )
  dept_chr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  ast_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='조교 명' )
  dept_appr_div = models.CharField(max_length=1, default='N', verbose_name='학과 승인 여부' )

  #dept_appr_dt = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과 승인 날짜' )
  dept_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='학과 승인 날짜' )

  dept_retn_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='학과 반려 사유' )
  id_pic = models.CharField(max_length=100, null=True, blank=True, verbose_name='증명사진 위치' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pr_yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='직전 학년도' )
  pr_sch_yr = models.CharField(max_length=1, null=True, blank=True, verbose_name='직전 학년' )
  pr_term_div = models.CharField(max_length=2, null=True, blank=True, verbose_name='직전학기코드' )
  cmp_term = models.PositiveIntegerField(null=True, blank=True, verbose_name='현재기준 이수학기' )
  ascore1 = models.DecimalField(default=0.0, max_digits=7, decimal_places=2,  verbose_name='가산점1' )
  ascore2 = models.DecimalField(default=0.0, max_digits=7, decimal_places=2,  verbose_name='가산점2' )
  ascore3 = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.0), verbose_name='가산점3' )
  ascore4 = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.0), verbose_name='가산점4' )
  ascore5 = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.0), verbose_name='가산점5' )
  ascore6 = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.0), verbose_name='가산점6' )
  file_job_fav = models.CharField(max_length=100, null=True, blank=True, verbose_name='직업선호도 조사지 파일 경로' )
  intv_cmt = models.CharField(max_length=500, null=True, blank=True, verbose_name='면접심사평' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )
  act_hr = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='총활동 시간' )
  cert_en = models.CharField(max_length=1, default='N', verbose_name='인증서 발급가능' )
  cert_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='인증번호' )
  prnt_dt = models.DateTimeField(null=True, blank=True, verbose_name='인증서 발급일' )
  exc_div = models.CharField(max_length=1, default='N', verbose_name='우수멘토 여부' )




  class Meta:
    verbose_name = '교육기부프로그램지원자및사정'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no")

    index_together = ["mntr_id"]








class mp_mtr_log(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  mntr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='멘토ID' )
  evt_gb = models.CharField(max_length=10, null=False, verbose_name='이벤트구분(MP0055)' )
  evt_dat = models.DateTimeField(null=True, blank=True, verbose_name='이벤트일시' )
  evt_rsn_grp = models.CharField(max_length=6, null=True, blank=True, verbose_name='이벤트 사유(그룹코드 STD_GRP_CODE)' )
  evt_rsn_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='이벤트 사유(공통코드 STD_DETL_CODE)' )
  evt_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name='이벤트 내용' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 지원자(멘토) 로그'
    verbose_name_plural =  verbose_name
    index_together = ["mp_id", "apl_no"]
    index_together = ["mntr_id", "mp_id"]




class mp_mtr_atc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  atc_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ → PK 자동생성 시 필요없음' )
  atc_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  atc_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  atc_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첨부파일종류' )
  atc_file_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첨부파일명' )
  atc_file_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='파일경로' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 지원자(멘토) 첨부파일'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "atc_seq")



class mp_chc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  chc_no = models.PositiveIntegerField(null=False, verbose_name='선택 NO' )
  att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
  att_cdh = models.CharField(max_length=6, null=False, verbose_name='속성 CODE HEADER' )
  att_cdd = models.CharField(max_length=10, null=False, verbose_name='선택 답변 코드' )
  chc_tp = models.CharField(max_length=1, null=True, blank=True, verbose_name='선택유형(MP0087:콤보,라디오,체크)' )
  chc_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='선택 답변 명' )
  chc_seq = models.PositiveIntegerField(null=False, verbose_name='선택 우선순위' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 순서' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '교육기부프로그램지원서선택형답변'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "chc_no")




class mp_ans(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 번호' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
  apl_nm = models.CharField(max_length=20, null=False, verbose_name='지원자 명' )
  sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬' )
  ans_div = models.CharField(max_length=1, default='2', verbose_name='질문구분(CM0003)' )
  ans_t1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='선다형 답' )
  ans_t2 = models.CharField(max_length=1000, null=True, blank=True, verbose_name='수필형 답' )
  ans_t3 = models.CharField(max_length=10, null=True, blank=True, verbose_name='선택 답' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '교육기부프로그램지원서답변'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "apl_no", "ques_no")




class mp_mrk(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)MP0039' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
  item_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='채점항목코드-SEQ별' )
  item_nm = models.CharField(max_length=60, null=True, blank=True, verbose_name='채점항목명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mrk_cmt = models.CharField(max_length=500, null=True, blank=True, verbose_name='심사평' )

  class Meta:
    verbose_name = '교육기부프로그램지원서채점'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "apl_no", "mrk_seq", "mrk_no")



class mp_mrk_h(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링프로그램ID' )
  test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)MP0039' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
  mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
  mrk_id = models.CharField(max_length=16, null=False, verbose_name='채점자 ID' )
  mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
  tot_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='총점' )
  grade = models.CharField(max_length=1, null=True, blank=True, verbose_name='' )
  cov_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '멘토링 프로그램 지원서 채점 합계'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "test_div", "apl_no", "mrk_seq", "mrk_no")




class mp_spc(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  spc_div = models.CharField(max_length=1, null=False, verbose_name='교육구분(MP0064)' )
  status = models.CharField(max_length=2, null=False, verbose_name='상태' )
  spc_name = models.CharField(max_length=100, null=False, verbose_name='학습외 프로그램 명' )
  spc_intro = models.CharField(max_length=1000, null=False, verbose_name='프로그램 소개, CMS ID' )
  yr = models.CharField(max_length=4, null=False, verbose_name='연도' )
  yr_seq = models.PositiveIntegerField(null=False, verbose_name='차수' )
  apl_ntc_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
  apl_ntc_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )
  apl_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='모집시기' )
  apl_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-시작' )
  apl_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-종료' )
  mnt_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='활동시기' )
  mnt_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
  mnt_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
  cnf_dt = models.DateTimeField(null=True, blank=True, verbose_name='참여인원 확정일' )
  appr_tm = models.PositiveIntegerField(null=False, verbose_name='인정시간' )
  tot_apl = models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격' )
  cnt_apl = models.PositiveIntegerField(default=0, verbose_name='지원인원' )
  cnt_pln = models.PositiveIntegerField(default=0, verbose_name='선발 (참여 계획) 인원' )
  cnt_att = models.PositiveIntegerField(default=0, verbose_name='실 참여 인원' )
  use_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용 여부' )
  pic_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='미션사진 첨부 여부' )
  rep_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='보고서 여부' )
  ord_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='모집 선착순 여부' )
  grd_appr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='보호자 승인 여부' )
  tch_appr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='교사 승인 여부' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  day_rand = models.CharField(max_length=10, null=True, blank=True, verbose_name='일별 출석용 난수' )
  atc_file_url = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일경로')
  
  class Meta:
    verbose_name = '학습외 프로그램'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "spc_no")


class mp_spc_sub(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
  att_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ' )
  att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
  att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
  att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )
  att_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 단위' )
  use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
  sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '학습외 프로그램 속성'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "spc_no", "att_id", "att_seq")



class mp_spc_mtr(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='프로그램 지원 NO' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  spc_apl_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램 지원(멘토) NO' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자 학번' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='신청일' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0085)' )
  cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
  cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '학습외 프로그램 참여 멘토'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "spc_no", "spc_apl_no")


class mp_spc_mte(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mnte_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  spc_apl_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램 지원(멘토) NO' )
  mnte_id = models.CharField(max_length=16, null=False, verbose_name='멘티ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='신청일' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='승인일' )
  appr_file = models.CharField(max_length=100, null=True, blank=True, verbose_name='확인서 파일 경로' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0085)' )
  cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
  cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '학습외 프로그램 참여 멘티'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mnte_no", "spc_no", "spc_apl_no")





class mp_mte(models.Model):
  query = "SELECT mp_id, mp_name FROM service20_mpgm"
  cursor.execute(query)
  MPID_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())
  mp_id = models.CharField(max_length=10, null=False, choices=MPID_CHOICES, verbose_name='멘토링 프로그램ID' )

  mnte_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  mnte_id = models.CharField(max_length=16, null=False, verbose_name='멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=False, verbose_name='멘티 명' )
  mnte_nm_e = models.CharField(max_length=50, null=False, verbose_name='멘티 영문명' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일(+ 멘티명 → 동일인 찾기)' )
  mp_hm = models.CharField(max_length=50, null=True, blank=True, verbose_name='멘토링 가능 시간' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0052'"
  cursor.execute(query)
  MP0052_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())


  mp_plc = models.CharField(max_length=1, null=True, blank=True, choices=MP0052_CHOICES, verbose_name='멘토링 장소 구분(MP0052)' )
  mp_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 주소' )
  sch_grd = models.CharField(max_length=1, null=False, verbose_name='학교구분' )
  sch_cd = models.CharField(max_length=10, null=False, verbose_name='학교' )
  sch_nm = models.CharField(max_length=30, null=False, verbose_name='학교명' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0012'"
  cursor.execute(query)
  MS0012_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())
  gen = models.CharField(max_length=1, null=False, choices=MS0012_CHOICES, verbose_name='성별(MS0012)' )

  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
  sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='집전화' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자명' )
  grd_tel = models.CharField(max_length=20, null=True, blank=True, verbose_name='보호자 연락처' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0047'"
  cursor.execute(query)
  MP0047_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  grd_rel = models.CharField(max_length=2, null=True, blank=True, choices=MP0047_CHOICES, verbose_name='보호자 관계(MP0047)' )

  prnt_nat_cd = models.CharField(max_length=10, null=False, verbose_name='부모출신국가코드' )
  prnt_nat_nm = models.CharField(max_length=20, null=False, verbose_name='부모출신국가명' )
  tchr_id = models.CharField(max_length=16, null=False, verbose_name='지도교사 ID' )
  tchr_nm = models.CharField(max_length=50, null=False, verbose_name='지도교사 명' )
  tchr_tel = models.CharField(max_length=20, null=False, verbose_name='지도교사 전화번호' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0048'"
  cursor.execute(query)
  MP0048_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  area_city = models.CharField(max_length=10, null=False, choices=MP0048_CHOICES, verbose_name='시/도(MP0048)' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0049'"
  cursor.execute(query)
  MP0049_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  area_gu = models.CharField(max_length=10, null=False, choices=MP0049_CHOICES, verbose_name='지역구(MP0049)-시/군' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  s_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='학교주소' )
  s_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='접수일(지원서 저장)' )

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0054'"
  cursor.execute(query)
  MP0054_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())
  status = models.CharField(max_length=2, null=True, blank=True, choices=MP0052_CHOICES, verbose_name='상태(MP0054)' )

  day_rand = models.CharField(max_length=10, null=True, blank=True, verbose_name='일별 출석용 난수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  m_lat = models.DecimalField(max_digits=10, decimal_places=7, default=0, verbose_name='멘토링 장소 위도' )
  m_lon = models.DecimalField(max_digits=10, decimal_places=7, default=0, verbose_name='멘토링 장소 경도' )


  class Meta:
    verbose_name = '멘토멘티매칭'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mnte_no")







class mp_mte_log(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mnte_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
  mnte_id = models.CharField(max_length=16, null=False, verbose_name='멘티ID' )
  evt_gb = models.CharField(max_length=6, null=False, verbose_name='이벤트구분(MP0055)' )
  evt_dat = models.DateTimeField(null=True, blank=True, verbose_name='이벤트일시' )
  evt_rsn_grp = models.CharField(max_length=6, null=True, blank=True, verbose_name='이벤트 사유(그룹코드 STD_GRP_CODE)' )
  evt_rsn_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='이벤트 사유(공통코드 STD_DETL_CODE)' )
  evt_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name='이벤트 내용' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta: 
    verbose_name = '프로그램 지원자(멘티) 로그'
    verbose_name_plural =  verbose_name
    index_together = ["mp_id", "mnte_no"]
    index_together = ["mnte_id", "mp_id"]




class cm_apl_q(models.Model):
  ques_no = models.PositiveIntegerField(primary_key=True, verbose_name='질문NO' )
  ans_type = models.CharField(max_length=1, null=False, verbose_name='질문유형' )
  ques_desc = models.CharField(max_length=500, null=False, verbose_name='질문지' )
  sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬' )
  use_yn = models.CharField(max_length=1, null=False, verbose_name='사용여부' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '지원서 질문'
    verbose_name_plural =  verbose_name


### 강주원 작업 시작
class cm_surv(models.Model):
  cursor = connection.cursor()

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'CM0001'"
  cursor.execute(query)
  CM0001_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'CM0002'"
  cursor.execute(query)
  CM0002_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'CM0003'"
  cursor.execute(query)
  CM0003_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  query = "select std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'CM0005'"
  cursor.execute(query)
  CM0005_CHOICES = tuple((c[0], c[1]) for c in cursor.fetchall())

  ques_no = models.PositiveIntegerField(primary_key=True, verbose_name='만족도 조사 항목 ID' )
  ansr_div = models.CharField(max_length=1, null=False, choices=CM0001_CHOICES, verbose_name='응답자 구분(CM0001)' )
  ques_type = models.CharField(max_length=1, null=False, choices=CM0002_CHOICES, verbose_name='질문유형(CM0002)' )
  ques_div = models.CharField(max_length=1, null=False, choices=CM0003_CHOICES, verbose_name='질문구분(CM0003)' )
  ques_desc = models.CharField(max_length=500, null=False, verbose_name='질문지' )
  use_yn = models.CharField(max_length=1, default='Y', choices=CM0005_CHOICES, verbose_name='사용여부(CM0005)' )
  sort_seq = models.PositiveIntegerField(null=True, blank=True, verbose_name='정렬 순서' )

  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '만족도 조사 문항'
    verbose_name_plural =  verbose_name

# 강주원 작업 종료


class cm_surv_t(models.Model):
  surv_id = models.PositiveIntegerField(primary_key=True, verbose_name='문항세트 ID' )
  surv_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='문항세트 명' )
  surv_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name='문항세트 설명' )
  ansr_div = models.CharField(max_length=1, null=False, verbose_name='응답자 구분(CM0001)' )
  ques_cnt = models.PositiveIntegerField(default=0, verbose_name='만족도 조사 항목 수' )
  use_yn = models.CharField(max_length=1, default='Y', verbose_name='사용여부(CM0005)' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '만족도 조사 출제 세트'
    verbose_name_plural =  verbose_name


class cm_surv_q(models.Model):
  surv_id = models.PositiveIntegerField(null=False, verbose_name='문항세트 ID' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='만족도 조사 항목 ID' )
  sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬 순서' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '만족도 조사 출제 문항'
    verbose_name_plural =  verbose_name
    unique_together=("surv_id", "ques_no")


class cm_surv_p(models.Model):
  pgm_id = models.CharField(max_length=10, null=False, verbose_name='만족도 조사 대상(멘토스쿨, 프로그램, 학습외)' )
  surv_seq = models.PositiveIntegerField(null=False, verbose_name='만족도 SEQ' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  surv_tp = models.CharField(max_length=2, null=False, verbose_name='대상 내 유형' )
  surv_ttl = models.CharField(max_length=50, null=True, blank=True, verbose_name='만족도 조사 제목' )
  surv_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name='만족도 조사 내용' )
  ntc_sdt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
  ntc_edt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )
  surv_sdt = models.DateTimeField(null=True, blank=True, verbose_name='만족도 조사 시작일' )
  surv_edt = models.DateTimeField(null=True, blank=True, verbose_name='만족도 조사 종료일' )
  cmp_dt = models.DateTimeField(null=True, blank=True, verbose_name='완료일' )
  status = models.CharField(max_length=2, default='10', verbose_name='상태(CM0008)' )
  avg_ans_t1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='오지선다형 평균' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램별 만족도 조사 관리'
    verbose_name_plural =  verbose_name
    unique_together=("pgm_id", "surv_seq")

class cm_surv_h(models.Model):
  pgm_id = models.CharField(max_length=10, null=False, verbose_name='만족도 조사 대상(멘토스쿨, 프로그램, 학습외)' )
  surv_seq = models.PositiveIntegerField(null=False, verbose_name='만족도 SEQ' )
  ansr_id = models.CharField(max_length=16, null=False, verbose_name='응답자 ID' )
  surv_id = models.PositiveIntegerField(null=False, verbose_name='문항세트 ID' )
  ansr_div = models.CharField(max_length=1, null=False, verbose_name='응답자 구분(CM0001)' )
  avg_ans_t1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='오지선다형 평균' )
  surv_dt = models.DateTimeField(null=True, blank=True, verbose_name='만족도 조사일' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(CM0006)' )
  mnte_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당멘티명' )
  tchr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당교사ID' )
  tchr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당교사명' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '만족도 조사 답변 헤드'
    verbose_name_plural =  verbose_name
    unique_together=("pgm_id", "surv_seq", "ansr_id")




class cm_surv_a(models.Model):
  pgm_id = models.CharField(max_length=10, null=False, verbose_name='만족도 조사 대상(멘토스쿨, 프로그램, 학습외)' )
  surv_seq = models.PositiveIntegerField(null=False, verbose_name='만족도 SEQ' )
  ansr_id = models.CharField(max_length=16, null=False, verbose_name='응답자 ID' )
  ques_no = models.PositiveIntegerField(null=False, verbose_name='만족도 조사 항목 ID' )
  surv_id = models.PositiveIntegerField(null=False, verbose_name='문항세트 ID' )
  ansr_div = models.CharField(max_length=1, null=False, verbose_name='응답자 구분(CM0001)' )
  ans_t1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='선다형 답' )
  ans_t2 = models.CharField(max_length=1000, null=True, blank=True, verbose_name='수필형 답' )
  ans_t3 = models.CharField(max_length=10, null=True, blank=True, verbose_name='선택 답' )
  ques_dt = models.CharField(max_length=8, null=False, verbose_name='설문조사일자' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '만족도 조사 답변 상세'
    verbose_name_plural =  verbose_name
    unique_together=("pgm_id", "surv_seq", "ansr_id", "ques_no")




class cm_cnv_scr(models.Model):
  eval_item = models.CharField(max_length=2, null=False, verbose_name='항목(MS0023)' )
  eval_cd = models.CharField(max_length=10, null=False, verbose_name='항목 종류' )
  eval_seq = models.PositiveIntegerField(null=False, verbose_name='순서' )
  eval_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='점수/코드 종류' )
  min_scr = models.PositiveIntegerField(null=False, verbose_name='최소 점수' )
  max_scr = models.PositiveIntegerField(null=False, verbose_name='최대 점수' )
  grade = models.CharField(max_length=50, null=False, verbose_name='코드 점수' )
  eval_unit = models.CharField(max_length=10, null=False, verbose_name='단위' )
  fin_scr = models.PositiveIntegerField(null=False, verbose_name='점수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '점수변환표'
    verbose_name_plural =  verbose_name
    unique_together=("eval_item", "eval_cd", "eval_seq")


class mp_cnv_scr(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  eval_item = models.CharField(max_length=2, null=False, verbose_name='항목(MS0023)' )
  eval_cd = models.CharField(max_length=10, null=False, verbose_name='항목 종류' )
  eval_seq = models.PositiveIntegerField(null=False, verbose_name='순서' )
  eval_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='점수/코드 종류' )
  min_scr = models.PositiveIntegerField(null=False, verbose_name='최소 점수' )
  max_scr = models.PositiveIntegerField(null=False, verbose_name='최대 점수' )
  grade = models.CharField(max_length=50, null=False, verbose_name='코드 점수' )
  eval_unit = models.CharField(max_length=10, null=False, verbose_name='단위' )
  fin_scr = models.PositiveIntegerField(null=False, verbose_name='점수' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램별 점수변환(환산)표'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "eval_item", "eval_cd", "eval_seq")




class cm_sms(models.Model):
  sys_menu_id = models.CharField(max_length=8, null=False, verbose_name='사용 프로그램 ID' )
  seq = models.PositiveIntegerField(null=False, verbose_name='순번' )
  msg_gbn_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='메세지구분명' )
  msg_ttl = models.CharField(max_length=100, null=True, blank=True, verbose_name='메세지제목' )
  msg_ctnt = models.CharField(max_length=2000, null=True, blank=True, verbose_name='메세지내용' )
  reply_telno = models.CharField(max_length=20, null=True, blank=True, verbose_name='회신번호' )
  msg_fg = models.CharField(max_length=1, null=True, blank=True, verbose_name='메세지구분{E0610}' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '문자메시지 형식'
    verbose_name_plural =  verbose_name
    unique_together=("sys_menu_id", "seq")


class mp_plnh(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  pln_weeks = models.PositiveIntegerField(null=False, verbose_name='계획 주차 수' )
  mtr_sub = models.CharField(max_length=50, null=True, blank=True, verbose_name='지도과목' )
  mtr_obj = models.CharField(max_length=1000, null=True, blank=True, verbose_name='학습목표' )
  pln_dt = models.DateTimeField(null=True, blank=True, verbose_name='계획작성일' )
  req_dt = models.DateTimeField(null=True, blank=True, verbose_name='승인요청일' )
  mnte_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당멘티명' )
  tchr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당교사ID' )
  tchr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당교사명' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자명' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램 수행 계획서'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no")

    index_together = ["apl_no"]


    

class mp_plnd(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )

  pln_no = models.PositiveIntegerField(null=False, verbose_name='계획 주차' )
  pln_sdt = models.DateField(null=True, blank=True, verbose_name='주 교육시작일(일)' )
  pln_edt = models.DateField(null=True, blank=True, verbose_name='주 교육종료일(토)' )
  mtr_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='멘토링 내용' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 수행 계획서 상세'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "pln_no")

    index_together = ["apl_no"]

class mp_att(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  att_no = models.PositiveIntegerField(null=False, verbose_name='출석순서(SEQ)' )
  mp_div = models.CharField(max_length=1, null=False, choices=MP0059_CHOICES, verbose_name='교육구분(MP0059)' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  att_div = models.CharField(max_length=1, null=False, choices=MP0063_CHOICES, verbose_name='출석구븐(MP0063)' )
  att_sts = models.CharField(max_length=1, null=False, choices=MP0060_CHOICES, verbose_name='출석 상태(MP0060)' )
  att_sdt = models.DateTimeField(null=True, blank=True, verbose_name='출석일시(교육시작일시)' )
  att_saddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 시작주소' )
  att_slat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 위도' )
  att_slon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 경도' )
  att_sdist = models.PositiveIntegerField(null=True, blank=True, verbose_name='멘토링 주소 거리(m)' )
  att_edt = models.DateTimeField(null=True, blank=True, verbose_name='교육종료일시' )
  att_eaddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 종료주소' )
  att_elat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 종료지 위도' )
  att_elon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 종료지 경도' )
  att_edist = models.PositiveIntegerField(null=True, blank=True, verbose_name='멘토링 주소 거리(m)' )
  elap_tm = models.TimeField(null=True, blank=True, verbose_name='경과시간' )
  appr_tm = models.PositiveIntegerField(null=True, blank=True, verbose_name='인정시간' )
  mtr_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='멘토링 내용(보고서)' )
  mtr_pic = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  expl_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='소명상태' )
  rep_no = models.PositiveIntegerField(null=True, blank=True, verbose_name='보고서 NO' )
  exp_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='활동비 지급여부(MP0061)' )
  exp_no = models.PositiveIntegerField(null=True, blank=True, verbose_name='활동비 지급 NO' )
  exp_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동비 지급일' )
  exp_amt = models.PositiveIntegerField(null=True, blank=True, verbose_name='지급 활동비' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  appr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='승인 반려 사유' )
  mgr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='관리자 반려 사유' )
  appr_div = models.CharField(max_length=1, default='N', verbose_name='학부모/교사 승인 상태' )
  mgr_div = models.CharField(max_length=1, default='N', verbose_name='관리자 승인 상태' )
  qr_div = models.CharField(max_length=1, default='N', verbose_name='QR 스켄 여부' )  
  mtr_pic2 = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )
  mtr_pic3 = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )
  mtr_pic4 = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )
  mtr_pic5 = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )


  class Meta:
    verbose_name = '프로그램 출석부(멘토)'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "att_no")

    index_together = ["apl_no"]




class mp_att_mte(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  mnte_no = models.PositiveIntegerField(null=False, verbose_name='멘티 지원 NO' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  att_no = models.PositiveIntegerField(null=False, verbose_name='출석순서(SEQ)' )
  att_div = models.CharField(max_length=1, null=False, verbose_name='출석구분(MP0063)' )
  att_sdt = models.DateTimeField(null=True, blank=True, verbose_name='교육시작일시' )
  att_edt = models.DateTimeField(null=True, blank=True, verbose_name='교육종료일시' )
  elap_tm = models.TimeField(null=True, blank=True, verbose_name='경과시간' )
  appr_tm = models.PositiveIntegerField(null=True, blank=True, verbose_name='인정시간' )
  mtr_thght = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 소감' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 출석부(멘티)'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "mnte_no", "apl_no", "att_no")

    index_together = ["apl_no"]
    index_together = ["mnte_no"]

    

class mp_att_req(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  req_no = models.PositiveIntegerField(null=False, verbose_name='소명순서(SEQ)' )
  att_no = models.PositiveIntegerField(null=False, verbose_name='출석순서(SEQ)' )
  mp_div = models.CharField(max_length=1, null=False, verbose_name='교육구분(MP0059)' )
  spc_no = models.PositiveIntegerField(null=False, verbose_name='학습외 프로그램NO' )
  f_att_div = models.CharField(max_length=1, null=False, verbose_name='출석구분(MP0063)' )
  f_att_sts = models.CharField(max_length=1, null=False, verbose_name='출석 상태(MP0060)' )
  f_att_sdt = models.DateTimeField(null=True, blank=True, verbose_name='출석일시(교육시작일시)' )
  f_att_saddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 시작주소' )
  f_att_slat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 위도' )
  f_att_slon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 경도' )
  f_att_sdist = models.PositiveIntegerField(null=True, blank=True, verbose_name='멘토링 주소 거리(m)' )
  f_att_edt = models.DateTimeField(null=True, blank=True, verbose_name='교육종료일시' )
  f_att_eaddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 종료주소' )
  f_att_elat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 위도' )
  f_att_elon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='멘토링 시작지 경도' )
  f_att_edist = models.PositiveIntegerField(null=True, blank=True, verbose_name='멘토링 주소 거리(m)' )
  f_elap_tm = models.TimeField(null=True, blank=True, verbose_name='경과시간' )
  f_appr_tm = models.PositiveIntegerField(null=True, blank=True, verbose_name='인정시간' )
  f_mtr_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='멘토링 내용(보고서)' )
  f_mtr_pic = models.CharField(max_length=200, null=True, blank=True, verbose_name='멘토링 사진(url)' )
  f_appr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='승인자ID' )
  f_appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  f_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  f_mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  f_mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  t_req_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='소명 내용' )
  t_att_div = models.CharField(max_length=1, null=False, verbose_name='소명-출석구분(MP0063)' )
  t_att_sts = models.CharField(max_length=1, null=False, verbose_name='소명-출석 상태(MP0060)' )
  t_att_sdt = models.DateTimeField(null=True, blank=True, verbose_name='소명-출석일시(교육시작일시)' )
  t_att_saddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='소명-멘토링 시작주소' )
  t_att_slat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='소명-멘토링 시작지 위도' )
  t_att_slon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='소명-멘토링 시작지 경도' )
  t_att_sdist = models.PositiveIntegerField(null=True, blank=True, verbose_name='소명-멘토링 주소 거리(m)' )
  t_att_edt = models.DateTimeField(null=True, blank=True, verbose_name='소명-교육종료일시' )
  t_att_eaddr = models.CharField(max_length=200, null=True, blank=True, verbose_name='소명-멘토링 종료주소' )
  t_att_elat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='소명-멘토링 시작지 위도' )
  t_att_elon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='소명-멘토링 시작지 경도' )
  t_att_edist = models.PositiveIntegerField(null=True, blank=True, verbose_name='소명-멘토링 주소 거리(m)' )
  t_elap_tm = models.TimeField(null=True, blank=True, verbose_name='소명-경과시간' )
  t_appr_tm = models.PositiveIntegerField(null=True, blank=True, verbose_name='소명-인정시간' )
  t_mtr_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='소명-멘토링 내용(보고서)' )
  t_mtr_pic = models.CharField(max_length=200, null=True, blank=True, verbose_name='소명-멘토링 사진(url)' )
  t_appr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='소명-승인자ID' )
  t_appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='소명-승인자명' )
  t_appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='소명-보호자 승인일시' )
  t_mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='소명-관리자ID' )
  t_mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='소명-관리자 승인일시' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  f_appr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='승인 반려 사유' )
  f_mgr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='관리자 반려 사유' )
  t_appr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='소명 승인 반려 사유' )
  t_mgr_ret_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='소명 관리자 반려 사유' )



  class Meta:
    verbose_name = '프로그램 출석 소명'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "req_no")

    index_together = ["apl_no"]






class mp_rep(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  rep_no = models.PositiveIntegerField(null=False, verbose_name='보고서 NO' )
  rep_div = models.CharField(max_length=1, null=False, verbose_name='보고서 구분(MP0062)' )
  rep_ym = models.CharField(max_length=6, null=True, blank=True, verbose_name='보고서 연월(월보고)' )
  mnte_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당멘티명' )
  tchr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당교사ID' )
  tchr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당교사명' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자명' )
  sch_nm = models.CharField(max_length=30, null=True, blank=True, verbose_name='학교명' )
  mtr_sub = models.CharField(max_length=50, null=True, blank=True, verbose_name='지도과목' )
  att_desc = models.CharField(max_length=50, null=True, blank=True, verbose_name='출석현황' )
  rep_ttl = models.CharField(max_length=200, null=True, blank=True, verbose_name='보고서 제목' )
  mtr_obj = models.CharField(max_length=4000, null=True, blank=True, verbose_name='학습목표' )
  rep_dt = models.DateTimeField(null=True, blank=True, verbose_name='보고서작성일' )
  req_dt = models.DateTimeField(null=True, blank=True, verbose_name='승인요청일' )
  mtr_desc = models.CharField(max_length=4000, null=True, blank=True, verbose_name='학습내용' )
  coatching = models.CharField(max_length=4000, null=True, blank=True, verbose_name='학습외 지도(상담)' )
  spcl_note = models.CharField(max_length=4000, null=True, blank=True, verbose_name='특이사항' )
  mtr_revw = models.CharField(max_length=4000, null=True, blank=True, verbose_name='소감문' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0070)' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 보고서'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "rep_no")

    index_together = ["apl_no", "mp_id"]
    index_together = ["apl_no"]







class mp_exp(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  exp_no = models.PositiveIntegerField(null=False, verbose_name='활동비 NO' )
  exp_mon = models.CharField(max_length=6, null=False, verbose_name='활동비 월' )
  exp_div = models.CharField(max_length=1, null=False, verbose_name='활동비 구분' )
  exp_ttl = models.CharField(max_length=200, null=True, blank=True, verbose_name='활동비 제목' )
  exp_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동비 작성일' )
  bank_dt = models.DateTimeField(null=True, blank=True, verbose_name='은행 자료 작성일' )
  elap_tm = models.TimeField(null=True, blank=True, verbose_name='활동시간 합계' )
  unit_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='시급(단가)' )
  appr_tm = models.PositiveIntegerField(null=True, blank=True, verbose_name='인정시간 합계' )
  sum_exp = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='활동비=APPR_TM * UNIT_PRICE' )
  bank_acct = models.CharField(max_length=20, null=True, blank=True, verbose_name='은행 계좌 번호' )
  bank_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='은행 코드' )
  bank_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행 명' )
  bank_dpsr = models.CharField(max_length=20, null=True, blank=True, verbose_name='예금주' )
  mp_sname = models.CharField(max_length=20, null=True, blank=True, verbose_name='입금자명-멘토링 프로그램 단명' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램 활동비'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "exp_no")
    index_together = ["apl_no", "mp_id"]
    index_together = ["apl_no"]





class mp_mtr_fe(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  fe_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  lang_kind_cd = models.CharField(max_length=4, null=False, verbose_name='어학종류코드' )
  lang_kind_nm = models.CharField(max_length=100, null=False, verbose_name='어학종류명' )
  lang_cd = models.CharField(max_length=3, null=False, verbose_name='어학상위코드' )
  lang_nm = models.CharField(max_length=100, null=False, verbose_name='어학상위코드명' )
  lang_detail_cd = models.CharField(max_length=2, null=False, verbose_name='어학하위코드' )
  lang_detail_nm = models.CharField(max_length=100, null=False, verbose_name='어학하위코드명' )
  frexm_cd = models.CharField(max_length=10, null=False, verbose_name='외국어시험 코드' )
  frexm_nm = models.CharField(max_length=200, null=False, verbose_name='외국어시험명' )
  score = models.CharField(max_length=30, null=False, verbose_name='시험점수' )
  grade = models.CharField(max_length=50, null=False, verbose_name='시험등급' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '프로그램 지원자(멘토) 어학 점수'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "fe_no")






class mte_grd(models.Model):
  mnte_id = models.CharField(max_length=16, null=False, verbose_name='멘티ID' )
  grdn_id = models.CharField(max_length=16, null=False, verbose_name='보호자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '멘티 보호자(n:n)→필요한 경우'
    verbose_name_plural =  verbose_name
    unique_together=("mnte_id", "grdn_id")

class teacher(models.Model):
  tchr_id = models.CharField(max_length=12, primary_key=True, verbose_name='교사 ID(학교별 부여)' )
  tchr_nm = models.CharField(max_length=50, null=False, verbose_name='교사명' )
  tchr_nm_e = models.CharField(max_length=50, null=False, verbose_name='교사 영문명' )
  sch_grd = models.CharField(max_length=1, null=False, verbose_name='학교구분' )
  sch_cd = models.CharField(max_length=10, null=False, verbose_name='학교' )
  sch_nm = models.CharField(max_length=30, null=False, verbose_name='학교명' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='사무실전화' )
  area_city = models.CharField(max_length=10, null=False, verbose_name='시/도' )
  area_gu = models.CharField(max_length=10, null=False, verbose_name='지역구(시/군)' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  s_addr = models.CharField(max_length=200, null=False, verbose_name='학교주소' )
  s_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  pwd = models.CharField(max_length=128, default='3', verbose_name='비밀번호' )

  class Meta:
    verbose_name = '교사(학교)'
    verbose_name_plural =  verbose_name



class manager(models.Model):
  mgr_id = models.CharField(max_length=16, primary_key=True, verbose_name='관리자 ID(교직원 번호)' )
  mgr_nm = models.CharField(max_length=50, null=False, verbose_name='관리자 명' )
  mgr_nm_e = models.CharField(max_length=50, null=False, verbose_name='관리자 영문명' )
  mng_area = models.CharField(max_length=2, null=True, blank=True, verbose_name='프로그램 관리 영역' )
  mgr_div = models.CharField(max_length=1, null=False, verbose_name='관리자구분' )
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='부서코드' )
  dept_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='부서명' )
  ofc_lvl_cd = models.CharField(max_length=10, null=False, verbose_name='직급코드' )
  ofc_lvl_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직급명' )
  func_cd = models.CharField(max_length=10, null=False, verbose_name='직책코드' )
  func_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직책명' )
  status = models.CharField(max_length=1, default= '1', verbose_name='상태값' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='사무실전화' )
  h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '멘토링 담당자'
    verbose_name_plural =  verbose_name

    
class dept_ast(models.Model):
  ast_id = models.CharField(max_length=10, primary_key=True, verbose_name='조교 ID(교직원 번호)' )
  ast_nm = models.CharField(max_length=50, null=False, verbose_name='조교 명' )
  ast_nm_e = models.CharField(max_length=50, null=True, blank=True, verbose_name='조교 영문명' )
  dept_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과코드' )
  dept_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='학과명' )
  ofc_lvl_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='직급코드' )
  ofc_lvl_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직급명' )
  func_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='직책코드' )
  func_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='직책명' )
  status = models.CharField(max_length=1, default= '1', verbose_name='상태값' )
  mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='사무실전화' )
  h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
  h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  dean_emp_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 교번' )
  dean_emp_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  dean_jw_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과코드' )
  dean_jw_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='학과명' )
  dean_mob_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='휴대전화' )
  dean_tel_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='사무실전화' )
  dean_email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )

  class Meta:
    verbose_name = '학과조교승인(관리자)'
    verbose_name_plural =  verbose_name


    index_together = ["ast_id", "mjr_cd"]



class dept_ast_dean(models.Model):
  dept_cd = models.CharField(max_length=10, null=False, verbose_name='학과코드' )
  dept_nm = models.CharField(max_length=100, null=False, verbose_name='학과명' )
  mjr_cd = models.CharField(max_length=6, null=True, blank=True, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='전공명' )
  ast_id = models.CharField(max_length=10, null=False, verbose_name='조교 ID(교직원 번호)' )
  ast_nm = models.CharField(max_length=50, null=False, verbose_name='조교 명' )
  dean_emp_id = models.CharField(max_length=16, null=False, verbose_name='학과장 교번' )
  dean_emp_nm = models.CharField(max_length=50, null=False, verbose_name='학과장 명' )
  use_div = models.CharField(max_length=1, default= 'Y', verbose_name='상태값' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '학과,전공 조교,학과장 매칭'
    verbose_name_plural =  verbose_name



class ms_apl_fe(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  fe_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  lang_kind_cd = models.CharField(max_length=4, null=False, verbose_name='어학종류코드' )
  lang_kind_nm = models.CharField(max_length=100, null=False, verbose_name='어학종류명' )
  lang_cd = models.CharField(max_length=3, null=False, verbose_name='어학상위코드' )
  lang_nm = models.CharField(max_length=100, null=False, verbose_name='어학상위코드명' )
  lang_detail_cd = models.CharField(max_length=2, null=False, verbose_name='어학하위코드' )
  lang_detail_nm = models.CharField(max_length=100, null=False, verbose_name='어학하위코드명' )
  frexm_cd = models.CharField(max_length=10, null=False, verbose_name='외국어시험 코드' )
  frexm_nm = models.CharField(max_length=200, null=False, verbose_name='외국어시험명' )
  score = models.CharField(max_length=30, null=False, verbose_name='시험점수' )
  grade = models.CharField(max_length=50, null=False, verbose_name='시험등급' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )




  class Meta:
    verbose_name = '멘토스쿨 지원자 어학점수'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "apl_no", "fe_no")

class mp_mtr_sa(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  sa_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  nation_inout_cd = models.CharField(max_length=4, null=False, verbose_name='국내외구분코드' )
  nation_inout_nm = models.CharField(max_length=100, null=False, verbose_name='국내외구분명' )
  sch_inout_cd = models.CharField(max_length=4, null=False, verbose_name='교내외구분코드' )
  sch_inout_nm = models.CharField(max_length=100, null=False, verbose_name='교내외구분명' )
  activity_nm = models.CharField(max_length=200, null=False, verbose_name='봉사명' )
  manage_org_nm = models.CharField(max_length=100, null=False, verbose_name='주관기관명' )
  start_date = models.CharField(max_length=10, null=False, verbose_name='시작일자' )
  start_time = models.CharField(max_length=4, null=False, verbose_name='시작시간' )
  end_date = models.CharField(max_length=10, null=False, verbose_name='종료일자' )
  end_time = models.CharField(max_length=4, null=False, verbose_name='종료시간' )
  tot_time = models.CharField(max_length=4, null=True, blank=True, verbose_name='총시간' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )




  class Meta:
    verbose_name = '프로그램 지원자(멘토) 봉사 리스트'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "sa_no")



class ms_apl_sa(models.Model):
  ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
  sa_no = models.PositiveIntegerField(null=False, verbose_name='어학점수 NO' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  nation_inout_cd = models.CharField(max_length=4, null=False, verbose_name='국내외구분코드' )
  nation_inout_nm = models.CharField(max_length=100, null=False, verbose_name='국내외구분명' )
  sch_inout_cd = models.CharField(max_length=4, null=False, verbose_name='교내외구분코드' )
  sch_inout_nm = models.CharField(max_length=100, null=False, verbose_name='교내외구분명' )
  activity_nm = models.CharField(max_length=200, null=False, verbose_name='봉사명' )
  manage_org_nm = models.CharField(max_length=100, null=False, verbose_name='주관기관명' )
  start_date = models.CharField(max_length=10, null=False, verbose_name='시작일자' )
  start_time = models.CharField(max_length=4, null=False, verbose_name='시작시간' )
  end_date = models.CharField(max_length=10, null=False, verbose_name='종료일자' )
  end_time = models.CharField(max_length=4, null=False, verbose_name='종료시간' )
  tot_time = models.CharField(max_length=4, null=True, blank=True, verbose_name='총시간' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '프로그램 지원자(멘토) 봉사 리스트'
    verbose_name_plural =  verbose_name
    unique_together=("ms_id", "apl_no", "sa_no")






class vw_nanum_service_activ(models.Model):
  apl_id = models.CharField(max_length=20, null=False, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  nation_inout_cd = models.CharField(max_length=4, null=False, verbose_name='국내외구분코드' )
  nation_inout_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='국내외구분명' )
  sch_inout_cd = models.CharField(max_length=4, null=False, verbose_name='교내외구분코드' )
  sch_inout_nm = models.CharField(max_length=100, null=False, verbose_name='교내외구분명' )
  activity_nm = models.CharField(max_length=200, null=False, verbose_name='봉사명' )
  manage_org_nm = models.CharField(max_length=100, null=False, verbose_name='주관기관명' )
  start_date = models.CharField(max_length=10, null=False, verbose_name='시작일자' )
  start_time = models.CharField(max_length=4, null=False, verbose_name='시작시간' )
  end_date = models.CharField(max_length=10, null=False, verbose_name='종료일자' )
  end_time = models.CharField(max_length=4, null=False, verbose_name='종료시간' )
  tot_time = models.CharField(max_length=4, null=False, verbose_name='총시간' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '학생 봉사 시간 VIEW(임시)'
    verbose_name_plural =  verbose_name





class vw_nanum_foreign_exam(models.Model):
  apl_id = models.CharField(max_length=10, null=False, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  lang_kind_cd = models.CharField(max_length=4, null=False, verbose_name='어학종류코드' )
  lang_kind_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='어학종류명' )
  lang_cd = models.CharField(max_length=3, null=False, verbose_name='어학상위코드' )
  lang_nm = models.CharField(max_length=100, null=False, verbose_name='어학상위코드명' )
  lang_detail_cd = models.CharField(max_length=2, null=False, verbose_name='어학하위코드' )
  lang_detail_nm = models.CharField(max_length=100, null=False, verbose_name='어학하위코드명' )
  frexm_nm = models.CharField(max_length=200, null=False, verbose_name='외국어시험명' )
  score = models.CharField(max_length=30, null=False, verbose_name='시험점수' )
  grade = models.CharField(max_length=50, null=False, verbose_name='시험등급' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '유효한 외국어 성적 리스트 VIEW(임시)'
    verbose_name_plural =  verbose_name


class vw_nanum_stdt(models.Model):
  apl_id = models.CharField(max_length=10, null=False, verbose_name='학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='성명' )
  apl_nm_e = models.CharField(max_length=150, null=True, blank=True, verbose_name='성명_영문' )
  unv_cd = models.CharField(max_length=1, null=False, verbose_name='대학교코드' )
  unv_nm = models.CharField(max_length=1, null=False, verbose_name='대학교명' )
  grad_div_cd = models.CharField(max_length=2, null=False, verbose_name='대학원구분코드' )
  grad_div_nm = models.CharField(max_length=4, null=False, verbose_name='대학원구분명' )
  cllg_cd = models.CharField(max_length=6, null=False, verbose_name='대학코드' )
  cllg_nm = models.CharField(max_length=50, null=False, verbose_name='대학명' )
  dept_cd = models.CharField(max_length=6, null=False, verbose_name='학과코드' )
  dept_nm = models.CharField(max_length=50, null=False, verbose_name='학과명' )
  mjr_cd = models.CharField(max_length=6, null=False, verbose_name='전공코드' )
  mjr_nm = models.CharField(max_length=50, null=False, verbose_name='전공명' )
  brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
  gen_cd = models.CharField(max_length=1, null=False, verbose_name='성별코드' )
  gen_nm = models.CharField(max_length=2, null=False, verbose_name='성별명' )
  yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
  sch_yr = models.DecimalField(max_digits=5, decimal_places=0, null=False, verbose_name='학년' )
  term_div = models.CharField(max_length=2, null=False, verbose_name='학기코드' )
  term_nm = models.CharField(max_length=5, null=True, blank=True, verbose_name='학기명' )
  stds_div = models.CharField(max_length=2, null=True, blank=True, verbose_name='학적상태코드' )
  stds_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='학적상태명' )
  mob_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='휴대전화번호' )
  tel_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='집전화' )
  tel_no_g = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자연락처' )
  h_addr = models.CharField(max_length=400, null=True, blank=True, verbose_name='집주소' )
  post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
  email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일주소' )
  bank_acct = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행계좌번호' )
  bank_cd = models.CharField(max_length=3, default=0, verbose_name='은행코드' )
  bank_nm = models.CharField(max_length=50, default=0, verbose_name='은행명' )
  bank_dpsr = models.CharField(max_length=50, default=0, verbose_name='예금주' )
  pr_yr = models.CharField(max_length=4, default=0, verbose_name='직전 학년도' )
  pr_sch_yr = models.CharField(max_length=1, null=True, blank=True, verbose_name='직전 학년' )
  pr_term_div = models.CharField(max_length=2, null=True, blank=True, verbose_name='직전학기코드')
  cmp_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='전체 이수학기' )
  score01 = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='직전학기 석차' )
  score02 = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='직전학기 총원' )
  score03 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='직전학기 학점' )
  score04 = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='봉사점수합계' )
  score05 = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='자격증 개수' )
  score06 = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='직전학기이수학점' )
  dept_chr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='학과장 ID' )
  dept_chr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과장 명' )
  ast_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='학과 조교 ID' )
  ast_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='학과 조교명' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '부산대학교 학생 정보'
    verbose_name_plural =  verbose_name




#개인정보동의약관
class agree_cont1(models.Model):
  title = models.CharField(max_length=255, null=True, blank=True, verbose_name='타이틀' )
  code = models.CharField(max_length=10, null=True, blank=True, verbose_name='코드' )
  html = RichTextField()
  content1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='기타1' )
  content2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='기타2' )
  content3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='기타3' )


class mp_rvw(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  rvwr_id = models.CharField(max_length=16, null=False, verbose_name='소감문 작성자ID' )
  rep_no = models.PositiveIntegerField(null=False, verbose_name='보고서 NO' )
  rvwr_nm = models.CharField(max_length=20, null=False, verbose_name='작성자 명' )
  rep_div = models.CharField(max_length=1, null=False, verbose_name='소감문 구분' )
  rvwr_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='속감문 작성자 구분' )
  apl_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='멘토 학번' )
  apl_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='멘토 이름' )
  mnte_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당멘티ID' )
  mnte_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당멘티명' )
  tchr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='담당교사ID' )
  tchr_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='담당교사명' )
  grd_id = models.CharField(max_length=16, null=False, verbose_name='주 보호자 ID' )
  grd_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='보호자명' )
  sch_nm = models.CharField(max_length=30, null=True, blank=True, verbose_name='학교명' )
  mtr_revw = models.CharField(max_length=1000, null=True, blank=True, verbose_name='소감문' )
  rvw_dt = models.DateTimeField(null=True, blank=True, verbose_name='작성일' )
  cmp_dt = models.DateTimeField(null=True, blank=True, verbose_name='제출일' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 확인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0070)' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


  class Meta:
    verbose_name = '프로그램 소감문'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "rvwr_id", "rep_no")





#bbs1
class bbs1(models.Model):
  subject = models.CharField(max_length=255, null=True, blank=True, verbose_name='타이틀' )
  name = models.CharField(max_length=50, null=True, blank=True, verbose_name='작성자' )

  html = RichTextUploadingField()

  file = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일1')
  file2 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일2')
  file3 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일3')
  file4 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일4')
  file5 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일5')
  file6 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일6')
  file7 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일7')
  file8 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일8')
  file9 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일9')
  file10 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일10')

  hits = models.IntegerField(max_length=50, null=True, blank=True, verbose_name='작성자' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  class Meta:
    verbose_name = '공지사항'  



class bbs2(models.Model):
  subject = models.CharField(max_length=255, null=True, blank=True, verbose_name='타이틀' )
  name = models.CharField(max_length=50, null=True, blank=True, verbose_name='작성자' )
  html = RichTextUploadingField()
  mp_id = models.CharField(max_length=10, null=False, choices=(('P190001','거점중학교육성사업대학생멘토링'),('P190002','기장희망꿈나무멘토링'),('P190003','글로벌브릿지효원레인보우국악오케스트라멘토링'),('P190004','꿈사다리장학생멘토링'),('P190005','3-DAYS프로그램 멘토링'),('P190006','부산대와함께하는금정지역멘토링'),('P190007','Hi-효원멘토링'),('P190008','마음건강멘토링'),('P190009','HUGTOGETHER멘토링'),('P190010','재능봉사캠프멘토링'),('P190011','다꿈멘토링'),('P190012','부산시교육청부산대주관다문화및탈북학생대학생멘토링'),('P190013','부산대해외봉사단'),('P190014','한국장학재단다문화및탈북학생멘토링')), verbose_name='멘토링 프로그램ID')
  file = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일')
  file2 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일2')
  file3 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일3')
  file4 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일4')
  file5 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일5')
  file6 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일6')
  file7 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일7')
  file8 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일8')
  file9 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일9')
  file10 = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일10')
  hits = models.IntegerField(max_length=50, null=True, blank=True, verbose_name='작성자' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  class Meta:
    verbose_name = '자료실'  




class mpgm_introduce(models.Model):
  subject = models.CharField(max_length=255, null=True, blank=True, verbose_name='타이틀' )
  name = models.CharField(max_length=50, null=True, blank=True, verbose_name='작성자' )
  mp_id = models.CharField(max_length=10, null=False, choices=(('01','거점중학교육성사업대학생멘토링'),('02','기장희망꿈나무멘토링'),('03','글로벌브릿지효원레인보우국악오케스트라멘토링'),('04','꿈사다리장학생멘토링'),('05','3-DAYS프로그램 멘토링'),('06','부산대와함께하는금정지역멘토링'),('07','Hi-효원멘토링'),('08','마음건강멘토링'),('09','HUGTOGETHER멘토링'),('10','재능봉사캠프멘토링'),('11','다꿈멘토링'),('12','부산시교육청부산대주관다문화및탈북학생대학생멘토링'),('13','부산대해외봉사단'),('14','한국장학재단다문화및탈북학생멘토링')), verbose_name='멘토링 프로그램' )
  html = RichTextUploadingField()
  file = models.FileField(upload_to='files',null=True,blank=True,verbose_name='파일')
  img = models.FileField(upload_to='files',null=True,blank=True,verbose_name='이미지소개') 
  hits = models.IntegerField(max_length=50, null=True, blank=True, verbose_name='작성자' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
  class Meta:
    verbose_name = '멘토링 프로그램 소개' 



class com_evt(models.Model):

  evt_gb = models.CharField(max_length=10, null=False, verbose_name='이벤트구분' )
  evt_userid = models.CharField(max_length=16, null=False, verbose_name='이벤트사용자ID' )
  evt_ip = models.CharField(max_length=22, null=False, verbose_name='이벤트발생 IP' )
  evt_dat = models.CharField(max_length=14, null=False, verbose_name='이벤트일시' )
  evt_desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='이벤트 내용' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )

  class Meta:
    verbose_name = '이벤트로그'
    verbose_name_plural =  verbose_name





class mp_ucmp_req(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  ucmp_seq = models.PositiveIntegerField(null=False, verbose_name='미완료 소명 No' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='멘토 학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='멘토 이름' )
  base_hr = models.PositiveIntegerField(default=0, verbose_name='기준 시간' )
  act_hr = models.PositiveIntegerField(default=0, verbose_name='활동 시간' )
  wrt_dt = models.DateTimeField(null=True, blank=True, verbose_name='작성일' )
  sbm_dt = models.DateTimeField(null=True, blank=True, verbose_name='제출일' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0070)' )
  uncmp_tp = models.CharField(max_length=2, default='99', verbose_name='미완료 유형(MP0096)' )
  uncmp_resp = models.CharField(max_length=1, default='M', verbose_name='미완료 귀책(MS0005)' )
  uncmp_desc = models.CharField(max_length=1000, null=True, blank=True, verbose_name='미완료 소명 사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )



  class Meta:
    verbose_name = '미완료 소명서'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "ucmp_seq")



class mp_stop_req(models.Model):
  mp_id = models.CharField(max_length=10, null=False, verbose_name='멘토링 프로그램ID' )
  apl_no = models.PositiveIntegerField(null=False, verbose_name='멘토 지원 NO' )
  stop_seq = models.PositiveIntegerField(null=False, verbose_name='미완료 소명 No' )
  apl_id = models.CharField(max_length=10, null=False, verbose_name='멘토 학번' )
  apl_nm = models.CharField(max_length=50, null=False, verbose_name='멘토 이름' )
  base_hr = models.PositiveIntegerField(default=0, verbose_name='기준 시간' )
  act_hr = models.PositiveIntegerField(default=0, verbose_name='활동 시간' )
  stop_dt = models.DateTimeField(null=True, blank=True, verbose_name='중단일' )
  wrt_dt = models.DateTimeField(null=True, blank=True, verbose_name='작성일' )
  sbm_dt = models.DateTimeField(null=True, blank=True, verbose_name='제출일' )
  appr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='승인자ID' )
  appr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='승인자명' )
  appr_dt = models.DateTimeField(null=True, blank=True, verbose_name='보호자 승인일시' )
  mgr_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='관리자ID' )
  mgr_dt = models.DateTimeField(null=True, blank=True, verbose_name='관리자 승인일시' )
  status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태(MP0070)' )
  stop_tp = models.CharField(max_length=2, default='99', verbose_name='중단 유형(MP0095)' )
  stop_resp = models.CharField(max_length=1, default='M', verbose_name='중단 귀책(MS0005)' )
  stop_desc = models.CharField(max_length=1000, null=True, blank=True, verbose_name='중단 사유' )
  ins_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='입력자ID' )
  ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
  ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
  ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
  upd_id = models.CharField(max_length=16, null=True, blank=True, verbose_name='수정자ID' )
  upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
  upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
  upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

  class Meta:
    verbose_name = '활동중단 사유서'
    verbose_name_plural =  verbose_name
    unique_together=("mp_id", "apl_no", "stop_seq")

class FCMToken(models.Model):
    user_id = models.CharField(
        max_length=50,
    )
    token = models.CharField(
        max_length=200,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @classmethod
    def send_push(cls, fcm_tokens, message='',  fcm_title=''):

      FCM_SERVER_KEY = "AAAA6XXtg80:APA91bFaIzIYVcfCZWNtikixJPtuHK06R8B66oV4vycgjlKWtSSLkV-wuZYK5C2gPiVfJKLFivECl9aHY9D2bsSM1CekrxV4nMPaxHB4OM-ucTv7E94v903DQdqts2ixha7viN6TTm5f"
      push_service = FCMNotification(api_key=FCM_SERVER_KEY)
      return push_service.notify_multiple_devices(registration_ids=fcm_tokens, message_title=fcm_title, message_body=message)