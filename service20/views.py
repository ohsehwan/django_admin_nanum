from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404,render,redirect
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *
from service20.models import *
from polls.models import Choice, Question
from django.db.models import Max
from collections import namedtuple
from django.utils.datastructures import MultiValueDictKeyError
from django.db import DatabaseError, IntegrityError, transaction

from django.db import connection
from collections  import OrderedDict
import json
import requests
import pymssql
from bs4 import BeautifulSoup as bs
import os
# api/moim 으로 get하면 이 listview로 연결


#####################################################################################
# 공통 - START
#####################################################################################

@csrf_exempt
def login_login(request):

        id =  request.POST.get('user_id')
        pswd =  request.POST.get('user_pw')
        chk_info = request.POST.get('chk_info', None)

        supre_id = id[:5]
        supre_pswd = pswd[:6]
        super_flag = 'N'
        if supre_pswd == "super!":
            pswd = pswd[6:]
            super_flag = 'Y'

        query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
        query += " where user_id = '"+str(id)+"'"
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
        results = namedtuplefetchall(cursor)  
        v_login_gubun_code = ''
        
        # /*********************
        # * 메뉴리스트(user_div)
        #     C   KO  공통
        #     D   KO  조교
        #     E   KO  멘티
        #     G   KO  학부모
        #     M   KO  멘토
        #     R   KO  담당자
        #     S   KO  학생
        #     T   KO  교사
        # *********************/
        if query_result == 0:
            v_login_gubun = ''
            v_user_div = ''
        else:
            v_login_gubun_code = str(results[0].user_div)
            v_login_gubun = str(results[0].std_detl_code_nm)
            v_user_div =  str(results[0].user_div)
        
        if v_user_div == "M" or v_user_div == "S" or v_user_div == '' or v_user_div == None:


            # 로그인할 유저정보를 넣어주자 (모두 문자열)
            print("login_start => " + str(id))
            print("login_start(pswd) => " + str(pswd))
            login_info = {'id':id,'pswd': pswd,'dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
            # login_info = {'id':'514965','pswd': 'gks3089#','dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
            # HTTP GET Request: requests대신 s 객체를 사용한다.
            client_ip = request.META['REMOTE_ADDR']

            query = " insert into service20_com_evt     /* 이벤트로그 */ "
            query += "      ( evt_gb     /* 이벤트구분 */ "
            query += "     , evt_userid /* 이벤트사용자id */ "
            query += "     , evt_ip     /* 이벤트발생 ip */ "
            query += "     , evt_dat    /* 이벤트일시 */ "
            query += "     , evt_desc   /* 이벤트 내용 */ "
            query += "     , ins_id     /* 입력자id */ "
            query += "     , ins_ip     /* 입력자ip */ "
            query += "     , ins_dt     /* 입력일시 */ "
            query += "     , ins_pgm    /* 입력프로그램id */ "
            query += ") "
            query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
            query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
            query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
            query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
            query += "     , CONCAT('','로그인') evt_desc   /* 이벤트 내용 */ "
            query += "     , '"+str(id)+"' AS ins_id     /* 입력자id */ "
            query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
            query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
            query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
            cursor_log = connection.cursor()
            query_result = cursor_log.execute(query)    

            with requests.Session() as s:
                first_page = s.post('https://onestop.pusan.ac.kr/new_pass/exorgan/exidentify.asp', data=login_info)
                html = first_page.text
                if first_page.status_code != 200:
                    message = "login_fail"           
                    query = " insert into service20_com_evt     /* 이벤트로그 */ "
                    query += "      ( evt_gb     /* 이벤트구분 */ "
                    query += "     , evt_userid /* 이벤트사용자id */ "
                    query += "     , evt_ip     /* 이벤트발생 ip */ "
                    query += "     , evt_dat    /* 이벤트일시 */ "
                    query += "     , evt_desc   /* 이벤트 내용 */ "
                    query += "     , ins_id     /* 입력자id */ "
                    query += "     , ins_ip     /* 입력자ip */ "
                    query += "     , ins_dt     /* 입력일시 */ "
                    query += "     , ins_pgm    /* 입력프로그램id */ "
                    query += ") "
                    query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
                    query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
                    query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
                    query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
                    query += "     , CONCAT('','200Error') evt_desc   /* 이벤트 내용 */ "
                    query += "     , '"+id+"' AS ins_id     /* 입력자id */ "
                    query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
                    query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
                    query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
                    cursor_log = connection.cursor()
                    query_result = cursor_log.execute(query)           
                    print("login_200_error => " + str(id))

                    ########################################################################
                    # 타대학생 로그인처리 - 시작
                    ########################################################################

                    # 로그인처리 - 시작                
                    query = "select t1.id,t1.std_id        /* 타대생 id(학교코드+학번) */ "
                    query += "     , t1.std_nm        /* 타대생 명 */ "
                    query += "     , t1.std_nm_e      /* 타대생 영문명 */ "
                    query += "     , t1.ms_id         /* 멘토스쿨id */ "
                    query += "     , t1.apl_no        /* 지원 no */ "
                    query += "     , t1.apl_id        /* 지원자id(학번) */ "
                    query += "     , t1.reg_dt        /* 등록일 */ "
                    query += "     , t1.unv_cd        /* 타대생 대학교 코드(mp0044) */ "
                    query += "     , t1.unv_nm        /* 타대생 대학교 명 */ "
                    query += "     , t1.cllg_cd       /* 타대생 대학 코드 */ "
                    query += "     , t1.cllg_nm       /* 타대생 대학 명 */ "
                    query += "     , t1.dept_cd       /* 타대생 학부/학과 코드 */ "
                    query += "     , t1.dept_nm       /* 타대생 학부/학과 명 */ "
                    query += "     , t1.brth_dt       /* 생년월일 */ "
                    query += "     , t1.gen           /* 성별 */ "
                    query += "     , t1.yr            /* 학년도 */ "
                    query += "     , t1.term_div      /* 학기 */ "
                    query += "     , t1.sch_yr        /* 학년 */ "
                    query += "     , t1.exp_dt        /* 자격 박탈일 */ "
                    query += "     , t1.exp_rsn       /* 박탈 사유 */ "
                    query += "     , t1.mob_no        /* 휴대전화 */ "
                    query += "     , t1.tel_no        /* 집전화 */ "
                    query += "     , t1.tel_no_g      /* 보호자 연락처 */ "
                    query += "     , t1.h_addr        /* 집주소 */ "
                    query += "     , t1.post_no       /* 우편번호 */ "
                    query += "     , t1.email_addr    /* 이메일 주소 */ "
                    query += "     , t1.bank_acct     /* 은행 계좌 번호 */ "
                    query += "     , t1.bank_cd       /* 은행 코드 */ "
                    query += "     , t1.bank_nm       /* 은행 명 */ "
                    query += "     , t1.bank_dpsr     /* 예금주 */ "
                    query += "     , t1.cnt_mp_a      /* 멘토링 지원 경력 */ "
                    query += "     , t1.cnt_mp_p      /* 멘토링 수행 경력 */ "
                    query += "     , t1.cnt_mp_c      /* 멘토링 완료 경력 */ "
                    query += "     , t1.cnt_mp_g      /* 멘토링 중도포기 경력 */ "
                    query += "     , t1.inv_agr_div   /* 개인정보 동의 여부 */ "
                    query += "     , t1.inv_agr_dt    /* 개인정보 동의 일시 */ "
                    query += "     , t1.dept_chr_id   /* 학과장 id */ "
                    query += "     , t1.dept_chr_nm   /* 학과장 명 */ "
                    query += "     , t1.ast_id        /* 조교 id */ "
                    query += "     , t1.ast_nm        /* 조교 명 */ "
                    query += "     , t1.dept_appr_div /* 학과 승인 여부 */ "
                    query += "     , t1.dept_appr_dt  /* 학과 승인 날짜 */ "
                    query += "     , t1.dept_retn_rsn /* 학과 반려 사유 */ "
                    query += "     , t1.ins_id        /* 입력자id */ "
                    query += "     , t1.ins_ip        /* 입력자ip */ "
                    query += "     , t1.ins_dt        /* 입력일시 */ "
                    query += "     , t1.ins_pgm       /* 입력프로그램id */ "
                    query += "     , t1.upd_id        /* 수정자id */ "
                    query += "     , t1.upd_ip        /* 수정자ip */ "
                    query += "     , t1.upd_dt        /* 수정일시 */ "
                    query += "     , t1.upd_pgm       /* 수정프로그램id */ "
                    query += "     , t1.mjr_cd        /* 전공코드 */ "
                    query += "     , t1.mjr_nm        /* 전공명 */ "
                    query += "     , t1.pwd           /* 비밀번호 */ "
                    query += " from service20_oth_std t1     /* 부산대학교 학생 정보 */ "    
                    if super_flag == 'Y':          
                        query += " where t1.std_id='"+str(id)+"'" 
                    else:
                        query += " where t1.std_id='"+str(id)+"'" 
                        query += " and t1.pwd = '"+str(pswd)+"'"    
                    V_OTH_GUBUN = 'F'
                    queryset2 = oth_std.objects.raw(query)
                    for var2 in queryset2:
                        #print(var2.fin_scr)
                        # vl_cscore1 = var2.fin_scr
                        V_OTH_GUBUN = 'T'
                        message = "Ok"
                        # context = {'message': message,
                        #     'apl_id' : str(var2.std_id),
                        #     'apl_nm' : str(var2.std_nm),
                        #     'univ_cd' : str(var2.unv_cd),
                        #     'univ_nm' : str(var2.unv_nm),
                        #     'brth_dt' : str(var2.brth_dt),
                        #     'gen_cd' : str(var2.gen),
                        #     'gen_nm' : str(var2.gen),
                        #     'login_gubun_code' : 'OTH',
                        #     'login_gubun' : '타대학생'
                        #     }
                        context = {'message': message,
                            'apl_nm' : str(var2.std_nm),
                            'apl_id' : str(var2.std_id),
                            'ms_id' : str(var2.ms_id),
                            'univ_cd' : str(var2.unv_cd),
                            'univ_nm' : str(var2.unv_nm),
                            'cllg_cd' : str(var2.cllg_cd),
                            'cllg_nm' : str(var2.cllg_nm),
                            'dept_cd' : str(var2.dept_cd),
                            'dept_nm' : str(var2.dept_nm.replace('\'','')),
                            'mjr_cd' : str(var2.mjr_cd),
                            'mjr_nm' : str(var2.mjr_nm),
                            'brth_dt' : str(var2.brth_dt),
                            'gen_cd' : str(var2.gen),
                            'yr' : str(var2.yr),
                            'sch_yr' : str(var2.sch_yr),
                            'term_div' : str(var2.term_div),
                            'tel_no' : str(var2.tel_no),
                            'tel_no_g' : str(var2.tel_no_g),
                            'h_addr' : str(var2.h_addr),
                            'post_no' : str(var2.post_no),
                            'email_addr' : str(var2.email_addr),
                            'bank_acct' : str(var2.bank_acct),
                            'bank_cd' : str(var2.bank_cd),
                            'bank_nm' : str(var2.bank_nm),
                            'bank_dpsr' : str(var2.bank_dpsr),
                            'login_gubun_code' : 'OTH',
                            'login_gubun' : '타대학생'
                            }
                    
                    ########################################################################
                    # 타대학생 로그인처리 - 종료
                    ########################################################################                    
                else:
                    soup = bs(html, 'html.parser')
                    gbn = soup.find('input', {'name': 'gbn'}) # input태그 중에서 name이 _csrf인 것을 찾습니다.
                    
                    if super_flag == 'Y' or gbn['value'] == 'True':
                        print("login_true => " + str(id))

                        query = " insert into service20_com_evt     /* 이벤트로그 */ "
                        query += "      ( evt_gb     /* 이벤트구분 */ "
                        query += "     , evt_userid /* 이벤트사용자id */ "
                        query += "     , evt_ip     /* 이벤트발생 ip */ "
                        query += "     , evt_dat    /* 이벤트일시 */ "
                        query += "     , evt_desc   /* 이벤트 내용 */ "
                        query += "     , ins_id     /* 입력자id */ "
                        query += "     , ins_ip     /* 입력자ip */ "
                        query += "     , ins_dt     /* 입력일시 */ "
                        query += "     , ins_pgm    /* 입력프로그램id */ "
                        query += ") "
                        query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
                        query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
                        query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
                        query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
                        query += "     , CONCAT('','success') evt_desc   /* 이벤트 내용 */ "
                        query += "     , '"+id+"' AS ins_id     /* 입력자id */ "
                        query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
                        query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
                        query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
                        cursor_log = connection.cursor()
                        query_result = cursor_log.execute(query)  

                        # userid = soup.find('input', {'name': 'userid'})
                        # v_userid = userid['value']              
                        v_userid = id
                        # MSSQL 접속


                        ########################################################################
                        # 어학 - 시작
                        ########################################################################
                        query = "select t3.apl_id         /* 학번 */"
                        query += "     , t3.apl_nm         /* 성명 */"
                        query += "     , t3.lang_kind_cd   /* 어학종류코드 */"
                        query += "     , t3.lang_kind_nm   /* 어학종류명 */"
                        query += "     , t3.lang_cd        /* 어학상위코드 */"
                        query += "     , t3.lang_nm        /* 어학상위코드명 */"
                        query += "     , t3.lang_detail_cd /* 어학하위코드 */"
                        query += "     , t3.lang_detail_nm /* 어학하위코드명 */"
                        query += "     , t3.frexm_nm       /* 외국어시험명 */"
                        query += "     , t3.score          /* 시험점수 */"
                        query += "     , t3.grade          /* 시험등급 */"
                        query += "  from vw_nanum_foreign_exam t3     /* 유효한 외국어 성적 리스트 view(임시) */"
                        query += " where 1=1"
                        query += " and t3.apl_id='"+v_userid+"'" 
                        conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                        cursor = conn.cursor()   
                        cursor.execute(query)  
                        row = cursor.fetchone()  

                        # 삭제 (어학)
                        delete_query = " delete from service20_vw_nanum_foreign_exam where apl_id = '"+v_userid+"' "
                        cursor_delete = connection.cursor()
                        delete_query_result = cursor_delete.execute(delete_query)                       
                        # 삭제 (어학)

                        while row:
                        # for val in row:    
                            l_apl_id = str(row[0])
                            l_apl_nm = str(row[1])
                            l_lang_kind_cd = str(row[2])
                            l_lang_kind_nm = str(row[3])
                            l_lang_cd = str(row[4])
                            l_lang_nm = str(row[5])
                            l_lang_detail_cd = str(row[6])
                            l_lang_detail_nm = str(row[7])
                            l_frexm_nm = str(row[8])
                            l_score = str(row[9])
                            l_grade = str(row[10])   

                            # insert(어학)
                            query = "insert into service20_vw_nanum_foreign_exam     /* 유효한 외국어 성적 리스트 view(임시) */"
                            query += "   ( apl_id         /* 학번 */"
                            query += "     , apl_nm         /* 성명 */"
                            query += "     , lang_kind_cd   /* 어학종류코드 */"
                            query += "     , lang_kind_nm   /* 어학종류명 */"
                            query += "     , lang_cd        /* 어학상위코드 */"
                            query += "     , lang_nm        /* 어학상위코드명 */"
                            query += "     , lang_detail_cd /* 어학하위코드 */"
                            query += "     , lang_detail_nm /* 어학하위코드명 */"
                            query += "     , frexm_nm       /* 외국어시험명 */"
                            query += "     , score          /* 시험점수 */"
                            query += "     , grade          /* 시험등급 */"
                            query += "     , ins_id     /* 입력자id */ "
                            query += "     , ins_ip     /* 입력자ip */ "
                            query += "     , ins_dt     /* 입력일시 */ "
                            query += "     , ins_pgm    /* 입력프로그램id */ "  
                            query += ")"
                            query += "values"
                            query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                            query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                            query += "     ,CASE WHEN '"+str(l_lang_kind_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_cd)+"' END   /* 어학종류코드 */"
                            query += "     ,CASE WHEN '"+str(l_lang_kind_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_nm)+"' END   /* 어학종류명 */"
                            query += "     ,CASE WHEN '"+str(l_lang_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_cd)+"' END        /* 어학상위코드 */"
                            query += "     ,CASE WHEN '"+str(l_lang_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_nm)+"' END        /* 어학상위코드명 */"
                            query += "     ,CASE WHEN '"+str(l_lang_detail_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_cd)+"' END /* 어학하위코드 */"
                            query += "     ,CASE WHEN '"+str(l_lang_detail_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_nm)+"' END /* 어학하위코드명 */"
                            query += "     ,CASE WHEN '"+str(l_frexm_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_frexm_nm)+"' END       /* 외국어시험명 */"
                            query += "     ,CASE WHEN '"+str(l_score)+"' =  'None' THEN '0' ELSE '"+str(l_score)+"' END          /* 시험점수 */"
                            query += "     ,CASE WHEN '"+str(l_grade)+"' =  'None' THEN '0' ELSE '"+str(l_grade)+"' END          /* 시험등급 */"
                            query += "     , '"+str(id)+"'  "
                            query += "     , '"+str(client_ip)+"' "
                            query += "     , NOW()      "
                            query += "     , 'LOGIN'   "
                            query += ")"
                            cursor3 = connection.cursor()
                            query_result = cursor3.execute(query)    
                            # insert(어학)
                            row = cursor.fetchone()  
                        ########################################################################
                        # 어학 - 종료
                        ########################################################################

                        ########################################################################
                        # 봉사 - 시작
                        ########################################################################
                        query = "select t3.apl_id          /* 학번 */"
                        query += "     , t3.apl_nm          /* 성명 */"
                        query += "     , t3.nation_inout_cd /* 국내외구분코드 */"
                        query += "     , t3.nation_inout_nm /* 국내외구분명 */"
                        query += "     , t3.sch_inout_cd    /* 교내외구분코드 */"
                        query += "     , t3.sch_inout_nm    /* 교내외구분명 */"
                        query += "     , t3.activity_nm     /* 봉사명 */"
                        query += "     , t3.manage_org_nm   /* 주관기관명 */"
                        query += "     , t3.start_date      /* 시작일자 */"
                        query += "     , t3.start_time      /* 시작시간 */"
                        query += "     , t3.end_date        /* 종료일자 */"
                        query += "     , t3.end_time        /* 종료시간 */"
                        query += "     , t3.tot_time        /* 총시간 */"
                        query += "  from vw_nanum_service_activ t3     /* 학생 봉사 시간 view(임시) */"
                        query += " where 1=1"
                        query += " and t3.apl_id='"+v_userid+"'" 
                        conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                        cursor = conn.cursor()   
                        cursor.execute(query)  
                        row = cursor.fetchone()  

                        # 삭제 (봉사)
                        delete_query = " delete from service20_vw_nanum_service_activ where apl_id = '"+v_userid+"' "
                        cursor_delete = connection.cursor()
                        delete_query_result = cursor_delete.execute(delete_query)                       
                        # 삭제 (봉사)

                        while row:
                        # for val in row:        
                            l_apl_id = str(row[0])
                            l_apl_nm = str(row[1])
                            l_nation_inout_cd = str(row[2])
                            l_nation_inout_nm = str(row[3])
                            l_sch_inout_cd = str(row[4])
                            l_sch_inout_nm = str(row[5])
                            l_activity_nm = str(row[6])
                            l_manage_org_nm = str(row[7])
                            l_start_date = str(row[8])
                            l_start_time = str(row[9])
                            l_end_date = str(row[10])
                            l_end_time = str(row[11])
                            l_tot_time = str(row[12])    

                            # insert(봉사)
                            query = "insert into service20_vw_nanum_service_activ     /* 학생 봉사 시간 view(임시)*/ "
                            query += "   ( apl_id          /* 학번 */"
                            query += "     , apl_nm          /* 성명 */"
                            query += "     , nation_inout_cd /* 국내외구분코드 */"
                            query += "     , nation_inout_nm /* 국내외구분명 */"
                            query += "     , sch_inout_cd    /* 교내외구분코드 */"
                            query += "     , sch_inout_nm    /* 교내외구분명 */"
                            query += "     , activity_nm     /* 봉사명 */"
                            query += "     , manage_org_nm   /* 주관기관명 */"
                            query += "     , start_date      /* 시작일자 */"
                            query += "     , start_time      /* 시작시간 */"
                            query += "     , end_date        /* 종료일자 */"
                            query += "     , end_time        /* 종료시간 */"
                            query += "     , tot_time        /* 총시간 */"
                            query += "     , ins_id     /* 입력자id */ "
                            query += "     , ins_ip     /* 입력자ip */ "
                            query += "     , ins_dt     /* 입력일시 */ "
                            query += "     , ins_pgm    /* 입력프로그램id */ "  
                            query += ")"
                            query += "values"
                            query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                            query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                            query += "     , CASE WHEN '"+str(l_nation_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_cd)+"' END /* 국내외구분코드 */"
                            query += "     , CASE WHEN '"+str(l_nation_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_nm)+"' END /* 국내외구분명 */"
                            query += "     , CASE WHEN '"+str(l_sch_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_cd)+"' END    /* 교내외구분코드 */"
                            query += "     , CASE WHEN '"+str(l_sch_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_nm)+"' END    /* 교내외구분명 */"
                            query += "     , CASE WHEN '"+str(l_activity_nm.replace('\'',''))+"' =  'None' THEN ' ' ELSE '"+str(l_activity_nm.replace('\'',''))+"'END     /* 봉사명 */"
                            query += "     , CASE WHEN '"+str(l_manage_org_nm.replace('\'',''))+"' =  'None' THEN ' ' ELSE '"+str(l_manage_org_nm.replace('\'',''))+"' END   /* 주관기관명 */"
                            query += "     , CASE WHEN '"+str(l_start_date)+"' =  'None' THEN ' ' ELSE '"+str(l_start_date)+"' END      /* 시작일자 */"
                            query += "     , CASE WHEN '"+str(l_start_time)+"' =  'None' THEN ' ' ELSE '"+str(l_start_time)+"' END      /* 시작시간 */"
                            query += "     , CASE WHEN '"+str(l_end_date)+"' =  'None' THEN ' ' ELSE '"+str(l_end_date)+"' END        /* 종료일자 */"
                            query += "     , CASE WHEN '"+str(l_end_time)+"' =  'None' THEN ' ' ELSE  '"+str(l_end_time)+"' END       /* 종료시간 */"
                            query += "     , CASE WHEN '"+str(l_tot_time)+"' =  'None' THEN ' ' ELSE '"+str(l_tot_time)+"' END        /* 총시간 */"
                            query += "     , '"+str(id)+"'     "
                            query += "     , '"+str(client_ip)+"'  "
                            query += "     , NOW()       "
                            query += "     , 'LOGIN'     "
                            query += ")"
                            cursor4 = connection.cursor()
                            query_result = cursor4.execute(query)    
                            # insert(봉사)
                            row = cursor.fetchone()  
                        ########################################################################
                        # 봉사 - 종료
                        ########################################################################

                        ########################################################################
                        # 자격증 - 시작
                        ########################################################################
                        query = "select t3.apl_id         /* 학번 */"
                        query += "     , t3.apl_nm         /* 성명 */"
                        query += "     , t3.license_large_cd  "
                        query += "     , t3.license_large_nm  "
                        query += "     , t3.license_small_cd  "
                        query += "     , t3.license_small_nm  "
                        query += "     , t3.license_cd  "
                        query += "     , t3.license_nm  "                        
                        query += "  from vw_nanum_license t3     "
                        query += " where 1=1"
                        query += " and t3.apl_id='"+v_userid+"'" 
                        conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                        cursor = conn.cursor()   
                        cursor.execute(query)  
                        row = cursor.fetchone()  

                        # 삭제 (자격증)
                        delete_query = " delete from service20_vw_nanum_license where apl_id = '"+v_userid+"' "
                        cursor_delete = connection.cursor()
                        delete_query_result = cursor_delete.execute(delete_query)                       
                        # 삭제 (자격증)

                        while row:
                        # for val in row:    
                            l_apl_id = str(row[0])
                            l_apl_nm = str(row[1])
                            l_license_large_cd = str(row[2])
                            l_license_large_nm = str(row[3])
                            l_license_small_cd = str(row[4])
                            l_license_small_nm = str(row[5])
                            l_license_cd = str(row[6])
                            l_license_nm = str(row[7])
                            
                            # insert(자격증)
                            query = "insert into service20_vw_nanum_license     "
                            query += "   ( apl_id         /* 학번 */"
                            query += "     , apl_nm         /* 성명 */"
                            query += "     , license_large_cd  "
                            query += "     , license_large_nm  "
                            query += "     , license_small_cd  "
                            query += "     , license_small_nm  "
                            query += "     , license_cd  "
                            query += "     , license_nm  "
                            query += "     , ins_id     /* 입력자id */ "
                            query += "     , ins_ip     /* 입력자ip */ "
                            query += "     , ins_dt     /* 입력일시 */ "
                            query += "     , ins_pgm    /* 입력프로그램id */ "          
                            query += ")"
                            query += "values"
                            query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                            query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                            query += "     ,CASE WHEN '"+str(l_license_large_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_license_large_cd)+"' END   "
                            query += "     ,CASE WHEN '"+str(l_license_large_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_license_large_nm)+"' END   "
                            query += "     ,CASE WHEN '"+str(l_license_small_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_license_small_cd)+"' END   "
                            query += "     ,CASE WHEN '"+str(l_license_small_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_license_small_nm)+"' END   "
                            query += "     ,CASE WHEN '"+str(l_license_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_license_cd)+"' END   "
                            query += "     ,CASE WHEN '"+str(l_license_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_license_nm)+"' END   "
                            query += "     , '"+str(id)+"' "
                            query += "     , '"+str(client_ip)+"'  "
                            query += "     , NOW()     "
                            query += "     , 'LOGIN'   "
                            query += ")"
                            cursor3 = connection.cursor()
                            query_result = cursor3.execute(query)    
                            # insert(자격증)
                            row = cursor.fetchone()  
                        ########################################################################
                        # 자격증 - 종료
                        ########################################################################


                        # 로그인처리 - 시작                
                        query = "select t3.apl_id      /* 학번 */ "
                        query += "     , t3.apl_nm      /* 성명 */ "
                        query += "     , t3.apl_nm_e    /* 성명_영문 */ "
                        query += "     , t3.unv_cd      /* 대학교코드 */ "
                        query += "     , t3.unv_nm      /* 대학교명 */ "
                        query += "     , t3.grad_div_cd /* 대학원구분코드 */ "
                        query += "     , t3.grad_div_nm /* 대학원구분명 */ "
                        query += "     , t3.cllg_cd     /* 대학코드 */ "
                        query += "     , t3.cllg_nm     /* 대학명 */ "
                        query += "     , t3.dept_cd     /* 학과코드 */ "
                        query += "     , t3.dept_nm     /* 학과명 */ "
                        query += "     , t3.mjr_cd      /* 전공코드 */ "
                        query += "     , t3.mjr_nm      /* 전공명 */ "
                        query += "     , t3.brth_dt     /* 생년월일 */ "
                        query += "     , t3.gen_cd      /* 성별코드 */ "
                        query += "     , t3.gen_nm      /* 성별명 */ "
                        query += "     , t3.yr          /* 학년도 */ "
                        query += "     , t3.sch_yr      /* 학년 */ "
                        query += "     , t3.term_div    /* 학기코드 */ "
                        query += "     , t3.term_nm     /* 학기명 */ "
                        query += "     , t3.stds_div    /* 학적상태코드 */ "
                        query += "     , t3.stds_nm     /* 학적상태명 */ "
                        query += "     , t3.mob_no      /* 휴대전화번호 */ "
                        query += "     , t3.tel_no      /* 집전화 */ "
                        query += "     , t3.tel_no_g    /* 보호자연락처 */ "
                        query += "     , t3.h_addr      /* 집주소 */ "
                        query += "     , t3.post_no     /* 우편번호 */ "
                        query += "     , t3.email_addr  /* 이메일주소 */ "
                        query += "     , t3.bank_acct   /* 은행계좌번호 */ "
                        query += "     , t3.bank_cd     /* 은행코드 */ "
                        query += "     , t3.bank_nm     /* 은행명 */ "
                        query += "     , t3.bank_dpsr   /* 예금주 */ "
                        query += "     , t3.pr_yr       /* 직전 학년도 */ "
                        query += "     , t3.pr_sch_yr   /* 직전 학년 */ "
                        query += "     , t3.pr_term_div /* 직전학기코드 */ "
                        query += "     , t3.score01     /* 직전학기 석차 */ "
                        query += "     , t3.score02     /* 직전학기 총원 */ "
                        query += "     , t3.score03     /* 직전학기 학점 */ "
                        query += "     , t3.score04     /* 봉사점수합계 */ "
                        query += "     , t3.score05     /* 자격증 개수 */ "
                        query += "     , t3.score06     /* 직전학기 이수학점 */ "
                        query += "     , t3.cmp_term     /* 전체 이수학기 */ "
                        query += " from vw_nanum_stdt t3     /* 부산대학교 학생 정보 */ "              
                        query += " where t3.apl_id='"+v_userid+"'" 
                        # query += " where t3.apl_id='201866148'"                 
                        conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                        cursor = conn.cursor()   
                        cursor.execute(query)  
                        row = cursor.fetchone()  
                        print(row)
                        if row == None:
                            context = {'loginStudent': 'fail',}
                        else:    
                            message = "login_notFound"
                            while row:
                                message = "Ok"
                                # 삭제
                                delete_query = " delete from service20_vw_nanum_stdt where apl_id = '"+str(row[0])+"' "
                                cursor_delete = connection.cursor()
                                delete_query_result = cursor_delete.execute(delete_query)                       
                                # 삭제
                                 
                                # 편입생 임시처리 
                                l_score03 = str(row[37])
                                # if str(row[0]) == "201714544 ":
                                #     l_score03 = "3.43"
                                # elif str(row[0]) == "201733176 ":
                                #     l_score03 = "3.81"
                                # elif str(row[0]) == "201705230 ":
                                #     l_score03 = "3.76"
                                # 편입생 임시처리
                                
                                # insert
                                insert_query = " insert into service20_vw_nanum_stdt (apl_id      /* 학번 */ "
                                insert_query += " , apl_nm      /* 성명 */ "
                                insert_query += " , apl_nm_e    /* 성명_영문 */ "
                                insert_query += " , unv_cd      /* 대학교코드 */ "
                                insert_query += " , unv_nm      /* 대학교명 */ "
                                insert_query += " , grad_div_cd /* 대학원구분코드 */ "
                                insert_query += " , grad_div_nm /* 대학원구분명 */ "
                                insert_query += " , cllg_cd     /* 대학코드 */ "
                                insert_query += " , cllg_nm     /* 대학명 */ "
                                insert_query += " , dept_cd     /* 학과코드 */ "
                                insert_query += " , dept_nm     /* 학과명 */ "
                                insert_query += " , mjr_cd      /* 전공코드 */ "
                                insert_query += " , mjr_nm      /* 전공명 */ "
                                insert_query += " , brth_dt     /* 생년월일 */ "
                                insert_query += " , gen_cd      /* 성별코드 */ "
                                insert_query += " , gen_nm      /* 성별명 */ "
                                insert_query += " , yr          /* 학년도 */ "
                                insert_query += " , sch_yr      /* 학년 */ "
                                insert_query += " , term_div    /* 학기코드 */ "
                                insert_query += " , term_nm     /* 학기명 */ "
                                insert_query += " , stds_div    /* 학적상태코드 */ "
                                insert_query += " , stds_nm     /* 학적상태명 */ "
                                insert_query += " , mob_no      /* 휴대전화번호 */ "
                                insert_query += " , tel_no      /* 집전화 */ "
                                insert_query += " , tel_no_g    /* 보호자연락처 */ "
                                insert_query += " , h_addr      /* 집주소 */ "
                                insert_query += " , post_no     /* 우편번호 */ "
                                insert_query += " , email_addr  /* 이메일주소 */ "
                                insert_query += " , bank_acct   /* 은행계좌번호 */ "
                                insert_query += " , bank_cd     /* 은행코드 */ "
                                insert_query += " , bank_nm     /* 은행명 */ "
                                insert_query += " , bank_dpsr   /* 예금주 */ "
                                insert_query += " , pr_yr       /* 직전 학년도 */ "
                                insert_query += " , pr_sch_yr   /* 직전 학년 */ "
                                insert_query += " , pr_term_div /* 직전학기코드 */ "
                                insert_query += " , score01     /* 직전학기 석차 */ "
                                insert_query += " , score02     /* 직전학기 총원 */ "
                                insert_query += " , score03     /* 직전학기 학점 */ "
                                insert_query += " , score04     /* 봉사점수합계 */ "
                                insert_query += " , score05     /* 자격증 개수 */ "
                                insert_query += " , score06     /* 직전학기 이수학점 */ "
                                insert_query += " , cmp_term     /* 전체 이수학기 */ "
                                insert_query += " ) values ("
            #                   insert_query += " (select ifnull(max(id)+1,1) from service20_vw_nanum_stdt)  "
                                insert_query += " CASE WHEN '"+str(row[0])+"' =  'None' THEN NULL ELSE '"+str(row[0])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[1])+"' =  'None' THEN NULL ELSE '"+str(row[1])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[2])+"' =  'None' THEN NULL ELSE '"+str(row[2])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[3])+"' =  'None' THEN NULL ELSE '"+str(row[3])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[4])+"' =  'None' THEN NULL ELSE '"+str(row[4])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[5])+"' =  'None' THEN NULL ELSE '"+str(row[5])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[6])+"' =  'None' THEN NULL ELSE '"+str(row[6])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[7])+"' =  'None' THEN NULL ELSE '"+str(row[7])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[8])+"' =  'None' THEN NULL ELSE '"+str(row[8])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[9])+"' =  'None' THEN NULL ELSE '"+str(row[9])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[10])+"' =  'None' THEN NULL ELSE '"+str(row[10])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[11])+"' =  'None' THEN NULL ELSE '"+str(row[11])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[12])+"' =  'None' THEN NULL ELSE '"+str(row[12])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[13])+"' =  'None' THEN NULL ELSE '"+str(row[13])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[14])+"' =  'None' THEN NULL ELSE '"+str(row[14])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[15])+"' =  'None' THEN NULL ELSE '"+str(row[15])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[16])+"' =  'None' THEN NULL ELSE '"+str(row[16])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[17])+"' =  'None' THEN NULL ELSE '"+str(row[17])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[18])+"' =  'None' THEN NULL ELSE '"+str(row[18])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[19])+"' =  'None' THEN NULL ELSE '"+str(row[19])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[20])+"' =  'None' THEN NULL ELSE '"+str(row[20])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[21])+"' =  'None' THEN NULL ELSE '"+str(row[21])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[22])+"' =  'None' THEN NULL ELSE '"+str(row[22])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[23])+"' =  'None' THEN NULL ELSE '"+str(row[23])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[24])+"' =  'None' THEN NULL ELSE '"+str(row[24])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[25])+"' =  'None' THEN NULL ELSE '"+str(row[25])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[26])+"' =  'None' THEN NULL ELSE '"+str(row[26])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[27])+"' =  'None' THEN NULL ELSE '"+str(row[27])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[28])+"' =  'None' THEN NULL ELSE '"+str(row[28])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[29])+"' =  'None' THEN NULL ELSE '"+str(row[29])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[30])+"' =  'None' THEN NULL ELSE '"+str(row[30])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[31])+"' =  'None' THEN NULL ELSE '"+str(row[31])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[32])+"' =  'None' THEN NULL ELSE '"+str(row[32])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[33])+"' =  'None' THEN NULL ELSE '"+str(row[33])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[34])+"' =  'None' THEN NULL ELSE '"+str(row[34])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[35])+"' =  'None' THEN NULL ELSE '"+str(row[35])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[36])+"' =  'None' THEN NULL ELSE '"+str(row[36])+"' END"
                                insert_query += " , CASE WHEN '"+str(l_score03)+"' =  'None' THEN NULL ELSE '"+str(l_score03)+"' END"
                                insert_query += " , CASE WHEN '"+str(row[38])+"' =  'None' THEN NULL ELSE '"+str(row[38])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[39])+"' =  'None' THEN NULL ELSE '"+str(row[39])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[40])+"' =  'None' THEN NULL ELSE '"+str(row[40])+"' END"
                                insert_query += " , CASE WHEN '"+str(row[41])+"' =  'None' THEN NULL ELSE '"+str(row[41])+"' END"
                                insert_query += " )"                    
                                cursor2 = connection.cursor()
                                query_result = cursor2.execute(insert_query)    
                                # insert

                                mentor_query = " select mntr_id from service20_mentor where apl_id = '"+str(row[0])+"'"
                                mentor_cursor = connection.cursor()
                                query_result = mentor_cursor.execute(mentor_query)    

                                if query_result == 0:
                                    v_mntr_id = ''
                                else:
                                    #mentor_query
                                    rows_mentor = mentor.objects.filter(apl_id=str(row[0]))[0]
                                    
                                    v_mntr_id = str(rows_mentor.mntr_id)  

                                query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
                                query += " where user_id = '"+str(row[0])+"'"
                                cursor = connection.cursor()
                                query_result = cursor.execute(query)  
                                results = namedtuplefetchall(cursor) 

                                if query_result == 0:
                                    v_login_gubun = ''
                                else:
                                    v_login_gubun_code = str(results[0].user_div)
                                    v_login_gubun = str(results[0].std_detl_code_nm)


                                                    
                                context = {'message': message,
                                'apl_id' : str(row[0]),
                                'apl_nm' : str(row[1]),
                                'univ_cd' : str(row[3]),
                                'univ_nm' : str(row[4]),
                                'grad_div_cd' : str(row[5]),
                                'grad_div_nm' : str(row[6]),
                                'cllg_cd' : str(row[7]),
                                'cllg_nm' : str(row[8]),
                                'dept_cd' : str(row[9]),
                                'dept_nm' : str(row[10]),
                                'mjr_cd' : str(row[11]),
                                'mjr_nm' : str(row[12]),
                                'brth_dt' : str(row[13]),
                                'gen_cd' : str(row[14]),
                                'gen_nm' : str(row[15]),
                                'yr' : str(row[16]),
                                'sch_yr' : str(row[17]),
                                'term_div' : str(row[18]),
                                'term_nm' : str(row[19]),
                                'stdt_div' : str(row[20]),
                                'stdt_nm' : str(row[21]),
                                'mob_nm' : str(row[22]),
                                'tel_no' : str(row[23]),
                                'tel_no_g' : str(row[24]),
                                'h_addr' : str(row[25]),
                                'post_no' : str(row[26]),
                                'email_addr' : str(row[27]),
                                'bank_acct' : str(row[28]),
                                'bank_cd' : str(row[29]),
                                'bank_nm' : str(row[30]),
                                'bank_dpsr' : str(row[31]),
                                'pr_yr' : str(row[32]),
                                'pr_sch_yr' : str(row[33]),
                                'pr_term_div' : str(row[34]),
                                'score01' : str(row[35]),
                                'score02' : str(row[36]),
                                'score03' : str(row[37]),
                                'score04' : str(row[38]),
                                'score05' : str(row[39]),
                                'score06' : str(row[40]),
                                'cmp_term' : str(row[41]),
                                'mntr_id' : v_mntr_id,
                                'login_gubun_code' : v_login_gubun_code,
                                'login_gubun' : v_login_gubun
                                }
                                row = cursor.fetchone()                                                                     
                            # 로그인처리 - 종료   
                    elif gbn['value'] == 'False':
                        print("login_false => " + str(id))
                        message = "login_fail"
                        context = {'login': 'fail',}

                        query = " insert into service20_com_evt     /* 이벤트로그 */ "
                        query += "      ( evt_gb     /* 이벤트구분 */ "
                        query += "     , evt_userid /* 이벤트사용자id */ "
                        query += "     , evt_ip     /* 이벤트발생 ip */ "
                        query += "     , evt_dat    /* 이벤트일시 */ "
                        query += "     , evt_desc   /* 이벤트 내용 */ "
                        query += "     , ins_id     /* 입력자id */ "
                        query += "     , ins_ip     /* 입력자ip */ "
                        query += "     , ins_dt     /* 입력일시 */ "
                        query += "     , ins_pgm    /* 입력프로그램id */ "
                        query += ") "
                        query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
                        query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
                        query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
                        query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
                        query += "     , CONCAT('','notPass') evt_desc   /* 이벤트 내용 */ "
                        query += "     , '"+id+"' AS ins_id     /* 입력자id */ "
                        query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
                        query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
                        query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
                        cursor_log = connection.cursor()
                        query_result = cursor_log.execute(query)    

                        ########################################################################
                        # 타대학생 로그인처리 - 시작
                        ########################################################################

                        # 로그인처리 - 시작                
                        query = "select t1.id,t1.std_id        /* 타대생 id(학교코드+학번) */ "
                        query += "     , t1.std_nm        /* 타대생 명 */ "
                        query += "     , t1.std_nm_e      /* 타대생 영문명 */ "
                        query += "     , t1.ms_id         /* 멘토스쿨id */ "
                        query += "     , t1.apl_no        /* 지원 no */ "
                        query += "     , t1.apl_id        /* 지원자id(학번) */ "
                        query += "     , t1.reg_dt        /* 등록일 */ "
                        query += "     , t1.unv_cd        /* 타대생 대학교 코드(mp0044) */ "
                        query += "     , t1.unv_nm        /* 타대생 대학교 명 */ "
                        query += "     , t1.cllg_cd       /* 타대생 대학 코드 */ "
                        query += "     , t1.cllg_nm       /* 타대생 대학 명 */ "
                        query += "     , t1.dept_cd       /* 타대생 학부/학과 코드 */ "
                        query += "     , t1.dept_nm       /* 타대생 학부/학과 명 */ "
                        query += "     , t1.brth_dt       /* 생년월일 */ "
                        query += "     , t1.gen           /* 성별 */ "
                        query += "     , t1.yr            /* 학년도 */ "
                        query += "     , t1.term_div      /* 학기 */ "
                        query += "     , t1.sch_yr        /* 학년 */ "
                        query += "     , t1.exp_dt        /* 자격 박탈일 */ "
                        query += "     , t1.exp_rsn       /* 박탈 사유 */ "
                        query += "     , t1.mob_no        /* 휴대전화 */ "
                        query += "     , t1.tel_no        /* 집전화 */ "
                        query += "     , t1.tel_no_g      /* 보호자 연락처 */ "
                        query += "     , t1.h_addr        /* 집주소 */ "
                        query += "     , t1.post_no       /* 우편번호 */ "
                        query += "     , t1.email_addr    /* 이메일 주소 */ "
                        query += "     , t1.bank_acct     /* 은행 계좌 번호 */ "
                        query += "     , t1.bank_cd       /* 은행 코드 */ "
                        query += "     , t1.bank_nm       /* 은행 명 */ "
                        query += "     , t1.bank_dpsr     /* 예금주 */ "
                        query += "     , t1.cnt_mp_a      /* 멘토링 지원 경력 */ "
                        query += "     , t1.cnt_mp_p      /* 멘토링 수행 경력 */ "
                        query += "     , t1.cnt_mp_c      /* 멘토링 완료 경력 */ "
                        query += "     , t1.cnt_mp_g      /* 멘토링 중도포기 경력 */ "
                        query += "     , t1.inv_agr_div   /* 개인정보 동의 여부 */ "
                        query += "     , t1.inv_agr_dt    /* 개인정보 동의 일시 */ "
                        query += "     , t1.dept_chr_id   /* 학과장 id */ "
                        query += "     , t1.dept_chr_nm   /* 학과장 명 */ "
                        query += "     , t1.ast_id        /* 조교 id */ "
                        query += "     , t1.ast_nm        /* 조교 명 */ "
                        query += "     , t1.dept_appr_div /* 학과 승인 여부 */ "
                        query += "     , t1.dept_appr_dt  /* 학과 승인 날짜 */ "
                        query += "     , t1.dept_retn_rsn /* 학과 반려 사유 */ "
                        query += "     , t1.ins_id        /* 입력자id */ "
                        query += "     , t1.ins_ip        /* 입력자ip */ "
                        query += "     , t1.ins_dt        /* 입력일시 */ "
                        query += "     , t1.ins_pgm       /* 입력프로그램id */ "
                        query += "     , t1.upd_id        /* 수정자id */ "
                        query += "     , t1.upd_ip        /* 수정자ip */ "
                        query += "     , t1.upd_dt        /* 수정일시 */ "
                        query += "     , t1.upd_pgm       /* 수정프로그램id */ "
                        query += "     , t1.mjr_cd        /* 전공코드 */ "
                        query += "     , t1.mjr_nm        /* 전공명 */ "
                        query += "     , t1.pwd           /* 비밀번호 */ "
                        query += " from service20_oth_std t1     /* 부산대학교 학생 정보 */ "              
                        if super_flag == 'Y':          
                            query += " where t1.std_id='"+str(id)+"'" 
                        else:
                            query += " where t1.std_id='"+str(id)+"'" 
                            query += " and t1.pwd = '"+str(pswd)+"'"    
                        V_OTH_GUBUN = 'F'
                        queryset2 = oth_std.objects.raw(query)
                        for var2 in queryset2:
                            #print(var2.fin_scr)
                            # vl_cscore1 = var2.fin_scr
                            V_OTH_GUBUN = 'T'
                            message = "Ok"
                            # context = {'message': message,
                            #     'apl_id' : str(var2.std_id),
                            #     'apl_nm' : str(var2.std_nm),
                            #     'univ_cd' : str(var2.unv_cd),
                            #     'univ_nm' : str(var2.unv_nm),
                            #     'brth_dt' : str(var2.brth_dt),
                            #     'gen_cd' : str(var2.gen),
                            #     'gen_nm' : str(var2.gen),
                            #     'login_gubun_code' : 'OTH',
                            #     'login_gubun' : '타대학생'
                            #     }
                            context = {'message': message,
                                'apl_nm' : str(var2.std_nm),
                                'apl_id' : str(var2.std_id),
                                'ms_id' : str(var2.ms_id),
                                'univ_cd' : str(var2.unv_cd),
                                'univ_nm' : str(var2.unv_nm),
                                'cllg_cd' : str(var2.cllg_cd),
                                'cllg_nm' : str(var2.cllg_nm),
                                'dept_cd' : str(var2.dept_cd),
                                'dept_nm' : str(var2.dept_nm.replace('\'','')),
                                'mjr_cd' : str(var2.mjr_cd),
                                'mjr_nm' : str(var2.mjr_nm),
                                'brth_dt' : str(var2.brth_dt),
                                'gen_cd' : str(var2.gen),
                                'yr' : str(var2.yr),
                                'sch_yr' : str(var2.sch_yr),
                                'term_div' : str(var2.term_div),
                                'tel_no' : str(var2.tel_no),
                                'tel_no_g' : str(var2.tel_no_g),
                                'h_addr' : str(var2.h_addr),
                                'post_no' : str(var2.post_no),
                                'email_addr' : str(var2.email_addr),
                                'bank_acct' : str(var2.bank_acct),
                                'bank_cd' : str(var2.bank_cd),
                                'bank_nm' : str(var2.bank_nm),
                                'bank_dpsr' : str(var2.bank_dpsr),
                                'login_gubun_code' : 'OTH',
                                'login_gubun' : '타대학생'
                                }
                        		# 타대학생 멘토

                        ########################################################################
                        # 타대학생 로그인처리 - 종료
                        ########################################################################         

        elif v_user_div == "G":
            # 학부모
            message = "Ok"
            if super_flag == "Y":
                created_flag2 = guardian.objects.filter(grdn_id=id).exists()
            else:
                created_flag2 = guardian.objects.filter(grdn_id=id,pwd=pswd).exists()

            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
                if super_flag == "Y":
                    rows = guardian.objects.filter(grdn_id=id)[0]
                else:
                    rows = guardian.objects.filter(grdn_id=id,pwd=pswd)[0]
                v_apl_id = rows.grdn_id
                v_apl_nm = rows.grdn_nm.replace('\'','')
                context = {'message': message,
                        'apl_nm' : v_apl_nm,
                        'apl_id' : v_apl_id,
                        'rel_tp' : rows.rel_tp,
                        'brth_dt' : rows.brth_dt,
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'moth_nat_cd' : rows.moth_nat_cd,
                        'moth_nat_nm' : rows.moth_nat_nm,
                        'tch_id' : rows.tch_id,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.h_post_no,
                        'email_addr' : rows.email_addr,
                        'login_gubun_code' : v_login_gubun_code,
                        'login_gubun' : v_login_gubun
                        }
        elif v_user_div == "T":
            # 교사
            message = "Ok"
            if super_flag == "Y":
                created_flag2 = teacher.objects.filter(tchr_id=id).exists()
            else:
                created_flag2 = teacher.objects.filter(tchr_id=id,pwd=pswd).exists()
            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
                if super_flag == "Y":
                    rows = teacher.objects.filter(tchr_id=id)[0]
                else:
                    rows = teacher.objects.filter(tchr_id=id,pwd=pswd)[0]
                v_apl_id = rows.tchr_id
                v_apl_nm = rows.tchr_nm.replace('\'','')
                context = {'message': message,
                        'apl_nm' : v_apl_nm,
                        'apl_id' : v_apl_id,
                        'sch_grd' : rows.sch_grd,
                        'sch_cd' : rows.sch_cd,
                        'sch_nm' : rows.sch_nm,
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'area_city' : rows.area_city,
                        'area_gu' : rows.area_gu,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.h_post_no,
                        's_addr' : rows.s_addr,
                        's_post_no' : rows.s_post_no,
                        'email_addr' : rows.email_addr,
                        'login_gubun_code' : v_login_gubun_code,
                        'login_gubun' : v_login_gubun
                        }
        elif v_user_div == "E":
            # 멘티
            message = "Ok"
            if super_flag == "Y":
                created_flag2 = mentee.objects.filter(mnte_id=id).exists()
            else:
                created_flag2 = mentee.objects.filter(mnte_id=id,pwd=pswd).exists()
            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
                if super_flag == "Y":
                    rows = mentee.objects.filter(mnte_id=id)[0]
                else:
                    rows = mentee.objects.filter(mnte_id=id,pwd=pswd)[0]
                v_apl_id = rows.mnte_id
                v_apl_nm = rows.mnte_nm.replace('\'','')
                context = {'message': message,
                        'apl_nm' : v_apl_nm,
                        'apl_id' : v_apl_id,
                        'brth_dt' : rows.brth_dt,
                        'sch_grd' : rows.sch_grd,
                        'sch_cd' : rows.sch_cd,
                        'sch_nm' : rows.sch_nm,
                        'gen' : rows.gen,
                        'yr' : rows.yr,
                        'term_div' : rows.term_div,
                        'sch_yr' : rows.sch_yr,                     
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.h_post_no,
                        'email_addr' : rows.email_addr,
                        'login_gubun_code' : v_login_gubun_code,
                        'login_gubun' : v_login_gubun
                        }        
        else:
            message = "Fail"
            context = {'message': message}    
#         context = {'message': message,'member_id':v_userid}

        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
                

@csrf_exempt
def login_login_admin(request):

        id =  request.POST.get('user_id')
        pswd =  request.POST.get('user_pw')
        # 로그인할 유저정보를 넣어주자 (모두 문자열)
        print("login_start => " + str(id))
        print("login_start(pswd) => " + str(pswd))
        login_info = {'id':id,'pswd': pswd,'dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
        # login_info = {'id':'514965','pswd': 'gks3089#','dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
        # HTTP GET Request: requests대신 s 객체를 사용한다.
        client_ip = request.META['REMOTE_ADDR']

        query = " insert into service20_com_evt     /* 이벤트로그 */ "
        query += "      ( evt_gb     /* 이벤트구분 */ "
        query += "     , evt_userid /* 이벤트사용자id */ "
        query += "     , evt_ip     /* 이벤트발생 ip */ "
        query += "     , evt_dat    /* 이벤트일시 */ "
        query += "     , evt_desc   /* 이벤트 내용 */ "
        query += "     , ins_id     /* 입력자id */ "
        query += "     , ins_ip     /* 입력자ip */ "
        query += "     , ins_dt     /* 입력일시 */ "
        query += "     , ins_pgm    /* 입력프로그램id */ "
        query += ") "
        query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
        query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
        query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
        query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
        query += "     , CONCAT('','로그인') evt_desc   /* 이벤트 내용 */ "
        query += "     , '"+str(id)+"' AS ins_id     /* 입력자id */ "
        query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
        query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
        query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
        cursor_log = connection.cursor()
        query_result = cursor_log.execute(query)    

        with requests.Session() as s:
       
            query = " insert into service20_com_evt     /* 이벤트로그 */ "
            query += "      ( evt_gb     /* 이벤트구분 */ "
            query += "     , evt_userid /* 이벤트사용자id */ "
            query += "     , evt_ip     /* 이벤트발생 ip */ "
            query += "     , evt_dat    /* 이벤트일시 */ "
            query += "     , evt_desc   /* 이벤트 내용 */ "
            query += "     , ins_id     /* 입력자id */ "
            query += "     , ins_ip     /* 입력자ip */ "
            query += "     , ins_dt     /* 입력일시 */ "
            query += "     , ins_pgm    /* 입력프로그램id */ "
            query += ") "
            query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ "
            query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ "
            query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ "
            query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ "
            query += "     , CONCAT('','success') evt_desc   /* 이벤트 내용 */ "
            query += "     , '"+id+"' AS ins_id     /* 입력자id */ "
            query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ "
            query += "     , NOW()     AS ins_dt     /* 입력일시 */ "
            query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ "
            cursor_log = connection.cursor()
            query_result = cursor_log.execute(query)  

            # userid = soup.find('input', {'name': 'userid'})
            # v_userid = userid['value']              
            v_userid = str(id)
            # MSSQL 접속


            ########################################################################
            # 어학 - 시작
            ########################################################################
            query = "select t3.apl_id         /* 학번 */"
            query += "     , t3.apl_nm         /* 성명 */"
            query += "     , t3.lang_kind_cd   /* 어학종류코드 */"
            query += "     , t3.lang_kind_nm   /* 어학종류명 */"
            query += "     , t3.lang_cd        /* 어학상위코드 */"
            query += "     , t3.lang_nm        /* 어학상위코드명 */"
            query += "     , t3.lang_detail_cd /* 어학하위코드 */"
            query += "     , t3.lang_detail_nm /* 어학하위코드명 */"
            query += "     , t3.frexm_nm       /* 외국어시험명 */"
            query += "     , t3.score          /* 시험점수 */"
            query += "     , t3.grade          /* 시험등급 */"
            query += "  from vw_nanum_foreign_exam t3     /* 유효한 외국어 성적 리스트 view(임시) */"
            query += " where 1=1"
            query += " and t3.apl_id='"+v_userid+"'" 
            conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
            cursor = conn.cursor()   
            cursor.execute(query)  
            row = cursor.fetchone()  

            # 삭제 (어학)
            delete_query = " delete from service20_vw_nanum_foreign_exam where apl_id = '"+v_userid+"' "
            cursor_delete = connection.cursor()
            delete_query_result = cursor_delete.execute(delete_query)                       
            # 삭제 (어학)

            while row:
            # for val in row:    
                l_apl_id = str(row[0])
                l_apl_nm = str(row[1])
                l_lang_kind_cd = str(row[2])
                l_lang_kind_nm = str(row[3])
                l_lang_cd = str(row[4])
                l_lang_nm = str(row[5])
                l_lang_detail_cd = str(row[6])
                l_lang_detail_nm = str(row[7])
                l_frexm_nm = str(row[8])
                l_score = str(row[9])
                l_grade = str(row[10])   

                # insert(어학)
                query = "insert into service20_vw_nanum_foreign_exam     /* 유효한 외국어 성적 리스트 view(임시) */"
                query += "   ( apl_id         /* 학번 */"
                query += "     , apl_nm         /* 성명 */"
                query += "     , lang_kind_cd   /* 어학종류코드 */"
                query += "     , lang_kind_nm   /* 어학종류명 */"
                query += "     , lang_cd        /* 어학상위코드 */"
                query += "     , lang_nm        /* 어학상위코드명 */"
                query += "     , lang_detail_cd /* 어학하위코드 */"
                query += "     , lang_detail_nm /* 어학하위코드명 */"
                query += "     , frexm_nm       /* 외국어시험명 */"
                query += "     , score          /* 시험점수 */"
                query += "     , grade          /* 시험등급 */"
                query += ")"
                query += "values"
                query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                query += "     ,CASE WHEN '"+str(l_lang_kind_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_cd)+"' END   /* 어학종류코드 */"
                query += "     ,CASE WHEN '"+str(l_lang_kind_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_nm)+"' END   /* 어학종류명 */"
                query += "     ,CASE WHEN '"+str(l_lang_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_cd)+"' END        /* 어학상위코드 */"
                query += "     ,CASE WHEN '"+str(l_lang_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_nm)+"' END        /* 어학상위코드명 */"
                query += "     ,CASE WHEN '"+str(l_lang_detail_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_cd)+"' END /* 어학하위코드 */"
                query += "     ,CASE WHEN '"+str(l_lang_detail_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_nm)+"' END /* 어학하위코드명 */"
                query += "     ,CASE WHEN '"+str(l_frexm_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_frexm_nm)+"' END       /* 외국어시험명 */"
                query += "     ,CASE WHEN '"+str(l_score)+"' =  'None' THEN '0' ELSE '"+str(l_score)+"' END          /* 시험점수 */"
                query += "     ,CASE WHEN '"+str(l_grade)+"' =  'None' THEN '0' ELSE '"+str(l_grade)+"' END          /* 시험등급 */"
                # query += "     ,CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 입력자id */"
                # query += "     ,CASE WHEN '"+str(client_ip)+"' =  'None' THEN NULL ELSE '"+str(client_ip)+"' END         /* 입력자ip */"
                # query += "     ,now()         /* 입력일시 */"
                # query += "     ,CASE WHEN '"+str(l_ins_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_ins_pgm)+"' END        /* 입력프로그램id */"
                # query += "     ,CASE WHEN '"+str(l_upd_id)+"' =  'None' THEN NULL ELSE '"+str(l_upd_id)+"' END         /* 수정자id */"
                # query += "     ,CASE WHEN '"+str(l_upd_ip)+"' =  'None' THEN NULL ELSE '"+str(l_upd_ip)+"' END         /* 수정자ip */"
                # query += "     ,CASE WHEN '"+str(l_upd_dt)+"' =  'None' THEN NULL ELSE '"+str(l_upd_dt)+"' END         /* 수정일시 */"
                # query += "     ,CASE WHEN '"+str(l_upd_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_upd_pgm)+"' END        /* 수정프로그램id */"
                query += ")"
                cursor3 = connection.cursor()
                query_result = cursor3.execute(query)    
                # insert(어학)
                row = cursor.fetchone()  
            ########################################################################
            # 어학 - 종료
            ########################################################################

            ########################################################################
            # 봉사 - 시작
            ########################################################################
            query = "select t3.apl_id          /* 학번 */"
            query += "     , t3.apl_nm          /* 성명 */"
            query += "     , t3.nation_inout_cd /* 국내외구분코드 */"
            query += "     , t3.nation_inout_nm /* 국내외구분명 */"
            query += "     , t3.sch_inout_cd    /* 교내외구분코드 */"
            query += "     , t3.sch_inout_nm    /* 교내외구분명 */"
            query += "     , t3.activity_nm     /* 봉사명 */"
            query += "     , t3.manage_org_nm   /* 주관기관명 */"
            query += "     , t3.start_date      /* 시작일자 */"
            query += "     , t3.start_time      /* 시작시간 */"
            query += "     , t3.end_date        /* 종료일자 */"
            query += "     , t3.end_time        /* 종료시간 */"
            query += "     , t3.tot_time        /* 총시간 */"
            query += "  from vw_nanum_service_activ t3     /* 학생 봉사 시간 view(임시) */"
            query += " where 1=1"
            query += " and t3.apl_id='"+v_userid+"'" 
            conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
            cursor = conn.cursor()   
            cursor.execute(query)  
            row = cursor.fetchone()  

            # 삭제 (봉사)
            delete_query = " delete from service20_vw_nanum_service_activ where apl_id = '"+v_userid+"' "
            cursor_delete = connection.cursor()
            delete_query_result = cursor_delete.execute(delete_query)                       
            # 삭제 (봉사)

            while row:
            # for val in row:        
                l_apl_id = str(row[0])
                l_apl_nm = str(row[1])
                l_nation_inout_cd = str(row[2])
                l_nation_inout_nm = str(row[3])
                l_sch_inout_cd = str(row[4])
                l_sch_inout_nm = str(row[5])
                l_activity_nm = str(row[6])
                l_manage_org_nm = str(row[7])
                l_start_date = str(row[8])
                l_start_time = str(row[9])
                l_end_date = str(row[10])
                l_end_time = str(row[11])
                l_tot_time = str(row[12])    

                # insert(봉사)
                query = "insert into service20_vw_nanum_service_activ     /* 학생 봉사 시간 view(임시)*/ "
                query += "   ( apl_id          /* 학번 */"
                query += "     , apl_nm          /* 성명 */"
                query += "     , nation_inout_cd /* 국내외구분코드 */"
                query += "     , nation_inout_nm /* 국내외구분명 */"
                query += "     , sch_inout_cd    /* 교내외구분코드 */"
                query += "     , sch_inout_nm    /* 교내외구분명 */"
                query += "     , activity_nm     /* 봉사명 */"
                query += "     , manage_org_nm   /* 주관기관명 */"
                query += "     , start_date      /* 시작일자 */"
                query += "     , start_time      /* 시작시간 */"
                query += "     , end_date        /* 종료일자 */"
                query += "     , end_time        /* 종료시간 */"
                query += "     , tot_time        /* 총시간 */"
                # query += "     , ins_id          /* 입력자id */"
                # query += "     , ins_ip          /* 입력자ip */"
                # query += "     , ins_dt          /* 입력일시 */"
                # query += "     , ins_pgm         /* 입력프로그램id */"
                # query += "     , upd_id          /* 수정자id */"
                # query += "     , upd_ip          /* 수정자ip */"
                # query += "     , upd_dt          /* 수정일시 */"
                # query += "     , upd_pgm         /* 수정프로그램id */"
                query += ")"
                query += "values"
                query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                query += "     , CASE WHEN '"+str(l_nation_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_cd)+"' END /* 국내외구분코드 */"
                query += "     , CASE WHEN '"+str(l_nation_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_nm)+"' END /* 국내외구분명 */"
                query += "     , CASE WHEN '"+str(l_sch_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_cd)+"' END    /* 교내외구분코드 */"
                query += "     , CASE WHEN '"+str(l_sch_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_nm)+"' END    /* 교내외구분명 */"
                query += "     , CASE WHEN '"+str(l_activity_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_activity_nm)+"'END     /* 봉사명 */"
                query += "     , CASE WHEN '"+str(l_manage_org_nm.replace('\'',''))+"' =  'None' THEN ' ' ELSE '"+str(l_manage_org_nm.replace('\'',''))+"' END   /* 주관기관명 */"
                query += "     , CASE WHEN '"+str(l_start_date)+"' =  'None' THEN ' ' ELSE '"+str(l_start_date)+"' END      /* 시작일자 */"
                query += "     , CASE WHEN '"+str(l_start_time)+"' =  'None' THEN ' ' ELSE '"+str(l_start_time)+"' END      /* 시작시간 */"
                query += "     , CASE WHEN '"+str(l_end_date)+"' =  'None' THEN ' ' ELSE '"+str(l_end_date)+"' END        /* 종료일자 */"
                query += "     , CASE WHEN '"+str(l_end_time)+"' =  'None' THEN ' ' ELSE  '"+str(l_end_time)+"' END       /* 종료시간 */"
                query += "     , CASE WHEN '"+str(l_tot_time)+"' =  'None' THEN ' ' ELSE '"+str(l_tot_time)+"' END        /* 총시간 */"
                # query += "     ,CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 입력자id */"
                # query += "     ,CASE WHEN '"+str(client_ip)+"' =  'None' THEN NULL ELSE '"+str(client_ip)+"' END         /* 입력자ip */"
                # query += "     ,now()         /* 입력일시 */"
                # query += "     , CASE WHEN '"+str(l_ins_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_ins_pgm)+"' END         /* 입력프로그램id */"
                # query += "     , CASE WHEN '"+str(l_upd_id)+"' =  'None' THEN NULL ELSE '"+str(l_upd_id)+"' END          /* 수정자id */"
                # query += "     , CASE WHEN '"+str(l_upd_ip)+"' =  'None' THEN NULL ELSE '"+str(l_upd_ip)+"' END          /* 수정자ip */"
                # query += "     , CASE WHEN '"+str(l_upd_dt)+"' =  'None' THEN NULL ELSE '"+str(l_upd_dt)+"' END          /* 수정일시 */"
                # query += "     , CASE WHEN '"+str(l_upd_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_upd_pgm)+"' END         /* 수정프로그램id */"
                query += ")"
                cursor4 = connection.cursor()
                query_result = cursor4.execute(query)    
                # insert(봉사)
                row = cursor.fetchone()  
            ########################################################################
            # 봉사 - 종료
            ########################################################################

            # 로그인처리 - 시작                
            query = "select t3.apl_id      /* 학번 */ "
            query += "     , t3.apl_nm      /* 성명 */ "
            query += "     , t3.apl_nm_e    /* 성명_영문 */ "
            query += "     , t3.unv_cd      /* 대학교코드 */ "
            query += "     , t3.unv_nm      /* 대학교명 */ "
            query += "     , t3.grad_div_cd /* 대학원구분코드 */ "
            query += "     , t3.grad_div_nm /* 대학원구분명 */ "
            query += "     , t3.cllg_cd     /* 대학코드 */ "
            query += "     , t3.cllg_nm     /* 대학명 */ "
            query += "     , t3.dept_cd     /* 학과코드 */ "
            query += "     , t3.dept_nm     /* 학과명 */ "
            query += "     , t3.mjr_cd      /* 전공코드 */ "
            query += "     , t3.mjr_nm      /* 전공명 */ "
            query += "     , t3.brth_dt     /* 생년월일 */ "
            query += "     , t3.gen_cd      /* 성별코드 */ "
            query += "     , t3.gen_nm      /* 성별명 */ "
            query += "     , t3.yr          /* 학년도 */ "
            query += "     , t3.sch_yr      /* 학년 */ "
            query += "     , t3.term_div    /* 학기코드 */ "
            query += "     , t3.term_nm     /* 학기명 */ "
            query += "     , t3.stds_div    /* 학적상태코드 */ "
            query += "     , t3.stds_nm     /* 학적상태명 */ "
            query += "     , t3.mob_no      /* 휴대전화번호 */ "
            query += "     , t3.tel_no      /* 집전화 */ "
            query += "     , t3.tel_no_g    /* 보호자연락처 */ "
            query += "     , t3.h_addr      /* 집주소 */ "
            query += "     , t3.post_no     /* 우편번호 */ "
            query += "     , t3.email_addr  /* 이메일주소 */ "
            query += "     , t3.bank_acct   /* 은행계좌번호 */ "
            query += "     , t3.bank_cd     /* 은행코드 */ "
            query += "     , t3.bank_nm     /* 은행명 */ "
            query += "     , t3.bank_dpsr   /* 예금주 */ "
            query += "     , t3.pr_yr       /* 직전 학년도 */ "
            query += "     , t3.pr_sch_yr   /* 직전 학년 */ "
            query += "     , t3.pr_term_div /* 직전학기코드 */ "
            query += "     , t3.score01     /* 직전학기 석차 */ "
            query += "     , t3.score02     /* 직전학기 총원 */ "
            query += "     , t3.score03     /* 직전학기 학점 */ "
            query += "     , t3.score04     /* 봉사점수합계 */ "
            query += "     , t3.score05     /* 자격증 개수 */ "
            query += "     , t3.score06     /* 직전학기 이수학점 */ "
            query += "     , t3.cmp_term     /* 전체 이수학기  */ "
            query += " from vw_nanum_stdt t3     /* 부산대학교 학생 정보 */ "              
            query += " where t3.apl_id='"+v_userid+"'" 
            # query += " where t3.apl_id='201866148'"                 
            conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
            cursor = conn.cursor()   
            cursor.execute(query)  
            row = cursor.fetchone()  
            print(row)
            if row == None:
                context = {'loginStudent': 'fail',}
            else:    
                message = "login_notFound"
                while row:
                    message = "Ok"
                    # 삭제
                    delete_query = " delete from service20_vw_nanum_stdt where apl_id = '"+str(row[0])+"' "
                    cursor_delete = connection.cursor()
                    delete_query_result = cursor_delete.execute(delete_query)                       
                    # 삭제
                    
                    # insert
                    insert_query = " insert into service20_vw_nanum_stdt (apl_id      /* 학번 */ "
                    insert_query += " , apl_nm      /* 성명 */ "
                    insert_query += " , apl_nm_e    /* 성명_영문 */ "
                    insert_query += " , unv_cd      /* 대학교코드 */ "
                    insert_query += " , unv_nm      /* 대학교명 */ "
                    insert_query += " , grad_div_cd /* 대학원구분코드 */ "
                    insert_query += " , grad_div_nm /* 대학원구분명 */ "
                    insert_query += " , cllg_cd     /* 대학코드 */ "
                    insert_query += " , cllg_nm     /* 대학명 */ "
                    insert_query += " , dept_cd     /* 학과코드 */ "
                    insert_query += " , dept_nm     /* 학과명 */ "
                    insert_query += " , mjr_cd      /* 전공코드 */ "
                    insert_query += " , mjr_nm      /* 전공명 */ "
                    insert_query += " , brth_dt     /* 생년월일 */ "
                    insert_query += " , gen_cd      /* 성별코드 */ "
                    insert_query += " , gen_nm      /* 성별명 */ "
                    insert_query += " , yr          /* 학년도 */ "
                    insert_query += " , sch_yr      /* 학년 */ "
                    insert_query += " , term_div    /* 학기코드 */ "
                    insert_query += " , term_nm     /* 학기명 */ "
                    insert_query += " , stds_div    /* 학적상태코드 */ "
                    insert_query += " , stds_nm     /* 학적상태명 */ "
                    insert_query += " , mob_no      /* 휴대전화번호 */ "
                    insert_query += " , tel_no      /* 집전화 */ "
                    insert_query += " , tel_no_g    /* 보호자연락처 */ "
                    insert_query += " , h_addr      /* 집주소 */ "
                    insert_query += " , post_no     /* 우편번호 */ "
                    insert_query += " , email_addr  /* 이메일주소 */ "
                    insert_query += " , bank_acct   /* 은행계좌번호 */ "
                    insert_query += " , bank_cd     /* 은행코드 */ "
                    insert_query += " , bank_nm     /* 은행명 */ "
                    insert_query += " , bank_dpsr   /* 예금주 */ "
                    insert_query += " , pr_yr       /* 직전 학년도 */ "
                    insert_query += " , pr_sch_yr   /* 직전 학년 */ "
                    insert_query += " , pr_term_div /* 직전학기코드 */ "
                    insert_query += " , score01     /* 직전학기 석차 */ "
                    insert_query += " , score02     /* 직전학기 총원 */ "
                    insert_query += " , score03     /* 직전학기 학점 */ "
                    insert_query += " , score04     /* 봉사점수합계 */ "
                    insert_query += " , score05     /* 자격증 개수 */ "
                    insert_query += " ) values ("
#                   insert_query += " (select ifnull(max(id)+1,1) from service20_vw_nanum_stdt)  "
                    insert_query += " CASE WHEN '"+str(row[0])+"' =  'None' THEN NULL ELSE '"+str(row[0])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[1])+"' =  'None' THEN NULL ELSE '"+str(row[1])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[2])+"' =  'None' THEN NULL ELSE '"+str(row[2])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[3])+"' =  'None' THEN NULL ELSE '"+str(row[3])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[4])+"' =  'None' THEN NULL ELSE '"+str(row[4])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[5])+"' =  'None' THEN NULL ELSE '"+str(row[5])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[6])+"' =  'None' THEN NULL ELSE '"+str(row[6])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[7])+"' =  'None' THEN NULL ELSE '"+str(row[7])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[8])+"' =  'None' THEN NULL ELSE '"+str(row[8])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[9])+"' =  'None' THEN NULL ELSE '"+str(row[9])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[10])+"' =  'None' THEN NULL ELSE '"+str(row[10])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[11])+"' =  'None' THEN NULL ELSE '"+str(row[11])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[12])+"' =  'None' THEN NULL ELSE '"+str(row[12])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[13])+"' =  'None' THEN NULL ELSE '"+str(row[13])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[14])+"' =  'None' THEN NULL ELSE '"+str(row[14])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[15])+"' =  'None' THEN NULL ELSE '"+str(row[15])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[16])+"' =  'None' THEN NULL ELSE '"+str(row[16])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[17])+"' =  'None' THEN NULL ELSE '"+str(row[17])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[18])+"' =  'None' THEN NULL ELSE '"+str(row[18])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[19])+"' =  'None' THEN NULL ELSE '"+str(row[19])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[20])+"' =  'None' THEN NULL ELSE '"+str(row[20])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[21])+"' =  'None' THEN NULL ELSE '"+str(row[21])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[22])+"' =  'None' THEN NULL ELSE '"+str(row[22])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[23])+"' =  'None' THEN NULL ELSE '"+str(row[23])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[24])+"' =  'None' THEN NULL ELSE '"+str(row[24])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[25])+"' =  'None' THEN NULL ELSE '"+str(row[25])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[26])+"' =  'None' THEN NULL ELSE '"+str(row[26])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[27])+"' =  'None' THEN NULL ELSE '"+str(row[27])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[28])+"' =  'None' THEN NULL ELSE '"+str(row[28])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[29])+"' =  'None' THEN NULL ELSE '"+str(row[29])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[30])+"' =  'None' THEN NULL ELSE '"+str(row[30])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[31])+"' =  'None' THEN NULL ELSE '"+str(row[31])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[32])+"' =  'None' THEN NULL ELSE '"+str(row[32])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[33])+"' =  'None' THEN NULL ELSE '"+str(row[33])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[34])+"' =  'None' THEN NULL ELSE '"+str(row[34])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[35])+"' =  'None' THEN NULL ELSE '"+str(row[35])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[36])+"' =  'None' THEN NULL ELSE '"+str(row[36])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[37])+"' =  'None' THEN NULL ELSE '"+str(row[37])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[38])+"' =  'None' THEN NULL ELSE '"+str(row[38])+"' END"
                    insert_query += " , CASE WHEN '"+str(row[39])+"' =  'None' THEN NULL ELSE '"+str(row[39])+"' END"
                    insert_query += " )"                    
                    cursor2 = connection.cursor()
                    query_result = cursor2.execute(insert_query)    
                    # insert

                    mentor_query = " select mntr_id from service20_mentor where apl_id = '"+str(row[0])+"'"
                    mentor_cursor = connection.cursor()
                    query_result = mentor_cursor.execute(mentor_query)    

                    if query_result == 0:
                        v_mntr_id = ''
                    else:
                        #mentor_query
                        rows_mentor = mentor.objects.filter(apl_id=str(row[0]))[0]
                        
                        v_mntr_id = str(rows_mentor.mntr_id)                            
                                        
                    context = {'message': message,
                    'apl_id' : str(row[0]),
                    'apl_nm' : str(row[1]),
                    'univ_cd' : str(row[3]),
                    'univ_nm' : str(row[4]),
                    'grad_div_cd' : str(row[5]),
                    'grad_div_nm' : str(row[6]),
                    'cllg_cd' : str(row[7]),
                    'cllg_nm' : str(row[8]),
                    'dept_cd' : str(row[9]),
                    'dept_nm' : str(row[10]),
                    'mjr_cd' : str(row[11]),
                    'mjr_nm' : str(row[12]),
                    'brth_dt' : str(row[13]),
                    'gen_cd' : str(row[14]),
                    'gen_nm' : str(row[15]),
                    'yr' : str(row[16]),
                    'sch_yr' : str(row[17]),
                    'term_div' : str(row[18]),
                    'term_nm' : str(row[19]),
                    'stdt_div' : str(row[20]),
                    'stdt_nm' : str(row[21]),
                    'mob_nm' : str(row[22]),
                    'tel_no' : str(row[23]),
                    'tel_no_g' : str(row[24]),
                    'h_addr' : str(row[25]),
                    'post_no' : str(row[26]),
                    'email_addr' : str(row[27]),
                    'bank_acct' : str(row[28]),
                    'bank_cd' : str(row[29]),
                    'bank_nm' : str(row[30]),
                    'bank_dpsr' : str(row[31]),
                    'pr_yr' : str(row[32]),
                    'pr_sch_yr' : str(row[33]),
                    'pr_term_div' : str(row[34]),
                    'score01' : str(row[35]),
                    'score02' : str(row[36]),
                    'score03' : str(row[37]),
                    'score04' : str(row[38]),
                    'score05' : str(row[39]),
                    'mntr_id' : v_mntr_id
                    }
                    row = cursor.fetchone()                                                                     
                # 로그인처리 - 종료   

        
#         context = {'message': message,'member_id':v_userid}

        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
        


@csrf_exempt
def login_returnsso(request):
        print("====login_returnsso====")
        a =  request.POST.get('gbn')
        request.session['member_id'] = 'test'
        print("====login_returnsso====")
        print(request.session['member_id'])
        
        message = "Ok"
        context = {'message': message,    }

        return redirect('http://nanum.pusan.ac.kr/login/success.html', { 'context': context })
                
@csrf_exempt
def login_session(request):
        v_member_id = request.session.get('member_id', None)
        if v_member_id == None:
            message = 'NoSession'       
        else:
            message = request.session['member_id']
        context = {'message': message,}
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#자료실
class com_datacenter_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = bbs2
        fields = '__all__'

class com_datacenter(generics.ListAPIView):
    queryset = bbs2.objects.all()
    serializer_class = com_datacenter_Serializer

    def list(self, request):   
        mp_id = request.GET.get('mp_id', "")
        # queryset = self.get_queryset()
        query = "select * from service20_bbs2 where mp_id like Ifnull(Nullif('"+str(mp_id)+"', ''), '%%') order by id desc; "

        queryset = bbs1.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#자료실 디테일
class com_datacenter_detail_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = bbs2
        fields = '__all__'

class com_datacenter_detail(generics.ListAPIView):
    queryset = bbs2.objects.all()
    serializer_class = com_datacenter_detail_Serializer

    def list(self, request):   
        l_id = request.GET.get('id', "")

        queryset = self.get_queryset()
        queryset = bbs2.objects.filter(id=l_id)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#공지사항
class com_notice_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = bbs1
        fields = '__all__'

class com_notice(generics.ListAPIView):
    queryset = bbs1.objects.all()
    serializer_class = com_notice_Serializer

    def list(self, request):   
        queryset = self.get_queryset()

        query = " select * from service20_bbs1  order by id desc "

        queryset = bbs1.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#공지사항 디테일
class com_notice_detail_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = bbs1
        fields = '__all__'

class com_notice_detail(generics.ListAPIView):
    queryset = bbs1.objects.all()
    serializer_class = com_notice_detail_Serializer

    def list(self, request):   
        l_id = request.GET.get('id', "")

        queryset = self.get_queryset()
        queryset = bbs1.objects.filter(id=l_id)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#멘토링 소개(리스트)
class com_mentoHistory_list_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm_introduce
        fields = '__all__'

class com_mentoHistory_list(generics.ListAPIView):
    queryset = mpgm_introduce.objects.all()
    serializer_class = com_mentoHistory_list_Serializer

    def list(self, request):   
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()
        
        queryset = mpgm_introduce.objects.all()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        


#멘토링 소개
class com_mentoHistory_Serializer(serializers.ModelSerializer):
    
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm_introduce
        fields = '__all__'

class com_mentoHistory(generics.ListAPIView):
    queryset = mpgm_introduce.objects.all()
    serializer_class = com_mentoHistory_Serializer

    def list(self, request):   
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()
        
        queryset = mpgm_introduce.objects.filter(mp_id=l_mp_id)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        


# 년도 콤보박스 ###################################################
class com_combo_yr_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_yr(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_yr_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '1' id,DATE_FORMAT(now(),'%%Y')-1 as std_detl_code,DATE_FORMAT(now(),'%%Y')-1 as std_detl_code_nm "
        query += " union "
        query += " select '2' id,DATE_FORMAT(now(),'%%Y') as std_detl_code,DATE_FORMAT(now(),'%%Y') as std_detl_code_nm "
        query += " union "
        query += " select '3' id,DATE_FORMAT(now(),'%%Y')+1 as std_detl_code,DATE_FORMAT(now(),'%%Y')+1 as std_detl_code_nm "
        query += " union "
        query += " select '4' id,DATE_FORMAT(now(),'%%Y')+2 as std_detl_code,DATE_FORMAT(now(),'%%Y')+2 as std_detl_code_nm "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 보호자승인 콤보박스 ###################################################
class com_combo_appr_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_appr(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_appr_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm "
        query += " union  "
        query += " select id as id "
        query += "     , std_detl_code as std_detl_code"
        query += "     , std_detl_code_nm as std_detl_code_nm"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'MP0082'    /* 승인여부 */"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 관리자승인 콤보박스 ###################################################
class com_combo_mgr_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_mgr(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_mgr_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm "
        query += " union  "
        query += " select id as id "
        query += "     , std_detl_code as std_detl_code"
        query += "     , std_detl_code_nm as std_detl_code_nm"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'MP0069'    /* 관리자승인여부 */"

        print(query)
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 계획서, 보고서 상태 콤보박스 ###################################################
class com_combo_pln_status_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_pln_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_pln_status_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        # query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm "
        # query += " union  "
        # query += " select id as id "
        # query += "     , std_detl_code as std_detl_code"
        # query += "     , std_detl_code_nm as std_detl_code_nm"
        # query += "  from service20_com_cdd"
        # query += " where std_grp_code = 'MP0070'    /* 계획서작성부 */"
        # query += "   and std_detl_code in ('20', '11', '30') "

        query = """
                select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm 
                union  
                select id as id, std_detl_code as std_detl_code
                    , case when trim(rmrk) = '' then std_detl_code_nm else concat(std_detl_code_nm, '(',rmrk ,')') end std_detl_code_nm 
                from service20_com_cdd
                where std_grp_code = 'MP0070'    /* 계획서작성부 */
                and std_detl_code in ('20', '11', '30');
        """
        
        print(query)
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학기 콤보박스 ###################################################
class com_combo_termdiv_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_termdiv(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_termdiv_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '1' id,'10' as std_detl_code,'1' as std_detl_code_nm "
        query += " union "
        query += " select '2' id,'20' as std_detl_code,'2' as std_detl_code_nm "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 월단위 콤보박스 ###################################################
class com_combo_month_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_month(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_month_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '' as id, '' as std_detl_code, '전체' as std_detl_code_nm"
        query += " union"
        query += " select '01' as id, '01' as std_detl_code, '01' as std_detl_code_nm"
        query += " union"
        query += " select '02' as id, '02' as std_detl_code, '02' as std_detl_code_nm"
        query += " union"
        query += " select '03' as id, '03' as std_detl_code, '03' as std_detl_code_nm"
        query += " union"
        query += " select '04' as id, '04' as std_detl_code, '04' as std_detl_code_nm"
        query += " union"
        query += " select '05' as id, '05' as std_detl_code, '05' as std_detl_code_nm"
        query += " union"
        query += " select '06' as id, '06' as std_detl_code, '06' as std_detl_code_nm"
        query += " union"
        query += " select '07' as id, '07' as std_detl_code, '07' as std_detl_code_nm"
        query += " union"
        query += " select '08' as id, '08' as std_detl_code, '08' as std_detl_code_nm"
        query += " union"
        query += " select '09' as id, '09' as std_detl_code, '09' as std_detl_code_nm"
        query += " union"
        query += " select '10' as id, '10' as std_detl_code, '10' as std_detl_code_nm"
        query += " union"
        query += " select '11' as id, '11' as std_detl_code, '11' as std_detl_code_nm"
        query += " union"
        query += " select '12' as id, '12' as std_detl_code, '12' as std_detl_code_nm"

        print(query)
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

###############################################################      
# 취소사유 (콤보) Start 
###############################################################
class com_combo_cnclRsn_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_cnclRsn(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_cnclRsn_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        
        query = " select id,std_grp_code,std_detl_code,std_detl_code_nm,rmrk,sort_seq_no from service20_com_cdd where std_grp_code = 'ms0004' and use_indc = 'Y'"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 
###############################################################      
# 취소사유 (콤보) End
############################################################### 
#
###############################################################      
# 멘티 학습외 취소사유 (콤보) Start 
###############################################################
class com_combo_mnteCnclRsn_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_mnteCnclRsn(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_mnteCnclRsn_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        
        query = " select id,std_grp_code,std_detl_code,std_detl_code_nm,rmrk,sort_seq_no from service20_com_cdd where std_grp_code = 'MP0098' and use_indc = 'Y'"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 
###############################################################      
# 멘티 학습외 취소사유 (콤보) End
###############################################################    

class com_combo_repdiv_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_repdiv(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_repdiv_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        
        query = "select id,std_detl_code"
        query += "     , std_detl_code_nm,sort_seq_no "
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'mp0062'"
        query += " order by sort_seq_no "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class com_combo_com_cdd_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_com_cdd(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_com_cdd_Serializer

    def list(self, request):
        l_code = request.GET.get('code', "")

        queryset = self.get_queryset()
        
        
        query = "select id,std_detl_code"
        query += "     , std_detl_code_nm, sort_seq_no"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = '"+str(l_code)+"'"
        query += " order by sort_seq_no "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class com_combo_program2_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mpgm
        fields = ('mp_id','status','mp_name','yr','mnt_term')


class com_combo_program2(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_program2_Serializer

    def list(self, request):
        yr = request.GET.get('yr', "")
        mnt_term = request.GET.get('apl_term', "")
        user_id = request.GET.get('user_id', "")
        status = request.GET.get('status', "")

        queryset = self.get_queryset()
        
        
        query = "select distinct"
        query += "       t1.mp_id         /* 멘토링 프로그램id */"
        query += "     , t1.status        /* 상태(mp0001) */"
        query += "     , t1.mp_name       /* 멘토링 프로그램 명 */"
        query += "     , t1.yr            /* 연도 */"
        query += "     , t1.mnt_term      /* 활동시기 */"
        query += "  from service20_mpgm t1"
        query += "  left join service20_mp_mtr    t3 on (t3.mp_id     = t1.mp_id)"
        query += "  left join service20_mp_mte    t4 on (t4.mp_id     = t3.mp_id"
        query += "                                   and t4.apl_no    = t3.apl_no )"
        query += " where t1.yr       = '"+str(yr)+"'"
        query += "   and t1.mnt_term = '"+str(mnt_term)+"'"
        query += "   and t1.status like Ifnull(Nullif('"+str(status)+"', ''), '%%')  "
        query += "   and ( t4.tchr_id = '"+str(user_id)+"'"
        query += "       or t4.grd_id  = '"+str(user_id)+"'"
        query += "       or t4.mnte_id = '"+str(user_id)+"'"
        query += "       or t3.apl_id = '"+str(user_id)+"' )"

        print(query)

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)  

class com_combo_program3_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mpgm
        fields = ('mp_id','status','mp_name','yr','mnt_term')


class com_combo_program3(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_program3_Serializer

    def list(self, request):
        yr = request.GET.get('yr', "")
        mnt_term = request.GET.get('apl_term', "")
        user_id = request.GET.get('user_id', "")
        status = request.GET.get('status', "")
        login_gubun_code = request.GET.get('login_gubun_code', "")
        queryset = self.get_queryset()
        
        
        query = "select distinct"
        query += "       t1.mp_id         /* 멘토링 프로그램id */"
        query += "     , t1.status        /* 상태(mp0001) */"
        query += "     , t1.mp_name       /* 멘토링 프로그램 명 */"
        query += "     , t1.yr            /* 연도 */"
        query += "     , t1.mnt_term      /* 활동시기 */"
        query += "  from service20_mpgm t1"
        query += "  left join service20_mp_mtr    t3 on (t3.mp_id     = t1.mp_id)"
        query += "  left join service20_mp_mte    t4 on (t4.mp_id     = t3.mp_id"
        query += "                                   and t4.apl_no    = t3.apl_no )"
        query += " where t1.yr       = '"+str(yr)+"'"
        query += "   and t1.mnt_term = '"+str(mnt_term)+"'"
        # query += "   and (('" + login_gubun_code + "' = 'M' and t3.status = '" + str(status) + "') "
        # query += "      or (('" + login_gubun_code + "' = 'T' or '" + login_gubun_code + "' = 'G' or '" + login_gubun_code + "' = 'E') and t4.status = '" + str(status) + "')) "

        query += "   and (('" + login_gubun_code + "' = 'M' and t3.status = '50') "
        query += "      or (('" + login_gubun_code + "' = 'T' or '" + login_gubun_code + "' = 'G' or '" + login_gubun_code + "' = 'E') and t4.status = '40')) "

        # query += "   and t3.status = '" + str(status) + "' "
        query += "   and ( t4.tchr_id = '"+str(user_id)+"'"
        query += "       or t4.grd_id  = '"+str(user_id)+"'"
        query += "       or t4.mnte_id = '"+str(user_id)+"'"
        query += "       or t3.apl_id = '"+str(user_id)+"' )"

        print(query)

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)  

class com_list_my_mentee_Serializer(serializers.ModelSerializer):

    mp_plc_nm = serializers.SerializerMethodField()
    grd_rel_nm = serializers.SerializerMethodField()
    class Meta:
        model = mp_mte
        fields = ('mp_id','mnte_no','mnte_id','mnte_nm','mnte_nm_e','apl_no','brth_dt','mp_hm','mp_plc','mp_addr','sch_grd','sch_cd','sch_nm','gen','yr','term_div','sch_yr','mob_no','tel_no','grd_id','grd_nm','grd_tel','grd_rel','prnt_nat_cd','prnt_nat_nm','tchr_id','tchr_nm','tchr_tel','area_city','area_gu','h_addr','h_post_no','s_addr','s_post_no','email_addr','apl_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_plc_nm','grd_rel_nm')
    
    def get_mp_plc_nm(self, obj):
        return obj.mp_plc_nm
    def get_grd_rel_nm(self, obj):
        return obj.grd_rel_nm

class com_list_my_mentee(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = com_list_my_mentee_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        
        # l_mp_id = "P182014"
        # l_apl_id = "201610101"

        queryset = self.get_queryset()
        
        query = " select (select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0052' and std_detl_code = S2.mp_plc and use_indc = 'Y') mp_plc_nm"
        query += " ,(select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0047' and std_detl_code = S2.grd_rel and use_indc = 'Y') grd_rel_nm "
        query += " , S2.* "
        query += " FROM service20_mp_mtr S1 "
        query += " LEFT JOIN service20_mp_mte S2  ON (S2.MP_ID  = S1.MP_ID "
        query += " AND S2.APL_NO = S1.APL_NO) "
        query += " LEFT JOIN service20_mp_plnh S3 ON (S3.MP_ID    = S1.MP_ID "
        query += " AND S3.APL_NO   = S1.APL_NO) "
        query += " WHERE 1=1 "
        query += " AND S1.MP_ID      = '"+l_mp_id+"'     /* 멘토링 프로그램ID */ "
        query += " AND S1.APL_ID    =  '"+l_apl_id+"' "


        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

# 교육구분 콤보박스 ###################################################
class com_combo_edu_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_edu(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_edu_Serializer

    def list(self, request):
        l_flag = request.GET.get('flag', "")
        queryset = self.get_queryset()
        
        query = ""
        if l_flag == 'T':
            query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm from dual union"
        elif l_flag == 'S':
            query = " select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm from dual union"

        query += " select id as id "
        query += "     , std_detl_code as std_detl_code"
        query += "     , std_detl_code_nm as std_detl_code_nm"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'MP0059'    /* 교육구분 */"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석구분 콤보박스 ###################################################
class com_combo_att_div_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_att_div(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_att_div_Serializer

    def list(self, request):
        l_flag = request.GET.get('flag', "")
        queryset = self.get_queryset()
        
        query = ""
        if l_flag == 'T':
            query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm from dual union"
        elif l_flag == 'S':
            query = " select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm from dual union"

        query += " select id as id "
        query += "     , std_detl_code as std_detl_code"
        query += "     , std_detl_code_nm as std_detl_code_nm"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'MP0063'    /* 출석구분 */"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석상태 콤보박스 ###################################################
class com_combo_att_status_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_att_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_att_status_Serializer

    def list(self, request):
        l_flag = request.GET.get('flag', "")
        queryset = self.get_queryset()
        
        query = ""
        if l_flag == 'T':
            query = " select '0' as id, '' as std_detl_code, '전체' as std_detl_code_nm from dual union"
        elif l_flag == 'S':
            query = " select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm from dual union"
            
        query += " select id as id "
        query += "     , std_detl_code as std_detl_code"
        query += "     , std_detl_code_nm as std_detl_code_nm"
        query += "  from service20_com_cdd"
        query += " where std_grp_code = 'MP0060'    /* 출석상태 */"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 취소사유 콤보박스
class com_combo_program_Serializer(serializers.ModelSerializer):

    mp_name = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    class Meta:
        model = mpgm
        fields = ('mp_id','apl_no','mp_name')

    def get_mp_name(self, obj):
        return obj.mp_name
    def get_apl_no(self, obj):
        return obj.apl_no

class com_combo_program(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = com_combo_program_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        status = request.GET.get('status', 0)
        

        queryset = self.get_queryset()

        query = " select A.mp_id "
        query += " , A.apl_no "
        query += " , B.mp_name "
        query += " FROM service20_mp_mtr A "
        query += " , service20_mpgm B "
        query += " WHERE apl_id = '"+str(apl_id)+"' "
        query += " AND mntr_id IS NOT null "
        query += " AND A.mp_id = B.mp_id "
        query += " AND A.status = '" + str(status) + "' "

        print(query)
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 모집상태 콤보박스
class com_combo_ms_status_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_ms_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_ms_status_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id,std_detl_code,std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0001' "
        query += " union  "
        query += " select '','xx','모집완료'  "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                

# 모집상태 콤보박스
class com_combo_mp_status_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_mp_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_mp_status_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id,std_detl_code,std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001' and std_detl_code in ('20', '30', '60', '90')"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                


# 어학점수
class com_user_fe_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = vw_nanum_foreign_exam
        fields = ('apl_id','apl_nm','lang_kind_cd','lang_kind_nm','lang_cd','lang_nm','lang_detail_cd','lang_detail_nm','frexm_nm','score','grade')


class com_user_fe(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = com_user_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        
        query = "select t3.id,t3.apl_id         /* 학번 */"
        query += "     , t3.apl_nm         /* 성명 */"
        query += "     , t3.lang_kind_cd   /* 어학종류코드 */"
        query += "     , t3.lang_kind_nm   /* 어학종류명 */"
        query += "     , t3.lang_cd        /* 어학상위코드 */"
        query += "     , t3.lang_nm        /* 어학상위코드명 */"
        query += "     , t3.lang_detail_cd /* 어학하위코드 */"
        query += "     , t3.lang_detail_nm /* 어학하위코드명 */"
        query += "     , t3.frexm_nm       /* 외국어시험명 */"
        query += "     , t3.score          /* 시험점수 */"
        query += "     , t3.grade          /* 시험등급 */"
        query += "  from service20_vw_nanum_foreign_exam t3     /* 유효한 외국어 성적 리스트 view(임시) */"
        query += " where 1=1"
        query += " and t3.apl_id='"+str(ida)+"'" 

        queryset = vw_nanum_foreign_exam.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 봉사점수
class com_user_sa_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = vw_nanum_service_activ
        fields = ('apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time')


class com_user_sa(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = com_user_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        

        query = "select t3.id,t3.apl_id          /* 학번 */"
        query += "     , t3.apl_nm          /* 성명 */"
        query += "     , t3.nation_inout_cd /* 국내외구분코드 */"
        query += "     , t3.nation_inout_nm /* 국내외구분명 */"
        query += "     , t3.sch_inout_cd    /* 교내외구분코드 */"
        query += "     , t3.sch_inout_nm    /* 교내외구분명 */"
        query += "     , t3.activity_nm     /* 봉사명 */"
        query += "     , t3.manage_org_nm   /* 주관기관명 */"
        query += "     , t3.start_date      /* 시작일자 */"
        query += "     , t3.start_time      /* 시작시간 */"
        query += "     , t3.end_date        /* 종료일자 */"
        query += "     , t3.end_time        /* 종료시간 */"
        query += "     , t3.tot_time        /* 총시간 */"
        query += "  from service20_vw_nanum_service_activ t3     /* 학생 봉사 시간 view(임시) */"
        query += " where 1=1"
        query += "   AND apl_id = '"+str(ida)+"' "

        queryset = vw_nanum_service_activ.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 사용자정보
class com_user_Serializer(serializers.ModelSerializer):
    
    mntr_id = serializers.SerializerMethodField()
    login_gubun_code = serializers.SerializerMethodField()
    login_gubun = serializers.SerializerMethodField()
 
    class Meta:
        model = vw_nanum_stdt
        fields = '__all__'

    def get_mntr_id(self,obj):
        return obj.mntr_id
    def get_login_gubun_code(self,obj):
        return obj.login_gubun_code
    def get_login_gubun(self,obj):
        return obj.login_gubun

class com_user(generics.ListAPIView):
    queryset = vw_nanum_stdt.objects.all()
    serializer_class = com_user_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        

        #mentor_query
        mentor_query = " select mntr_id from service20_mentor where apl_id = '"+str(ida)+"'"
        mentor_cursor = connection.cursor()
        query_result = mentor_cursor.execute(mentor_query)  


        if query_result == 0:
            v_mntr_id = ''
        else:
            #mentor_query
            rows_mentor = mentor.objects.filter(apl_id=str(ida))[0]
            v_mntr_id = str(rows_mentor.mntr_id)


        query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
        query += " where user_id = '"+str(ida)+"'"
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
        results = namedtuplefetchall(cursor)  
        v_login_gubun_code = ''
        
        if query_result == 0:
            v_login_gubun = ''
        else:
            v_login_gubun_code = str(results[0].user_div)
            v_login_gubun = str(results[0].std_detl_code_nm)

        query = "select '"+str(v_mntr_id)+"' as mntr_id, '"+str(v_login_gubun_code)+"' as login_gubun_code, '"+str(v_login_gubun)+"' as login_gubun, t1.* "
        query += "  from service20_vw_nanum_stdt t1 "
        query += " where 1=1"
        query += "   AND apl_id = '"+str(ida)+"' "

        queryset = vw_nanum_stdt.objects.raw(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
#####################################################################################
# 공통 - END
#####################################################################################

#####################################################################################
# mypage - START
#####################################################################################

# 멘토 마이페이지 ###################################################
class mentoMypage_list_Serializer(serializers.ModelSerializer):

    class Meta:
        model = vw_nanum_stdt
        fields = '__all__'


class mentoMypage_list(generics.ListAPIView):
    queryset = vw_nanum_stdt.objects.all()
    serializer_class = mentoMypage_list_Serializer


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = " select t1.id "
        query += "      , t1.apl_id     /* 지원자(멘토,학생) 학번 */  "
        query += "      , t1.apl_nm          /* 지원자(멘토,학생) 명 */  "
        query += "      , t1.brth_dt         /* 생년월일 */  "
        query += "      , t1.gen_nm             /* 성별 */  "
        query += "      , t1.cllg_nm         /* 지원자 대학 명 */  "
        query += "      , t1.dept_nm         /* 지원자 학부/학과 명 */  "
        query += "      , t1.mob_no          /* 휴대전화 */  "
        query += "      , t1.email_addr      /* 이메일 주소 */  "
        query += "  from service20_vw_nanum_stdt t1 "
        query += " where 1=1 "
        query += "   and t1.apl_id = '"+l_user_id+"' "
        query += " union all"
        query += " select  t2.id "
        query += "       , t2.apl_id as apl_id"
        query += "      , t2.std_nm as apl_nm"
        query += "      , t2.brth_dt         /* 생년월일 */  "
        query += "      , case when t2.gen = '1' then '남'             /* 성별 */  "
        query += "             else '여' end as gen_nm             /* 성별 */  "
        query += "      , t2.cllg_nm         /* 지원자 대학 명 */  "
        query += "      , t2.dept_nm         /* 지원자 학부/학과 명 */  "
        query += "      , t2.mob_no          /* 휴대전화 */  "
        query += "      , t2.email_addr      /* 이메일 주소 */  "
        query += "   from service20_oth_std t2 "
        query += "  where t2.std_id = '"+l_user_id+"'  "

        queryset = vw_nanum_stdt.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 멘티 마이페이지 ###################################################
class menteMypage_list_Serializer(serializers.ModelSerializer):

    gen_nm = serializers.SerializerMethodField()
    term_div_nm = serializers.SerializerMethodField()
    mp_plc_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = ('mnte_id', 'mnte_nm', 'gen', 'gen_nm', 'sch_nm', 'mob_no', 'tel_no', 'email_addr', 'grd_id', 'grd_nm', 'tchr_id', 'tchr_nm', 'yr', 'term_div', 'term_div_nm', 'mp_id', 'mp_name', 'mp_hm', 'mp_plc', 'mp_plc_nm', 'status', 'status_nm')

    def get_gen_nm(self,obj):
        return obj.gen_nm
    def get_term_div_nm(self,obj):
        return obj.term_div_nm                                     
    def get_mp_plc_nm(self,obj):
        return obj.mp_plc_nm
    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_mp_name(self,obj):
        return obj.mp_name   

class menteMypage_list(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = menteMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = " select t1.id     "
        query += " , t1.mnte_id     /* 멘티id */ "
        query += " , t1.mnte_nm     /* 멘티 명 */ "
        query += " , t1.gen         /* 성별(ms0012) */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.gen and std_grp_code = 'ms0012') as gen_nm "
        query += " , t1.sch_nm      /* 학교명 */ "
        query += " , t1.mob_no      /* 휴대전화 */ "
        query += " , t1.tel_no      /* 집전화 */  "
        query += " , t1.email_addr  /* 이메일 주소 */ "
        query += " , t1.grd_id      /* 주 보호자 id */ "
        query += " , t1.grd_nm      /* 보호자명 */     "
        query += " , t1.tchr_id     /* 지도교사 id */ "
        query += " , t1.tchr_nm     /* 지도교사 명 */     "
        query += " , t1.yr          /* 학년도 */ "
        query += " , t1.term_div    /* 학기 */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.term_div and std_grp_code = 'MS0022') as term_div_nm "
        query += " , t1.mp_id       /* 멘토링 프로그램id */ "
        query += " , t2.mp_name     /* 멘토링 프로그램명 */ "
        query += " , t1.mp_hm       /* 멘토링 가능 시간 */ "
        query += " , t1.mp_plc      /* 멘토링 장소 구분(mp0052) */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.mp_plc and std_grp_code = 'mp0052') as mp_plc_nm "
        query += " , t1.status      /* 상태(mp0054) */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.status and std_grp_code = 'mp0054') as status_nm "
        query += " from service20_mp_mte t1     /* 프로그램 지원자(멘티) */ "
        query += " , service20_mpgm t2           "
        query += " where 1=1 "
        query += " and t1.mp_id    = t2.mp_id "
        query += " and t1.mnte_id  = '"+l_user_id+"'     /* 지원 no */ "
        query += " order by t1.yr desc "
        query += " , t1.term_div desc "
        query += " , t1.status "

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 교사 마이페이지 ###################################################
class tchrMypage_list_Serializer(serializers.ModelSerializer):

    class Meta:
        model = teacher
        fields = '__all__'    

class tchrMypage_list(generics.ListAPIView):
    queryset = teacher.objects.all()
    serializer_class = tchrMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = " select t1.tchr_id     /* 지도교사 id */  "
        query += "     , t1.tchr_nm     /* 지도교사 명 */  "        
        query += " from service20_teacher t1     "
        query += " where 1=1  "
        query += " and t1.tchr_id = '"+l_user_id+"'  "

        queryset = teacher.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    

# 학부모 마이페이지 ###################################################
class grdMypage_list_Serializer(serializers.ModelSerializer):

    grd_rel_nm = serializers.SerializerMethodField()

    class Meta:
        model = guardian
        fields = '__all__'

    def get_grd_rel_nm(self,obj):
        return obj.grd_rel_nm          

class grdMypage_list(generics.ListAPIView):
    queryset = guardian.objects.all()
    serializer_class = grdMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = " select t1.grdn_id   /* 주 보호자 id */ "
        query += " , t1.grdn_nm        /* 보호자명 */ "
        query += " , t1.mob_no         /* 보호자 연락처 */ "
        query += " , t1.rel_tp         /* 보호자 관계(mp0047) */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.rel_tp and std_grp_code = 'mp0047') as grd_rel_nm "
        query += " , t1.moth_nat_nm     /* 국적 */  "
        query += " , t1.email_addr     /* 이메일 */     "
        query += " from service20_guardian t1     "
        query += " where 1=1 "
        query += " and t1.grdn_id      = '"+l_user_id+"' "

        queryset = guardian.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 기타사용자 마이페이지 ###################################################
class ectUserListMypage_list_Serializer(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField()
    user_nm = serializers.SerializerMethodField()
    user_div_nm = serializers.SerializerMethodField()
    user_sch_nm2 = serializers.SerializerMethodField()

    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_user_id(self,obj):
        return obj.user_id          
    def get_user_nm(self,obj):
        return obj.user_nm          
    def get_user_div_nm(self,obj):
        return obj.user_div_nm          
    def get_user_sch_nm2(self,obj):
        return obj.user_sch_nm2                                  

class ectUserListMypage_list(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = ectUserListMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query = " select '1' id, t1.user_id "
        query += "      , t1.user_nm "
        query += "      , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.user_div and std_grp_code = 'cm0001') as user_div_nm "
        query += "      , t1.user_sch_nm2 "
        query += "   from vw_nanum_login t1 "
        query += "  where user_id = '"+l_user_id+"'  "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 마이페이지 프로그램리스트 ###################################################
class programMypage_list_Serializer(serializers.ModelSerializer):

    tchr_id = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    yr = serializers.SerializerMethodField()
    term_div = serializers.SerializerMethodField()
    term_div_nm = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = '__all__'


    def get_tchr_id(self,obj):
        return obj.tchr_id  
    def get_tchr_nm(self,obj):
        return obj.tchr_nm  
    def get_yr(self,obj):
        return obj.yr  
    def get_term_div(self,obj):
        return obj.term_div  
    def get_term_div_nm(self,obj):
        return obj.term_div_nm  
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm  
    def get_status(self,obj):
        return obj.status  
    def get_status_nm(self,obj):
        return obj.status_nm                                                                                          

class programMypage_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = programMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = "select distinct "
        query += "       t1.mp_id as mp_id      /* 멘토링 프로그램id */     "
        query += "     , t2.tchr_id     /* 지도교사 id */  "
        query += "     , t2.tchr_nm     /* 지도교사 명 */  "
        query += "     , t2.yr          /* 학년도 */  "
        query += "     , t2.term_div    /* 학기 */  "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.term_div and std_grp_code = 'ms0022') as term_div_nm  "
        query += "     , t1.mp_name     /* 멘토링 프로그램명 */  "
        query += "     , t1.sup_org     /* 주관기관(mp0004) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.sup_org and std_grp_code = 'mp0004') as sup_org_nm "
        query += "     , substring(t1.apl_fr_dt,1,10) as apl_fr_dt   /* 모집기간-시작 */"
        query += "     , substring(t1.apl_to_dt,1,10) as apl_to_dt   /* 모집기간-종료 */"
        query += "     , substring(t1.mnt_fr_dt,1,10) as mnt_fr_dt   /* 활동기간-시작 */"
        query += "     , substring(t1.mnt_to_dt,1,10) as mnt_to_dt   /* 활동기간-시작 */          "
        query += "     , t2.status      /* 상태(mp0054) */  "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.status and std_grp_code = 'mp0054') as status_nm       "
        query += "  from service20_mpgm t1 "
        query += "  left join service20_mp_mte t2 on (t2.mp_id     = t1.mp_id ) "
        query += " where 1=1   "
        query += "   and ( t2.tchr_id = '"+str(l_user_id)+"' "
        query += "      or t2.grd_id  = '"+str(l_user_id)+"' "
        query += "      or t2.mnte_id = '"+str(l_user_id)+"' )  "
        query += " order by t2.yr desc  "
        query += "     , t2.term_div desc  "
        query += "     , t2.status  "
        query += "     , t2.mp_id  "
        query += "     , t2.mnte_nm    "

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 멘토 프로그램별 멘티 리스트 ###################################################
class mentoMenteMypage_list_Serializer(serializers.ModelSerializer):

    gen_nm = serializers.SerializerMethodField()
    mp_plc_nm = serializers.SerializerMethodField()
    grd_rel_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = '__all__'

    def get_gen_nm(self,obj):
        return obj.gen_nm
    def get_mp_plc_nm(self,obj):
        return obj.mp_plc_nm  
    def get_grd_rel_nm(self,obj):
        return obj.grd_rel_nm                       

class mentoMenteMypage_list(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = mentoMenteMypage_list_Serializer


    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = " select t1.id " 
        query += "     , t1.mnte_nm     /* 멘티 명 */ "
        query += "     , t1.brth_dt     /* 생년월일(+ 멘티명 → 동일인 찾기) */"
        query += "     , t1.gen         /* 성별(ms0012) */"
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.gen and std_grp_code = 'ms0012') as gen_nm "        
        query += "     , t1.sch_nm      /* 학교명 */  "
        query += "     , t1.sch_yr      /* 학년 */"
        query += "     , t1.mob_no      /* 휴대전화 */"
        query += "     , t1.h_addr      /* 집주소 */"
        query += "     , t1.mp_plc      /* 멘토링 장소 구분(mp0052) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.mp_plc and std_grp_code = 'mp0052') as mp_plc_nm   "
        query += "     , t1.tchr_nm     /* 지도교사 명 */     "
        query += "     , t1.tchr_tel    /* 지도교사 전화번호 */"
        query += "     , t1.grd_nm      /* 보호자명 */ "
        query += "     , t1.grd_tel     /* 보호자 연락처 */"
        query += "     , t1.grd_rel     /* 보호자 관계(mp0047) */"
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.grd_rel and std_grp_code = 'mp0047') as grd_rel_nm "
        query += "     , t1.prnt_nat_nm /* 부모출신국가명 */"
        query += "     , t1.mp_id       /* 멘토링 프로그램id */ "
        query += "     , t1.mnte_no     /* 지원 no */ "
        query += " from service20_mp_mte t1     /* 프로그램 지원자(멘티) */ "
        query += " , service20_mp_mtr t2 "
        query += " where 1=1 "
        query += " and t1.mp_id  = t2.mp_id "
        query += " and t1.apl_no = t2.apl_no "
        query += " and t1.mp_id  = '"+l_mp_id+"'       /* 멘토링 프로그램id */ "
        query += " and t2.apl_id = '"+l_user_id+"'     /* 지원 no */ "

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 교사,학부모별 프로그램별 멘티 리스트 ###################################################
class pgmMenteMypage_list_Serializer(serializers.ModelSerializer):

    apl_nm = serializers.SerializerMethodField()
    mp_plc_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = '__all__'


    def get_apl_nm(self,obj):
        return obj.apl_nm                                     
    def get_mp_plc_nm(self,obj):
        return obj.mp_plc_nm       

class pgmMenteMypage_list(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = pgmMenteMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = " select t1.id  "
        query += " , t1.mnte_nm     /* 멘티 명 */   "
        query += " , t3.apl_nm      /* 멘토 명 */         "
        query += " , t1.sch_nm      /* 멘토 학교명 */         "
        query += " , t1.mp_hm       /* 멘토링 가능 시간 */  "
        query += " , t1.mp_plc      /* 멘토링 장소 구분(mp0052) */  "
        query += " , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.mp_plc and std_grp_code = 'mp0052') as mp_plc_nm  "
        query += " from service20_mp_mte t1     /* 프로그램 지원자(멘티) */  "
        query += " , service20_mpgm t2  "
        query += " , service20_mp_mtr t3  "
        query += " where 1=1  "
        query += " and t1.mp_id   = t2.mp_id  "
        query += " and t1.mp_id   = t3.mp_id  "
        query += " and t1.apl_no  = t3.apl_no "
        query += " and ( t1.tchr_id = '"+str(l_user_id)+"' "
        query += "    or t1.grd_id  = '"+str(l_user_id)+"' "
        query += "    or t1.mnte_id = '"+str(l_user_id)+"' )  "
        query += " and t1.mp_id   = '"+l_mp_id+"'  "
        query += " order by t1.yr desc  "
        query += " , t1.term_div desc  "
        query += " , t1.status  "
        query += " , t1.mp_id  "
        query += " , t1.mnte_nm  "

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)          

# 멘토스쿨 리스트 ###################################################
class mschListMypage_list_Serializer(serializers.ModelSerializer):

    sch_yr = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    apply_status = serializers.SerializerMethodField()
    apply_status_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    mntr_dt = serializers.SerializerMethodField()

    class Meta:
        model = msch
        fields = '__all__'


    def get_sch_yr(self,obj):
        return obj.sch_yr                                     
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm   
    def get_apply_status(self,obj):
        return obj.apply_status                                     
    def get_apply_status_nm(self,obj):
        return obj.apply_status_nm   
    def get_status_nm(self,obj):
        return obj.status_nm                                     
    def get_mntr_dt(self,obj):
        return obj.mntr_dt                       

class mschListMypage_list(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = mschListMypage_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = "select t1.yr            /* 연도 */ "
        query += "     , t1.yr_seq        /* 차수 */    "
        query += "     , t2.sch_yr        /* 학년 */     "
        query += "     , t1.ms_id         /* 멘토스쿨id */"
        query += "     , t1.ms_name       /* 멘토스쿨 명 */  "
        query += "     , t1.sup_org       /* 주관기관(mp0004) */"
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.sup_org and std_grp_code = 'mp0004') as sup_org_nm "
        query += "     , ifnull(t2.status, 'N')  as apply_status      /* 상태(ms0024) */ "
        query += "     , case when t2.status = '90' then '합격' "
        query += "            else (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.status and std_grp_code = 'ms0024') end as apply_status_nm "
        query += "     , substring(t1.apl_fr_dt,1,10) as apl_fr_dt    /* 모집기간-시작 */ "
        query += "     , substring(t1.apl_to_dt,1,10) as apl_to_dt    /* 모집기간-종료 */ "
        query += "     , substring(t1.trn_fr_dt,1,10) as trn_fr_dt    /* 교육기간-시작 */ "
        query += "     , substring(t1.trn_to_dt,1,10) as trn_to_dt    /* 교육기간-종료 */ "
        query += "     , t1.status        /* 상태(ms0001) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.status and std_grp_code = 'ms0001') as status_nm "
        query += "     , t2.mntr_dt         /* 멘토 자격 부여일 */ "
        query += "  from service20_msch t1     /* 개설멘토스쿨 */ "
        query += "     left join service20_ms_apl t2 on (t1.ms_id = t2.ms_id) "
        query += " where 1=1 "
        query += "   and t2.apl_id = '"+str(l_user_id)+"' "

        queryset = msch.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

# 멘토 활동내역 리스트 ###################################################
class mentoActiveListMypage_list_Serializer(serializers.ModelSerializer):

    evt_gb_nm = serializers.SerializerMethodField()
    evt_dat = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_log
        fields = '__all__'


    def get_evt_gb_nm(self,obj):
        return obj.evt_gb_nm                              
    def get_evt_dat(self,obj):
        return obj.evt_dat  
        
class mentoActiveListMypage_list(generics.ListAPIView):
    queryset = mp_mtr_log.objects.all()
    serializer_class = mentoActiveListMypage_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()

        query  = "select t1.id  "
        query += "     , t1.mp_id       /* 멘토링 프로그램id */ "
        query += "     , t1.apl_no      /* 지원 no */ "
        query += "     , t1.mntr_id     /* 멘토id */ "
        query += "     , t1.evt_gb      /* 이벤트구분(mp0055) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.evt_gb and std_grp_code = 'mp0055') as evt_gb_nm "
        query += "     , substring(t1.evt_dat,1,10) as evt_dat      /* 이벤트일시 */ "
        query += "     , t1.evt_rsn_grp /* 이벤트 사유(mp0056) */ "
        query += "     , t1.evt_rsn_cd  /* 이벤트 사유(공통코드 std_detl_code) */ "
        query += "     , t1.evt_desc    /* 이벤트 내용 */ "
        query += "  from service20_mp_mtr_log t1     /* 프로그램 지원자(멘토) 로그 */ "
        query += " where 1=1 "
        query += "   and t1.mp_id = '"+str(l_mp_id)+"' "
        query += "   and t1.apl_no = '"+str(l_apl_no)+"' "

        queryset = mp_mtr_log.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)       

# 멘티 활동내역 리스트 ###################################################
class menteActiveListMypage_list_Serializer(serializers.ModelSerializer):

    evt_gb_nm = serializers.SerializerMethodField()
    evt_dat = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte_log
        fields = '__all__'


    def get_evt_gb_nm(self,obj):
        return obj.evt_gb_nm                              
    def get_evt_dat(self,obj):
        return obj.evt_dat  
        
class menteActiveListMypage_list(generics.ListAPIView):
    queryset = mp_mte_log.objects.all()
    serializer_class = menteActiveListMypage_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = "select t1.id  "
        query += "     , t1.mp_id       /* 멘토링 프로그램id */ "
        query += "     , t1.mnte_no      /* 지원 no */ "
        query += "     , t1.mnte_id     /* 멘토id */ "
        query += "     , t1.evt_gb      /* 이벤트구분(mp0055) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.evt_gb and std_grp_code = 'mp0056') as evt_gb_nm "
        query += "     , substring(t1.evt_dat,1,10) as evt_dat     /* 이벤트일시 */ "
        query += "     , t1.evt_rsn_grp /* 이벤트 사유 */ "
        query += "     , t1.evt_rsn_cd  /* 이벤트 사유(공통코드 std_detl_code) */ "
        query += "     , t1.evt_desc    /* 이벤트 내용 */ "
        query += "  from service20_mp_mte_log t1     /* 프로그램 지원자(멘토) 로그 */ "
        query += " where 1=1 "
        query += "   and t1.mp_id = '"+str(l_mp_id)+"' "
        query += "   and t1.mnte_id = '"+str(l_user_id)+"' "

        queryset = mp_mte_log.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)   

# 멘토 출석 리스트 ###################################################
class mentoAttdListMypage_list_Serializer(serializers.ModelSerializer):

    apl_no = serializers.SerializerMethodField()
    sum_elap_tm = serializers.SerializerMethodField()
    sum_appr_tm = serializers.SerializerMethodField()
    sum_exp_amt = serializers.SerializerMethodField()
    cum_appr_tm = serializers.SerializerMethodField()
    att_ym = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','sum_elap_tm','sum_appr_tm','sum_exp_amt','cum_appr_tm', 'att_ym')
    
    def get_apl_no(self,obj):
        return obj.apl_no
    def get_sum_elap_tm(self,obj):
        return obj.sum_elap_tm
    def get_sum_appr_tm(self,obj):
        return obj.sum_appr_tm
    def get_sum_exp_amt(self,obj):
        return obj.sum_exp_amt
    def get_cum_appr_tm(self,obj):
        return obj.cum_appr_tm
    def get_att_ym(self,obj):
        return obj.att_ym


class mentoAttdListMypage_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mentoAttdListMypage_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        query = " select t3.id,t3.mp_id     /* 멘토링 프로그램id*/ "
        query += " , t1.apl_no    /* 멘토 지원 no*/ "
        query += " , t3.mntr_id         /* 멘토id*/ "
        query += " , t3.apl_nm          /* 지원자(멘토,학생) 명*/ "
        query += " , t3.unv_nm          /* 지원자 대학교 명*/ "
        query += " , t3.cllg_nm         /* 지원자 대학 명*/ "
        query += " , t3.dept_nm         /* 지원자 학부/학과 명*/ "
        query += " , t3.sch_yr          /* 학년 */"
        query += " , substring(t1.att_sdt, 1, 7) AS att_ym"
        query += " , TIME_FORMAT(sec_to_time( sum(time_to_sec(t1.elap_tm)) ), '%%H시간 %%i분 %%s초')  sum_elap_tm  /* 경과시간*/ "
        query += " , sum(t1.appr_tm)   sum_appr_tm /* 인정시간*/ "
        query += " , sum(t1.exp_amt)   sum_exp_amt /* 지급 활동비 */"
        query += " , sum(t1.appr_tm)   cum_appr_tm /* 누적시간*/ "
        query += " , t3.bank_nm         /* 은행 명*/ "
        query += " , t3.bank_acct       /* 은행 계좌 번호*/ "
        query += " , t3.apl_id "
        query += " from service20_mp_att t1     /* 프로그램 출석부(멘토)*/ "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id "
        query += " and t3.apl_no   = t1.apl_no) "
        query += " where 1=1 "       
        query += " and t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */ "
        query += " and t3.apl_id   = '" + l_apl_id + "'   "
        query += " group by t1.mp_id     /* 멘토링 프로그램id */ "
        query += " , substring(t1.att_sdt, 1, 7) "
        query += " , t1.apl_no    /* 멘토 지원 no */ "
        query += " , t3.mntr_id         /* 멘토id  */ "
        query += " , t3.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += " , t3.unv_nm          /* 지원자 대학교 명 */ "
        query += " , t3.cllg_nm         /* 지원자 대학 명 */ "
        query += " , t3.dept_nm         /* 지원자 학부/학과 명 */ "
        query += " , t3.sch_yr          /* 학년 */ "
        query += " , t3.bank_nm         /* 은행 명 */ "
        query += " , t3.bank_acct "

        print(query)
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토 출석 리스트 상세 ###################################################
class mentoAttdDetailListMypage_list_Serializer(serializers.ModelSerializer):

    mp_div_nm = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    expl_yn = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    att_etm = serializers.SerializerMethodField()
    att_stm = serializers.SerializerMethodField()
    mnte_no = serializers.SerializerMethodField()
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mp_att
        fields = '__all__'
    
    def get_mp_div_nm(self,obj):
        return obj.mp_div_nm
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_expl_yn(self,obj):
        return obj.expl_yn
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_att_etm(self,obj):
        return obj.att_etm
    def get_att_stm(self,obj):
        return obj.att_stm  
    def get_mnte_no(self,obj):
        return obj.mnte_no  


class mentoAttdDetailListMypage_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mentoAttdDetailListMypage_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        query = " select t1.id,t1.mp_id     /* 멘토링 프로그램id */  "
        query += " , t1.apl_no    /* 멘토 지원 no */  "
        query += " , t1.att_no    /* 출석순서(seq) */  "
        query += " , t1.mp_div    /* 교육구분(mp0059) */  "
        query += " , c1.std_detl_code_nm   as mp_div_nm "
        query += " , t2.mnte_id     /* 멘티id */  "
        query += " , t2.mnte_no     /* 멘티지원No */  "
        query += " , t2.mnte_nm     /* 멘티명 */  "
        query += " , substring(t1.att_sdt, 1, 10) as att_sdt   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_sdt, 12, 5) as att_stm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_edt, 12, 5) as att_etm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.elap_tm, 1, 5)  as elap_tm   /* 경과시간*/ "
        query += " , t1.appr_tm   /* 인정시간 */  "
        query += " , t1.mtr_desc  /* 멘토링 내용(보고서) */  "
        query += " , t1.appr_id   /* 승인자id */  "
        query += " , t1.appr_nm   /* 승인자명 */  "
        query += " , substring(t1.appr_dt, 1, 16)  as appr_dt  /* 보호자 승인일시 */  "
        query += " , t1.mgr_id    /* 관리자id */  "
        query += " , t4.mgr_nm    /* 관리자명 */  "
        query += " , substring(t1.mgr_dt, 1, 16)  as mgr_dt   /* 관리자 승인일시 */  "
        query += " , t1.expl_yn as expl_yn   /* 소명상태 */  "
        query += " , t1.exp_amt   /* 지급 활동비 */  "
        query += " , t3.apl_id /* 학번 */ "
        query += " from service20_mp_att t1     /* 프로그램 출석부(멘토) */ "
        query += " left join service20_mp_mte t2  on (t2.mp_id  = t1.mp_id and t2.apl_no = t1.apl_no)  "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id and t3.apl_no   = t1.apl_no) "
        query += " left join service20_mpgm   t4 on (t4.mp_id    = t1.mp_id) "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'mp0059' and c1.std_detl_code = t1.mp_div) "
        query += " where 1=1 "     
        query += " and t1.mp_id    = '" + l_mp_id + "'   /* 멘토링 프로그램id */ "
        query += " and t3.apl_id   = '" + l_apl_id + "' "
        query += " order by t1.att_no DESC    /* 출석순서(seq) */ "



        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    

# 인증서 ###################################################
class certificateListMypage_list_Serializer(serializers.ModelSerializer):

    brth_dt = serializers.SerializerMethodField()
    yr = serializers.SerializerMethodField()
    apl_term = serializers.SerializerMethodField()
    sup_org = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()    
    mp_name = serializers.SerializerMethodField()
    mnt_fr_dt = serializers.SerializerMethodField()
    mnt_to_dt = serializers.SerializerMethodField()
    prnt_dt = serializers.SerializerMethodField()
    chc_val = serializers.SerializerMethodField()
    act_hr = serializers.SerializerMethodField()
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_brth_dt(self,obj):
        return obj.brth_dt
    def get_yr(self,obj):
        return obj.yr
    def get_apl_term(self,obj):
        return obj.apl_term    
    def get_sup_org(self,obj):
        return obj.sup_org
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm            
    def get_mp_name(self,obj):
        return obj.mp_name
    def get_mnt_fr_dt(self,obj):
        return obj.mnt_fr_dt
    def get_mnt_to_dt(self,obj):
        return obj.mnt_to_dt
    def get_prnt_dt(self,obj):
        return obj.prnt_dt
    def get_chc_val(self,obj):
        return obj.chc_val
    def get_act_hr(self,obj):
        return obj.act_hr

class certificateListMypage_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = certificateListMypage_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = "select t1.id   "
        query += "     , t1.cllg_cd         /* 지원자 대학 코드 */ "
        query += "     , t1.cllg_nm         /* 지원자 대학 명 */ "
        query += "     , t1.dept_cd         /* 지원자 학부/학과 코드 */ "
        query += "     , t1.dept_nm         /* 지원자 학부/학과 명 */ "
        query += "     , t1.apl_id          /* 지원자(멘토,학생) 학번 */ "
        query += "     , t1.apl_no          /* 지원자(멘토,학생) 학번 */ "
        query += "     , t1.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += "     , CONCAT(SUBSTRING(t1.brth_dt,1,4),'.',SUBSTRING(t1.brth_dt,5,2),'.',SUBSTRING(t1.brth_dt,7,2)) as brth_dt    /* 생년월일 */ "
        query += "     , t2.yr              /* 연도 */ "
        query += "     , t2.apl_term        /* 모집시기 */    "     
        query += "     , t2.sup_org         /* 주관기관(mp0004) */ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.sup_org and std_grp_code = 'mp0004') as sup_org_nm "
        query += "     , t1.mp_id           /* 멘토링 프로그램id */ "
        query += "     , t2.mp_name         /* 멘토링 프로그램명 */ "
        query += "     , DATE_FORMAT(t2.mnt_fr_dt, '%%Y.%%m.%%d') as mnt_fr_dt       /* 활동기간-시작 */ "
        query += "     , DATE_FORMAT(t2.mnt_to_dt, '%%Y.%%m.%%d') as mnt_to_dt       /* 활동기간-종료 */ "
        query += "     , SUBSTRING(t1.act_hr,1,3) as act_hr  /* 총활동 시간 */ "
        query += "     , t1.cert_en         /* 인증서 발급가능 */ "
        query += "     , t1.cert_no         /* 인증번호 */ "
        query += "     , DATE_FORMAT(t1.prnt_dt, '%%Y년 %%m월 %%d일') as prnt_dt         /* 인증서 발급일 */ "
        query += "     , t3.chc_val         /* 봉사 국가 */      "        
        query += "  from service20_mp_mtr t1 "
        query += "    left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += "    left join service20_mp_chc t3 on (t3.mp_id  = t1.mp_id "
        query += "                                   and t3.apl_no = t1.apl_no "
        query += "                                   and t3.att_id = 'mp0090' "
        query += "                                   and t3.att_cdh = 'mp0092')    "        
        query += " where t1.apl_id = '" + l_user_id + "'  "
        query += "   and t1.mp_id = '" + l_mp_id + "' "

        queryset = mp_mtr.objects.raw(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)     

# 패스워드 변경
@csrf_exempt
def mypage_update(request):
    l_id = request.POST.get('id', "")
    l_password = request.POST.get('password', "")
    l_ins_id = request.POST.get('ins_id', "")
    l_ins_pgm = request.POST.get('ins_pgm', "")
    client_ip = request.META['REMOTE_ADDR']

    chk1 = guardian.objects.filter(grdn_id=l_id).exists()
    chk2 = teacher.objects.filter(tchr_id=l_id).exists()
    chk3 = mentee.objects.filter(mnte_id=l_id).exists()
    chk4 = oth_std.objects.filter(std_id=l_id).exists()

    # 보호자
    if chk1:
        query = "update service20_guardian "
        query += "   set pwd = '" + l_password + "' "
        query += "     , upd_id = '" + l_ins_id + "' "
        query += "     , upd_ip = '" + client_ip + "' "
        query += "     , upd_pgm = '" + l_ins_pgm + "' "
        query += " where grdn_id = '" + l_id + "' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
    # 교사
    elif chk2:
        query = "update service20_teacher "
        query += "   set pwd = '" + l_password + "' "
        query += "     , upd_id = '" + l_ins_id + "' "
        query += "     , upd_ip = '" + client_ip + "' "
        query += "     , upd_pgm = '" + l_ins_pgm + "' "
        query += " where tchr_id = '" + l_id + "' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
    # 멘티
    elif chk3:
        query = "update service20_mentee "
        query += "   set pwd = '" + l_password + "' "
        query += "     , upd_id = '" + l_ins_id + "' "
        query += "     , upd_ip = '" + client_ip + "' "
        query += "     , upd_pgm = '" + l_ins_pgm + "' "
        query += " where mnte_id = '" + l_id + "' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
    # 타대학생
    elif chk4:
        query = "update service20_oth_std "
        query += "   set pwd = '" + l_password + "' "
        query += "     , upd_id = '" + l_ins_id + "' "
        query += "     , upd_ip = '" + client_ip + "' "
        query += "     , upd_pgm = '" + l_ins_pgm + "' "
        query += " where std_id = '" + l_id + "' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  

    message = "Ok"
    context = {'message': 'Ok'}

    #return HttpResponse(json.dumss(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})                                         
#####################################################################################
# mypage - END
#####################################################################################

 
#####################################################################################
# MS0101M - START
#####################################################################################

class MS0101M_list_chk_1_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MS0101M_list_chk_1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_1_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # 학년체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_ms_sub_desc_select_01('"+ms_id+"','MS0010') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_ms_sub_desc_select_01('"+ms_id+"','MS0010'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.sch_yr IN  "
        query += "                   (SELECT t3.att_cdd "
        query += "                      FROM service20_ms_sub t3 "
        query += "                     WHERE t3.ms_id   = '"+ms_id+"' "
        query += "                       AND t3.att_id  = 'MS0010' "
        query += "                       AND t3.att_cdh = 'MS0010' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_chk_2_Serializer(serializers.ModelSerializer):

    
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('name','code')

    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code

class MS0101M_list_chk_2(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_2_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # -- 직전학기 학점 제한
        query = " select t2.id,CASE WHEN t2.score03 >= t3.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', t3.att_val, '미만') END as name "
        query += "      , CASE WHEN t2.score03 >= t3.att_val THEN 'Y' ELSE 'N' END as code "
        query += "   FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "      , (  /* 학점 제한 */ "
        query += "         select IFNULL(max(att_val),3) att_val "
        query += "           FROM service20_ms_sub t3 "
        query += "          WHERE t3.ms_id   = '"+ms_id+"' "
        query += "            AND t3.att_id  = 'MS0013' "
        query += "            AND t3.att_cdh = 'MS0013' "
        query += "            AND t3.att_cdd = '40' "
        query += "       ) t3 "
        query += "   WHERE t2.apl_id = '"+apl_id+"' "

        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_chk_3_Serializer(serializers.ModelSerializer):

    
    chk = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_chk(self, obj):
        return obj.chk

class MS0101M_list_chk_3(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_3_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # -- 신청가능한 대학/학과체크

        query = " select '1' as id,COUNT(*) as chk "
        query += "   FROM ( "
        query += "          select att_val "
        query += "            FROM service20_ms_sub t3 "
        query += "           WHERE t3.ms_id   = '"+ms_id+"' "
        query += "             AND t3.att_id  = 'MP0010' "
        query += "             AND t3.att_cdh = 'MP0010' "
        query += "             AND t3.att_cdd = '20' /* 대학 */ "
        query += "           UNION ALL "
        query += "          select att_val "
        query += "            FROM service20_ms_sub t3 "
        query += "           WHERE t3.ms_id   = '"+ms_id+"' "
        query += "             AND t3.att_id  = 'MP0010' "
        query += "             AND t3.att_cdh = 'MP0010' "
        query += "             AND t3.att_cdd = '30'  /* 학과 */ "
        query += "       ) T1 "

        
        queryset = com_cdd.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_chk_4_Serializer(serializers.ModelSerializer):

    
    chk = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_chk(self, obj):
        return obj.chk

class MS0101M_list_chk_4(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_4_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # -- 신청가능한 대학/학과체크

        query = " select '1' as id,COUNT(*) as chk "
        query += "   FROM ( "
        query += "          select apl_id "
        query += "            FROM service20_vw_nanum_stdt b "
        query += "           WHERE cllg_nm IN ( SELECT att_val "
        query += "                                FROM service20_ms_sub t3 "
        query += "                               WHERE t3.ms_id   = '"+ms_id+"' "
        query += "                                 AND t3.att_id  = 'MP0010' "
        query += "                                 AND t3.att_cdh = 'MP0010' "
        query += "                                 AND t3.att_cdd = '20' /* 대학 */ "
        query += "                             ) "
        query += "            AND APL_ID = '"+apl_id+"' "
        query += "         UNION ALL "
        query += "          select apl_id "
        query += "            FROM service20_vw_nanum_stdt b "
        query += "           WHERE dept_nm IN ( SELECT att_val "
        query += "                                FROM service20_ms_sub t3 "
        query += "                               WHERE t3.ms_id   = '"+ms_id+"' "
        query += "                                 AND t3.att_id  = 'MP0010' "
        query += "                                 AND t3.att_cdh = 'MP0010' "
        query += "                                 AND t3.att_cdd = '30'  /* 학과 */ "
        query += "                             ) "
        query += "            AND apl_id = '"+apl_id+"' "
        query += "        ) T1 "

        queryset = com_cdd.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

class MS0101M_list_chk_5_Serializer(serializers.ModelSerializer):

    

    mentor_num = serializers.SerializerMethodField()
    class Meta:
        model = mentor
        fields = '__all__'

    def get_mentor_num(self, obj):
        return obj.mentor_num


class MS0101M_list_chk_5(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_5_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")

        # -- 멘토체크
        query = "select COUNT(*) as mentor_num,A.* from service20_mentor A where apl_id = '"+str(apl_id)+"'"

        queryset = mentor.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)          

class MS0101M_list_chk_7_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MS0101M_list_chk_7(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_7_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # 학년체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_ms_sub_desc_select_01('"+ms_id+"','MS0011') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_ms_sub_desc_select_01('"+ms_id+"','MS0011'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.cmp_term IN  "
        query += "                   (SELECT t3.att_cdd*1 "
        query += "                      FROM service20_ms_sub t3 "
        query += "                     WHERE t3.ms_id   = '"+ms_id+"' "
        query += "                       AND t3.att_id  = 'MS0011' "
        query += "                       AND t3.att_cdh = 'MS0011' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_chk_8_Serializer(serializers.ModelSerializer):

    class Meta:
        model = msch
        fields = ('ms_id', 'apl_fr_dt','apl_to_dt')

class MS0101M_list_chk_8(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = MS0101M_list_chk_8_Serializer

    def list(self, request):

        ms_id = request.GET.get('ms_id', "")

        # 모집기간 체크
        query = " SELECT ms_id, apl_fr_dt, apl_to_dt FROM service20_msch WHERE ms_id = '" + ms_id + "'"

        queryset = msch.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    dept_appr_div = serializers.SerializerMethodField()
    
    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    trn_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    trn_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = msch
        fields = '__all__'

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_status(self,obj):
        return obj.status
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm
    def get_dept_appr_div(self,obj):
        return obj.dept_appr_div

class MS0101M_list(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = MS0101M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', None)
        l_apl_term = request.GET.get('trn_term', None)
        l_user_id = request.GET.get('user_id', None)
        l_status = request.GET.get('status', '')


        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MS0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MS0024'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += " B.dept_appr_div   AS dept_appr_div, "
        query += "        A.*  "
        query += " FROM   service20_msch A  "
        query += "        LEFT JOIN service20_ms_apl B  "
        query += "               ON ( A.ms_id = B.ms_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(l_user_id)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += " WHERE  A.yr = '"+str(l_yr)+"'  "
        query += "        AND A.apl_term = '"+str(l_apl_term)+"'  "
        query += "        AND A.use_div = 'Y' "
        
        query += "        AND A.status > '10'  "

        # query += "        AND (SELECT Count(1)  "
        # query += "             FROM   service20_mentor  "
        # query += "             WHERE  apl_id = '"+str(ida)+"') > 0  "
        query += "        AND IF(A.status = '10'  "
        query += "               AND Now() > A.apl_to_dt, 'xx', A.status) LIKE  "
        query += "            Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        query += "            or '%%'  "
        query += " ORDER  BY A.ms_id DESC, A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "
        queryset = msch.objects.raw(query)

        
        


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토스쿨 질문유형 가져오기
class MS0101M_quest_Serializer(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    ans_min_len = serializers.SerializerMethodField()
    ans_max_len = serializers.SerializerMethodField()
    class Meta:
        model = ms_sub
        fields = ('id','ms_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk','ans_min_len','ans_max_len')

        
    def get_std_detl_code(self,obj):
        return obj.std_detl_code
        
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk    
    def get_ans_min_len(self,obj):
        return obj.ans_min_len  
    def get_ans_max_len(self,obj):
        return obj.ans_max_len  

# 멘토스쿨 질문유형 가져오기
class MS0101M_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None)           
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0014' and B.use_indc = 'Y' and A.ms_id = '"+key1+"' order by A.sort_seq"

        query = "select  "
        query += "     t3.std_detl_code, "
        query += "     t3.std_detl_code_nm, "
        query += "     t3.rmrk, "
        query += "     fn_ms_sub_att_val_select_01(t1.ms_id, t1.att_id, 'MS0028', t1.att_cdd) ans_min_len, "
        query += "     fn_ms_sub_att_val_select_01(t1.ms_id, t1.att_id, 'MS0029', t1.att_cdd) ans_max_len, "
        query += "     t1.* "
        query += "FROM service20_ms_sub t1 "
        query += "LEFT JOIN service20_com_cdd t3 ON (t3.std_grp_code  = t1.att_cdh "
        query += "                               AND t3.std_detl_code = t1.att_cdd) "
        query += "WHERE t1.ms_id   = '"+key1+"' "
        query += " AND t1.att_id  = 'MS0014' "
        query += " AND t1.att_cdh = 'MS0014' "
        query += "ORDER BY t1.sort_seq "

        queryset = ms_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토스쿨 신청
@csrf_exempt
def MS0101M_save(request):
    ida = request.POST.get('memberNo', None)
    programId = request.POST.get('programID', None)
    que1 = request.POST.get('que1', None)
    que2 = request.POST.get('que2', None)
    que3 = request.POST.get('que3', None)
    que4 = request.POST.get('que4', None)
    que5 = request.POST.get('que5', None)

    ms_ida = request.POST.get('ms_id', None)
    apl_max = request.POST.get('aplMax', 0)
    
    client_ip = request.META['REMOTE_ADDR']

    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id = programId
    ms_apl_max = ms_apl.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
    #ms_apl_max = ms_apl.objects.all().last()
    #ms_apl_max = ms_apl_max + 1
    apl_no = ms_apl_max
    apl_id = ida
    v_gen = ""
    if str(rows.gen_cd) == "1":
        v_gen = "M"
    else:
        v_gen = "F"
    
    max_no = ms_apl_max['vlMax']    

    if max_no == None:
        apl_no = 0
    else:
        apl_no = ms_apl_max['vlMax']
        apl_no = apl_no + 1
        
    query = "select ifnull(max(apl_no),0) as apl_no from service20_ms_apl where ms_id = '"+ms_id+"'"  
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    apl_no = results[0].apl_no
    apl_no = apl_no+1

    query = " select t2.ms_id,t2.yr FROM service20_msch t2  WHERE 1=1 "
    query += " AND t2.ms_id          = '"+ms_id+"'"
    queryset = msch.objects.raw(query)[0]

    rowsChk = ms_apl.objects.filter(apl_id=apl_id,ms_id=ms_id).exists()

    if rowsChk == True:
        context = {'message': 'duplicate'}
    else:

        if rows.tel_no == None:
            v_tel_no = ''
        else:
            v_tel_no = rows.tel_no.replace('-', '')


        if rows.mob_no == None:
            v_mob_no = ''
        else:
            v_mob_no = rows.mob_no.replace('-', '')
            
        if rows.tel_no_g == None:
            v_tel_no_g = ''
        else:
            v_tel_no_g = rows.tel_no_g.replace('-', '')
            
        score01 = rows.score01
        score02 = rows.score02
        score03 = rows.score03
        score04 = rows.score04
        score05 = rows.score05
        score06 = rows.score06
        if score01 == None:
            score01 = 0
        if score02 == None:
            score02 = 0
        if score03 == None:
            score03 = 0
        if score04 == None:
            score04 = 0
        if score05 == None:
            score05 = 0
        if score06 == None:
            score06 = 0
        
        model_instance = ms_apl(
            ms_id=ms_id, 
            apl_no=apl_no, 
            mntr_id=ida,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            unv_cd=str(rows.unv_cd),
            unv_nm=str(rows.unv_nm),
            cllg_cd=rows.cllg_cd,
            cllg_nm=rows.cllg_nm,
            dept_cd=rows.dept_cd,
            dept_nm=rows.dept_nm,
            brth_dt=rows.brth_dt,
            gen=v_gen,
            yr=queryset.yr,
            term_div=rows.term_div,
            sch_yr=rows.sch_yr,
            mob_no=v_mob_no,
            tel_no=v_tel_no,
            tel_no_g=v_tel_no_g,
            h_addr=rows.h_addr,
            email_addr=rows.email_addr,
            score1=score01,
            score2=score02,
            score3=score03,
            score4=score04,
            score5=score05,
            score6=score06,
            cmp_term=rows.cmp_term,
            pr_yr=rows.pr_yr,
            pr_sch_yr=rows.pr_sch_yr,
            pr_term_div=rows.pr_term_div,
            status='10', # 지원
            mjr_cd=rows.mjr_cd,
            mjr_nm=rows.mjr_nm,
            ins_id=apl_id,
            ins_ip=str(client_ip),
            ins_dt=datetime.datetime.today()
            )
        model_instance.save()
        
        apl_max = int(apl_max)

        for i in range(0,apl_max):
            anst2 = request.POST.get('que'+str(i+1), None)
            ques_no = request.POST.get('ques_no'+str(i+1), None)

            model_instance2 = ms_ans(
                ms_id=ms_id, 
                test_div='10', 
                apl_no=apl_no,
                ques_no=ques_no,
                apl_id=apl_id,
                apl_nm=rows.apl_nm,
                sort_seq =i+1,
                ans_t2=anst2
                )
            model_instance2.save()

        
        # mp_mntr/ms_apl  -> mp_id만 조건 걸어서 count(*)
        # 해당 cnt값을 mpgm/msch -> cnt_apl

        update_text = " update service20_msch a "
        update_text += " SET a.cnt_apl = (select count(*) from service20_ms_apl where ms_id = '"+ms_id+"' and status='10') "
        update_text += " WHERE 1=1 "
        update_text += " AND a.ms_id = '"+ms_id+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text) 


        # -- 생성_어학(ms_apl_fe)_FROM_vw_nanum_foreign_exam

        update_text = " insert into service20_ms_apl_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
        update_text += "      ( ms_id          /* 멘토링 프로그램id */ "
        update_text += "      , apl_no         /* 지원 no */ "
        update_text += "      , fe_no          /* 어학점수 no */ "
        update_text += "      , apl_id         /* 학번 */ "
        update_text += "      , apl_nm         /* 성명 */ "
        update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
        update_text += "      , lang_kind_nm   /* 어학종류명 */ "
        update_text += "      , lang_cd        /* 어학상위코드 */ "
        update_text += "      , lang_nm        /* 어학상위코드명 */ "
        update_text += "      , lang_detail_cd /* 어학하위코드 */ "
        update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
        update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
        update_text += "      , frexm_nm       /* 외국어시험명 */ "
        update_text += "      , score          /* 시험점수 */ "
        update_text += "      , grade          /* 시험등급 */ "
        update_text += "      , ins_id         /* 입력자id */ "
        update_text += "      , ins_ip         /* 입력자ip */ "
        update_text += "      , ins_dt         /* 입력일시 */ "
        update_text += "      , ins_pgm        /* 입력프로그램id */ "
        update_text += " ) "
        update_text += " select '"+str(ms_id)+"' AS ms_id "
        update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "      , @curRank := @curRank +1 AS fe_no  "
        update_text += "      , t1.apl_id         /* 학번 */ "
        update_text += "      , t1.apl_nm         /* 성명 */ "
        update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
        update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
        update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
        update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
        update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
        update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
        update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
        update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
        update_text += "      , t1.score          /* 시험점수 */ "
        update_text += "      , t1.grade          /* 시험등급 */ "
        update_text += "      , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "      , NOW() ins_dt         /* 입력일시 */ "
        update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
        update_text += "      , (SELECT @curRank := 0) r "
        update_text += "  WHERE 1=1 "
        update_text += "    AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        # -- 생성_봉사(ms_apl_sa)_FROM_vw_nanum_foreign_exam

        update_text = "insert into service20_ms_apl_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
        update_text += "     ( ms_id           /* 멘토링 프로그램id */ "
        update_text += "     , apl_no          /* 지원 no */ "
        update_text += "     , sa_no           /* 어학점수 no */ "
        update_text += "     , apl_id          /* 학번 */ "
        update_text += "     , apl_nm          /* 성명 */ "
        update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
        update_text += "     , nation_inout_nm /* 국내외구분명 */ "
        update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
        update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
        update_text += "     , activity_nm     /* 봉사명 */ "
        update_text += "     , manage_org_nm   /* 주관기관명 */ "
        update_text += "     , start_date      /* 시작일자 */ "
        update_text += "     , start_time      /* 시작시간 */ "
        update_text += "     , end_date        /* 종료일자 */ "
        update_text += "     , end_time        /* 종료시간 */ "
        update_text += "     , tot_time        /* 총시간 */ "
        update_text += "     , ins_id          /* 입력자id */ "
        update_text += "     , ins_ip          /* 입력자ip */ "
        update_text += "     , ins_dt          /* 입력일시 */ "
        update_text += "     , ins_pgm         /* 입력프로그램id */ "
        update_text += ") "
        update_text += "select '"+str(ms_id)+"' AS ms_id "
        update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "     , @curRank := @curRank +1 AS sa_no "
        update_text += "     , t1.apl_id          /* 학번 */ "
        update_text += "     , t1.apl_nm          /* 성명 */ "
        update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
        update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
        update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
        update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
        update_text += "     , t1.activity_nm     /* 봉사명 */ "
        update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
        update_text += "     , t1.start_date      /* 시작일자 */ "
        update_text += "     , t1.start_time      /* 시작시간 */ "
        update_text += "     , t1.end_date        /* 종료일자 */ "
        update_text += "     , t1.end_time        /* 종료시간 */ "
        update_text += "     , t1.tot_time        /* 총시간 */ "
        update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "     , NOW() ins_dt         /* 입력일시 */ "
        update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
        update_text += "     , (SELECT @curRank := 0) r "
        update_text += " WHERE 1=1 "
        update_text += "   AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)     


        # query = " select b.* from service20_vw_nanum_stdt a where a.apl_id = '"+apl_id+"' "
        # cursor = connection.cursor()
        # query_result = cursor.execute(query)  
        # results_st = namedtuplefetchall(cursor)  
        # v_dept_cd = results_st[0].dept_cd
        # v_mjr_cd = results_st[0].mjr_cd

        # -- 생성_자격증(ms_apl_lc)_FROM_service20_vw_nanum_license

        update_text = "insert into service20_ms_apl_lc      "
        update_text += "     ( ms_id           /* 멘토링 프로그램id */ "
        update_text += "     , apl_no          /* 지원 no */ "
        update_text += "     , lc_no           /* 자격 no */ "
        update_text += "     , apl_id          /* 학번 */ "
        update_text += "     , apl_nm          /* 성명 */ "
        update_text += "     , license_large_cd  "
        update_text += "     , license_large_nm  "
        update_text += "     , license_small_cd     "
        update_text += "     , license_small_nm     "
        update_text += "     , license_cd      "
        update_text += "     , license_nm    "        
        update_text += "     , ins_id          /* 입력자id */ "
        update_text += "     , ins_ip          /* 입력자ip */ "
        update_text += "     , ins_dt          /* 입력일시 */ "
        update_text += "     , ins_pgm         /* 입력프로그램id */ "
        update_text += ") "
        update_text += "select '"+str(ms_id)+"' AS ms_id "
        update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "     , @curRank := @curRank +1 AS lc_no "
        update_text += "     , t1.apl_id          /* 학번 */ "
        update_text += "     , t1.apl_nm          /* 성명 */ "
        update_text += "     , t1.license_large_cd  "
        update_text += "     , t1.license_large_nm  "
        update_text += "     , t1.license_small_cd     "
        update_text += "     , t1.license_small_nm     "
        update_text += "     , t1.license_cd      "
        update_text += "     , t1.license_nm    "        
        update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "     , NOW() ins_dt         /* 입력일시 */ "
        update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "  FROM service20_vw_nanum_license t1      "
        update_text += "     , (SELECT @curRank := 0) r "
        update_text += " WHERE 1=1 "
        update_text += "   AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_service20_vw_nanum_license::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)  

        # -- 자격증 종료

        query = " select b.* from service20_vw_nanum_stdt a, service20_dept_ast b where a.dept_cd = b.dept_cd and b.status = 'Y' and a.apl_id = '"+apl_id+"' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
        results = namedtuplefetchall(cursor)  
        query_cnt = len(list(results))
        print("::query_cnt::")
        print(query_cnt)
        update_text = " update service20_ms_apl set dept_appr_div = 'N' "
        update_text += " where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    

        # if query_cnt == '1':
        #     # MP_MTR.DEPT_CHR_ID(학과장 ID) = DEPT_AST.DEAN_EMP_ID
        #     # MP_MTR.DEPT_CHR_NM(학과장 명) = DEPT_AST.DEAN_EMP_NM
        #     # MP_MTR.AST_ID(조교 ID)        = DEPT_AST.AST_ID
        #     # MP_MTR.AST_NM(조교 명)        = DEPT_AST.AST_NM
        #     # MP_MTR.DEPT_APPR_DIV(학과 승인 여부) = 'N'

        #     # service20_ms_apl
        #     update_text = " update service20_ms_apl set dept_chr_id = '"+results[0].dean_emp_id+"', dept_chr_nm = '"+results[0].dean_emp_nm+"', ast_id = '"+results[0].ast_id+"', dept_appr_div = '"+results[0].ast_nm+"', dept_appr_div = 'N' "
        #     update_text += " where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
        # elif query_cnt != '0':
        #     query2 = " select b.* from service20_vw_nanum_stdt a, service20_dept_ast b where a.dept_cd = b.dept_cd and a.mjr_cd = b.mjr_cd and b.status = 'Y' and a.apl_id = '"+apl_id+"' "
        #     cursor = connection.cursor()
        #     query_result = cursor.execute(query2)
        #     results = namedtuplefetchall(cursor)

        #     queryset = dept_ast.objects.raw(query2)
        #     for val in queryset:
        #         update_text = " update service20_ms_apl set dept_chr_id = '"+val.dean_emp_id+"', dept_chr_nm = '"+val.dean_emp_nm+"', ast_id = '"+val.ast_id+"', dept_appr_div = '"+val.ast_nm+"', dept_appr_div = 'N' "
        #         update_text += " where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"

        # mjr_cd
        # 멘토스쿨/프로그램 지원 시 학과조교 검색 시
        # 전공까지 조건 걸어서 조회해야하는데
        # 1.학과로만 조교 찾아서 세팅
        # 2.1에서 2건이상 나오면 학과,전공 걸어서 조교 찾아서 세팅


        # queryset = dept_ast.objects.raw(query)
        # for val in queryset:
        #     # 문자전송
        #     query = " select a.* from service20_ms_apl a where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
        #     cursor = connection.cursor()
        #     query_result = cursor.execute(query)  
        #     results_m = namedtuplefetchall(cursor)  

        #     user_id = '515440'
        #     push_chk = 'PO'
        #     # push_userid = '515440'
        #     push_userid = val.ast_id
        #     push_title = "지원서 학과장 승인 요청"
        #     push_content = results_m[0].apl_nm + " 학생 멘토스쿨 지원서 학과장 승인 요청"
        #     tickerText = ' '
        #     push_time = '60'
        #     # cdr_id = '515440'
        #     cdr_id = results[0].ast_id
        #     sms_content = push_content
        #     sms_nb = '0515103322'
        #     client_ip = request.META['REMOTE_ADDR']
        #     data_info = {'user_id':user_id,'push_chk': push_chk,'push_userid': push_userid,'push_title': push_title,'push_content': push_content,'tickerText': tickerText,'push_time': push_time,'cdr_id': cdr_id,'sms_content': sms_content,'sms_nb': sms_nb}
        #     print("::data_info::")
        #     print(data_info)
        #     # with requests.Session() as s:
        #     #     first_page = s.post('http://msg.pusan.ac.kr/api/push.asp', data=data_info)
        #     #     html = first_page.text
        #     #     #print(html)
        #     #     soup = bs(html, 'html.parser')

        message = "Ok"
        
        context = {'message': 'Ok'}

    #return HttpResponse(json.dumss(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def MS0101M_detail(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)
    
    
    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
    msch_flag = msch.objects.filter(ms_id=ms_ida,status='20').exists()
    # ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id=ms_ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,yr=l_yr,ms_id=ms_ida).exists()

    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vw_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vw_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        if not msch_flag:
            message = "Fail"
            context = {'message': message}
        else:

            message = "Ok"
            rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
            rows2 = ms_sub.objects.filter(ms_id=ms_ida)
            rows3 = msch.objects.filter(ms_id=ms_ida)[0]


            for val in rows2:
                key1 = val.att_id
                #key2 = val.att_cdd

            #question01 = com_cdd.objects.filter(std_grp_code=key1)[0].rmrk
            #question02 = com_cdd.objects.filter(std_grp_code=key1)[1].rmrk
            #question03 = com_cdd.objects.filter(std_grp_code=key1)[2].rmrk
            #question04 = com_cdd.objects.filter(std_grp_code=key1)[3].rmrk
            #question05 = com_cdd.objects.filter(std_grp_code=key1)[4].rmrk
            context = {'message': message,
                        'applyYn' : applyYn,
                        'apl_nm' : rows.apl_nm,
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
                        'grad_div_cd' : rows.grad_div_cd,
                        'grad_div_nm' : rows.grad_div_nm,
                        'cllg_cd' : rows.cllg_cd,
                        'cllg_nm' : rows.cllg_nm,
                        'dept_cd' : rows.dept_cd,
                        'dept_nm' : rows.dept_nm,
                        'mjr_cd' : rows.mjr_cd,
                        'mjr_nm' : rows.mjr_nm,
                        'brth_dt' : rows.brth_dt,
                        'gen_cd' : rows.gen_cd,
                        'gen_nm' : rows.gen_nm,
                        'yr' : rows.yr,
                        'sch_yr' : rows.sch_yr,
                        'term_div' : rows.term_div,
                        'term_nm' : rows.term_nm,
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'tel_no_g' : rows.tel_no_g,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.post_no,
                        'email_addr' : rows.email_addr,
                        'bank_acct' : rows.bank_acct,
                        'bank_cd' : rows.bank_cd,
                        'bank_nm' : rows.bank_nm,
                        'bank_dpsr' : rows.bank_dpsr,
                        'pr_yr' : rows.pr_yr,
                        'pr_sch_yr' : rows.pr_sch_yr,
                        'pr_term_div' : rows.pr_term_div,
                        'score01' : rows.score01,
                        'score02' : rows.score02,
                        'score03' : rows.score03,
                        'score04' : rows.score04,
                        'score05' : rows.score05,
                        'ms_id' : rows3.ms_id,
                        'ms_name' : rows3.ms_name,
                        }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

class MS0101M_adm_list_Serializer(serializers.ModelSerializer):
    
    ms_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    # statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    # acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = ms_apl
        # fields = ('ms_id','apl_no','mntr_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','ms_name','pr_yr','pr_sch_yr','pr_term_div','statusCode','status_nm')
        fields = '__all__'

    def get_ms_name(self,obj):
        return obj.ms_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm
    def get_status(self,obj):
        return obj.status

class MS0101M_adm_list(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # msch
        query = " select   "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, 'xx', C.status) as statusCode,  "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, '모집완료', (select std_detl_code_nm  "
        query += " from   service20_com_cdd  "
        query += " where  "
        query += " std_grp_code = 'MS0001'  "
        query += " and use_indc = 'y'  "
        query += " and std_detl_code = C.status)) as status_nm,  "

        query += " C.ms_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_ms_apl A,service20_vw_nanum_stdt B,service20_msch C where A.apl_id=B.apl_id and A.ms_id = C.ms_id and A.yr='"+l_yr+"' and A.ms_id = '"+ms_ida+"' and A.apl_id='"+ida+"'"
        
        queryset = ms_apl.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 어학
class MS0101M_adm_list_fe_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = ms_apl_fe
        fields = ('frexm_cd','frexm_nm','score','grade','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score

class MS0101M_adm_list_fe(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select id,  "
        query += "        frexm_cd,  "
        query += "        frexm_nm,  "
        query += "        score,  "
        query += "        grade,  "
        query += "   fn_ms_apl_fe_select_01('"+str(ms_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_ms_apl_fe  "
        query += " WHERE  ms_id = '"+str(ms_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = ms_apl_fe.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 봉사
class MS0101M_adm_list_sa_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = ms_apl_sa
        fields = ('ms_id','apl_no','sa_no','apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score


class MS0101M_adm_list_sa(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select a.* , "
        query += "   fn_mp_mtr_sa_select_01('"+str(ms_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_ms_apl_sa a  "
        query += " WHERE  ms_id = '"+str(ms_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = ms_apl_sa.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토스쿨(관리자) - 질문2
class MS0101M_adm_quest_Serializer2(serializers.ModelSerializer):

    
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = ms_ans
        fields = ('id','ms_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code','std_detl_code_nm','rmrk')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk

# 멘토스쿨(관리자) - 질문
class MS0101M_adm_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_adm_quest_Serializer2
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        l_exist = ms_sub.objects.filter(ms_id=key1).exists()
        
        # query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.use_indc = 'Y' and B.std_grp_code in (select att_cdh from service20_ms_sub where att_id='MS0014' and ms_id = '"+str(key1)+"') and A.ms_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"' order by A.sort_seq"

        query = f"""
            SELECT B.std_detl_code
                , B.std_detl_code_nm
                , B.rmrk
                , A.*
                , fn_ms_sub_att_val_select_01(A.ms_id, t1.att_id, 'MS0028', t1.att_cdd) ans_min_len
                , fn_ms_sub_att_val_select_01(A.ms_id, t1.att_id, 'MS0029', t1.att_cdd) ans_max_len
            FROM service20_ms_ans A
            LEFT JOIN service20_ms_sub t1 ON (t1.ms_id = A.ms_id AND t1.att_id = 'MS0014' AND t1.att_cdh = 'MS0014' and t1.att_cdd = A.ques_no)
            LEFT JOIN service20_com_cdd B ON (B.std_detl_code = A.ques_no AND B.std_grp_code = 'MS0014' AND B.use_indc = 'Y')
            where A.ms_id = '{key1}'
            AND A.apl_id = '{l_user_id}'
            ORDER BY A.sort_seq;
        """

        queryset = ms_ans.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토스쿨 수락
@csrf_exempt
def MS0101M_adm_acpt_save(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_ms_apl a "
    update_text += " SET a.acpt_dt = NOW() "
    update_text += " , a.acpt_div = 'Y' "
    update_text += " , a.acpt_cncl_rsn = null "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 멘토스쿨 수락취소
@csrf_exempt
def MS0101M_adm_acpt_cancle(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_ms_apl a "
    update_text += " SET a.acpt_dt = null "
    update_text += " , a.acpt_div = 'N' "
    update_text += " , a.acpt_cncl_rsn = '"+acpt_cncl_rsn+"' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토스쿨 update
@csrf_exempt
def MS0101M_adm_update(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    maxRow = request.POST.get('maxRow', 0)
    client_ip = request.META['REMOTE_ADDR']

    update_text = " update service20_ms_apl a,service20_vw_nanum_stdt b "
    update_text += " SET a.status = '10' "
    update_text += " , a.score1 = IFNULL(b.score01,0) "
    update_text += " , a.score2 = IFNULL(b.score02,0) "
    update_text += " , a.score3 = IFNULL(b.score03,0) "
    update_text += " , a.score4 = IFNULL(b.score04,0) "
    update_text += " , a.score5 = IFNULL(b.score05,0) "
    update_text += " , a.score6 = IFNULL(b.score06,0) "
    update_text += " , a.cmp_term = b.cmp_term "
    update_text += " , a.h_addr = b.h_addr "
    update_text += " , a.email_addr = b.email_addr "
    update_text += " , a.tel_no_g = b.tel_no_g "
    update_text += " , a.tel_no = b.tel_no "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+str(ms_id)+"' "
    update_text += " AND a.apl_id = '"+str(apl_id)+"' "
    update_text += " AND a.apl_id = b.apl_id "
    update_text += " AND ifnull(a.dept_appr_div,'N') = 'N' "
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    apl_max = int(maxRow)

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)
        ans_t2 = request.POST.get('ans_t2_'+str(i+1), None)

        # update_text = " update service20_ms_ans a "
        # update_text += " SET a.ans_t2 = '"+str(ans_t2)+"' "
        # update_text += " WHERE 1=1 "
        # update_text += " AND a.ms_id = '"+str(ms_id)+"' " 
        # update_text += " AND a.apl_no = '"+str(apl_no)+"' "
        # update_text += " AND a.ques_no = '"+str(ques_no)+"' "
        # print(update_text)
        # cursor = connection.cursor()
        # query_result = cursor.execute(update_text)

        ms_ans.objects.filter(ms_id=str(ms_id),apl_no=str(apl_no),ques_no=str(ques_no)).update(ans_t2=str(ans_t2))

    

    delete_text = "delete from service20_ms_apl_fe where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)    

    delete_text = "delete from service20_ms_apl_sa where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)

    delete_text = "delete from service20_ms_apl_lc where ms_id = '"+str(ms_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)

    # -- 생성_어학(ms_apl_fe)_FROM_vw_nanum_foreign_exam

    update_text = " insert into service20_ms_apl_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
    update_text += "      ( ms_id          /* 멘토링 프로그램id */ "
    update_text += "      , apl_no         /* 지원 no */ "
    update_text += "      , fe_no          /* 어학점수 no */ "
    update_text += "      , apl_id         /* 학번 */ "
    update_text += "      , apl_nm         /* 성명 */ "
    update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
    update_text += "      , lang_kind_nm   /* 어학종류명 */ "
    update_text += "      , lang_cd        /* 어학상위코드 */ "
    update_text += "      , lang_nm        /* 어학상위코드명 */ "
    update_text += "      , lang_detail_cd /* 어학하위코드 */ "
    update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
    update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
    update_text += "      , frexm_nm       /* 외국어시험명 */ "
    update_text += "      , score          /* 시험점수 */ "
    update_text += "      , grade          /* 시험등급 */ "
    update_text += "      , ins_id         /* 입력자id */ "
    update_text += "      , ins_ip         /* 입력자ip */ "
    update_text += "      , ins_dt         /* 입력일시 */ "
    update_text += "      , ins_pgm        /* 입력프로그램id */ "
    update_text += " ) "
    update_text += " select '"+str(ms_id)+"' AS ms_id "
    update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "      , @curRank := @curRank +1 AS fe_no  "
    update_text += "      , t1.apl_id         /* 학번 */ "
    update_text += "      , t1.apl_nm         /* 성명 */ "
    update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
    update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
    update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
    update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
    update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
    update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
    update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
    update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
    update_text += "      , t1.score          /* 시험점수 */ "
    update_text += "      , t1.grade          /* 시험등급 */ "
    update_text += "      , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "      , NOW() ins_dt         /* 입력일시 */ "
    update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
    update_text += "      , (SELECT @curRank := 0) r "
    update_text += "  WHERE 1=1 "
    update_text += "    AND t1.apl_id = '"+str(apl_id)+"' "
    print("::_FROM_vw_nanum_foreign_exam::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)    


    # -- 생성_봉사(ms_apl_sa)_FROM_vw_nanum_foreign_exam

    update_text = "insert into service20_ms_apl_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
    update_text += "     ( ms_id           /* 멘토링 프로그램id */ "
    update_text += "     , apl_no          /* 지원 no */ "
    update_text += "     , sa_no           /* 어학점수 no */ "
    update_text += "     , apl_id          /* 학번 */ "
    update_text += "     , apl_nm          /* 성명 */ "
    update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
    update_text += "     , nation_inout_nm /* 국내외구분명 */ "
    update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
    update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
    update_text += "     , activity_nm     /* 봉사명 */ "
    update_text += "     , manage_org_nm   /* 주관기관명 */ "
    update_text += "     , start_date      /* 시작일자 */ "
    update_text += "     , start_time      /* 시작시간 */ "
    update_text += "     , end_date        /* 종료일자 */ "
    update_text += "     , end_time        /* 종료시간 */ "
    update_text += "     , tot_time        /* 총시간 */ "
    update_text += "     , ins_id          /* 입력자id */ "
    update_text += "     , ins_ip          /* 입력자ip */ "
    update_text += "     , ins_dt          /* 입력일시 */ "
    update_text += "     , ins_pgm         /* 입력프로그램id */ "
    update_text += ") "
    update_text += "select '"+str(ms_id)+"' AS ms_id "
    update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "     , @curRank := @curRank +1 AS sa_no "
    update_text += "     , t1.apl_id          /* 학번 */ "
    update_text += "     , t1.apl_nm          /* 성명 */ "
    update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
    update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
    update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
    update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
    update_text += "     , t1.activity_nm     /* 봉사명 */ "
    update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
    update_text += "     , t1.start_date      /* 시작일자 */ "
    update_text += "     , t1.start_time      /* 시작시간 */ "
    update_text += "     , t1.end_date        /* 종료일자 */ "
    update_text += "     , t1.end_time        /* 종료시간 */ "
    update_text += "     , t1.tot_time        /* 총시간 */ "
    update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
    update_text += "     , (SELECT @curRank := 0) r "
    update_text += " WHERE 1=1 "
    update_text += "   AND t1.apl_id = '"+str(apl_id)+"' "
    print("::_FROM_vw_nanum_foreign_exam::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text) 

    # update_text = " update service20_ms_apl a,service20_vw_nanum_foreign_exam b    /* 프로그램 지원자(멘토) 어학 리스트 */ set "
    # update_text += "      a.score1 = '"++"' "
    # update_text += "  WHERE a.apl_id = b.apl_id "
    # update_text += "    AND a.apl_id = '"+str(apl_id)+"' "
    # update_text += "    AND a.ms_id = '"+ms_id+"' "
    # print("::_FROM_vw_nanum_foreign_exam::")
    # print(update_text) 
    # cursor = connection.cursor()
    # query_result = cursor.execute(update_text)    
    
    # -- 생성_자격증(ms_apl_lc)_FROM_service20_vw_nanum_license

    update_text = "insert into service20_ms_apl_lc      "
    update_text += "     ( ms_id           /* 멘토링 프로그램id */ "
    update_text += "     , apl_no          /* 지원 no */ "
    update_text += "     , lc_no           /* 자격 no */ "
    update_text += "     , apl_id          /* 학번 */ "
    update_text += "     , apl_nm          /* 성명 */ "
    update_text += "     , license_large_cd  "
    update_text += "     , license_large_nm  "
    update_text += "     , license_small_cd     "
    update_text += "     , license_small_nm     "
    update_text += "     , license_cd      "
    update_text += "     , license_nm    "        
    update_text += "     , ins_id          /* 입력자id */ "
    update_text += "     , ins_ip          /* 입력자ip */ "
    update_text += "     , ins_dt          /* 입력일시 */ "
    update_text += "     , ins_pgm         /* 입력프로그램id */ "
    update_text += ") "
    update_text += "select '"+str(ms_id)+"' AS ms_id "
    update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "     , @curRank := @curRank +1 AS lc_no "
    update_text += "     , t1.apl_id          /* 학번 */ "
    update_text += "     , t1.apl_nm          /* 성명 */ "
    update_text += "     , t1.license_large_cd  "
    update_text += "     , t1.license_large_nm  "
    update_text += "     , t1.license_small_cd     "
    update_text += "     , t1.license_small_nm     "
    update_text += "     , t1.license_cd      "
    update_text += "     , t1.license_nm    "        
    update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "  FROM service20_vw_nanum_license t1      "
    update_text += "     , (SELECT @curRank := 0) r "
    update_text += " WHERE 1=1 "
    update_text += "   AND t1.apl_id = '"+apl_id+"' "
    print("::_FROM_service20_vw_nanum_license::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)  

    # -- 자격증 종료

    update_text = " update service20_msch a "
    update_text += " SET a.cnt_apl = (select count(*) from service20_ms_apl where ms_id = '"+ms_id+"' and status='10') "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text) 


    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토스쿨 cancle
@csrf_exempt
def MS0101M_adm_cancle(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_ms_apl a "
    update_text += " SET status = '19' "
    update_text += " , doc_cncl_dt = now() "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "

    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    update_text = " update service20_msch a "
    update_text += " SET a.cnt_apl = (select count(*) from service20_ms_apl where ms_id = '"+ms_id+"' and status='10') "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)


    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   

class MS0101M_report_list_Serializer(serializers.ModelSerializer):
    
    ms_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    pr_term_cnt = serializers.SerializerMethodField()
    trn_term_nm = serializers.SerializerMethodField()
    trn_term = serializers.SerializerMethodField()
    mpgm_yr = serializers.SerializerMethodField()
    ins_dt2 = serializers.SerializerMethodField()
    dept_appr_dt2 = serializers.SerializerMethodField()


    # acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')
    ins_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = ms_apl
        #fields = ('ms_id','apl_no','mntr_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','ms_name','pr_yr','pr_sch_yr','pr_term_div','statusNm','statusCode','pr_term_cnt','trn_term_nm','trn_term','mpgm_yr')
        fields = '__all__'
    def get_ms_name(self,obj):
        return obj.ms_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

    def get_pr_term_cnt(self,obj):
        return obj.pr_term_cnt
    def get_trn_term_nm(self,obj):
        return obj.trn_term_nm
    def get_trn_term(self,obj):
        return obj.trn_term
    def get_mpgm_yr(self,obj):
        return obj.mpgm_yr
    def get_ins_dt2(self,obj):
        return obj.ins_dt2
    def get_dept_appr_dt2(self,obj):
        return obj.dept_appr_dt2

    def get_statusNm(self,obj):
        now = datetime.datetime.today()
        msch_query = msch.objects.all()
        msch_query = msch_query.filter(ms_id=obj.ms_id)[0]

        if msch_query.apl_fr_dt == None:
            return '개설중'
        elif now < msch_query.apl_fr_dt:
            return '개설중'
        elif msch_query.apl_fr_dt <= now < msch_query.apl_to_dt:
            return '모집중'
        elif now > msch_query.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'

    def get_statusCode(self,obj):
        now = datetime.datetime.today()
        msch_query = msch.objects.all()
        msch_query = msch_query.filter(ms_id=obj.ms_id)[0]
        if msch_query.apl_fr_dt == None:
            # 개설중
            return '1'
        elif now < msch_query.apl_fr_dt:
            # 개설중
            return '1'
        elif msch_query.apl_fr_dt <= now < msch_query.apl_to_dt:
            # 모집중
            return '2'
        elif now > msch_query.apl_to_dt:
            # 모집완료
            return '3'  
        else:
            # 개설중
            return '1'    

class MS0101M_report_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MS0101M_report_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # ms_apl
        query = "select C.ms_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_ms_apl A,service20_vw_nanum_stdt B,service20_msch C where A.apl_id=B.apl_id and A.ms_id = C.ms_id and A.yr='"+str(l_yr)+"' and A.ms_id = '"+str(ms_ida)+"' and A.apl_id='"+str(ida)+"'"
        
        query = "select c.yr AS mpgm_yr,  "
        query += "       c.trn_term,  "
        query += "       c.ms_name,  "
        query += "       b.pr_yr,  "
        query += "       b.pr_sch_yr,  "
        query += "       b.pr_term_div, "
        # query += "       cast( ((b.pr_sch_yr-1)*2)+(substr(b.pr_term_div,1,1)*1) as UNSIGNED) pr_term_cnt, "
        query += "       a.cmp_term AS pr_term_cnt,"
        query += "       d.std_detl_code_nm AS trn_term_nm,  "
        query += "       DATE_FORMAT(a.dept_appr_dt,'%%Y년  %%m월  %%d일') dept_appr_dt2,  "
        query += "       DATE_FORMAT(a.ins_dt,'%%Y년  %%m월  %%d일') ins_dt2,  "
        query += "       a.*  "
        query += "FROM   service20_ms_apl a,  " 
        query += "       service20_vw_nanum_stdt b, "
        query += "       service20_msch c,  "
        query += "       service20_com_cdd d "
        query += " WHERE a.ms_id = c.ms_id  "
        query += "   AND a.apl_id = b.apl_id "
        query += "   AND a.ms_id = '"+str(ms_ida)+"'  "
        query += "   AND a.apl_id = '"+str(ida)+"' "
        query += "   AND d.std_grp_code  = 'MS0022' "
        query += "   AND d.std_detl_code = c.trn_term "
        queryset = ms_apl.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
#####################################################################################
# MS0101M - END
#####################################################################################




#####################################################################################
# MP0101M - START
#####################################################################################

class MP0101M_list_chk_1_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MP0101M_list_chk_1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_1_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # 학년체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_mp_sub_desc_select_01('"+mp_id+"','MS0010') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_mp_sub_desc_select_01('"+mp_id+"','MS0010'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.sch_yr IN  "
        query += "                   (SELECT t3.att_cdd "
        query += "                      FROM service20_mp_sub t3 "
        query += "                     WHERE t3.mp_id   = '"+mp_id+"' "
        query += "                       AND t3.att_id  = 'MS0010' "
        query += "                       AND t3.att_cdh = 'MS0010' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_2_Serializer(serializers.ModelSerializer):

    
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('name','code')

    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code

class MP0101M_list_chk_2(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_2_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # -- 직전학기 학점 제한
        query = " select t2.id,CASE WHEN t2.score03 >= t3.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', t3.att_val, '미만') END as name "
        query += "      , CASE WHEN t2.score03 >= t3.att_val THEN 'Y' ELSE 'N' END as code "
        query += "   FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "      , (  /* 학점 제한 */ "
        query += "         select IFNULL(max(att_val),3) att_val "
        query += "           FROM service20_mp_sub t3 "
        query += "          WHERE t3.mp_id   = '"+mp_id+"' "
        query += "            AND t3.att_id  = 'MS0013' "
        query += "            AND t3.att_cdh = 'MS0013' "
        query += "            AND t3.att_cdd = '40' "
        query += "       ) t3 "
        query += "   WHERE t2.apl_id = '"+apl_id+"' "

        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_3_Serializer(serializers.ModelSerializer):

    
    chk = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_chk(self, obj):
        return obj.chk

class MP0101M_list_chk_3(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_3_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # -- 신청가능한 대학/학과체크

        query = " select '1' as id,COUNT(*) as chk "
        query += "   FROM ( "
        query += "          select att_val "
        query += "            FROM service20_mp_sub t3 "
        query += "           WHERE t3.mp_id   = '"+mp_id+"' "
        query += "             AND t3.att_id  = 'MP0010' "
        query += "             AND t3.att_cdh = 'MP0010' "
        query += "             AND t3.att_cdd = '20' /* 대학 */ "
        query += "           UNION ALL "
        query += "          select att_val "
        query += "            FROM service20_mp_sub t3 "
        query += "           WHERE t3.mp_id   = '"+mp_id+"' "
        query += "             AND t3.att_id  = 'MP0010' "
        query += "             AND t3.att_cdh = 'MP0010' "
        query += "             AND t3.att_cdd = '30'  /* 학과 */ "
        query += "       ) T1 "

        
        queryset = com_cdd.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_4_Serializer(serializers.ModelSerializer):

    
    chk = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_chk(self, obj):
        return obj.chk

class MP0101M_list_chk_4(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_4_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # -- 신청가능한 대학/학과체크

        query = " select '1' as id,COUNT(*) as chk "
        query += "   FROM ( "
        query += "          select apl_id "
        query += "            FROM service20_vw_nanum_stdt b "
        query += "           WHERE cllg_nm IN ( SELECT att_val "
        query += "                                FROM service20_mp_sub t3 "
        query += "                               WHERE t3.mp_id   = '"+mp_id+"' "
        query += "                                 AND t3.att_id  = 'MP0010' "
        query += "                                 AND t3.att_cdh = 'MP0010' "
        query += "                                 AND t3.att_cdd = '20' /* 대학 */ "
        query += "                             ) "
        query += "            AND APL_ID = '"+apl_id+"' "
        query += "         UNION ALL "
        query += "          select apl_id "
        query += "            FROM service20_vw_nanum_stdt b "
        query += "           WHERE dept_nm IN ( SELECT att_val "
        query += "                                FROM service20_mp_sub t3 "
        query += "                               WHERE t3.mp_id   = '"+mp_id+"' "
        query += "                                 AND t3.att_id  = 'MP0010' "
        query += "                                 AND t3.att_cdh = 'MP0010' "
        query += "                                 AND t3.att_cdd = '30'  /* 학과 */ "
        query += "                             ) "
        query += "            AND apl_id = '"+apl_id+"' "
        query += "        ) T1 "

        queryset = com_cdd.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class MP0101M_list_chk_5_Serializer(serializers.ModelSerializer):

    
    mentor_num = serializers.SerializerMethodField()
    class Meta:
        model = mentor
        fields = '__all__'

    def get_mentor_num(self, obj):
        return obj.mentor_num

class MP0101M_list_chk_5(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_5_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")

        # -- 멘토체크
        query = "select COUNT(*) as mentor_num,A.* from service20_mentor A where apl_id = '"+str(apl_id)+"'"

        queryset = mentor.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class MP0101M_list_chk_6_Serializer(serializers.ModelSerializer):

    
    apl_cnt = serializers.SerializerMethodField()
    intv_rslt = serializers.SerializerMethodField()
    fnl_rslt = serializers.SerializerMethodField()
    fnl_rslt1 = serializers.SerializerMethodField()
    apl_en = serializers.SerializerMethodField()
    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_apl_cnt(self, obj):
        return obj.apl_cnt
    def get_intv_rslt(self, obj):
        return obj.intv_rslt
    def get_fnl_rslt(self, obj):
        return obj.fnl_rslt
    def get_fnl_rslt1(self, obj):
        return obj.fnl_rslt1
    def get_apl_en(self, obj):
        return obj.apl_en

class MP0101M_list_chk_6(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_6_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")
        yr = request.GET.get('yr', "")

        # -- 멘토체크
        query = "select '0' as id "
        query += "      , COUNT(t1.apl_id)           AS apl_cnt  /* 지원여부 */"
        query += "      , IFNULL(MAX(intv_rslt), 'N') AS intv_rslt /* 합격여부 */"
        # query += "      , IFNULL(MAX(fnl_rslt), 'N') AS fnl_rslt /* 합격여부 */"
        # query += "      , IFNULL(MAX(IFNULL(intv_rslt,fnl_rslt)), 'N') AS fnl_rslt1 /* 합격여부 */"        
        query += "      , 'Y' AS fnl_rslt /* 합격여부 */"
        query += "      , 'Y' AS fnl_rslt1 /* 합격여부 */"        
        query += "      , CASE (SELECT trim( IFNULL(MIN(ATT_CDD), 'Y') ) "
        query += "                FROM service20_mp_sub"
        query += "               WHERE MP_ID   = '"+str(mp_id)+"'"
        query += "                 AND ATT_ID  = 'MP0012' /* 멘토 여부 */"
        query += "                 AND ATT_CDH = 'MP0012') WHEN 'Y' THEN CASE WHEN (SELECT COUNT(*) FROM service20_mentor t3 WHERE t3.apl_id = '"+str(apl_id)+"') > 0 THEN 'Y' ELSE 'N' END"
        query += "                                         WHEN 'N' THEN 'Y'"
        query += "                                                  ELSE 'Y'"
        query += "        END AS apl_en"
        query += "   FROM service20_ms_apl t1"
        query += "  INNER JOIN service20_msch   t2 ON (t2.ms_id = t1.ms_id AND t2.status >= '60' ) /* 교육진행중 */ "
        query += "  WHERE 1=1"
        query += "    AND t1.apl_id = '"+str(apl_id)+"'"
        query += "    AND t2.yr in (select t3.yr from service20_mpgm t3 where t3.mp_id = '"+str(mp_id)+"')"

        queryset = mp_mtr.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class MP0101M_list_chk_7_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MP0101M_list_chk_7(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_7_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # 이수학기 체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_mp_sub_desc_select_01('"+mp_id+"','MS0011') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_mp_sub_desc_select_01('"+mp_id+"','MS0011'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.cmp_term IN  "
        query += "                   (SELECT t3.att_cdd*1 "
        query += "                      FROM service20_mp_sub t3 "
        query += "                     WHERE t3.mp_id   = '"+mp_id+"' "
        query += "                       AND t3.att_id  = 'MS0011' "
        query += "                       AND t3.att_cdh = 'MS0011' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_8_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mpgm
        fields = ('mp_id', 'apl_fr_dt','apl_to_dt')

class MP0101M_list_chk_8(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_8_Serializer

    def list(self, request):

        mp_id = request.GET.get('mp_id', "")

        # 모집기간 체크
        query = " SELECT mp_id, apl_fr_dt, apl_to_dt FROM service20_mpgm WHERE mp_id = '" + mp_id + "'"

        queryset = mpgm.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_9_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_team
        fields = '__all__'

class MP0101M_list_chk_9(generics.ListAPIView):
    queryset = mp_team.objects.all()
    serializer_class = MP0101M_list_chk_9_Serializer

    def list(self, request):

        mp_id = request.GET.get('mp_id', "")
        team_id = request.GET.get('team_id', "")

        # 팀명 중복 체크
        query = " SELECT id, mp_id, count(0) AS team_id FROM service20_mp_team WHERE mp_id = '" + mp_id + "' AND team_id = '" + team_id + "' "

        queryset = mp_team.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    code  = serializers.SerializerMethodField()
    code_nm = serializers.SerializerMethodField()
    score03 = serializers.SerializerMethodField()
    att_val = serializers.SerializerMethodField()
    dateAplYn = serializers.SerializerMethodField()
    dept_appr_div = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = '__all__'

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_status(self,obj):
        return obj.status
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm
    def get_code(self,obj):
        return obj.code
    def get_code_nm(self,obj):
        return obj.code_nm
    def get_score03(self,obj):
        return obj.score03
    def get_att_val(self,obj):
        return obj.att_val
    def get_dateAplYn(self,obj):
        return obj.dateAplYn
    def get_dept_appr_div(self,obj):
        return obj.dept_appr_div

class MP0101M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")

        query = "select ifnull((select 'Y' from service20_mp_mtr where yr = '"+str(l_yr)+"' and apl_id = '"+str(ida)+"' and mp_id = A.mp_id),'N') AS applyFlag,A.* from service20_mpgm A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"'"
        
        # SELECT att_val
        #   FROM service20_mp_sub T3
        #  WHERE T3.mp_id   = 'P182014'
        #    AND T3.att_id  = 'MP0071'
        #    AND T3.att_cdh = 'MP0071'
        #    AND T3.att_cdd = '10'
        #    /*미만*/

        # 멘토만 조회가능.

        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
        
        query += " case when now() between A.apl_fr_dt and A.apl_to_dt then 'Y' else 'N' end dateAplYn, "

        query += " E.score03, D.att_val,"

        query += " CASE WHEN E.score03 >= D.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', D.att_val, '미만') END code_nm,CASE WHEN E.score03 >= D.att_val THEN 'Y' ELSE 'N' END code, "

        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += " B.dept_appr_div   AS dept_appr_div, "
        query += "        A.*  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        

        query += "        LEFT JOIN        (  /* 학점 제한 */ "
        query += "               select cast(att_val as unsigned) att_val,mp_id "
        query += "                 FROM service20_mp_sub t3 "
        query += "                WHERE t3.att_id  = 'MP0071' "
        query += "                  AND t3.att_cdh = 'MP0071' "
        query += "                  AND t3.att_cdd = '10' "
        query += "               ) D ON (A.mp_id = D.mp_id) "

        # query += "       LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        # query += "             FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        # query += "            WHERE t2.sch_yr IN  "
        # query += "                  (SELECT t3.att_cdd "
        # query += "                     FROM service20_mp_sub t3 "
        # query += "                    WHERE t3.mp_id   = 'P182014' "
        # query += "                      AND t3.att_id  = 'MS0010' "
        # query += "                      AND t3.att_cdh = 'MS0010' "
        # query += "                  ) "
        # query += "            GROUP BY t2.apl_id "
        # query += "           ) t4 ON (t4.apl_id = t1.apl_id) "

        query += " , service20_vw_nanum_stdt E "

        query += " WHERE  A.yr = '"+str(l_yr)+"'  "
        query += "        AND A.apl_term = '"+str(l_apl_term)+"'  "
        query += "        AND A.use_div = 'Y' "

        query += "        AND E.apl_id = '"+str(ida)+"'"
        # query += "        AND (SELECT Count(1)  "
        # query += "             FROM   service20_mentor  "
        # query += "             WHERE  apl_id = '"+str(ida)+"') > 0  "
        
        query += "        AND A.status > '10'  "

        query += "        AND IF(A.status = '10'  "
        query += "               AND Now() > A.apl_to_dt, 'xx', A.status) LIKE  "
        query += "            Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        query += "            or '%%'  "
        query += " ORDER  BY A.mp_id DESC, A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "


        
        queryset = mpgm.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_all_hompage_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    mng_org_nm = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    cert_en = serializers.SerializerMethodField()
    apl_status = serializers.SerializerMethodField()
    apl_status_nm = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = (
            'mp_id',
            'mp_name',
            'status',
            'statusCode',
            'yr',
            'yr_seq',
            'sup_org',
            'mng_org',
            'applyFlag',
            'applyStatus',
            'apl_fr_dt',
            'apl_to_dt',
            'mnt_fr_dt',
            'mnt_to_dt',
            'cnt_trn',
            'status',
            'status_nm',
            'applyFlagNm',
            'sup_org_nm',
            'mng_org_nm',
            'mgr_nm',
            'apl_no',
            'apl_id',
            'cert_en',
            'apl_status',
            'apl_status_nm',
        )

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   

    def get_status(self,obj):
        return obj.status

    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm

    def get_mng_org_nm(self, obj):
        return obj.mng_org_nm

    def get_apl_no(self, obj):
        return obj.apl_no

    def get_apl_id(self, obj):
        return obj.apl_id
    def get_cert_en(self, obj):
        return obj.cert_en
    def get_apl_status(self, obj):
        return obj.apl_status
    def get_apl_status_nm(self, obj):
        return obj.apl_status_nm                


class MP0101M_list_all_hompage(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_all_hompage_Serializer

    def list(self, request):
        ida = request.GET.get('user_id', "")

        
        # 멘토만 조회가능.
        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += " c2.std_detl_code_nm   AS mng_org_nm, "
        query += " B.apl_no   AS apl_no, B.apl_id AS apl_id, "
        query += " B.cert_en   AS cert_en,"
        query += " B.status    as apl_status,"
        query += " (select std_detl_code_nm from service20_com_cdd where B.status = std_detl_code and std_grp_code = 'MP0053') as apl_status_nm,"
        query += "        A.*  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"'  "
        query += "                    AND B.fnl_rslt = 'P' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += "        LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code = 'MP0003' AND c2.std_detl_code = A.mng_org)"
        query += " WHERE  B.apl_id = '"+str(ida)+"'  "
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "

        queryset = mpgm.objects.raw(query)  

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 앱사용(시작)
class MP0101M_list_all_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    # cert_en = serializers.SerializerMethodField()
    # apl_status = serializers.SerializerMethodField()
    # apl_status_nm = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = (
            'mp_id',
            'mp_name',
            'status',
            'statusCode',
            'yr',
            'yr_seq',
            'sup_org',
            'mng_org',
            'applyFlag',
            'applyStatus',
            'apl_fr_dt',
            'apl_to_dt',
            'mnt_fr_dt',
            'mnt_to_dt',
            'cnt_trn',
            'status',
            'status_nm',
            'applyFlagNm',
            'sup_org_nm',
            'mgr_nm',
            'apl_id',
            'apl_no',
            # 'cert_en',
            # 'apl_status',
            # 'apl_status_nm',
        )

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   

    def get_status(self,obj):
        return obj.status

    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm

    def get_apl_id(self,obj):
        return obj.apl_id

    def get_apl_no(self,obj):
        return obj.apl_no

    # def get_cert_en(self, obj):
    #     return obj.cert_en
    # def get_apl_status(self, obj):
    #     return obj.apl_status
    # def get_apl_status_nm(self, obj):
    #     return obj.apl_status_nm                


class MP0101M_list_all(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_all_Serializer

    def list(self, request):
        ida = request.GET.get('user_id', "")

        
        # 멘토만 조회가능.
        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += "        A.*  "
        query += "      , B.apl_id as apl_id  "
        query += "      , B.apl_no as apl_no  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += " WHERE  B.apl_id = '"+str(ida)+"'  "        
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "

        queryset = mpgm.objects.raw(query)  

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
# 앱사용(종료) 

class MP0101M_list_all_mypage_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    mng_org_nm = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    cert_en = serializers.SerializerMethodField()
    apl_status = serializers.SerializerMethodField()
    apl_status_nm = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = (
            'mp_id',
            'mp_name',
            'status',
            'statusCode',
            'yr',
            'yr_seq',
            'sup_org',
            'mng_org',
            'applyFlag',
            'applyStatus',
            'apl_fr_dt',
            'apl_to_dt',
            'mnt_fr_dt',
            'mnt_to_dt',
            'cnt_trn',
            'status',
            'status_nm',
            'applyFlagNm',
            'sup_org_nm',
            'mng_org_nm',
            'mgr_nm',
            'apl_no',
            'apl_id',
            'cert_en',
            'apl_status',
            'apl_status_nm',
        )

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   

    def get_status(self,obj):
        return obj.status

    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm

    def get_mng_org_nm(self, obj):
        return obj.mng_org_nm

    def get_apl_no(self, obj):
        return obj.apl_no

    def get_apl_id(self, obj):
        return obj.apl_id
    def get_cert_en(self, obj):
        return obj.cert_en
    def get_apl_status(self, obj):
        return obj.apl_status
    def get_apl_status_nm(self, obj):
        return obj.apl_status_nm                


class MP0101M_list_all_mypage(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_all_mypage_Serializer

    def list(self, request):
        ida = request.GET.get('user_id', "")

        
        # 멘토만 조회가능.
        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += " c2.std_detl_code_nm   AS mng_org_nm, "
        query += " B.apl_no   AS apl_no, B.apl_id AS apl_id, "
        query += " B.cert_en   AS cert_en,"
        query += " B.status    as apl_status,"
        query += " (select std_detl_code_nm from service20_com_cdd where B.status = std_detl_code and std_grp_code = 'MP0053') as apl_status_nm,"
        query += "        A.*  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += "        LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code = 'MP0003' AND c2.std_detl_code = A.mng_org)"
        query += " WHERE  B.apl_id = '"+str(ida)+"'  "
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "

        queryset = mpgm.objects.raw(query)  

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 질문유형 가져오기
class MP0101M_quest_Serializer(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    ans_min_len = serializers.SerializerMethodField()
    ans_max_len = serializers.SerializerMethodField()
    class Meta:
        model = mp_sub
        fields = ('id','mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk','ans_min_len','ans_max_len')

        
    def get_std_detl_code(self,obj):
        return obj.std_detl_code
        
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk    
    def get_ans_min_len(self,obj):
        return obj.ans_min_len  
    def get_ans_max_len(self,obj):
        return obj.ans_max_len

# 멘토링 프로그램 질문유형 가져오기
class MP0101M_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_quest_Serializer
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None)           
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0014' and B.use_indc = 'Y' and A.mp_id = '"+key1+"' order by A.sort_seq"
        
        query = "select  "
        query += "     t3.std_detl_code, "
        query += "     t3.std_detl_code_nm, "
        query += "     t3.rmrk, "
        query += "     fn_mp_sub_att_val_select_01(t1.mp_id, t1.att_id, 'MS0028', t1.att_cdd) ans_min_len, "
        query += "     fn_mp_sub_att_val_select_01(t1.mp_id, t1.att_id, 'MS0029', t1.att_cdd) ans_max_len, "
        query += "     t1.* "
        query += "FROM service20_mp_sub t1 "
        query += "LEFT JOIN service20_com_cdd t3 ON (t3.std_grp_code  = t1.att_cdh "
        query += "                               AND t3.std_detl_code = t1.att_cdd) "
        query += "WHERE t1.mp_id   = '"+key1+"' "
        query += " AND t1.att_id  = 'MS0014' "
        query += " AND t1.att_cdh = 'MS0014' "
        query += "ORDER BY t1.sort_seq "

        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 신청
@csrf_exempt
def MP0101M_save(request):
    ida = request.POST.get('memberNo', None)
    programId = request.POST.get('programID', None)
    que1 = request.POST.get('que1', None)
    que2 = request.POST.get('que2', None)
    que3 = request.POST.get('que3', None)
    que4 = request.POST.get('que4', None)
    que5 = request.POST.get('que5', None)
    indv_div = request.POST.get('indv_div', None)
    mentoTeamMax = request.POST.get('mentoTeamMax', 0)
    team_nm = request.POST.get('Team_memberNo', "")

    # 저장상태구분 I(제출)/S(임시저장)
    save_status = request.POST.get('save_status', "")

    ms_ida = request.POST.get('ms_id', None)
    apl_max = request.POST.get('aplMax', 0)
    apl_max_team = request.POST.get('aplMaxTeam', 0)
    client_ip = request.META['REMOTE_ADDR']
    
    print("::ida::")
    print(ida)
    print("::mentoTeamMax::")
    print(mentoTeamMax)
    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    mp_id = programId
    mp_mtr_max = mp_mtr.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
    #mp_mtr_max = mp_mtr.objects.all().last()
    #mp_mtr_max = mp_mtr_max + 1

    print("::start::")
    l_status = '10'
    team_l_status = '10'
    if save_status == "I":
        # 제출
        l_status = '10'
        team_l_status = '10'
    elif save_status == "S":    
        # 저장
       l_status = '00'
       team_l_status = '00'
        
    apl_no = mp_mtr_max
    apl_id = ida
    v_gen = ""
    if str(rows.gen_cd) == "1":
        v_gen = "M"
    else:
        v_gen = "F"
    
    max_no = mp_mtr_max['vlMax']    
    print("::max_no::")
    print(max_no)
    if max_no == None:
        apl_no = 0
    else:
        apl_no = mp_mtr_max['vlMax']
        apl_no = apl_no + 1

    
    # query = "select ifnull(max(apl_no),0) as apl_no,ifnull(max(team_id),0) as team_no from service20_mp_mtr where mp_id = '"+mp_id+"'"  
    query = "select ifnull( nullif(max(apl_no),0) ,0) as apl_no,ifnull( nullif(max(team_id),0) ,0) as team_no from service20_mp_mtr where mp_id = '"+mp_id+"'"  
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    apl_no = int(results[0].apl_no)
    apl_no = apl_no+1

    team_no = int(results[0].team_no)
    team_no = team_no+1
    # 팀단위 추가.
    if indv_div != 'T':
        team_no = ''

    print("::apl_no::")
    print(apl_no)
    
    if rows.unv_cd == None:
        v_unv_cd = ''
    else:
        v_unv_cd = rows.unv_cd 

    if rows.unv_nm == None:
        v_unv_nm = ''
    else:
        v_unv_nm = rows.unv_nm


    query = " select t2.mp_id,t2.yr FROM service20_mpgm t2  WHERE 1=1 "
    query += " AND t2.mp_id          = '"+mp_id+"'"
    queryset = mpgm.objects.raw(query)[0]


    
    rowsChk = mp_mtr.objects.filter(apl_id=apl_id,mp_id=mp_id).exists()

    if rowsChk == True:
        context = {'message': 'duplicate'}
    else:
        print("::rows.tel_no::")
        print(rows.tel_no)
        if rows.tel_no == None:
            v_tel_no = ''
        else:
            v_tel_no = rows.tel_no.replace('-', '')


        if rows.mob_no == None:
            v_mob_no = ''
        else:
            v_mob_no = rows.mob_no.replace('-', '')
            
        if rows.tel_no_g == None:
            v_tel_no_g = ''
        else:
            v_tel_no_g = rows.tel_no_g.replace('-', '')   

        model_instance = mp_mtr(
            mp_id=mp_id, 
            apl_no=apl_no, 
            mntr_id=ida,
            team_id=str(team_no),
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            unv_cd=str(v_unv_cd),
            unv_nm=str(v_unv_nm),
            cllg_cd=rows.cllg_cd,
            cllg_nm=rows.cllg_nm,
            dept_cd=rows.dept_cd,
            dept_nm=rows.dept_nm,
            brth_dt=rows.brth_dt,
            gen=v_gen,
            yr=queryset.yr,
            term_div=rows.term_div,
            sch_yr=rows.sch_yr,
            mob_no=v_mob_no,
            tel_no=v_tel_no,
            tel_no_g=v_tel_no_g,
            h_addr=rows.h_addr,
            email_addr=rows.email_addr,
            bank_acct=rows.bank_acct,
            bank_cd=rows.bank_cd,
            bank_nm=rows.bank_nm,
            score1=rows.score01,
            score2=rows.score02,
            score3=rows.score03,
            score4=rows.score04,
            score5=rows.score05,
            score6=rows.score06,
            cmp_term=rows.cmp_term,
            pr_yr=rows.pr_yr,
            pr_sch_yr=rows.pr_sch_yr,
            pr_term_div=rows.pr_term_div,
            inv_agr_div = 'Y',
            inv_agr_dt = datetime.datetime.today(),
            status=l_status, # 지원
            mjr_cd=rows.mjr_cd,
            mjr_nm=rows.mjr_nm,
            ins_id=apl_id,
            ins_ip=str(client_ip),
            ins_dt=datetime.datetime.today()
            )
        model_instance.save()
        
        # 팀단위 추가.
        if indv_div == 'T':
            model_instance_team_mem = mp_team_mem(
                mp_id=mp_id, 
                team_id=str(team_no),
                apl_no=apl_no,
                ins_id=apl_id,
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today(),
                upd_id=apl_id,
                upd_ip=str(client_ip),
                upd_dt=datetime.datetime.today(),
                )
            model_instance_team_mem.save()

        apl_max = int(apl_max)

        for i in range(0,apl_max):
            anst2 = request.POST.get('que'+str(i+1), None)
            ques_no = request.POST.get('ques_no'+str(i+1), None)

            model_instance2 = mp_ans(
                mp_id=mp_id, 
                test_div='10', 
                apl_no=apl_no,
                ques_no=ques_no,
                apl_id=apl_id,
                apl_nm=rows.apl_nm,
                sort_seq =i+1,
                ans_t2=anst2,
                ans_div='2',
                ins_id=apl_id,
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today()
                )
            model_instance2.save()

        # 팀단위 추가.
        if indv_div == 'T':
            ################################## 팀 단위 mp_team 생성
            model_instance2 = mp_team(
                mp_id=mp_id, 
                team_no=team_no,
                team_nm=team_nm,
                team_id=team_no,
                ldr_id=apl_id,
                apl_dt=datetime.datetime.today(),
                status='00',
                score1=rows.score01,
                score2=rows.score02,
                score3=rows.score03,
                score4=rows.score04,
                score5=rows.score05,
                score6=rows.score06,
                ins_id=apl_id,
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today(),
                upd_id=apl_id,
                upd_ip=str(client_ip),
                upd_dt=datetime.datetime.today()
                )
            model_instance2.save()
            #######################################################

            for i in range(0,int(apl_max_team)):
                anst2 = request.POST.get('que_team'+str(i+1), None)
                ques_no = request.POST.get('ques_no_team'+str(i+1), None)

                model_instance2 = mp_team_ans(
                    mp_id=mp_id, 
                    test_div='10', 
                    team_no=team_no,                    
                    ques_no=ques_no,
                    team_id=team_no,
                    team_nm=team_nm,
                    sort_seq =i+1,
                    ans_t2=anst2,
                    ans_div='2',
                    ins_id=apl_id,
                    ins_ip=str(client_ip),
                    ins_dt=datetime.datetime.today()
                    )
                model_instance2.save()

            for i in range(0,int(mentoTeamMax)):
                l_team_apl_id = request.POST.get('mentoTeam'+str(i+1), None)
                rows = vw_nanum_stdt.objects.filter(apl_id=l_team_apl_id)[0]
                #mp_mtr_max = mp_mtr.objects.all().last()
                #mp_mtr_max = mp_mtr_max + 1

                print("::team_start::"+l_team_apl_id)

                team_apl_no = mp_mtr_max
                team_apl_id = l_team_apl_id
                v_gen = ""
                if str(rows.gen_cd) == "1":
                    v_gen = "M"
                else:
                    v_gen = "F"
                
                max_no = mp_mtr_max['vlMax']    
                print("::max_no::")
                print(max_no)
                if max_no == None:
                    team_apl_no = 0
                else:
                    team_apl_no = mp_mtr_max['vlMax']
                    team_apl_no = team_apl_no + 1

                
                query = "select ifnull( nullif(max(apl_no),0) ,0) as apl_no,ifnull( nullif(max(team_id),0) ,0) as team_no from service20_mp_mtr where mp_id = '"+mp_id+"'"  
                cursor = connection.cursor()
                cursor.execute(query)    
                results = namedtuplefetchall(cursor)    
                team_apl_no = int(results[0].apl_no)
                team_apl_no = team_apl_no+1

                # team_no = int(results[0].team_no)
                # team_no = team_no+1

                print("::apl_no::")
                print(team_apl_no)
                
                if rows.unv_cd == None:
                    v_unv_cd = ''
                else:
                    v_unv_cd = rows.unv_cd 

                if rows.unv_nm == None:
                    v_unv_nm = ''
                else:
                    v_unv_nm = rows.unv_nm


                query = " select t2.mp_id,t2.yr FROM service20_mpgm t2  WHERE 1=1 "
                query += " AND t2.mp_id          = '"+mp_id+"'"
                queryset = mpgm.objects.raw(query)[0]


                
                rowsChk = mp_mtr.objects.filter(apl_id=team_apl_id,mp_id=mp_id).exists()

                if rowsChk == True:
                    context = {'message': 'duplicate'}
                else:
                    print("::rows.tel_no::")
                    print(rows.tel_no)
                    if rows.tel_no == None:
                        v_tel_no = ''
                    else:
                        v_tel_no = rows.tel_no.replace('-', '')


                    if rows.mob_no == None:
                        v_mob_no = ''
                    else:
                        v_mob_no = rows.mob_no.replace('-', '')
                        
                    if rows.tel_no_g == None:
                        v_tel_no_g = ''
                    else:
                        v_tel_no_g = rows.tel_no_g.replace('-', '')   

                    model_instance = mp_mtr(
                        mp_id=mp_id, 
                        apl_no=team_apl_no, 
                        mntr_id=team_apl_id,
                        apl_id=team_apl_id,
                        team_id=str(team_no),
                        apl_nm=rows.apl_nm,
                        unv_cd=str(v_unv_cd),
                        unv_nm=str(v_unv_nm),
                        cllg_cd=rows.cllg_cd,
                        cllg_nm=rows.cllg_nm,
                        dept_cd=rows.dept_cd,
                        dept_nm=rows.dept_nm,
                        brth_dt=rows.brth_dt,
                        gen=v_gen,
                        yr=queryset.yr,
                        term_div=rows.term_div,
                        sch_yr=rows.sch_yr,
                        mob_no=v_mob_no,
                        tel_no=v_tel_no,
                        tel_no_g=v_tel_no_g,
                        h_addr=rows.h_addr,
                        email_addr=rows.email_addr,
                        bank_acct=rows.bank_acct,
                        bank_cd=rows.bank_cd,
                        bank_nm=rows.bank_nm,
                        score1=rows.score01,
                        score2=rows.score02,
                        score3=rows.score03,
                        score4=rows.score04,
                        score5=rows.score05,
                        score6=rows.score06,
                        cmp_term=rows.cmp_term,
                        pr_yr=rows.pr_yr,
                        pr_sch_yr=rows.pr_sch_yr,
                        pr_term_div=rows.pr_term_div,
                        inv_agr_div = 'Y',
                        inv_agr_dt = datetime.datetime.today(),
                        status='00', # 저장
                        mjr_cd=rows.mjr_cd,
                        mjr_nm=rows.mjr_nm,
                        ins_id=apl_id,
                        ins_ip=str(client_ip),
                        ins_dt=datetime.datetime.today()
                        )
                    model_instance.save()

                    model_instance_team_mem = mp_team_mem(
                        mp_id=mp_id, 
                        team_id=str(team_no),
                        apl_no=team_apl_no,
                        ins_id=apl_id,
                        ins_ip=str(client_ip),
                        ins_dt=datetime.datetime.today(),
                        upd_id=apl_id,
                        upd_ip=str(client_ip),
                        upd_dt=datetime.datetime.today(),
                        )
                    model_instance_team_mem.save()

                    # -- 생성_어학(mp_mtr_fe)_FROM_vw_nanum_foreign_exam

                    update_text = " insert into service20_mp_mtr_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
                    update_text += "      ( mp_id          /* 멘토링 프로그램id */ "
                    update_text += "      , apl_no         /* 지원 no */ "
                    update_text += "      , fe_no          /* 어학점수 no */ "
                    update_text += "      , apl_id         /* 학번 */ "
                    update_text += "      , apl_nm         /* 성명 */ "
                    update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
                    update_text += "      , lang_kind_nm   /* 어학종류명 */ "
                    update_text += "      , lang_cd        /* 어학상위코드 */ "
                    update_text += "      , lang_nm        /* 어학상위코드명 */ "
                    update_text += "      , lang_detail_cd /* 어학하위코드 */ "
                    update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
                    update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
                    update_text += "      , frexm_nm       /* 외국어시험명 */ "
                    update_text += "      , score          /* 시험점수 */ "
                    update_text += "      , grade          /* 시험등급 */ "
                    update_text += "      , ins_id         /* 입력자id */ "
                    update_text += "      , ins_ip         /* 입력자ip */ "
                    update_text += "      , ins_dt         /* 입력일시 */ "
                    update_text += "      , ins_pgm        /* 입력프로그램id */ "
                    update_text += " ) "
                    update_text += " select '"+str(mp_id)+"' AS mp_id "
                    update_text += "      , '"+str(team_apl_no)+"' apl_no         /* 지원 no */ "
                    update_text += "      , @curRank := @curRank +1 AS fe_no  "
                    update_text += "      , t1.apl_id         /* 학번 */ "
                    update_text += "      , t1.apl_nm         /* 성명 */ "
                    update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
                    update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
                    update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
                    update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
                    update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
                    update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
                    update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
                    update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
                    update_text += "      , t1.score          /* 시험점수 */ "
                    update_text += "      , t1.grade          /* 시험등급 */ "
                    update_text += "      , '"+team_apl_id+"' ins_id         /* 입력자id */ "
                    update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
                    update_text += "      , NOW() ins_dt         /* 입력일시 */ "
                    update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
                    update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
                    update_text += "      , (SELECT @curRank := 0) r "
                    update_text += "  WHERE 1=1 "
                    update_text += "    AND t1.apl_id = '"+team_apl_id+"' "
                    print("::_FROM_vw_nanum_foreign_exam::")
                    print(update_text) 
                    cursor = connection.cursor()
                    query_result = cursor.execute(update_text)    


                    # -- 생성_봉사(mp_mtr_sa)_FROM_vw_nanum_foreign_exam

                    update_text = "insert into service20_mp_mtr_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
                    update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
                    update_text += "     , apl_no          /* 지원 no */ "
                    update_text += "     , sa_no           /* 어학점수 no */ "
                    update_text += "     , apl_id          /* 학번 */ "
                    update_text += "     , apl_nm          /* 성명 */ "
                    update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
                    update_text += "     , nation_inout_nm /* 국내외구분명 */ "
                    update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
                    update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
                    update_text += "     , activity_nm     /* 봉사명 */ "
                    update_text += "     , manage_org_nm   /* 주관기관명 */ "
                    update_text += "     , start_date      /* 시작일자 */ "
                    update_text += "     , start_time      /* 시작시간 */ "
                    update_text += "     , end_date        /* 종료일자 */ "
                    update_text += "     , end_time        /* 종료시간 */ "
                    update_text += "     , tot_time        /* 총시간 */ "
                    update_text += "     , ins_id          /* 입력자id */ "
                    update_text += "     , ins_ip          /* 입력자ip */ "
                    update_text += "     , ins_dt          /* 입력일시 */ "
                    update_text += "     , ins_pgm         /* 입력프로그램id */ "
                    update_text += ") "
                    update_text += "select '"+str(mp_id)+"' AS mp_id "
                    update_text += "     , '"+str(team_apl_no)+"' apl_no         /* 지원 no */ "
                    update_text += "     , @curRank := @curRank +1 AS sa_no "
                    update_text += "     , t1.apl_id          /* 학번 */ "
                    update_text += "     , t1.apl_nm          /* 성명 */ "
                    update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
                    update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
                    update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
                    update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
                    update_text += "     , t1.activity_nm     /* 봉사명 */ "
                    update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
                    update_text += "     , t1.start_date      /* 시작일자 */ "
                    update_text += "     , t1.start_time      /* 시작시간 */ "
                    update_text += "     , t1.end_date        /* 종료일자 */ "
                    update_text += "     , t1.end_time        /* 종료시간 */ "
                    update_text += "     , t1.tot_time        /* 총시간 */ "
                    update_text += "     , '"+team_apl_id+"' ins_id         /* 입력자id */ "
                    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
                    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
                    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
                    update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
                    update_text += "     , (SELECT @curRank := 0) r "
                    update_text += " WHERE 1=1 "
                    update_text += "   AND t1.apl_id = '"+team_apl_id+"' "
                    print("::_FROM_vw_nanum_foreign_exam::")
                    print(update_text) 
                    cursor = connection.cursor()
                    query_result = cursor.execute(update_text)    

                    # query = " select b.* from service20_vw_nanum_stdt a where a.apl_id = '"+apl_id+"' "
                    # cursor = connection.cursor()
                    # query_result = cursor.execute(query)  
                    # results_st = namedtuplefetchall(cursor)  
                    # v_dept_cd = results_st[0].dept_cd
                    # v_mjr_cd = results_st[0].mjr_cd


                    # -- 생성_자격증(mp_mtr_lc)_FROM_service20_vw_nanum_license

                    update_text = "insert into service20_mp_mtr_lc      "
                    update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
                    update_text += "     , apl_no          /* 지원 no */ "
                    update_text += "     , lc_no           /* 자격 no */ "
                    update_text += "     , apl_id          /* 학번 */ "
                    update_text += "     , apl_nm          /* 성명 */ "
                    update_text += "     , license_large_cd  "
                    update_text += "     , license_large_nm  "
                    update_text += "     , license_small_cd     "
                    update_text += "     , license_small_nm     "
                    update_text += "     , license_cd      "
                    update_text += "     , license_nm    "        
                    update_text += "     , ins_id          /* 입력자id */ "
                    update_text += "     , ins_ip          /* 입력자ip */ "
                    update_text += "     , ins_dt          /* 입력일시 */ "
                    update_text += "     , ins_pgm         /* 입력프로그램id */ "
                    update_text += ") "
                    update_text += "select '"+str(mp_id)+"' AS mp_id "
                    update_text += "     , '"+str(team_apl_no)+"' apl_no         /* 지원 no */ "
                    update_text += "     , @curRank := @curRank +1 AS lc_no "
                    update_text += "     , t1.apl_id          /* 학번 */ "
                    update_text += "     , t1.apl_nm          /* 성명 */ "
                    update_text += "     , t1.license_large_cd  "
                    update_text += "     , t1.license_large_nm  "
                    update_text += "     , t1.license_small_cd     "
                    update_text += "     , t1.license_small_nm     "
                    update_text += "     , t1.license_cd      "
                    update_text += "     , t1.license_nm    "        
                    update_text += "     , '"+team_apl_id+"' ins_id         /* 입력자id */ "
                    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
                    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
                    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
                    update_text += "  FROM service20_vw_nanum_license t1      "
                    update_text += "     , (SELECT @curRank := 0) r "
                    update_text += " WHERE 1=1 "
                    update_text += "   AND t1.apl_id = '"+team_apl_id+"' "
                    print("::_FROM_service20_vw_nanum_license::")
                    print(update_text) 
                    cursor = connection.cursor()
                    query_result = cursor.execute(update_text)  

                    apl_max = int(apl_max)

                    # for i in range(0,apl_max):
                    #     anst2 = request.POST.get('que'+str(i+1), None)
                    #     ques_no = request.POST.get('ques_no'+str(i+1), None)

                    #     model_instance2 = mp_ans(
                    #         mp_id=mp_id, 
                    #         test_div='10', 
                    #         apl_no=team_apl_no,
                    #         ques_no=ques_no,
                    #         apl_id=apl_id,
                    #         apl_nm=rows.apl_nm,
                    #         sort_seq =i+1,
                    #         ans_t2='', # 내용
                    #         ans_div='2',
                    #         ins_id=team_apl_id,
                    #         ins_ip=str(client_ip),
                    #         ins_dt=datetime.datetime.today()
                    #         )
                    #     model_instance2.save()
        # 팀단위 종료


        # mp_mntr/ms_apl  -> mp_id만 조건 걸어서 count(*)
        # 해당 cnt값을 mpgm/msch -> cnt_apl

        update_text = " update service20_mpgm a "
        update_text += " SET a.cnt_apl = (select count(*) from service20_mp_mtr where mp_id = '"+mp_id+"' and status = '10') "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+mp_id+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        # -- 생성_어학(mp_mtr_fe)_FROM_vw_nanum_foreign_exam

        update_text = " insert into service20_mp_mtr_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
        update_text += "      ( mp_id          /* 멘토링 프로그램id */ "
        update_text += "      , apl_no         /* 지원 no */ "
        update_text += "      , fe_no          /* 어학점수 no */ "
        update_text += "      , apl_id         /* 학번 */ "
        update_text += "      , apl_nm         /* 성명 */ "
        update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
        update_text += "      , lang_kind_nm   /* 어학종류명 */ "
        update_text += "      , lang_cd        /* 어학상위코드 */ "
        update_text += "      , lang_nm        /* 어학상위코드명 */ "
        update_text += "      , lang_detail_cd /* 어학하위코드 */ "
        update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
        update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
        update_text += "      , frexm_nm       /* 외국어시험명 */ "
        update_text += "      , score          /* 시험점수 */ "
        update_text += "      , grade          /* 시험등급 */ "
        update_text += "      , ins_id         /* 입력자id */ "
        update_text += "      , ins_ip         /* 입력자ip */ "
        update_text += "      , ins_dt         /* 입력일시 */ "
        update_text += "      , ins_pgm        /* 입력프로그램id */ "
        update_text += " ) "
        update_text += " select '"+str(mp_id)+"' AS mp_id "
        update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "      , @curRank := @curRank +1 AS fe_no  "
        update_text += "      , t1.apl_id         /* 학번 */ "
        update_text += "      , t1.apl_nm         /* 성명 */ "
        update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
        update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
        update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
        update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
        update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
        update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
        update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
        update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
        update_text += "      , t1.score          /* 시험점수 */ "
        update_text += "      , t1.grade          /* 시험등급 */ "
        update_text += "      , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "      , NOW() ins_dt         /* 입력일시 */ "
        update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
        update_text += "      , (SELECT @curRank := 0) r "
        update_text += "  WHERE 1=1 "
        update_text += "    AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        # -- 생성_봉사(mp_mtr_sa)_FROM_vw_nanum_foreign_exam

        update_text = "insert into service20_mp_mtr_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
        update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
        update_text += "     , apl_no          /* 지원 no */ "
        update_text += "     , sa_no           /* 어학점수 no */ "
        update_text += "     , apl_id          /* 학번 */ "
        update_text += "     , apl_nm          /* 성명 */ "
        update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
        update_text += "     , nation_inout_nm /* 국내외구분명 */ "
        update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
        update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
        update_text += "     , activity_nm     /* 봉사명 */ "
        update_text += "     , manage_org_nm   /* 주관기관명 */ "
        update_text += "     , start_date      /* 시작일자 */ "
        update_text += "     , start_time      /* 시작시간 */ "
        update_text += "     , end_date        /* 종료일자 */ "
        update_text += "     , end_time        /* 종료시간 */ "
        update_text += "     , tot_time        /* 총시간 */ "
        update_text += "     , ins_id          /* 입력자id */ "
        update_text += "     , ins_ip          /* 입력자ip */ "
        update_text += "     , ins_dt          /* 입력일시 */ "
        update_text += "     , ins_pgm         /* 입력프로그램id */ "
        update_text += ") "
        update_text += "select '"+str(mp_id)+"' AS mp_id "
        update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "     , @curRank := @curRank +1 AS sa_no "
        update_text += "     , t1.apl_id          /* 학번 */ "
        update_text += "     , t1.apl_nm          /* 성명 */ "
        update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
        update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
        update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
        update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
        update_text += "     , t1.activity_nm     /* 봉사명 */ "
        update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
        update_text += "     , t1.start_date      /* 시작일자 */ "
        update_text += "     , t1.start_time      /* 시작시간 */ "
        update_text += "     , t1.end_date        /* 종료일자 */ "
        update_text += "     , t1.end_time        /* 종료시간 */ "
        update_text += "     , t1.tot_time        /* 총시간 */ "
        update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "     , NOW() ins_dt         /* 입력일시 */ "
        update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
        update_text += "     , (SELECT @curRank := 0) r "
        update_text += " WHERE 1=1 "
        update_text += "   AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    

        # query = " select b.* from service20_vw_nanum_stdt a where a.apl_id = '"+apl_id+"' "
        # cursor = connection.cursor()
        # query_result = cursor.execute(query)  
        # results_st = namedtuplefetchall(cursor)  
        # v_dept_cd = results_st[0].dept_cd
        # v_mjr_cd = results_st[0].mjr_cd


        # -- 생성_자격증(mp_mtr_lc)_FROM_service20_vw_nanum_license

        update_text = "insert into service20_mp_mtr_lc      "
        update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
        update_text += "     , apl_no          /* 지원 no */ "
        update_text += "     , lc_no           /* 자격 no */ "
        update_text += "     , apl_id          /* 학번 */ "
        update_text += "     , apl_nm          /* 성명 */ "
        update_text += "     , license_large_cd  "
        update_text += "     , license_large_nm  "
        update_text += "     , license_small_cd     "
        update_text += "     , license_small_nm     "
        update_text += "     , license_cd      "
        update_text += "     , license_nm    "        
        update_text += "     , ins_id          /* 입력자id */ "
        update_text += "     , ins_ip          /* 입력자ip */ "
        update_text += "     , ins_dt          /* 입력일시 */ "
        update_text += "     , ins_pgm         /* 입력프로그램id */ "
        update_text += ") "
        update_text += "select '"+str(mp_id)+"' AS mp_id "
        update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
        update_text += "     , @curRank := @curRank +1 AS lc_no "
        update_text += "     , t1.apl_id          /* 학번 */ "
        update_text += "     , t1.apl_nm          /* 성명 */ "
        update_text += "     , t1.license_large_cd  "
        update_text += "     , t1.license_large_nm  "
        update_text += "     , t1.license_small_cd     "
        update_text += "     , t1.license_small_nm     "
        update_text += "     , t1.license_cd      "
        update_text += "     , t1.license_nm    "        
        update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
        update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
        update_text += "     , NOW() ins_dt         /* 입력일시 */ "
        update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
        update_text += "  FROM service20_vw_nanum_license t1      "
        update_text += "     , (SELECT @curRank := 0) r "
        update_text += " WHERE 1=1 "
        update_text += "   AND t1.apl_id = '"+apl_id+"' "
        print("::_FROM_service20_vw_nanum_license::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)  

        # -- 자격증 종료

        query = " select b.* from service20_vw_nanum_stdt a, service20_dept_ast b where a.dept_cd = b.dept_cd and b.status = 'Y' and a.apl_id = '"+apl_id+"' "
        cursor = connection.cursor()
        query_result = cursor.execute(query)  
        results = namedtuplefetchall(cursor)  
        query_cnt = len(list(results))
        print("::query_cnt::")
        print(query_cnt)

        update_text = " update service20_mp_mtr set dept_appr_div = 'N' "
        update_text += " where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    

        # if query_cnt == '1':
        #     # MP_MTR.DEPT_CHR_ID(학과장 ID) = DEPT_AST.DEAN_EMP_ID
        #     # MP_MTR.DEPT_CHR_NM(학과장 명) = DEPT_AST.DEAN_EMP_NM
        #     # MP_MTR.AST_ID(조교 ID)        = DEPT_AST.AST_ID
        #     # MP_MTR.AST_NM(조교 명)        = DEPT_AST.AST_NM
        #     # MP_MTR.DEPT_APPR_DIV(학과 승인 여부) = 'N'

        #     # service20_ms_apl
        #     update_text = " update service20_mp_mtr set dept_chr_id = '"+results[0].dean_emp_id+"', dept_chr_nm = '"+results[0].dean_emp_nm+"', ast_id = '"+results[0].ast_id+"', dept_appr_div = '"+results[0].ast_nm+"', dept_appr_div = 'N' "
        #     update_text += " where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
        # elif query_cnt != '0':
        #     query2 = " select b.* from service20_vw_nanum_stdt a, service20_dept_ast b where a.dept_cd = b.dept_cd and a.mjr_cd = b.mjr_cd and b.status = 'Y' and a.apl_id = '"+apl_id+"' "
        #     cursor = connection.cursor()
        #     query_result = cursor.execute(query2)
        #     results = namedtuplefetchall(cursor)

        #     queryset = dept_ast.objects.raw(query2)
        #     for val in queryset:
        #         update_text = " update service20_mp_mtr set dept_chr_id = '"+val.dean_emp_id+"', dept_chr_nm = '"+val.dean_emp_nm+"', ast_id = '"+val.ast_id+"', dept_appr_div = '"+val.ast_nm+"', dept_appr_div = 'N' "
        #         update_text += " where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"

        # mjr_cd
        # 멘토스쿨/프로그램 지원 시 학과조교 검색 시
        # 전공까지 조건 걸어서 조회해야하는데
        # 1.학과로만 조교 찾아서 세팅
        # 2.1에서 2건이상 나오면 학과,전공 걸어서 조교 찾아서 세팅


        # queryset = dept_ast.objects.raw(query)
        # for val in queryset:
        #     # 문자전송
        #     query = " select a.* from service20_mp_mtr a where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
        #     cursor = connection.cursor()
        #     query_result = cursor.execute(query)  
        #     results_m = namedtuplefetchall(cursor)  

        #     user_id = '515440'
        #     push_chk = 'PO'
        #     # push_userid = '515440'
        #     push_userid = val.ast_id
        #     push_title = "지원서 학과장 승인 요청"
        #     push_content = results_m[0].apl_nm + " 학생 교육기부 지원서 학과장 승인 요청"
        #     tickerText = ' '
        #     push_time = '60'
        #     # cdr_id = '515440'
        #     cdr_id = results[0].ast_id
        #     sms_content = push_content
        #     sms_nb = '0515103322'
        #     client_ip = request.META['REMOTE_ADDR']
        #     data_info = {'user_id':user_id,'push_chk': push_chk,'push_userid': push_userid,'push_title': push_title,'push_content': push_content,'tickerText': tickerText,'push_time': push_time,'cdr_id': cdr_id,'sms_content': sms_content,'sms_nb': sms_nb}
        #     print("::data_info::")
        #     print(data_info)
            # with requests.Session() as s:
            #     first_page = s.post('http://msg.pusan.ac.kr/api/push.asp', data=data_info)
            #     html = first_page.text
            #     #print(html)
            #     soup = bs(html, 'html.parser')

        context = {'message': 'Ok','apl_no':str(apl_no),'team_no':str(team_no)}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def MP0101M_detail(request):    

    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)

    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
    mpgm_flag = mpgm.objects.filter(mp_id=ms_ida,status='20').exists()
    ms_apl_flag = mp_mtr.objects.filter(apl_id=ida,mp_id=ms_ida).exists()
    print(mpgm_flag)
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    print('========')
    if not created_flag:
        print('0')
        message = "Fail"
        context = {'message': message}
    else:
        if mpgm_flag == False:
            print('1')
            message = "Fail"
            context = {'message': message}
        else:
            print('2')
            message = "Ok"
            rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
            rows2 = mp_sub.objects.filter(mp_id=ms_ida)
            rows3 = mpgm.objects.filter(mp_id=ms_ida)[0]
            

            query = "select case when now() between A.apl_fr_dt and A.apl_to_dt then 'Y' else 'N' end dateAplYn "
            query += " from service20_mpgm A where mp_id = '"+ms_ida+"'"
            cursor = connection.cursor()
            query_result = cursor.execute(query)  
            results = namedtuplefetchall(cursor) 

            if query_result == 0:
                v_dateAplYn = 'N'
            else:
                v_dateAplYn = str(results[0].dateAplYn)


            for val in rows2:
                key1 = val.att_id
                #key2 = val.att_cdd


            context = {'message': message,
                        'applyYn' : applyYn,
                        'apl_nm' : rows.apl_nm,
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
                        'grad_div_cd' : rows.grad_div_cd,
                        'grad_div_nm' : rows.grad_div_nm,
                        'cllg_cd' : rows.cllg_cd,
                        'cllg_nm' : rows.cllg_nm,
                        'dept_cd' : rows.dept_cd,
                        'dept_nm' : rows.dept_nm,
                        'mjr_cd' : rows.mjr_cd,
                        'mjr_nm' : rows.mjr_nm,
                        'brth_dt' : rows.brth_dt,
                        'gen_cd' : rows.gen_cd,
                        'gen_nm' : rows.gen_nm,
                        'yr' : rows.yr,
                        'sch_yr' : rows.sch_yr,
                        'term_div' : rows.term_div,
                        'term_nm' : rows.term_nm,
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'tel_no_g' : rows.tel_no_g,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.post_no,
                        'email_addr' : rows.email_addr,
                        'bank_acct' : rows.bank_acct,
                        'bank_cd' : rows.bank_cd,
                        'bank_nm' : rows.bank_nm,
                        'bank_dpsr' : rows.bank_dpsr,
                        'pr_yr' : rows.pr_yr,
                        'pr_sch_yr' : rows.pr_sch_yr,
                        'pr_term_div' : rows.pr_term_div,
                        'score01' : rows.score01,
                        'score02' : rows.score02,
                        'score03' : rows.score03,
                        'score04' : rows.score04,
                        'score05' : rows.score05,
                        'ms_id' : rows3.mp_id,
                        'ms_name' : rows3.mp_name,
                        'dateAplYn' : v_dateAplYn,
                        'indv_div' : rows3.indv_div,
                        'mem_cnt' : rows3.mem_cnt,
                        'mem_min' : rows3.mem_min,
                        }
        

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

class MP0101M_adm_list_Serializer(serializers.ModelSerializer):
    
    mp_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    indv_div = serializers.SerializerMethodField()
    ldr_id = serializers.SerializerMethodField()
    acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')
    intv_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = mp_mtr
        #fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','statusCode','status_nm')
        fields = '__all__'

    def get_mp_name(self,obj):
        return obj.mp_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div  

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm
    def get_status(self,obj):
        return obj.status
    def get_indv_div(self,obj):
        return obj.indv_div
    def get_ldr_id(self,obj):
        return obj.ldr_id

class MP0101M_adm_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        # mpgm

        query = " select   "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, 'xx', C.status) as statusCode,  "
        query += " if(A.status = '10'  "
        query += " and now() > C.apl_to_dt, '모집완료', (select std_detl_code_nm  "
        query += " from   service20_com_cdd  " 
        query += " where  "
        query += " std_grp_code = 'MP0001'  "
        query += " and use_indc = 'y'  "
        query += " and std_detl_code = C.status)) as status_nm,  "
        query += " (select indv_div from service20_mpgm where mp_id = A.mp_id) indv_div, "

        # 팀 리더
        query += " (select ldr_id from service20_mp_team where mp_id = A.mp_id and team_id = A.team_id) ldr_id, "

        query += " C.mp_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_mp_mtr A left join service20_vw_nanum_stdt B on (A.apl_id = B.apl_id),service20_mpgm C where A.mp_id = C.mp_id and A.mp_id = '"+mp_ida+"' and A.apl_id='"+ida+"'"
        queryset = mp_mtr.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 어학
class MP0101M_adm_list_fe_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_fe
        fields = ('frexm_cd','frexm_nm','score','grade','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score

class MP0101M_adm_list_fe(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select id,  "
        query += "        frexm_cd,  "
        query += "        frexm_nm,  "
        query += "        score,  "        
        query += "        grade,  "
        query += "   fn_mp_mtr_fe_select_01('"+str(mp_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_mp_mtr_fe  "
        query += " WHERE  mp_id = '"+str(mp_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = mp_mtr_fe.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 봉사
class MP0101M_adm_list_sa_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_sa
        fields = ('mp_id','apl_no','sa_no','apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score

class MP0101M_adm_list_sa(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select a.* , "
        query += "   fn_mp_mtr_sa_select_01('"+str(mp_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_mp_mtr_sa a  "
        query += " WHERE  mp_id = '"+str(mp_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = mp_mtr_sa.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 질문2
class MP0101M_adm_quest_Serializer2(serializers.ModelSerializer):

    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    val = serializers.SerializerMethodField()
    ans_min_len = serializers.SerializerMethodField()
    ans_max_len = serializers.SerializerMethodField()
    class Meta:
        model = mp_ans
        fields = ('id','mp_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code','std_detl_code_nm','rmrk','val','ans_min_len','ans_max_len')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm    

    def get_rmrk(self,obj):
        return obj.rmrk

    def get_val(self,obj):
        return obj.val

    def get_ans_min_len(self,obj):
        return obj.ans_min_len

    def get_ans_max_len(self,obj):
        return obj.ans_max_len

# 멘토링 프로그램(관리자) - 질문
class MP0101M_adm_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_adm_quest_Serializer2
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        l_exist = mp_sub.objects.filter(mp_id=key1).exists()
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,fn_mp_sub_val_select_01(A.mp_id, 'MP0086', 'MP0112', B.std_detl_code) val,A.* from service20_mp_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.use_indc = 'Y' and B.std_grp_code in (select att_cdh from service20_mp_sub where att_id='MS0014' and mp_id = '"+str(key1)+"') and A.mp_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"' order by A.sort_seq"

        query = "select "
        query += "    B.std_detl_code, "
        query += "    B.std_detl_code_nm, "
        query += "    B.rmrk, "
        query += "    fn_mp_sub_val_select_01(A.mp_id, 'MP0086', 'MP0112', B.std_detl_code) val, "
        query += "    fn_mp_sub_att_val_select_01(A.mp_id, 'MP0086', 'MS0028', B.std_detl_code) ans_min_len, "
        query += "    fn_mp_sub_att_val_select_01(A.mp_id, 'MP0086', 'MS0029', B.std_detl_code) ans_max_len, "
        query += "    A.* "
        query += "from "
        query += "    service20_mp_ans A, "
        query += "    service20_com_cdd B "
        query += "where "
        query += "    A.ques_no = B.std_detl_code "
        query += "    and B.use_indc = 'Y' "
        query += "    and B.std_grp_code in ( "
        query += "        select att_cdh "
        query += "    from "
        query += "        service20_mp_sub "
        query += "    where "
        query += "        att_id = 'MS0014' "
        query += "        and mp_id = '"+str(key1)+"') "
        query += "    and A.mp_id = '"+str(key1)+"' "
        query += "    and apl_id = '"+str(l_user_id)+"' "
        query += " order by A.sort_seq"
    

        queryset = mp_ans.objects.raw(query)

        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 수락
@csrf_exempt
def MP0101M_adm_acpt_save(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_mp_mtr a "
    update_text += " SET a.acpt_dt = NOW() "
    update_text += " , a.acpt_div = 'Y' "
    update_text += " , a.acpt_cncl_rsn = null "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 멘토링 프로그램 수락취소
@csrf_exempt
def MP0101M_adm_acpt_cancle(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_mp_mtr a "
    update_text += " SET a.acpt_dt = null "
    update_text += " , a.acpt_div = 'N' "
    update_text += " , a.acpt_cncl_rsn = '"+acpt_cncl_rsn+"' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램 update
@csrf_exempt
def MP0101M_adm_update(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    team_no = request.POST.get('team_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    maxRow = request.POST.get('maxRow', 0)
    maxTeamRow = request.POST.get('maxTeamRow', 0)
    client_ip = request.META['REMOTE_ADDR']

    apl_max = int(maxRow)
    apl_team_max = int(maxTeamRow)
    

    # update_text = " update service20_mp_mtr a "
    # update_text += " SET a.status = '10' "
    # update_text += " WHERE 1=1 "
    # update_text += " AND a.mp_id = '"+str(mp_id)+"' "
    # update_text += " AND a.apl_id = '"+str(apl_id)+"' "
    # cursor = connection.cursor()
    # query_result = cursor.execute(update_text)

    update_text = " update service20_mp_mtr a,service20_vw_nanum_stdt b "
    update_text += " SET a.status = '10' "
    update_text += " , a.score1 = b.score01 "
    update_text += " , a.score2 = b.score02 "
    update_text += " , a.score3 = b.score03 "
    update_text += " , a.score4 = b.score04 "
    update_text += " , a.score5 = b.score05 "
    update_text += " , a.score6 = b.score06 "
    update_text += " , a.cmp_term = b.cmp_term "
    update_text += " , a.h_addr = b.h_addr "
    update_text += " , a.email_addr = b.email_addr "
    update_text += " , a.tel_no_g = b.tel_no_g "
    update_text += " , a.tel_no = b.tel_no "
    update_text += " , a.bank_acct = b.bank_acct "
    update_text += " , a.bank_cd = b.bank_cd "
    update_text += " , a.bank_nm = b.bank_nm "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+str(mp_id)+"' "
    update_text += " AND a.apl_id = '"+str(apl_id)+"' "
    update_text += " AND a.apl_id = b.apl_id "
    # update_text += " AND ifnull(a.dept_appr_div,'N') = 'N' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)


    # 팀별
    query = "select indv_div "
    query += " from service20_mpgm A where mp_id = '"+mp_id+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(query)  
    results = namedtuplefetchall(cursor) 
    v_indv_div = str(results[0].indv_div)

    if v_indv_div == "T":
        update_text = " update service20_mp_mtr a "
        update_text += " SET status = '10' "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+mp_id+"' "
        update_text += " AND a.team_id in ( select team_id from service20_mp_mtr as sub_a where sub_a.mp_id = '"+mp_id+"' and sub_a.apl_no = '"+apl_no+"' ) "        
    # 팀별 

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)
        ans_t2 = request.POST.get('ans_t2_'+str(i+1), None)

        # update_text = " update service20_mp_ans a "
        # update_text += ' SET a.ans_t2 = " '+str(ans_t2)+' " ' 
        # update_text += " WHERE 1=1 "
        # update_text += " AND a.mp_id = '"+str(mp_id)+"' "
        # update_text += " AND a.apl_no = '"+str(apl_no)+"' "
        # update_text += " AND a.ques_no = '"+str(ques_no)+"' "
        
        # cursor = connection.cursor()
        # query_result = cursor.execute(update_text)

        mp_ans.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),ques_no=str(ques_no)).update(ans_t2=str(ans_t2))


    for i in range(0,apl_team_max):
        anst2 = request.POST.get('que_team'+str(i+1), None)
        ques_no = request.POST.get('ques_no_team'+str(i+1), None)
        ans_t2 = request.POST.get('team_ans_t2_'+str(i+1), None)

        # update_text = " update service20_mp_ans a "
        # update_text += ' SET a.ans_t2 = " '+str(ans_t2)+' " ' 
        # update_text += " WHERE 1=1 "
        # update_text += " AND a.mp_id = '"+str(mp_id)+"' "
        # update_text += " AND a.apl_no = '"+str(apl_no)+"' "
        # update_text += " AND a.ques_no = '"+str(ques_no)+"' "
        
        # cursor = connection.cursor()
        # query_result = cursor.execute(update_text)

        mp_team_ans.objects.filter(mp_id=str(mp_id),team_no=str(team_no),ques_no=str(ques_no)).update(ans_t2=str(ans_t2))


    delete_text = "delete from service20_mp_mtr_fe where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)    

    delete_text = "delete from service20_mp_mtr_sa where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)

    delete_text = "delete from service20_mp_mtr_lc where mp_id = '"+str(mp_id)+"' and apl_no = '"+str(apl_no)+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(delete_text)

    # -- 생성_어학(mp_mtr_fe)_FROM_vw_nanum_foreign_exam

    update_text = " insert into service20_mp_mtr_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
    update_text += "      ( mp_id          /* 멘토링 프로그램id */ "
    update_text += "      , apl_no         /* 지원 no */ "
    update_text += "      , fe_no          /* 어학점수 no */ "
    update_text += "      , apl_id         /* 학번 */ "
    update_text += "      , apl_nm         /* 성명 */ "
    update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
    update_text += "      , lang_kind_nm   /* 어학종류명 */ "
    update_text += "      , lang_cd        /* 어학상위코드 */ "
    update_text += "      , lang_nm        /* 어학상위코드명 */ "
    update_text += "      , lang_detail_cd /* 어학하위코드 */ "
    update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
    update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
    update_text += "      , frexm_nm       /* 외국어시험명 */ "
    update_text += "      , score          /* 시험점수 */ "
    update_text += "      , grade          /* 시험등급 */ "
    update_text += "      , ins_id         /* 입력자id */ "
    update_text += "      , ins_ip         /* 입력자ip */ "
    update_text += "      , ins_dt         /* 입력일시 */ "
    update_text += "      , ins_pgm        /* 입력프로그램id */ "
    update_text += " ) "
    update_text += " select '"+str(mp_id)+"' AS mp_id "
    update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "      , @curRank := @curRank +1 AS fe_no  "
    update_text += "      , t1.apl_id         /* 학번 */ "
    update_text += "      , t1.apl_nm         /* 성명 */ "
    update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
    update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
    update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
    update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
    update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
    update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
    update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
    update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
    update_text += "      , t1.score          /* 시험점수 */ "
    update_text += "      , t1.grade          /* 시험등급 */ "
    update_text += "      , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "      , NOW() ins_dt         /* 입력일시 */ "
    update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
    update_text += "      , (SELECT @curRank := 0) r "
    update_text += "  WHERE 1=1 "
    update_text += "    AND t1.apl_id = '"+str(apl_id)+"' "
    print("::_FROM_vw_nanum_foreign_exam::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)    


    # -- 생성_봉사(mp_mtr_sa)_FROM_vw_nanum_foreign_exam

    update_text = "insert into service20_mp_mtr_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
    update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
    update_text += "     , apl_no          /* 지원 no */ "
    update_text += "     , sa_no           /* 어학점수 no */ "
    update_text += "     , apl_id          /* 학번 */ "
    update_text += "     , apl_nm          /* 성명 */ "
    update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
    update_text += "     , nation_inout_nm /* 국내외구분명 */ "
    update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
    update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
    update_text += "     , activity_nm     /* 봉사명 */ "
    update_text += "     , manage_org_nm   /* 주관기관명 */ "
    update_text += "     , start_date      /* 시작일자 */ "
    update_text += "     , start_time      /* 시작시간 */ "
    update_text += "     , end_date        /* 종료일자 */ "
    update_text += "     , end_time        /* 종료시간 */ "
    update_text += "     , tot_time        /* 총시간 */ "
    update_text += "     , ins_id          /* 입력자id */ "
    update_text += "     , ins_ip          /* 입력자ip */ "
    update_text += "     , ins_dt          /* 입력일시 */ "
    update_text += "     , ins_pgm         /* 입력프로그램id */ "
    update_text += ") "
    update_text += "select '"+str(mp_id)+"' AS mp_id "
    update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "     , @curRank := @curRank +1 AS sa_no "
    update_text += "     , t1.apl_id          /* 학번 */ "
    update_text += "     , t1.apl_nm          /* 성명 */ "
    update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
    update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
    update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
    update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
    update_text += "     , t1.activity_nm     /* 봉사명 */ "
    update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
    update_text += "     , t1.start_date      /* 시작일자 */ "
    update_text += "     , t1.start_time      /* 시작시간 */ "
    update_text += "     , t1.end_date        /* 종료일자 */ "
    update_text += "     , t1.end_time        /* 종료시간 */ "
    update_text += "     , t1.tot_time        /* 총시간 */ "
    update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
    update_text += "     , (SELECT @curRank := 0) r "
    update_text += " WHERE 1=1 "
    update_text += "   AND t1.apl_id = '"+str(apl_id)+"' "
    print("::_FROM_vw_nanum_foreign_exam::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text) 

    # update_text = " update service20_mp_mtr a,service20_vw_nanum_foreign_exam b    /* 프로그램 지원자(멘토) 어학 리스트 */ set "
    # update_text += "      a.score1 = '"++"' "
    # update_text += "  WHERE a.apl_id = b.apl_id "
    # update_text += "    AND a.apl_id = '"+str(apl_id)+"' "
    # update_text += "    AND a.mp_id = '"+mp_id+"' "
    # print("::_FROM_vw_nanum_foreign_exam::")
    # print(update_text) 
    # cursor = connection.cursor()
    # query_result = cursor.execute(update_text)    

    # -- 생성_자격증(mp_mtr_lc)_FROM_service20_vw_nanum_license

    update_text = "insert into service20_mp_mtr_lc      "
    update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
    update_text += "     , apl_no          /* 지원 no */ "
    update_text += "     , lc_no           /* 자격 no */ "
    update_text += "     , apl_id          /* 학번 */ "
    update_text += "     , apl_nm          /* 성명 */ "
    update_text += "     , license_large_cd  "
    update_text += "     , license_large_nm  "
    update_text += "     , license_small_cd     "
    update_text += "     , license_small_nm     "
    update_text += "     , license_cd      "
    update_text += "     , license_nm    "        
    update_text += "     , ins_id          /* 입력자id */ "
    update_text += "     , ins_ip          /* 입력자ip */ "
    update_text += "     , ins_dt          /* 입력일시 */ "
    update_text += "     , ins_pgm         /* 입력프로그램id */ "
    update_text += ") "
    update_text += "select '"+str(mp_id)+"' AS mp_id "
    update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
    update_text += "     , @curRank := @curRank +1 AS lc_no "
    update_text += "     , t1.apl_id          /* 학번 */ "
    update_text += "     , t1.apl_nm          /* 성명 */ "
    update_text += "     , t1.license_large_cd  "
    update_text += "     , t1.license_large_nm  "
    update_text += "     , t1.license_small_cd     "
    update_text += "     , t1.license_small_nm     "
    update_text += "     , t1.license_cd      "
    update_text += "     , t1.license_nm    "        
    update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ "
    update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
    update_text += "     , NOW() ins_dt         /* 입력일시 */ "
    update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
    update_text += "  FROM service20_vw_nanum_license t1      "
    update_text += "     , (SELECT @curRank := 0) r "
    update_text += " WHERE 1=1 "
    update_text += "   AND t1.apl_id = '"+apl_id+"' "
    print("::_FROM_service20_vw_nanum_license::")
    print(update_text) 
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)  

    # -- 자격증 종료
    
    update_text = " update service20_mpgm a "
    update_text += " SET a.cnt_apl = (select count(*) from service20_mp_mtr where mp_id = '"+mp_id+"' and status = '10') "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text) 



        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 


# 멘토링 프로그램 cancle
@csrf_exempt
def MP0101M_adm_cancle(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")


    update_text = " update service20_mp_mtr a "
    update_text += " SET status = '19' "
    update_text += " , doc_cncl_dt = now() "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)


    # 팀별
    query = "select indv_div "
    query += " from service20_mpgm A where mp_id = '"+mp_id+"'"
    cursor = connection.cursor()
    query_result = cursor.execute(query)  
    results = namedtuplefetchall(cursor) 
    v_indv_div = str(results[0].indv_div)

    if v_indv_div == "T":
        update_text = " update service20_mp_mtr a "
        update_text += " SET status = '19' "
        update_text += " , doc_cncl_dt = now() "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+mp_id+"' "
        update_text += " AND a.team_id in ( select team_id from service20_mp_mtr as sub_a where sub_a.mp_id = '"+mp_id+"' and sub_a.apl_no = '"+apl_no+"' ) "        
    # 팀별 


    update_text = " update service20_mpgm a "
    update_text += " SET a.cnt_apl = (select count(*) from service20_mp_mtr where mp_id = '"+mp_id+"' and status = '10') "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text) 


    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})            

class MP0101M_report_list_Serializer(serializers.ModelSerializer):
    
    mp_name = serializers.SerializerMethodField()
    statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    mpgm_yr = serializers.SerializerMethodField()
    mnt_term = serializers.SerializerMethodField()
    mnt_term_nm = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    pr_term_cnt = serializers.SerializerMethodField()
    dept_appr_dt2  = serializers.SerializerMethodField()
    ins_dt2  = serializers.SerializerMethodField()
    acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')
    ins_dt = serializers.DateTimeField(format='%Y년 %m월 %d일')


    class Meta:
        model = mp_mtr
        #fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','statusNm','statusCode','id_pic','mpgm_yr','mnt_term','mnt_term_nm','pr_yr','pr_sch_yr','pr_term_div','pr_term_cnt','dept_appr_dt2','dept_chr_nm')
        fields = '__all__'

    def get_mp_name(self,obj):
        return obj.mp_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div  

    def get_pr_term_cnt(self,obj):
        return obj.pr_term_cnt      
    def get_dept_appr_dt2(self,obj):
        return obj.dept_appr_dt2      
    def get_ins_dt2(self,obj):
        return obj.ins_dt2      

    def get_statusNm(self,obj):
        now = datetime.datetime.today()
        mpgm_query = mpgm.objects.all()
        mpgm_query = mpgm_query.filter(mp_id=obj.mp_id)[0]

        if mpgm_query.apl_fr_dt == None:
            return '개설중'
        elif now < mpgm_query.apl_fr_dt:
            return '개설중'
        elif mpgm_query.apl_fr_dt <= now < mpgm_query.apl_to_dt:
            return '모집중'
        elif now > mpgm_query.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'

    def get_statusCode(self,obj):
        now = datetime.datetime.today()
        mpgm_query = mpgm.objects.all()
        mpgm_query = mpgm_query.filter(mp_id=obj.mp_id)[0]
        if mpgm_query.apl_fr_dt == None:
            # 개설중
            return '1'
        elif now < mpgm_query.apl_fr_dt:
            # 개설중
            return '1'
        elif mpgm_query.apl_fr_dt <= now < mpgm_query.apl_to_dt:
            # 모집중
            return '2'
        elif now > mpgm_query.apl_to_dt:
            # 모집완료
            return '3'  
        else:
            # 개설중
            return '1'      
    def get_mpgm_yr(self,obj):
        return obj.mpgm_yr
    def get_mnt_term(self,obj):
        return obj.mnt_term
    def get_mnt_term_nm(self,obj):
        return obj.mnt_term_nm

class MP0101M_report_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_report_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        # mpgm
        # query = "select C.yr as mpgm_yr,C.mnt_term,C.mp_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_mp_mtr A,service20_vw_nanum_stdt B,service20_mpgm C where A.apl_id=B.apl_id and A.mp_id = C.mp_id and A.mp_id = '"+str(mp_ida)+"' and A.apl_id='"+str(ida)+"'"

        query = "select c.yr AS mpgm_yr,  "
        query += "       c.mnt_term,  "
        query += "       c.mp_name,  "
        query += "       b.pr_yr,  "
        query += "       b.pr_sch_yr,  "
        query += "       b.pr_term_div, "
        # query += "       cast( ((b.pr_sch_yr-1)*2)+(substr(b.pr_term_div,1,1)*1) as UNSIGNED) pr_term_cnt, "
        query += "       a.cmp_term AS pr_term_cnt,"
        query += "       d.std_detl_code_nm AS mnt_term_nm,  "
        query += "       DATE_FORMAT(a.dept_appr_dt,'%%Y년  %%m월  %%d일') dept_appr_dt2,  "
        query += "       DATE_FORMAT(a.ins_dt,'%%Y년  %%m월  %%d일') ins_dt2,  "
        # dept_appr_dt
        query += "       a.*  "
        query += "FROM   service20_mp_mtr a  " 
        query += "    left join   service20_vw_nanum_stdt b on (a.apl_id = b.apl_id), "
        query += "       service20_mpgm c,  "
        query += "       service20_com_cdd d "
        query += " WHERE a.mp_id = c.mp_id  "
        query += "   AND a.mp_id = '"+str(mp_ida)+"'  "
        query += "   AND a.apl_id = '"+str(ida)+"' "
        query += "   AND d.std_grp_code  = 'MS0022' "
        query += "   AND d.std_detl_code = c.mnt_term "


        queryset = mp_mtr.objects.raw(query)
        
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (카운트) ###################################################
class MP0101M_service_cnt_Serializer(serializers.ModelSerializer):
    
    std_grp_code_nm = serializers.SerializerMethodField()
    chc_tp = serializers.SerializerMethodField()
    chc_cnt = serializers.SerializerMethodField()
    chc_unit = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_grp_code_nm(self,obj):
        return obj.std_grp_code_nm
    def get_chc_tp(self,obj):
        return obj.chc_tp
    def get_chc_cnt(self,obj):
        return obj.chc_cnt
    def get_chc_unit(self,obj):
        return obj.chc_unit


class MP0101M_service_cnt(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_cnt_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = "/* 1.선택형 질문 리스트 */"
        query += " select t1.id, t1.att_cdh "
        query += "     , t2.std_grp_code_nm "
        query += "     , max(case t1.att_cdd when '1' then t1.att_val end) as chc_tp   /* 선택 유형 : 1 콤보, 2 라디오, 3 체크 */ "
        query += "     , max(case t1.att_cdd when '2' then t1.att_val end) as chc_cnt  /* 선택 가능 갯수                       */ "
        query += "     , max(case t1.att_cdd when '2' then ifnull(t1.att_unit, '') end) as chc_unit  /* 지망, 비지망 구분       */ "
        query += "  from service20_mp_sub t1 "
        query += "  left join service20_com_cdh t2 on (t2.std_grp_code = t1.att_cdh) "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "'"
        query += "   and t1.att_id  = 'MP0089' /* 선택형 질문             */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " group by t1.att_cdh "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램 - 해외봉사활동 프로그램 (희망도시 콤보) ###################################################
class MP0101M_service_combo_city_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_combo_city(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_combo_city_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = "/* 2.질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code  /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "' "
        query += "   and t1.att_id  = 'MP0090' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = 'MP0092' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (분야 콤보) ###################################################
class MP0101M_service_combo_field_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_combo_field(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_combo_field_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', None)

        query = "/* 질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + l_mp_id + "' "
        query += "   and t1.att_id  = 'MP0090' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = 'MP0093' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램 - 해외봉사활동 프로그램 (업로드 카운트) ###################################################
class MP0101M_service_upload_cnt_Serializer(serializers.ModelSerializer):

    val = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_val(self,obj):
        return obj.val

class MP0101M_service_upload_cnt(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_upload_cnt_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        # query = " select t1.id, t1.mp_id    /* 멘토링프로그램id     */ "
        # query += "     , t1.att_cdh  /* 첨부파일 code header */ "
        # query += "     , t1.att_cdd  /* 첨부파일 code        */ "
        # query += "     , t1.att_val  /* 첨부파일 종류        */ "
        # query += "  from service20_mp_sub t1 "
        # query += " where mp_id   ='" + l_mp_id + "'  "
        # query += "   and att_cdh = 'MP0086' "
        # query += "   and use_yn  = 'Y' "
        # query += " order by sort_seq; "


        query = "     select t1.id, t1.mp_id    /* 멘토링프로그램id     */ "
        query += "           , t1.att_cdh  /* 첨부파일 code header */ "
        query += "           , t1.att_cdd  /* 첨부파일 code        */ "
        query += "           , t1.att_val  /* 첨부파일 종류        */ "
        query += "           , fn_mp_sub_val_select_01(t1.mp_id, t1.att_id, 'MP0112', t1.att_cdd) val"
        query += "        FROM service20_mp_sub t1"
        query += "        LEFT JOIN service20_com_cdd t3 ON (t3.std_grp_code  = t1.att_cdh"
        query += "                                       AND t3.std_detl_code = t1.att_cdd)"
        query += "       WHERE t1.mp_id   = '" + l_mp_id + "'"
        query += "         AND t1.att_id  = 'MP0086'"
        query += "         AND t1.att_cdh = 'MP0086'"
        query += "       ORDER BY t1.sort_seq"

        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기) ###################################################
class MP0101M_service_apl_no_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mtr
        fields = '__all__'

class MP0101M_service_apl_no(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_service_apl_no_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select id, mp_id, max(apl_no) as apl_no from service20_mp_mtr where mp_id = '" + l_mp_id + "'"

        print(query)
        queryset = mp_mtr.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
        
# 멘토링 프로그램 - 해외봉사활동 프로그램 (insert) ###################################################
@csrf_exempt
def MP0101M_service_insert(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_apl_no = request.POST.get('apl_no', "")
    l_length = request.POST.get('over_service_length', "")
    l_att_cdd = list()
    l_att_cdh = list()
    l_chc_tp = list()
    l_seq = list()

    print("apl_no====" + l_apl_no)
    print("length==" + l_length)

    com_cnt = 0
    sel_cnt = 0
    chk_cnt = 0
    for i in range(0,int(l_length)):
        # l_att_cdd.append(request.POST.get('select_'+str(i), ""))
        l_att_cdh.append(request.POST.get('att_cdh'+str(i), ""))
        l_chc_tp.append(request.POST.get('chc_tp'+str(i), ""))
        l_seq.append(request.POST.get('seq'+str(i), ""))

        if l_chc_tp[i] == '1':
            l_att_cdd.append(request.POST.get('service_combo'+str(com_cnt), ""))
            com_cnt = com_cnt + 1
        elif l_chc_tp[i] == '3':
            l_att_cdd.append(request.POST.get('service_chkbox'+str(chk_cnt), ""))
            chk_cnt = chk_cnt + 1
        else:
            l_att_cdd.append(request.POST.get('service_select'+str(sel_cnt), ""))
            sel_cnt = sel_cnt + 1
    
        print("l_att_cdd===" + l_att_cdd[i])
        print("l_att_cdh===" + l_att_cdh[i])
        print("l_chc_tp===" + l_chc_tp[i])
        print("l_seq===" + l_seq[i])

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    

    # delete
    query = " delete FROM service20_mp_chc WHERE mp_id = '" + l_mp_id + "' AND apl_no = '" + l_apl_no + "'"
    cursor = connection.cursor()
    cursor.execute(query) 

    for i in range(0,int(l_length)):
        query = " insert "
        query += "    into "
        query += "        service20_mp_chc(mp_id "
        query += "        , apl_no "
        query += "        , chc_no "
        query += "        , att_id "
        query += "        , att_cdh "
        query += "        , att_cdd "
        query += "        , chc_tp "
        query += "        , chc_val "
        query += "        , chc_seq "
        query += "        , ques_no "
        query += "        , ins_id "
        query += "        , ins_ip "
        query += "        , ins_dt "
        query += "        , ins_pgm "
        query += "        , upd_id "
        query += "        , upd_ip "
        query += "        , upd_dt "
        query += "        , upd_pgm) "
        query += "    values ( "
        query += "    '" + str(l_mp_id) + "'"
        query += "    , '" + str(l_apl_no) + "'"
        query += "    , (select ifnull(max(t1.chc_no), 0) + 1 from service20_mp_chc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "')"
        query += "    , 'MP0090' "
        query += "    , '" + str(l_att_cdh[i]) + "'"
        query += "    , '" + str(l_att_cdd[i]) + "'"
        query += "    , '" + str(l_chc_tp[i]) + "'"
        query += "    , (select t2.att_val  /* 선택형 답변 가능수      */ "
        query += "          from service20_mp_sub t2 "
        query += "         where t2.mp_id   = '" + str(l_mp_id) + "'"
        query += "           and t2.att_id  = 'MP0090' /* 선택형 질문             */ "
        query += "           and t2.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
        query += "           and t2.att_cdd = '" + str(l_att_cdd[i]) + "'"
        query += "           and t2.use_yn  = 'Y') "
        query += "    , '" + str(l_seq[i]) + "' "
        query += "    , (select t3.sort_seq  /* 답변 NO      */ "
        query += "          from service20_mp_sub t3 "
        query += "         where t3.mp_id   = '" + str(l_mp_id) + "'"
        query += "           and t3.att_id  = 'MP0090' /* 선택형 질문             */ "
        query += "           and t3.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
        query += "           and t3.att_cdd = '" + str(l_att_cdd[i]) + "'"
        query += "           and t3.use_yn  = 'Y') "
        query += "    , '" + str(ins_id) + "'"
        query += "    , '" + str(client_ip) + "'"
        query += "    , now() "
        query += "    , '" + str(ins_pgm) + "'"
        query += "    , '" + str(upd_id) + "'"
        query += "    , '" + str(client_ip) + "'"
        query += "    , now() "
        query += "    , '" + str(upd_pgm) + "'"
        query += " ) "

        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(query) 

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(insert) ###################################################
@csrf_exempt
def MP0101M_upload(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/MP0101M/'
    UPLOAD_DIR = '/NANUM/www/img/atc/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_mp_id = request.POST.get("mp_id")
        l_apl_no = request.POST.get("apl_no")
        l_apl_id = request.POST.get("apl_id") 
        l_length = request.POST.get("upload_length")
        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")

        client_ip = request.META['REMOTE_ADDR']

        l_att_cdd = list()
        l_att_cdh = list()
        l_service_upload_text = list()
        l_service_upload = list()
        l_upload_no = list()


        for i in range(0,int(l_length)):
            l_att_cdd.append(request.POST.get('att_cdd_up'+str(i), ""))
            l_service_upload_text.append(request.POST.get('service_upload_text'+str(i), ""))
            l_service_upload.append(request.POST.get('service_upload'+str(i), ""))
            l_att_cdh.append(request.POST.get('att_cdh_up'+str(i), ""))
            l_upload_no.append(request.POST.get('upload_no'+str(i), ""))

            print("l_upload=====" + str(l_upload_no[i]) + "    i=====" + str(i))

            if(str(l_upload_no[i]) == str(i)):
                file = request.FILES['service_upload' + str(i)]
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_apl_id) + str(l_att_cdh[i]) + str(l_att_cdd[i]) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
                
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/atc/"+ str(n_filename)

                query = " insert into service20_mp_mtr_atc ( "
                query += "    mp_id "
                query += "    , apl_no "
                query += "    , atc_seq "
                query += "    , atc_cdh "
                query += "    , atc_cdd "
                query += "    , atc_nm "
                query += "    , atc_file_nm "
                query += "    , atc_file_url "
                query += "    , ins_id "
                query += "    , ins_ip "
                query += "    , ins_dt "
                query += "    , ins_pgm "
                query += "    , upd_id "
                query += "    , upd_ip "
                query += "    , upd_dt "
                query += "    , upd_pgm "
                query += " ) "
                query += " values ( "
                query += "    '" + str(l_mp_id) + "'"
                query += "    , '" + str(l_apl_no) + "'"
                query += "    , (select ifnull(max(t1.atc_seq), 0) + 1 from service20_mp_mtr_atc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "') "
                query += "    , '" + str(l_att_cdh[i]) + "'"
                query += "    , '" + str(l_att_cdd[i]) + "'"
                query += "    , (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "')"
                query += "    , '" + str(filename) + "'"
                query += "    , '" + str(fullFile) + "'"
                query += "    , '" + str(ins_id) + "'"
                query += "    , '" + str(client_ip) + "'"
                query += "    , now() "
                query += "    , '" + str(ins_pgm) + "'"
                query += "    , '" + str(upd_id) + "'"
                query += "    , '" + str(client_ip) + "'"
                query += "    , now() "
                query += "    , '" + str(upd_pgm) + "'"
                query += " ) "

                cursor.execute(query)


        return HttpResponse('File Uploaded')

# 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (데이터) ###################################################
class MP0101M_admin_service_chc_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_chc
        fields = '__all__'

class MP0101M_admin_service_chc(generics.ListAPIView):
    queryset = mp_chc.objects.all()
    serializer_class = MP0101M_admin_service_chc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        query = " select id as id "
        query += "     , mp_id as mp_id "
        query += "     , apl_no as apl_no "
        query += "     , chc_no as chc_no "
        query += "     , att_id as att_id "
        query += "     , att_cdh as att_cdh "
        query += "     , att_cdd as att_cdd "
        query += "     , chc_tp as chc_tp "
        query += "     , chc_val as chc_val "
        query += "     , chc_seq as chc_seq "
        query += "     , ques_no as ques_no "
        query += "  from service20_mp_chc "
        query += " where mp_id = '" + l_mp_id + "' "
        query += "   and apl_no = '"+ l_apl_no + "'"
        query += " order by chc_no, chc_seq "

        queryset = mp_chc.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (첨부데이터) ###################################################
class MP0101M_admin_service_atc_Serializer(serializers.ModelSerializer):

    val = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_atc
        fields = '__all__'

    def get_val(self,obj):
        return obj.val 

class MP0101M_admin_service_atc(generics.ListAPIView):
    queryset = mp_mtr_atc.objects.all()
    serializer_class = MP0101M_admin_service_atc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        query = " select id as id "
        query += "     , mp_id as mp_id "
        query += "     , apl_no as apl_no "
        query += "     , atc_seq as atc_seq "
        query += "     , atc_cdh as atc_cdh "
        query += "     , atc_cdd as atc_cdd "
        query += "     , atc_nm as atc_nm "
        query += "     , atc_file_nm as atc_file_nm "
        query += "     , atc_file_url as atc_file_url "
        query += "     , fn_mp_sub_val_select_01(mp_id, atc_cdh, 'MP0112', atc_cdd) val"
        query += "  from service20_mp_mtr_atc "
        query += " where mp_id = '" + l_mp_id + "' "
        query += "   and apl_no = '" + l_apl_no + "' "
        query += "   and atc_cdh = 'MP0086' "
        query += " order by atc_seq "


        queryset = mp_mtr_atc.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (update) ###################################################
@csrf_exempt
def MP0101M_service_update(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_apl_no = request.POST.get('apl_no', "")
    l_length = request.POST.get('over_service_length', "")
    l_att_cdd = list()
    l_att_cdh = list()
    l_chc_tp = list()
    l_chc_no = list()
    l_seq = list()

    print("apl_no====" + l_apl_no)
    print("length==" + l_length)
    com_cnt = 0
    sel_cnt = 0
    chk_cnt = 0
    for i in range(0,int(l_length)):
        # l_att_cdd.append(request.POST.get('select_'+str(i), ""))
        l_att_cdh.append(request.POST.get('att_cdh'+str(i), ""))
        l_chc_tp.append(request.POST.get('chc_tp'+str(i), ""))
        l_chc_no.append(request.POST.get('chc_no'+str(i), ""))
        l_seq.append(request.POST.get('seq'+str(i), ""))

        if l_chc_tp[i] == '1':
            l_att_cdd.append(request.POST.get('service_combo'+str(com_cnt), ""))
            com_cnt = com_cnt + 1
        elif l_chc_tp[i] == '3':
            l_att_cdd.append(request.POST.get('service_chkbox'+str(chk_cnt), ""))
            chk_cnt = chk_cnt + 1
        else:
            l_att_cdd.append(request.POST.get('service_select'+str(sel_cnt), ""))
            sel_cnt = sel_cnt + 1
    
        print("l_att_cdd===" + l_att_cdd[i])
        print("l_att_cdh===" + l_att_cdh[i])
        print("l_chc_tp===" + l_chc_tp[i])
        print("l_seq===" + l_seq[i])
        print("l_chc_no===" + l_chc_no[i])

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    
    query = " SELECT count(0) as up_cnt FROM service20_mp_chc WHERE mp_id = '" + l_mp_id + "' AND apl_no = '" + l_apl_no + "'"
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    up_cnt = int(results[0].up_cnt)

    # 저장된 선택사항과 mp_sub에 관리되는 선택사항의 개수가 일치할 때는 update
    if l_length == up_cnt:
        # update
        for i in range(0,int(l_length)):
            query = "  update service20_mp_chc "
            query += "     set att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "       , chc_val = (select t1.att_val  "
            query += "                      from service20_mp_sub t1 "
            query += "                     where t1.mp_id = '" + str(l_mp_id) + "' "
            query += "                       and t1.att_id = 'MP0090' "
            query += "                       and t1.att_cdh = '" + str(l_att_cdh[i]) + "' "
            query += "                       and t1.att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "                       and t1.use_yn = 'Y') "
            query += "       , chc_seq = '" + l_seq[i] + "' "
            query += "       , ques_no = (select t2.sort_seq  "
            query += "                      from service20_mp_sub t2 "
            query += "                     where t2.mp_id = '" + str(l_mp_id) + "' "
            query += "                       and t2.att_id = 'MP0090' "
            query += "                       and t2.att_cdh = '" + str(l_att_cdh[i]) + "' "
            query += "                       and t2.att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "                       and t2.use_yn = 'Y') "
            query += "       , upd_id = '" + str(upd_id) + "' "
            query += "       , upd_ip = '" + str(client_ip) + "' "
            query += "       , upd_dt = now() "
            query += "       , upd_pgm = '" + str(upd_pgm) + "' "
            query += "   where mp_id = '" + str(l_mp_id) + "' "
            query += "     and apl_no = '" + str(l_apl_no) + "' "
            query += "     and chc_no = '" + str(l_chc_no[i]) + "' "
            
            print(query)
            cursor = connection.cursor()
            query_result = cursor.execute(query)
    # 저장된 선택사항과 mp_sub에 관리되는 선택사항의 개수가 일치하지 않을 때는 기존꺼 전체 0delete 후 전체 isnert
    else:
        # delete
        query = " delete FROM service20_mp_chc WHERE mp_id = '" + l_mp_id + "' AND apl_no = '" + l_apl_no + "'"
        cursor = connection.cursor()
        cursor.execute(query)    

        # insert
        for i in range(0,int(l_length)):
            query = " insert "
            query += "    into "
            query += "        service20_mp_chc(mp_id "
            query += "        , apl_no "
            query += "        , chc_no "
            query += "        , att_id "
            query += "        , att_cdh "
            query += "        , att_cdd "
            query += "        , chc_tp "
            query += "        , chc_val "
            query += "        , chc_seq "
            query += "        , ques_no "
            query += "        , ins_id "
            query += "        , ins_ip "
            query += "        , ins_dt "
            query += "        , ins_pgm "
            query += "        , upd_id "
            query += "        , upd_ip "
            query += "        , upd_dt "
            query += "        , upd_pgm) "
            query += "    values ( "
            query += "    '" + str(l_mp_id) + "'"
            query += "    , '" + str(l_apl_no) + "'"
            query += "    , (select ifnull(max(t1.chc_no), 0) + 1 from service20_mp_chc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "')"
            query += "    , 'MP0090' "
            query += "    , '" + str(l_att_cdh[i]) + "'"
            query += "    , '" + str(l_att_cdd[i]) + "'"
            query += "    , '" + str(l_chc_tp[i]) + "'"
            query += "    , (select t2.att_val  /* 선택형 답변 가능수      */ "
            query += "          from service20_mp_sub t2 "
            query += "         where t2.mp_id   = '" + str(l_mp_id) + "'"
            query += "           and t2.att_id  = 'MP0090' /* 선택형 질문             */ "
            query += "           and t2.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
            query += "           and t2.att_cdd = '" + str(l_att_cdd[i]) + "'"
            query += "           and t2.use_yn  = 'Y') "
            query += "    , '" + str(l_seq[i]) + "' "
            query += "    , (select t3.sort_seq  /* 답변 NO      */ "
            query += "          from service20_mp_sub t3 "
            query += "         where t3.mp_id   = '" + str(l_mp_id) + "'"
            query += "           and t3.att_id  = 'MP0090' /* 선택형 질문             */ "
            query += "           and t3.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
            query += "           and t3.att_cdd = '" + str(l_att_cdd[i]) + "'"
            query += "           and t3.use_yn  = 'Y') "
            query += "    , '" + str(ins_id) + "'"
            query += "    , '" + str(client_ip) + "'"
            query += "    , now() "
            query += "    , '" + str(ins_pgm) + "'"
            query += "    , '" + str(upd_id) + "'"
            query += "    , '" + str(client_ip) + "'"
            query += "    , now() "
            query += "    , '" + str(upd_pgm) + "'"
            query += " ) "

            print(query)
            cursor = connection.cursor()
            query_result = cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 


# 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(update) ###################################################
@csrf_exempt
def MP0101M_upload_update(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/MP0101M/'
    UPLOAD_DIR = '/NANUM/www/img/atc/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_mp_id = request.POST.get("mp_id")
        l_apl_no = request.POST.get("apl_no")
        l_apl_id = request.POST.get("apl_id") 
        l_length = request.POST.get("upload_length")
        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")

        client_ip = request.META['REMOTE_ADDR']

        l_att_cdd = list()
        l_att_cdh = list()
        l_service_upload_text = list()
        l_service_upload = list()
        l_atc_seq = list()
        l_upload_no = list()

        for i in range(0,int(l_length)):
            l_att_cdd.append(request.POST.get('att_cdd_up'+str(i), ""))
            l_service_upload_text.append(request.POST.get('service_upload_text'+str(i), ""))
            l_service_upload.append(request.POST.get('service_upload'+str(i), ""))
            l_att_cdh.append(request.POST.get('att_cdh_up'+str(i), ""))
            l_atc_seq.append(request.POST.get('atc_seq'+str(i), ""))
            l_upload_no.append(request.POST.get('upload_no'+str(i), ""))

            print("l_upload=====" + str(l_upload_no[i]) + "    i=====" + str(i))

            if(str(l_upload_no[i]) == str(i)):
                file = request.FILES['service_upload' + str(i)]
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_apl_id) + str(l_att_cdh[i]) + str(l_att_cdd[i]) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
            
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/atc/"+ str(n_filename)

                # atc_flag = mp_mtr_atc.objects.filter(mp_id=l_mp_id,apl_no=l_apl_no,atc_cdd=l_att_cdd[i]).exists()
                query = " select * from service20_mp_mtr_atc where mp_id = '" + str(l_mp_id) + "' and apl_no = '" + str(l_apl_no) + "' and atc_cdh = '" + str(l_att_cdh[i]) + "' and atc_cdd = '" + str(l_att_cdd[i]) + "'"

                query_result = cursor.execute(query)  

                if query_result == 0:
                    query = " insert into service20_mp_mtr_atc ( "
                    query += "    mp_id "
                    query += "    , apl_no "
                    query += "    , atc_seq "
                    query += "    , atc_cdh "
                    query += "    , atc_cdd "
                    query += "    , atc_nm "
                    query += "    , atc_file_nm "
                    query += "    , atc_file_url "
                    query += "    , ins_id "
                    query += "    , ins_ip "
                    query += "    , ins_dt "
                    query += "    , ins_pgm "
                    query += "    , upd_id "
                    query += "    , upd_ip "
                    query += "    , upd_dt "
                    query += "    , upd_pgm "
                    query += " ) "
                    query += " values ( "
                    query += "    '" + str(l_mp_id) + "'"
                    query += "    , '" + str(l_apl_no) + "'"
                    query += "    , (select ifnull(max(t1.atc_seq), 0) + 1 from service20_mp_mtr_atc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "') "
                    query += "    , '" + str(l_att_cdh[i]) + "'"
                    query += "    , '" + str(l_att_cdd[i]) + "'"
                    query += "    , (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "')"
                    query += "    , '" + str(filename) + "'"
                    query += "    , '" + str(fullFile) + "'"
                    query += "    , '" + str(ins_id) + "'"
                    query += "    , '" + str(client_ip) + "'"
                    query += "    , now() "
                    query += "    , '" + str(ins_pgm) + "'"
                    query += "    , '" + str(upd_id) + "'"
                    query += "    , '" + str(client_ip) + "'"
                    query += "    , now() "
                    query += "    , '" + str(upd_pgm) + "'"
                    query += " ) "

                    print(query)
                    cursor.execute(query)
                else:
                    query = " update service20_mp_mtr_atc "
                    query += "    set atc_cdd = '" + str(l_att_cdd[i]) + "' "
                    query += "      , atc_nm = (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "') "
                    query += "      , atc_file_nm = '" + str(filename) + "' "
                    query += "      , atc_file_url = '" + str(fullFile) + "' "
                    query += "      , upd_id = '" + upd_id + "'"
                    query += "      , upd_ip = '" + client_ip + "'"
                    query += "      , upd_dt = now()"
                    query += "      , upd_pgm = '" + upd_pgm + "'"
                    query += "  where mp_id = '" + str(l_mp_id) + "' "
                    query += "    and apl_no = '" + str(l_apl_no) + "' "
                    query += "    and atc_seq = '" + str(l_atc_seq[i]) + "' "

                    print(query)
                    cursor.execute(query)

        return HttpResponse('File Uploaded')

# 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기) ###################################################
class MP0101M_service_report_chc_Serializer(serializers.ModelSerializer):
    std_grp_code_nm = serializers.SerializerMethodField()
    chc_val = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_grp_code_nm(self,obj):
        return obj.std_grp_code_nm
    def get_chc_val(self,obj):
        return obj.chc_val

class MP0101M_service_report_chc(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_report_chc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        query = "/* 선택한 리스트 조회 */ "
        query += "select t1.id, t1.att_cdh "
        query += "     , t2.std_grp_code_nm "
        query += "     , fn_mp_chc_select_01('" + l_mp_id + "', t3.apl_no, t1.att_cdh) as chc_val "
        query += "  from service20_mp_sub t1 "
        query += "  left join service20_com_cdh t2 on (t2.std_grp_code = t1.att_cdh) "
        query += "  left join service20_mp_mtr  t3 on (t3.mp_id        = t1.mp_id) "
        query += " where t1.mp_id   = '" + l_mp_id + "' "
        query += "   and t1.att_id  = 'MP0089' "
        query += "   and t1.att_cdd = '2' "
        query += "   and t1.use_yn = 'Y' "
        query += "   and t3.apl_no  = '" + l_apl_no + "' ; "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (mp_sub 코드) ###################################################
class MP0101M_service_sub_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_sub
        fields = '__all__'


class MP0101M_service_sub(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_sub_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select id, att_id from service20_mp_sub where mp_id = '" + l_mp_id + "' group by att_id "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (콤보) ###################################################
class MP0101M_service_combo_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_combo(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_combo_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_att_cdh = request.GET.get('att_cdh', "")

        query = "/* 2.질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code  /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "' "
        query += "   and t1.att_id  = 'MP0090' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = '" + l_att_cdh + "' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#팀단위 추가!!!
# 멘토링 프로그램 - 해외봉사활동 프로그램 (카운트) ###################################################
class MP0101M_service_team_cnt_Serializer(serializers.ModelSerializer):
    
    std_grp_code_nm = serializers.SerializerMethodField()
    chc_tp = serializers.SerializerMethodField()
    chc_cnt = serializers.SerializerMethodField()
    chc_unit = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_grp_code_nm(self,obj):
        return obj.std_grp_code_nm
    def get_chc_tp(self,obj):
        return obj.chc_tp
    def get_chc_cnt(self,obj):
        return obj.chc_cnt
    def get_chc_unit(self,obj):
        return obj.chc_unit


class MP0101M_service_team_cnt(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_cnt_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = "/* 1.선택형 질문 리스트 */"
        query += " select t1.id, t1.att_cdh "
        query += "     , t2.std_grp_code_nm "
        query += "     , max(case t1.att_cdd when '1' then t1.att_val end) as chc_tp   /* 선택 유형 : 1 콤보, 2 라디오, 3 체크 */ "
        query += "     , max(case t1.att_cdd when '2' then t1.att_val end) as chc_cnt  /* 선택 가능 갯수                       */ "
        query += "     , max(case t1.att_cdd when '2' then ifnull(t1.att_unit, '') end) as chc_unit  /* 지망, 비지망 구분       */ "
        query += "  from service20_mp_sub t1 "
        query += "  left join service20_com_cdh t2 on (t2.std_grp_code = t1.att_cdh) "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "'"
        query += "   and t1.att_id  = 'MP0110' /* 선택형 질문             */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " group by t1.att_cdh "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램 - 해외봉사활동 프로그램 (희망도시 콤보) ###################################################
class MP0101M_service_team_combo_city_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_team_combo_city(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_combo_city_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = "/* 2.질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code  /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "' "
        query += "   and t1.att_id  = 'MP0111' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = 'MP0092' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (분야 콤보) ###################################################
class MP0101M_service_team_combo_field_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_team_combo_field(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_combo_field_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', None)

        query = "/* 질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + l_mp_id + "' "
        query += "   and t1.att_id  = 'MP0111' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = 'MP0093' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램 - 해외봉사활동 프로그램 (업로드 카운트) ###################################################
class MP0101M_service_team_upload_cnt_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_sub
        fields = '__all__'

class MP0101M_service_team_upload_cnt(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_upload_cnt_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select t1.id, t1.mp_id    /* 멘토링프로그램id     */ "
        query += "     , t1.att_cdh  /* 첨부파일 code header */ "
        query += "     , t1.att_cdd  /* 첨부파일 code        */ "
        query += "     , t1.att_val  /* 첨부파일 종류        */ "
        query += "  from service20_mp_sub t1 "
        query += " where mp_id   ='" + l_mp_id + "'  "
        query += "   and att_cdh = 'MP0105' "
        query += "   and use_yn  = 'Y' "
        query += " order by sort_seq; "

        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기) ###################################################
class MP0101M_service_team_apl_no_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mtr
        fields = '__all__'

class MP0101M_service_team_apl_no(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_service_team_apl_no_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select id, mp_id, max(apl_no) as apl_no from service20_mp_mtr where mp_id = '" + l_mp_id + "'"

        print(query)
        queryset = mp_mtr.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
        
# 멘토링 프로그램 - 해외봉사활동 프로그램 (insert) ###################################################
@csrf_exempt
def MP0101M_service_team_insert(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_apl_no = request.POST.get('apl_no_team', "")
    l_length = request.POST.get('over_service_team_length', "")
    l_att_cdd = list()
    l_att_cdh = list()
    l_chc_tp = list()
    l_seq = list()

    print("apl_no====" + l_apl_no)
    print("length==" + l_length)

    com_cnt = 0
    sel_cnt = 0
    chk_cnt = 0
    for i in range(0,int(l_length)):
        # l_att_cdd.append(request.POST.get('select_'+str(i), ""))
        l_att_cdh.append(request.POST.get('att_cdh_team'+str(i), ""))
        l_chc_tp.append(request.POST.get('chc_tp_team'+str(i), ""))
        l_seq.append(request.POST.get('seq_team'+str(i), ""))

        if l_chc_tp[i] == '1':
            l_att_cdd.append(request.POST.get('service_team_combo'+str(com_cnt), ""))
            com_cnt = com_cnt + 1
        elif l_chc_tp[i] == '3':
            l_att_cdd.append(request.POST.get('service_team_chkbox'+str(chk_cnt), ""))
            chk_cnt = chk_cnt + 1
        else:
            l_att_cdd.append(request.POST.get('service_team_select'+str(sel_cnt), ""))
            sel_cnt = sel_cnt + 1
    
        print("l_att_cdd===" + l_att_cdd[i])
        print("l_att_cdh===" + l_att_cdh[i])
        print("l_chc_tp===" + l_chc_tp[i])
        print("l_seq===" + l_seq[i])

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    
    # delete
    query = " delete FROM service20_mp_team_chc WHERE mp_id = '" + l_mp_id + "' AND team_no = '" + l_apl_no + "'"
    cursor = connection.cursor()
    cursor.execute(query)
    
    for i in range(0,int(l_length)):
        query = " insert "
        query += "    into "
        query += "        service20_mp_team_chc(mp_id "
        query += "        , team_no "
        query += "        , chc_no "
        query += "        , att_id "
        query += "        , att_cdh "
        query += "        , att_cdd "
        query += "        , chc_tp "
        query += "        , chc_val "
        query += "        , chc_seq "
        query += "        , ques_no "
        query += "        , ins_id "
        query += "        , ins_ip "
        query += "        , ins_dt "
        query += "        , ins_pgm "
        query += "        , upd_id "
        query += "        , upd_ip "
        query += "        , upd_dt "
        query += "        , upd_pgm) "
        query += "    values ( "
        query += "    '" + str(l_mp_id) + "'"
        query += "    , '" + str(l_apl_no) + "'"
        query += "    , (select ifnull(max(t1.chc_no), 0) + 1 from service20_mp_team_chc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.team_no = '" + str(l_apl_no) + "')"
        query += "    , 'MP0090' "
        query += "    , '" + str(l_att_cdh[i]) + "'"
        query += "    , '" + str(l_att_cdd[i]) + "'"
        query += "    , '" + str(l_chc_tp[i]) + "'"
        query += "    , (select t2.att_val  /* 선택형 답변 가능수      */ "
        query += "          from service20_mp_sub t2 "
        query += "         where t2.mp_id   = '" + str(l_mp_id) + "'"
        query += "           and t2.att_id  = 'MP0111' /* 선택형 질문             */ "
        query += "           and t2.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
        query += "           and t2.att_cdd = '" + str(l_att_cdd[i]) + "'"
        query += "           and t2.use_yn  = 'Y') "
        query += "    , '" + str(l_seq[i]) + "' "
        query += "    , (select t3.sort_seq  /* 답변 NO      */ "
        query += "          from service20_mp_sub t3 "
        query += "         where t3.mp_id   = '" + str(l_mp_id) + "'"
        query += "           and t3.att_id  = 'MP0111' /* 선택형 질문             */ "
        query += "           and t3.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
        query += "           and t3.att_cdd = '" + str(l_att_cdd[i]) + "'"
        query += "           and t3.use_yn  = 'Y') "
        query += "    , '" + str(ins_id) + "'"
        query += "    , '" + str(client_ip) + "'"
        query += "    , now() "
        query += "    , '" + str(ins_pgm) + "'"
        query += "    , '" + str(upd_id) + "'"
        query += "    , '" + str(client_ip) + "'"
        query += "    , now() "
        query += "    , '" + str(upd_pgm) + "'"
        query += " ) "

        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(query) 

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(insert) ###################################################
@csrf_exempt
def MP0101M_team_upload(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/MP0101M/'
    UPLOAD_DIR = '/NANUM/www/img/atc_team/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_mp_id = request.POST.get("mp_id")
        l_apl_no = request.POST.get("apl_no_team")
        l_apl_id = request.POST.get("apl_id") 
        l_length = request.POST.get("upload_team_length")
        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")
        
        print("==team_upload=="+l_length)

        client_ip = request.META['REMOTE_ADDR']

        l_att_cdd = list()
        l_att_cdh = list()
        l_service_upload_text = list()
        l_service_upload = list()
        l_upload_no = list()


        for i in range(0,int(l_length)):
            l_att_cdd.append(request.POST.get('att_cdd_up_team'+str(i), ""))
            l_service_upload_text.append(request.POST.get('service_team_upload_text'+str(i), ""))
            l_service_upload.append(request.POST.get('service_team_upload'+str(i), ""))
            l_att_cdh.append(request.POST.get('att_cdh_up_team'+str(i), ""))
            l_upload_no.append(request.POST.get('upload_team_no'+str(i), ""))

            print("l_upload=====" + str(l_upload_no[i]) + "    i=====" + str(i))

            if(str(l_upload_no[i]) == str(i)):
                file = request.FILES['service_team_upload' + str(i)]
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_apl_id) + str(l_att_cdh[i]) + str(l_att_cdd[i]) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
                
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/atc_team/"+ str(n_filename)

                query = " insert into service20_mp_team_atc ( "
                query += "    mp_id "
                query += "    , team_no "
                query += "    , atc_seq "
                query += "    , atc_cdh "
                query += "    , atc_cdd "
                query += "    , atc_nm "
                query += "    , atc_file_nm "
                query += "    , atc_file_url "
                query += "    , ins_id "
                query += "    , ins_ip "
                query += "    , ins_dt "
                query += "    , ins_pgm "
                query += "    , upd_id "
                query += "    , upd_ip "
                query += "    , upd_dt "
                query += "    , upd_pgm "
                query += " ) "
                query += " values ( "
                query += "    '" + str(l_mp_id) + "'"
                query += "    , '" + str(l_apl_no) + "'"
                query += "    , (select ifnull(max(t1.atc_seq), 0) + 1 from service20_mp_team_atc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.team_no = '" + str(l_apl_no) + "') "
                query += "    , '" + str(l_att_cdh[i]) + "'"
                query += "    , '" + str(l_att_cdd[i]) + "'"
                query += "    , (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "')"
                query += "    , '" + str(filename) + "'"
                query += "    , '" + str(fullFile) + "'"
                query += "    , '" + str(ins_id) + "'"
                query += "    , '" + str(client_ip) + "'"
                query += "    , now() "
                query += "    , '" + str(ins_pgm) + "'"
                query += "    , '" + str(upd_id) + "'"
                query += "    , '" + str(client_ip) + "'"
                query += "    , now() "
                query += "    , '" + str(upd_pgm) + "'"
                query += " ) "

                cursor.execute(query)


        return HttpResponse('File Uploaded')

# 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (데이터) ###################################################
class MP0101M_admin_service_team_chc_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_chc
        fields = '__all__'

class MP0101M_admin_service_team_chc(generics.ListAPIView):
    queryset = mp_chc.objects.all()
    serializer_class = MP0101M_admin_service_team_chc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")
        l_team_no = request.GET.get('team_no', "")

        query = " select id as id "
        query += "     , mp_id as mp_id "
        query += "     , team_no as apl_no "
        query += "     , chc_no as chc_no "
        query += "     , att_id as att_id "
        query += "     , att_cdh as att_cdh "
        query += "     , att_cdd as att_cdd "
        query += "     , chc_tp as chc_tp "
        query += "     , chc_val as chc_val "
        query += "     , chc_seq as chc_seq "
        query += "     , ques_no as ques_no "
        query += "  from service20_mp_team_chc "
        query += " where mp_id = '" + l_mp_id + "' "
        query += "   and team_no = '"+ l_team_no + "'"
        query += " order by chc_no, chc_seq "

        queryset = mp_chc.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (첨부데이터) ###################################################
class MP0101M_admin_service_team_atc_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mtr_atc
        fields = '__all__'

class MP0101M_admin_service_team_atc(generics.ListAPIView):
    queryset = mp_mtr_atc.objects.all()
    serializer_class = MP0101M_admin_service_team_atc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")
        l_team_no = request.GET.get('team_no', "")

        query = " select id as id "
        query += "     , mp_id as mp_id "
        query += "     , team_no as apl_no "
        query += "     , atc_seq as atc_seq "
        query += "     , atc_cdh as atc_cdh "
        query += "     , atc_cdd as atc_cdd "
        query += "     , atc_nm as atc_nm "
        query += "     , atc_file_nm as atc_file_nm "
        query += "     , atc_file_url as atc_file_url "
        query += "  from service20_mp_team_atc "
        query += " where mp_id = '" + l_mp_id + "' "
        query += "   and team_no = '" + l_team_no + "' "
        query += "   and atc_cdh = 'MP0105' "
        query += " order by atc_seq "


        queryset = mp_mtr_atc.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (update) ###################################################
@csrf_exempt
def MP0101M_service_team_update(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_apl_no = request.POST.get('team_no', "")
    l_length = request.POST.get('over_service_team_length', "")
    l_att_cdd = list()
    l_att_cdh = list()
    l_chc_tp = list()
    l_chc_no = list()
    l_seq = list()

    print("apl_no====" + l_apl_no)
    print("length==" + l_length)
    com_cnt = 0
    sel_cnt = 0
    chk_cnt = 0
    for i in range(0,int(l_length)):
        # l_att_cdd.append(request.POST.get('select_'+str(i), ""))
        l_att_cdh.append(request.POST.get('att_cdh_team'+str(i), ""))
        l_chc_tp.append(request.POST.get('chc_tp_team'+str(i), ""))
        l_chc_no.append(request.POST.get('chc_no_team'+str(i), ""))
        l_seq.append(request.POST.get('seq_team'+str(i), ""))

        if l_chc_tp[i] == '1':
            l_att_cdd.append(request.POST.get('service_combo_team'+str(com_cnt), ""))
            com_cnt = com_cnt + 1
        elif l_chc_tp[i] == '3':
            l_att_cdd.append(request.POST.get('service_chkbox_team'+str(chk_cnt), ""))
            chk_cnt = chk_cnt + 1
        else:
            l_att_cdd.append(request.POST.get('service_select_team'+str(sel_cnt), ""))
            sel_cnt = sel_cnt + 1
    
        print("l_att_cdd===" + l_att_cdd[i])
        print("l_att_cdh===" + l_att_cdh[i])
        print("l_chc_tp===" + l_chc_tp[i])
        print("l_seq===" + l_seq[i])
        print("l_chc_no===" + l_chc_no[i])

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    
    query = " SELECT count(0) as up_cnt FROM service20_mp_team_chc WHERE mp_id = '" + str(l_mp_id) + "' AND team_no = '" + str(l_apl_no) + "'"
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    up_cnt = int(results[0].up_cnt)

    # 저장된 선택사항과 mp_sub에 관리되는 선택사항의 개수가 일치할 때는 update
    if l_length == up_cnt:
        # update
        for i in range(0,int(l_length)):
            query = "  update service20_mp_team_chc "
            query += "     set att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "       , chc_val = (select t1.att_val  "
            query += "                      from service20_mp_sub t1 "
            query += "                     where t1.mp_id = '" + str(l_mp_id) + "' "
            query += "                       and t1.att_id = 'MP0111' "
            query += "                       and t1.att_cdh = '" + str(l_att_cdh[i]) + "' "
            query += "                       and t1.att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "                       and t1.use_yn = 'Y') "
            query += "       , chc_seq = '" + l_seq[i] + "' "
            query += "       , ques_no = (select t2.sort_seq  "
            query += "                      from service20_mp_sub t2 "
            query += "                     where t2.mp_id = '" + str(l_mp_id) + "' "
            query += "                       and t2.att_id = 'MP0111' "
            query += "                       and t2.att_cdh = '" + str(l_att_cdh[i]) + "' "
            query += "                       and t2.att_cdd = '" + str(l_att_cdd[i]) + "' "
            query += "                       and t2.use_yn = 'Y') "
            query += "       , upd_id = '" + str(upd_id) + "' "
            query += "       , upd_ip = '" + str(client_ip) + "' "
            query += "       , upd_dt = now() "
            query += "       , upd_pgm = '" + str(upd_pgm) + "' "
            query += "   where mp_id = '" + str(l_mp_id) + "' "
            query += "     and team_no = '" + str(l_apl_no) + "' "
            query += "     and chc_no = '" + str(l_chc_no[i]) + "' "
            
            print(query)
            cursor = connection.cursor()
            query_result = cursor.execute(query)
    # 저장된 선택사항과 mp_sub에 관리되는 선택사항의 개수가 일치하지 않을 때는 기존꺼 전체 0delete 후 전체 isnert
    else:
        # delete
        query = " delete FROM service20_mp_team_chc WHERE mp_id = '" + str(l_mp_id) + "' AND team_no = '" + str(l_apl_no) + "'"
        cursor = connection.cursor()
        cursor.execute(query)    

        # insert
        for i in range(0,int(l_length)):
            query = " insert "
            query += "    into "
            query += "        service20_mp_team_chc(mp_id "
            query += "        , team_no "
            query += "        , chc_no "
            query += "        , att_id "
            query += "        , att_cdh "
            query += "        , att_cdd "
            query += "        , chc_tp "
            query += "        , chc_val "
            query += "        , chc_seq "
            query += "        , ques_no "
            query += "        , ins_id "
            query += "        , ins_ip "
            query += "        , ins_dt "
            query += "        , ins_pgm "
            query += "        , upd_id "
            query += "        , upd_ip "
            query += "        , upd_dt "
            query += "        , upd_pgm) "
            query += "    values ( "
            query += "    '" + str(l_mp_id) + "'"
            query += "    , '" + str(l_apl_no) + "'"
            query += "    , (select ifnull(max(t1.chc_no), 0) + 1 from service20_mp_team_chc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.team_no = '" + str(l_apl_no) + "')"
            query += "    , 'MP0111' "
            query += "    , '" + str(l_att_cdh[i]) + "'"
            query += "    , '" + str(l_att_cdd[i]) + "'"
            query += "    , '" + str(l_chc_tp[i]) + "'"
            query += "    , (select t2.att_val  /* 선택형 답변 가능수      */ "
            query += "          from service20_mp_sub t2 "
            query += "         where t2.mp_id   = '" + str(l_mp_id) + "'"
            query += "           and t2.att_id  = 'MP0111' /* 선택형 질문             */ "
            query += "           and t2.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
            query += "           and t2.att_cdd = '" + str(l_att_cdd[i]) + "'"
            query += "           and t2.use_yn  = 'Y') "
            query += "    , '" + str(l_seq[i]) + "' "
            query += "    , (select t3.sort_seq  /* 답변 NO      */ "
            query += "          from service20_mp_sub t3 "
            query += "         where t3.mp_id   = '" + str(l_mp_id) + "'"
            query += "           and t3.att_id  = 'MP0111' /* 선택형 질문             */ "
            query += "           and t3.att_cdh = '" + str(l_att_cdh[i]) + "' /* 선택형 질문 유형        */ "
            query += "           and t3.att_cdd = '" + str(l_att_cdd[i]) + "'"
            query += "           and t3.use_yn  = 'Y') "
            query += "    , '" + str(ins_id) + "'"
            query += "    , '" + str(client_ip) + "'"
            query += "    , now() "
            query += "    , '" + str(ins_pgm) + "'"
            query += "    , '" + str(upd_id) + "'"
            query += "    , '" + str(client_ip) + "'"
            query += "    , now() "
            query += "    , '" + str(upd_pgm) + "'"
            query += " ) "

            print(query)
            cursor = connection.cursor()
            query_result = cursor.execute(query)

    # for i in range(0,int(l_length)):
    #     query = "  update service20_mp_team_chc "
    #     query += "     set att_cdd = '" + str(l_att_cdd[i]) + "' "
    #     query += "       , chc_val = (select t1.att_val  "
    #     query += "                      from service20_mp_sub t1 "
    #     query += "                     where t1.mp_id = '" + str(l_mp_id) + "' "
    #     query += "                       and t1.att_id = 'MP0111' "
    #     query += "                       and t1.att_cdh = '" + str(l_att_cdh[i]) + "' "
    #     query += "                       and t1.att_cdd = '" + str(l_att_cdd[i]) + "' "
    #     query += "                       and t1.use_yn = 'Y') "
    #     query += "       , chc_seq = '" + l_seq[i] + "' "
    #     query += "       , ques_no = (select t2.sort_seq  "
    #     query += "                      from service20_mp_sub t2 "
    #     query += "                     where t2.mp_id = '" + str(l_mp_id) + "' "
    #     query += "                       and t2.att_id = 'MP0111' "
    #     query += "                       and t2.att_cdh = '" + str(l_att_cdh[i]) + "' "
    #     query += "                       and t2.att_cdd = '" + str(l_att_cdd[i]) + "' "
    #     query += "                       and t2.use_yn = 'Y') "
    #     query += "       , upd_id = '" + str(upd_id) + "' "
    #     query += "       , upd_ip = '" + str(client_ip) + "' "
    #     query += "       , upd_dt = now() "
    #     query += "       , upd_pgm = '" + str(upd_pgm) + "' "
    #     query += "   where mp_id = '" + str(l_mp_id) + "' "
    #     query += "     and team_no = '" + str(l_apl_no) + "' "
    #     query += "     and chc_no = '" + str(l_chc_no[i]) + "' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(query) 

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 


# 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(update) ###################################################
@csrf_exempt
def MP0101M_team_upload_update(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/MP0101M/'
    UPLOAD_DIR = '/NANUM/www/img/atc_team/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_mp_id = request.POST.get("mp_id")
        l_apl_no = request.POST.get("team_no")
        l_apl_id = request.POST.get("apl_id") 
        l_length = request.POST.get("upload_team_length")
        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")

        client_ip = request.META['REMOTE_ADDR']

        l_att_cdd = list()
        l_att_cdh = list()
        l_service_upload_text = list()
        l_service_upload = list()
        l_atc_seq = list()
        l_upload_no = list()

        for i in range(0,int(l_length)):
            l_att_cdd.append(request.POST.get('att_cdd_up_team'+str(i), ""))
            l_service_upload_text.append(request.POST.get('service_team_upload_text'+str(i), ""))
            l_service_upload.append(request.POST.get('service_team_upload'+str(i), ""))
            l_att_cdh.append(request.POST.get('att_cdh_up_team'+str(i), ""))
            l_atc_seq.append(request.POST.get('atc_seq_team'+str(i), ""))
            l_upload_no.append(request.POST.get('upload_no_team'+str(i), ""))

            print("l_upload=====" + str(l_upload_no[i]) + "    i=====" + str(i))

            if(str(l_upload_no[i]) == str(i)):
                file = request.FILES['service_team_upload' + str(i)]
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_apl_id) + str(l_att_cdh[i]) + str(l_att_cdd[i]) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
            
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/atc_team/"+ str(n_filename)

                # atc_flag = mp_mtr_atc.objects.filter(mp_id=l_mp_id,apl_no=l_apl_no,atc_cdd=l_att_cdd[i]).exists()
                query = " select * from service20_mp_team_atc where mp_id = '" + str(l_mp_id) + "' and team_no = '" + str(l_apl_no) + "' and atc_cdh = '" + str(l_att_cdh[i]) + "' and atc_cdd = '" + str(l_att_cdd[i]) + "'"

                query_result = cursor.execute(query)  

                if query_result == 0:
                    query = " insert into service20_mp_team_atc ( "
                    query += "    mp_id "
                    query += "    , team_no "
                    query += "    , atc_seq "
                    query += "    , atc_cdh "
                    query += "    , atc_cdd "
                    query += "    , atc_nm "
                    query += "    , atc_file_nm "
                    query += "    , atc_file_url "
                    query += "    , ins_id "
                    query += "    , ins_ip "
                    query += "    , ins_dt "
                    query += "    , ins_pgm "
                    query += "    , upd_id "
                    query += "    , upd_ip "
                    query += "    , upd_dt "
                    query += "    , upd_pgm "
                    query += " ) "
                    query += " values ( "
                    query += "    '" + str(l_mp_id) + "'"
                    query += "    , '" + str(l_apl_no) + "'"
                    query += "    , (select ifnull(max(t1.atc_seq), 0) + 1 from service20_mp_team_atc t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.team_no = '" + str(l_apl_no) + "') "
                    query += "    , '" + str(l_att_cdh[i]) + "'"
                    query += "    , '" + str(l_att_cdd[i]) + "'"
                    query += "    , (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "')"
                    query += "    , '" + str(filename) + "'"
                    query += "    , '" + str(fullFile) + "'"
                    query += "    , '" + str(ins_id) + "'"
                    query += "    , '" + str(client_ip) + "'"
                    query += "    , now() "
                    query += "    , '" + str(ins_pgm) + "'"
                    query += "    , '" + str(upd_id) + "'"
                    query += "    , '" + str(client_ip) + "'"
                    query += "    , now() "
                    query += "    , '" + str(upd_pgm) + "'"
                    query += " ) "

                    print(query)
                    cursor.execute(query)
                else:
                    query = " update service20_mp_team_atc "
                    query += "    set atc_cdd = '" + str(l_att_cdd[i]) + "' "
                    query += "      , atc_nm = (select std_detl_code_nm from service20_com_cdd where std_grp_code = '" + str(l_att_cdh[i]) + "' and std_detl_code = '" + str(l_att_cdd[i]) + "') "
                    query += "      , atc_file_nm = '" + str(filename) + "' "
                    query += "      , atc_file_url = '" + str(fullFile) + "' "
                    query += "      , upd_id = '" + upd_id + "'"
                    query += "      , upd_ip = '" + client_ip + "'"
                    query += "      , upd_dt = now()"
                    query += "      , upd_pgm = '" + upd_pgm + "'"
                    query += "  where mp_id = '" + str(l_mp_id) + "' "
                    query += "    and team_no = '" + str(l_apl_no) + "' "
                    query += "    and atc_seq = '" + str(l_atc_seq[i]) + "' "

                    print(query)
                    cursor.execute(query)

        return HttpResponse('File Uploaded')

# 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기) ###################################################
class MP0101M_service_team_report_chc_Serializer(serializers.ModelSerializer):
    std_grp_code_nm = serializers.SerializerMethodField()
    chc_val = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_grp_code_nm(self,obj):
        return obj.std_grp_code_nm
    def get_chc_val(self,obj):
        return obj.chc_val

class MP0101M_service_team_report_chc(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_report_chc_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        query = "/* 선택한 리스트 조회 */ "
        query += "select t1.id, t1.att_cdh "
        query += "     , t2.std_grp_code_nm "
        query += "     , fn_mp_chc_select_01('" + l_mp_id + "', t3.apl_no, t1.att_cdh) as chc_val "
        query += "  from service20_mp_sub t1 "
        query += "  left join service20_com_cdh t2 on (t2.std_grp_code = t1.att_cdh) "
        query += "  left join service20_mp_mtr  t3 on (t3.mp_id        = t1.mp_id) "
        query += " where t1.mp_id   = '" + l_mp_id + "' "
        query += "   and t1.att_id  = 'MP0110' "
        query += "   and t1.att_cdd = '2' "
        query += "   and t3.apl_no  = '" + l_apl_no + "' ; "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
# 멘토링 프로그램 - 해외봉사활동 프로그램 (mp_sub 코드) ###################################################
class MP0101M_service_team_sub_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_sub
        fields = '__all__'


class MP0101M_service_team_sub(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_sub_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select id, att_id from service20_mp_sub where mp_id = '" + l_mp_id + "' group by att_id "

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 - 해외봉사활동 프로그램 (콤보) ###################################################
class MP0101M_service_team_combo_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_sub
        fields = '__all__'

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP0101M_service_team_combo(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_combo_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_att_cdh = request.GET.get('att_cdh', "")

        query = "/* 2.질문리스트의 선택 콤보에 들어갈 항목 리스트 조회 */"
        query += " select t1.id, t1.att_cdd as std_detl_code  /* 선택형 답변 가능수 code */ "
        query += "     , t1.att_val as std_detl_code_nm  /* 선택형 답변 가능수      */ "
        query += "  from service20_mp_sub t1 "
        query += " where t1.mp_id   = '" + str(l_mp_id) + "' "
        query += "   and t1.att_id  = 'MP0111' /* 선택형 질문             */ "
        query += "   and t1.att_cdh = '" + l_att_cdh + "' /* 선택형 질문 유형        */ "
        query += "   and t1.use_yn  = 'Y' "
        query += " order by t1.sort_seq"

        print(query)
        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 리스트에서 팀 단위 status 가져오기
class MP0101M_team_status_Serializer(serializers.ModelSerializer):
    indv_div = serializers.SerializerMethodField()
    
    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_indv_div(self,obj):
        return obj.indv_div


# 멘토링 프로그램 리스트에서 팀 단위 status 가져오기
class MP0101M_team_status(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_team_status_Serializer
    def list(self, request):       
        l_mp_id = request.GET.get('mp_id', '') 
        l_apl_id = request.GET.get('apl_id', '')           

        query = "select t1.id as id, t1.status as status "
        query += "     , t2.indv_div as indv_div "
        query += "  from service20_mp_mtr t1 "
        query += "  left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += " where t1.mp_id = '" + l_mp_id + "' "
        query += "   and apl_id = '" + l_apl_id + "'; "

        print(query)
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 팀단위 로그인id 가져오기
class MP0101M_team_logininfo_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_nm = serializers.SerializerMethodField()
    user_brth_dt = serializers.SerializerMethodField()
    user_sch_nm1 = serializers.SerializerMethodField()
    user_sch_nm2 = serializers.SerializerMethodField()
    stds_div = serializers.SerializerMethodField()
    stds_nm = serializers.SerializerMethodField()
    score03 = serializers.SerializerMethodField()
    mob_no = serializers.SerializerMethodField()
    score_yn = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = ('id', 'user_id', 'user_nm','user_brth_dt','user_sch_nm1','user_sch_nm2','stds_div','stds_nm','score03','mob_no','score_yn')

    def get_id(self,obj):
        return obj.id
    def get_user_id(self,obj):
        return obj.user_id
    def get_user_nm(self,obj):
        return obj.user_nm
    def get_user_brth_dt(self,obj):
        return obj.user_brth_dt
    def get_user_sch_nm1(self,obj):
        return obj.user_sch_nm1
    def get_user_sch_nm2(self,obj):
        return obj.user_sch_nm2
    def get_stds_div(self,obj):
        return obj.stds_div
    def get_stds_nm(self,obj):
        return obj.stds_nm
    def get_score03(self,obj):
        return obj.score03
    def get_mob_no(self,obj):
        return obj.mob_no
    def get_score_yn(self,obj):
        return obj.score_yn

# 멘토링 프로그램 팀단위 로그인id 가져오기
class MP0101M_team_logininfo(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_team_logininfo_Serializer
    def list(self, request):       
        
        query = " select 0 as id, user_id "
        query += "      , user_nm "
        query += "      , user_brth_dt "
        query += "      , user_sch_nm1 "
        query += "      , user_sch_nm2 "
        query += "  from vw_nanum_login "
        query += " where user_div in ('M','S') "


        query = "select"
        query += "    0 as id,"
        query += "    A.user_id,"
        query += "    A.user_nm,"
        query += "    A.user_brth_dt,"
        query += "    A.user_sch_nm1,"
        query += "    A.user_sch_nm2,"
        query += "    B.stds_div,"
        query += "    B.stds_nm,"
        query += "    B.score03,"
        query += "    B.mob_no,"
        query += "    case when B.score03*1 > 2.5 then 'Y' else 'N' end score_yn"
        query += " from"
        query += "    vw_nanum_login A"
        query += " left join service20_vw_nanum_stdt B on"
        query += "    (A.user_id = B.apl_id)"
        query += " where A.user_div in ('M','S')   "
        query += "    and B.stds_div = '01'        "

        print(query)
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 질문유형 가져오기
class MP0101M_team_quest_Serializer(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    ans_min_len = serializers.SerializerMethodField()
    ans_max_len = serializers.SerializerMethodField()
    class Meta:
        model = mp_sub
        fields = ('id','mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk','ans_min_len','ans_max_len')

        
    def get_std_detl_code(self,obj):
        return obj.std_detl_code
        
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk    
    def get_ans_min_len(self,obj):
        return obj.ans_min_len  
    def get_ans_max_len(self,obj):
        return obj.ans_max_len

# 멘토링 프로그램 질문유형 가져오기
class MP0101M_team_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_team_quest_Serializer
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None)           
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0026' and B.use_indc = 'Y' and A.mp_id = '"+key1+"'"

        query = "select  "
        query += "     t3.std_detl_code, "
        query += "     t3.std_detl_code_nm, "
        query += "     t3.rmrk, "
        query += "     fn_mp_sub_att_val_select_01(t1.mp_id, t1.att_id, 'MS0028', t1.att_cdd) ans_min_len, "
        query += "     fn_mp_sub_att_val_select_01(t1.mp_id, t1.att_id, 'MS0029', t1.att_cdd) ans_max_len, "
        query += "     t1.* "
        query += "FROM service20_mp_sub t1 "
        query += "LEFT JOIN service20_com_cdd t3 ON (t3.std_grp_code  = t1.att_cdh "
        query += "                               AND t3.std_detl_code = t1.att_cdd) "
        query += "WHERE t1.mp_id   = '"+key1+"' "
        query += " AND t1.att_id  = 'MS0026' "
        query += " AND t1.att_cdh = 'MS0026' "
        query += "ORDER BY t1.sort_seq "

        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 질문2
class MP0101M_adm_team_quest_Serializer2(serializers.ModelSerializer):

    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = mp_ans
        fields = ('id','mp_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code','std_detl_code_nm','rmrk')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm    

    def get_rmrk(self,obj):
        return obj.rmrk

# 멘토링 프로그램(관리자) - 질문
class MP0101M_adm_team_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_adm_team_quest_Serializer2
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        l_exist = mp_sub.objects.filter(mp_id=key1).exists()
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_team_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.use_indc = 'Y' and B.std_grp_code in (select att_cdh from service20_mp_sub where att_id='MS0026' and mp_id = '"+str(key1)+"') and A.mp_id = '"+str(key1)+"' and A.team_no in (select team_id from service20_mp_mtr where apl_id = '"+str(l_user_id)+"' and mp_id = '"+str(key1)+"')"
        queryset = mp_ans.objects.raw(query)

        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        
#팀단위 추가!!!


# 멘토링 프로그램 - 업로드 가능한 첨부파일 ###################################################
class MP0101M_service_team_upload_file_chk_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_sub
        fields = '__all__'

class MP0101M_service_team_upload_file_chk(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = MP0101M_service_team_upload_file_chk_Serializer
    
    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        query = " select t1.id, t1.mp_id    /* 멘토링프로그램id     */ "
        query += "     , t1.att_cdh  /* 첨부파일 code header */ "
        query += "     , t1.att_cdd  /* 첨부파일 code        */ "
        query += "     , t1.att_val  /* 첨부파일 종류        */ "
        query += "  from service20_mp_sub t1 "
        query += " where mp_id   ='" + l_mp_id + "'  "
        query += "   and att_cdh = 'MP0112' "
        query += "   and use_yn  = 'Y' "
        query += " group by att_cdd "
        query += " order by sort_seq"

        queryset = mp_sub.objects.raw(query)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(팀원팝업) - 조회
class popupTeam_list_Serializer(serializers.ModelSerializer):

    ldr_id = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_ldr_id(self,obj):
        return obj.ldr_id

class popupTeam_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = popupTeam_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', None) 
        l_team_id = request.GET.get('team_id', None)           
        
        query = " select t2.id, trim(t2.apl_id) as apl_id "
        query += "     , t2.apl_nm as apl_nm "
        query += "     , t3.ldr_id as ldr_id "
        query += "     , t2.apl_no as apl_no "
        query += "  from service20_mp_team_mem t1 "
        query += "  left join service20_mp_mtr t2 on (t2.mp_id = t1.mp_id and t2.apl_no = t1.apl_no and t2.team_id = t1.team_id) "
        query += "  left join service20_mp_team t3 on (t3.mp_id = t1.mp_id and t3.team_id = t1.team_id) "
        query += " where t1.mp_id = '" + l_mp_id + "' "
        query += "   and t1.team_id = '" + l_team_id + "' "

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)     

# 멘토링 프로그램(팀원팝업) - delete
@csrf_exempt
def popupTeam_delete(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_team_id = request.POST.get('team_id', "")
    l_team_min = request.POST.get('team_min', "")
    l_apl_id = request.POST.get('apl_id', "")
    l_apl_no = request.POST.get('apl_no', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    query = "delete from service20_mp_mtr where mp_id = '" + l_mp_id + "' and apl_id = '" + l_apl_id + "' and team_id = '" + l_team_id + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_ans where mp_id = '" + l_mp_id + "' and apl_id = '" + l_apl_id + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_mtr_fe where mp_id = '" + l_mp_id + "' and apl_id = '" + l_apl_id + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_mtr_sa where mp_id = '" + l_mp_id + "' and apl_id = '" + l_apl_id + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_chc where mp_id = '" + l_mp_id + "' and apl_no = '" + l_apl_no + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_mtr_atc where mp_id = '" + l_mp_id + "' and apl_no = '" + l_apl_no + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    query = "delete from service20_mp_team_mem where mp_id = '" + l_mp_id + "' and team_id = '" + l_team_id + "' and apl_no = '" + l_apl_no + "' "
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램(팀원팝업) - insert
@csrf_exempt
def popupTeam_insert(request):
    l_mp_id = request.POST.get('mp_id', "")    
    l_team_id = request.POST.get('team_id', "")
    l_team_min = request.POST.get('team_row', "")
    l_team_min = int(l_team_min) + 1
    l_apl_id = list()
    l_apl_no = list()

    print("l_mp_id===" + l_mp_id)
    print("l_team_id===" + l_team_id)
    print("l_team_min===" + str(l_team_min))

    # 팀장 row를 제외하여 index를 2부터 시작(팀장을 포함하면 1부터 시작)
    # apl_id, apl_no를 여러개 받기
    for i in range(2,int(l_team_min)):
        l_apl_id.append(request.POST.get('apl_id'+str(i), ""))
        l_apl_no.append(request.POST.get('apl_no'+str(i), ""))
        print(l_apl_id)
        print(l_apl_no)

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    
    print("forlen===" + str(len(l_apl_id)))
    l_team_min = int(len(l_apl_id))
    for i in range(0,int(l_team_min)):
        if l_apl_no[i] == "":
            l_apl_no[i] = 0
        mtr_chk = mp_mtr.objects.filter(mp_id=str(l_mp_id),apl_id=str(l_apl_id[i]),team_id=str(l_team_id)).exists()
        mtr_fe_chk = mp_mtr_fe.objects.filter(mp_id=str(l_mp_id),apl_id=str(l_apl_id[i])).exists()
        mtr_sa_chk = mp_mtr_sa.objects.filter(mp_id=str(l_mp_id),apl_id=str(l_apl_id[i])).exists()
        mtr_lc_chk = mp_mtr_lc.objects.filter(mp_id=str(l_mp_id),apl_id=str(l_apl_id[i])).exists()
        team_mem_chk = mp_team_mem.objects.filter(mp_id=str(l_mp_id),team_id=str(l_team_id),apl_no=int(l_apl_no[i])).exists()
        
        stdt_rows = vw_nanum_stdt.objects.filter(apl_id=str(l_apl_id[i]))[0]
        mpgm_rows = mpgm.objects.filter(mp_id=str(l_mp_id))[0]
        query = "select ifnull( nullif(max(apl_no),0) ,0) as apl_no,ifnull( nullif(max(team_id),0) ,0) as team_no from service20_mp_mtr where mp_id = '"+l_mp_id+"'"  
        cursor = connection.cursor()
        cursor.execute(query)    
        results = namedtuplefetchall(cursor)    
        apl_no = int(results[0].apl_no)
        apl_no = apl_no+1

        # 팀원 멘토링 프로그램 신청
        if not mtr_chk:
            if stdt_rows.unv_cd == None:
                v_unv_cd = ''
            else:
                v_unv_cd = stdt_rows.unv_cd 

            if stdt_rows.unv_nm == None:
                v_unv_nm = ''
            else:
                v_unv_nm = stdt_rows.unv_nm

            if stdt_rows.mob_no == None:
                v_mob_no = ''
            else:
                v_mob_no = stdt_rows.mob_no.replace('-', '')
                
            if stdt_rows.tel_no == None:
                v_tel_no = ''
            else:
                v_tel_no = stdt_rows.tel_no.replace('-', '')

            if stdt_rows.tel_no_g == None:
                v_tel_no_g = ''
            else:
                v_tel_no_g = stdt_rows.tel_no_g.replace('-', '')   

            v_gen = ""
            if str(stdt_rows.gen_cd) == "1":
                v_gen = "M"
            else:
                v_gen = "F"

            model_instance = mp_mtr(
                mp_id=str(l_mp_id), 
                apl_no=int(apl_no), 
                mntr_id=str(l_apl_id[i]),
                team_id=str(l_team_id),
                apl_id=str(l_apl_id[i]),
                apl_nm=str(stdt_rows.apl_nm),
                unv_cd=str(v_unv_cd),
                unv_nm=str(v_unv_nm),
                cllg_cd=str(stdt_rows.cllg_cd),
                cllg_nm=str(stdt_rows.cllg_nm),
                dept_cd=str(stdt_rows.dept_cd),
                dept_nm=str(stdt_rows.dept_nm),
                brth_dt=str(stdt_rows.brth_dt),
                gen=v_gen,
                yr=str(mpgm_rows.yr),
                term_div=str(stdt_rows.term_div),
                sch_yr=str(stdt_rows.sch_yr),
                mob_no=str(v_mob_no),
                tel_no=str(v_tel_no),
                tel_no_g=str(v_tel_no_g),
                h_addr=str(stdt_rows.h_addr),
                email_addr=str(stdt_rows.email_addr),
                bank_acct=str(stdt_rows.bank_acct),
                bank_cd=str(stdt_rows.bank_cd),
                bank_nm=str(stdt_rows.bank_nm),
                score1=stdt_rows.score01,
                score2=stdt_rows.score02,
                score3=stdt_rows.score03,
                score4=stdt_rows.score04,
                score5=stdt_rows.score05,
                score6=stdt_rows.score06,
                cmp_term=str(stdt_rows.cmp_term),
                pr_yr=str(stdt_rows.pr_yr),
                pr_sch_yr=str(stdt_rows.pr_sch_yr),
                pr_term_div=str(stdt_rows.pr_term_div),
                inv_agr_div = 'Y',
                inv_agr_dt = datetime.datetime.today(),
                status='10', # 지원
                mjr_cd=str(stdt_rows.mjr_cd),
                mjr_nm=str(stdt_rows.mjr_nm),
                ins_id=str(ins_id),
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today(),
                upd_id=str(ins_id),
                upd_ip=str(client_ip),
                upd_dt=datetime.datetime.today()
                )
            model_instance.save()

        # 팀원 어학 점수
        if not mtr_fe_chk:
            # -- 생성_어학(mp_mtr_fe)_FROM_vw_nanum_foreign_exam
            update_text = " insert into service20_mp_mtr_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ "
            update_text += "      ( mp_id          /* 멘토링 프로그램id */ "
            update_text += "      , apl_no         /* 지원 no */ "
            update_text += "      , fe_no          /* 어학점수 no */ "
            update_text += "      , apl_id         /* 학번 */ "
            update_text += "      , apl_nm         /* 성명 */ "
            update_text += "      , lang_kind_cd   /* 어학종류코드 */ "
            update_text += "      , lang_kind_nm   /* 어학종류명 */ "
            update_text += "      , lang_cd        /* 어학상위코드 */ "
            update_text += "      , lang_nm        /* 어학상위코드명 */ "
            update_text += "      , lang_detail_cd /* 어학하위코드 */ "
            update_text += "      , lang_detail_nm /* 어학하위코드명 */ "
            update_text += "      , frexm_cd       /* 외국어시험 코드 */ "
            update_text += "      , frexm_nm       /* 외국어시험명 */ "
            update_text += "      , score          /* 시험점수 */ "
            update_text += "      , grade          /* 시험등급 */ "
            update_text += "      , ins_id         /* 입력자id */ "
            update_text += "      , ins_ip         /* 입력자ip */ "
            update_text += "      , ins_dt         /* 입력일시 */ "
            update_text += "      , ins_pgm        /* 입력프로그램id */ "
            update_text += " ) "
            update_text += " select '"+str(l_mp_id)+"' AS mp_id "
            update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
            update_text += "      , @curRank := @curRank +1 AS fe_no  "
            update_text += "      , t1.apl_id         /* 학번 */ "
            update_text += "      , t1.apl_nm         /* 성명 */ "
            update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ "
            update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ "
            update_text += "      , t1.lang_cd        /* 어학상위코드 */ "
            update_text += "      , t1.lang_nm        /* 어학상위코드명 */ "
            update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ "
            update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ "
            update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ "
            update_text += "      , t1.frexm_nm       /* 외국어시험명 */ "
            update_text += "      , t1.score          /* 시험점수 */ "
            update_text += "      , t1.grade          /* 시험등급 */ "
            update_text += "      , '"+str(l_apl_id[i])+"' ins_id         /* 입력자id */ "
            update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
            update_text += "      , NOW() ins_dt         /* 입력일시 */ "
            update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ "
            update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ "
            update_text += "      , (SELECT @curRank := 0) r "
            update_text += "  WHERE 1=1 "
            update_text += "    AND t1.apl_id = '"+str(l_apl_id[i])+"' "
            print("::_FROM_vw_nanum_foreign_exam::")
            print(update_text) 
            cursor = connection.cursor()
            query_result = cursor.execute(update_text)
        
        # 팀원 봉사 점수
        if not mtr_sa_chk:
            # -- 생성_봉사(mp_mtr_sa)_FROM_vw_nanum_foreign_exam
            update_text = "insert into service20_mp_mtr_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ "
            update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
            update_text += "     , apl_no          /* 지원 no */ "
            update_text += "     , sa_no           /* 어학점수 no */ "
            update_text += "     , apl_id          /* 학번 */ "
            update_text += "     , apl_nm          /* 성명 */ "
            update_text += "     , nation_inout_cd /* 국내외구분코드 */ "
            update_text += "     , nation_inout_nm /* 국내외구분명 */ "
            update_text += "     , sch_inout_cd    /* 교내외구분코드 */ "
            update_text += "     , sch_inout_nm    /* 교내외구분명 */ "
            update_text += "     , activity_nm     /* 봉사명 */ "
            update_text += "     , manage_org_nm   /* 주관기관명 */ "
            update_text += "     , start_date      /* 시작일자 */ "
            update_text += "     , start_time      /* 시작시간 */ "
            update_text += "     , end_date        /* 종료일자 */ "
            update_text += "     , end_time        /* 종료시간 */ "
            update_text += "     , tot_time        /* 총시간 */ "
            update_text += "     , ins_id          /* 입력자id */ "
            update_text += "     , ins_ip          /* 입력자ip */ "
            update_text += "     , ins_dt          /* 입력일시 */ "
            update_text += "     , ins_pgm         /* 입력프로그램id */ "
            update_text += ") "
            update_text += "select '"+str(l_mp_id)+"' AS mp_id "
            update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
            update_text += "     , @curRank := @curRank +1 AS sa_no "
            update_text += "     , t1.apl_id          /* 학번 */ "
            update_text += "     , t1.apl_nm          /* 성명 */ "
            update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ "
            update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ "
            update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ "
            update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ "
            update_text += "     , t1.activity_nm     /* 봉사명 */ "
            update_text += "     , t1.manage_org_nm   /* 주관기관명 */ "
            update_text += "     , t1.start_date      /* 시작일자 */ "
            update_text += "     , t1.start_time      /* 시작시간 */ "
            update_text += "     , t1.end_date        /* 종료일자 */ "
            update_text += "     , t1.end_time        /* 종료시간 */ "
            update_text += "     , t1.tot_time        /* 총시간 */ "
            update_text += "     , '"+str(l_apl_id[i])+"' ins_id         /* 입력자id */ "
            update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
            update_text += "     , NOW() ins_dt         /* 입력일시 */ "
            update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
            update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ "
            update_text += "     , (SELECT @curRank := 0) r "
            update_text += " WHERE 1=1 "
            update_text += "   AND t1.apl_id = '"+str(l_apl_id[i])+"' "
            print("::_FROM_vw_nanum_foreign_exam::")
            print(update_text) 
            cursor = connection.cursor()
            query_result = cursor.execute(update_text)    

        # 팀원 자격증
        if not mtr_lc_chk:
            # -- 생성_자격증(mp_mtr_lc)_FROM_service20_vw_nanum_license
            update_text = "insert into service20_mp_mtr_lc      "
            update_text += "     ( mp_id           /* 멘토링 프로그램id */ "
            update_text += "     , apl_no          /* 지원 no */ "
            update_text += "     , lc_no           /* 자격 no */ "
            update_text += "     , apl_id          /* 학번 */ "
            update_text += "     , apl_nm          /* 성명 */ "
            update_text += "     , license_large_cd  "
            update_text += "     , license_large_nm  "
            update_text += "     , license_small_cd     "
            update_text += "     , license_small_nm     "
            update_text += "     , license_cd      "
            update_text += "     , license_nm    "        
            update_text += "     , ins_id          /* 입력자id */ "
            update_text += "     , ins_ip          /* 입력자ip */ "
            update_text += "     , ins_dt          /* 입력일시 */ "
            update_text += "     , ins_pgm         /* 입력프로그램id */ "
            update_text += ") "
            update_text += "select '"+str(l_mp_id)+"' AS mp_id "
            update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ "
            update_text += "     , @curRank := @curRank +1 AS lc_no "
            update_text += "     , t1.apl_id          /* 학번 */ "
            update_text += "     , t1.apl_nm          /* 성명 */ "
            update_text += "     , t1.license_large_cd  "
            update_text += "     , t1.license_large_nm  "
            update_text += "     , t1.license_small_cd     "
            update_text += "     , t1.license_small_nm     "
            update_text += "     , t1.license_cd      "
            update_text += "     , t1.license_nm    "        
            update_text += "     , '"+str(l_apl_id[i])+"' ins_id         /* 입력자id */ "
            update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ "
            update_text += "     , NOW() ins_dt         /* 입력일시 */ "
            update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ "
            update_text += "  FROM service20_vw_nanum_license t1      "
            update_text += "     , (SELECT @curRank := 0) r "
            update_text += " WHERE 1=1 "
            update_text += "   AND t1.apl_id = '"+str(l_apl_id[i])+"' "
            print("::_FROM_service20_vw_nanum_license::")
            print(update_text) 
            cursor = connection.cursor()
            query_result = cursor.execute(update_text)  

        # 팀원 추가
        if not team_mem_chk:
            model_instance_team_mem = mp_team_mem(
                mp_id=str(l_mp_id), 
                team_id=str(l_team_id),
                apl_no=int(apl_no),
                ins_id=str(l_apl_id[i]),
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today(),
                upd_id=str(l_apl_id[i]),
                upd_ip=str(client_ip),
                upd_dt=datetime.datetime.today(),
                )
            model_instance_team_mem.save()

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 
#####################################################################################
# MP0101M - END 
#####################################################################################




#####################################################################################
# MP0102M - START
#####################################################################################

# 학습외신청(멘토) 리스트 ###################################################
class MP0102M_list_Serializer(serializers.ModelSerializer):

    mp_name = serializers.SerializerMethodField()
    # mnte_no = serializers.SerializerMethodField()
    # mnte_id = serializers.SerializerMethodField()
    # mnte_nm = serializers.SerializerMethodField()
    spc_no = serializers.SerializerMethodField()
    spc_status = serializers.SerializerMethodField()
    spc_status_nm = serializers.SerializerMethodField()
    # mte_status = serializers.SerializerMethodField()
    mtr_status = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    # mte_mgr_id = serializers.SerializerMethodField()
    # mte_mgr_dt = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    spc_apl_no = serializers.SerializerMethodField()
    att_status = serializers.SerializerMethodField()
    att_no = serializers.SerializerMethodField()
    cncl_rsn = serializers.SerializerMethodField()
    cncl_nm = serializers.SerializerMethodField()
    sati_status = serializers.SerializerMethodField()
    appr_file = serializers.SerializerMethodField()
    # partici = serializers.SerializerMethodField()

    class Meta:
        model = mp_spc
        fields = '__all__'

    def get_mp_name(self, obj):
        return obj.mp_name
    # def get_mnte_no(self, obj):
    #     return obj.mnte_no
    # def get_mnte_id(self, obj):
    #     return obj.mnte_id
    # def get_mnte_nm(self, obj):
    #     return obj.mnte_nm
    def get_spc_no(self, obj):
        return obj.spc_no
    def get_spc_status(self, obj):
        return obj.spc_status
    def get_spc_status_nm(self, obj):
        return obj.spc_status_nm
    # def get_mte_status(self, obj):
    #     return obj.mte_status
    def get_mtr_status(self, obj):
        return obj.mtr_status
    def get_mgr_id(self, obj):
        return obj.mgr_id
    def get_mgr_dt(self, obj):
        return obj.mgr_dt
    # def get_mte_mgr_id(self, obj):
    #     return obj.mte_mgr_id
    # def get_mte_mgr_dt(self, obj):
    #     return obj.mte_mgr_dt
    def get_mgr_nm(self, obj):
        return obj.mgr_nm
    def get_apl_no(self, obj):
        return obj.apl_no
    def get_spc_apl_no(self, obj):
        return obj.spc_apl_no
    def get_att_status(self, obj):
        return obj.att_status
    def get_att_no(self, obj):
        return obj.att_no
    def get_cncl_rsn(self, obj):
        return obj.cncl_rsn
    def get_cncl_nm(self, obj):
        return obj.cncl_nm
    def get_sati_status(self, obj):
        return obj.sati_status
    def get_appr_file(self, obj):
        return obj.appr_file
    # def get_partici(self, obj):
    #     return obj.partici


class MP0102M_list(generics.ListAPIView):
    queryset = mp_spc.objects.all()
    serializer_class = MP0102M_list_Serializer

    # mp_spc

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('trn_term', "")
        l_status = request.GET.get('status', "")
        l_spc_div = request.GET.get('spc_div', "")
        l_apl_id = request.GET.get('apl_id', "")
        
        queryset = self.get_queryset()
        
        # query = "/* 학습외 프로그램별 멘티 조회 */    "
        # query += " select t2.id, t3.mp_id as mp_id "
        # query += "     , t6.mp_name as mp_name "
        # query += "     , t1.mnte_no as mnte_no "
        # query += "     , t1.mnte_id as mnte_id "
        # query += "     , t5.mnte_nm as mnte_nm "
        # query += "     , t3.spc_no as spc_no  "
        # query += "     , t2.spc_div as spc_div "
        # query += "     , t2.status as spc_status "
        # query += "     , t7.std_detl_code_nm as spc_status_nm "
        # query += "     , t1.status as mte_status "
        # query += "     , t3.status as mtr_status "
        # query += "     , t2.spc_name as spc_name "
        # query += "     , t3.mgr_id as mtr_mgr_id "
        # query += "     , t3.mgr_dt as mtr_mgr_dt "
        # query += "     , t1.appr_id as appr_id "
        # query += "     , t1.appr_dt as appr_dt "
        # query += "     , t1.appr_nm as appr_nm "
        # query += "     , t1.mgr_id as mte_mgr_id "
        # query += "     , t1.mgr_dt as mte_mgr_dt "
        # query += "     , t6.mgr_nm as mgr_nm "
        # query += "     , substring(t2.ins_dt, 1, 10) as ins_dt "
        # query += "     , t2.spc_intro as spc_intro "
        # query += "     , t2.yr as yr "
        # query += "     , t2.yr_seq as yr_seq "
        # query += "     , substring(t2.apl_ntc_fr_dt, 1, 10) as apl_ntc_fr_dt "
        # query += "     , substring(t2.apl_ntc_to_dt, 1, 10) as apl_ntc_to_dt "
        # query += "     , t2.apl_term as apl_term "
        # query += "     , substring(t2.apl_fr_dt, 1, 10) as apl_fr_dt "
        # query += "     , substring(t2.apl_to_dt, 1, 10) as apl_to_dt "
        # query += "     , case when t2.mnt_term = '10' then '1' "
        # query += "            else '2' end as mnt_term "
        # query += "     , substring(t2.mnt_fr_dt, 1, 10) as mnt_fr_dt "
        # query += "     , substring(t2.mnt_to_dt, 1, 10) as mnt_to_dt "
        # query += "     , substring(t2.cnf_dt, 1, 10) as cnf_dt "
        # query += "     , t2.appr_tm as appr_tm "
        # query += "     , t2.tot_apl as tot_apl "
        # query += "     , t2.cnt_apl as cnt_apl "
        # query += "     , t2.cnt_pln as cnt_pln "
        # query += "     , t2.cnt_att as cnt_att "
        # query += "     , t2.use_div as use_div "
        # query += "     , t2.pic_div as pic_div "
        # query += "     , t2.rep_div as rep_div "
        # query += "     , t2.ord_div as ord_div "
        # query += "     , t3.apl_no as apl_no "
        # query += "     , t3.spc_apl_no as spc_apl_no "
        # query += "     , t8.att_sts as att_status "
        # query += "     , t8.att_no as att_no "
        # query += "     , (select count(0) "
        # query += "          from service20_cm_surv_a st1 "
        # query += "          left join service20_cm_surv_h st2 on (st2.pgm_id = st1.pgm_id and st2.surv_seq = st1.surv_seq and st2.ansr_id = st1.ansr_id) "
        # query += "          left join service20_cm_surv_p st3 on (st3.pgm_id = st1.pgm_id) "
        # query += "         where st3.spc_no = t2.spc_no "
        # query += "     ) as sati_status "
        # query += "     , t9.std_detl_code_nm as cncl_rsn "
        # query += "     , t10.std_detl_code_nm as partici "
        # query += "  from service20_mp_spc_mte t1 "
        # query += "  left join service20_mp_spc t2 on (t2.mp_id = t1.mp_id and t2.spc_no = t1.spc_no) "
        # query += "  left join service20_mp_spc_mtr t3 on (t3.mp_id = t1.mp_id and t3.spc_no = t1.spc_no and t3.spc_apl_no = t1.spc_apl_no and t3.apl_no = t1.apl_no) "
        # query += "  left join service20_mp_mtr t4 on (t4.mp_id = t1.mp_id and t4.apl_no = t1.apl_no) "
        # query += "  left join service20_mp_mte t5 on (t5.mp_id = t1.mp_id and t5.mnte_no = t1.mnte_no and t5.apl_no = t1.apl_no) "
        # query += "  left join service20_mpgm t6 on (t6.mp_id = t1.mp_id) "
        # query += "  left join service20_com_cdd t7 on (t7.std_grp_code = 'MP0084' and t7.std_detl_code = t2.status) "
        # query += "  left join service20_mp_att t8 on (t8.mp_id = t1.mp_id and t8.apl_no = t1.apl_no and t8.spc_no = t2.spc_no) "
        # query += "  left join service20_com_cdd t9 on (t9.std_grp_code = 'MP0099' and t9.std_detl_code = t3.cncl_rsn) "
        # query += "  left join service20_com_cdd t10 on (t10.std_grp_code = 'MP0054' and t10.std_detl_code = t5.status) "
        # query += " where t2.yr = '" + str(l_yr) + "' "
        # query += "   and t2.apl_term = '" + str(l_apl_term) + "' "
        # query += "   and t2.spc_div like ifnull(nullif('" + str(l_spc_div) + "', ''), '%%') "
        # query += "   and t2.status like ifnull(nullif('" + str(l_status) + "', ''), '%%') "
        # query += "   and t3.apl_id = trim('" + str(l_apl_id) + "') "

        query = f"""
                SELECT t1.id
                    , t1.mp_id AS mp_id
                    , t1.spc_no AS spc_no
                    , t3.mp_name AS mp_name
                    , t1.spc_name AS spc_name
                    , t1.spc_div AS spc_div
                    , SUBSTRING(t1.ins_dt, 1, 10) AS ins_dt
                    , t3.mgr_nm AS mgr_nm
                    , CASE WHEN t1.mnt_term = '10' THEN '1'
                            ELSE '2' END AS mnt_term
                    , SUBSTRING(t1.apl_fr_dt, 1, 10) AS apl_fr_dt
                    , SUBSTRING(t1.apl_to_dt, 1, 10) AS apl_to_dt
                    , SUBSTRING(t1.mnt_fr_dt, 1, 10) AS mnt_fr_dt
                    , SUBSTRING(t1.mnt_to_dt, 1, 10) AS mnt_to_dt
                    , t1.status AS spc_status  /* 학습외 프로그램의 상태 */
                    , t5.std_detl_code_nm AS spc_status_nm
                    , t1.appr_tm AS appr_tm
                    , t1.cnt_apl AS cnt_apl
                    , t1.tot_apl AS tot_apl
                    , t2.spc_apl_no AS spc_apl_no
                    , t2.apl_no AS apl_no
                    , t2.status AS mtr_status  /* 신청, 취소, 선발 여부 확인 */
                    , t2.cncl_rsn AS cncl_rsn
                    , t6.std_detl_code_nm AS cncl_nm
                    , t2.mgr_id AS mgr_id
                    , SUBSTRING(t2.mgr_dt, 1, 10) AS mgr_dt
                    , SUBSTRING(t1.cnf_dt, 1, 10) AS cnf_dt
                    , t4.att_sts AS att_status
                    , t4.att_no AS att_no
                    , t2.appr_file as appr_file
                    , (select st2.status
                        from service20_cm_surv_a st1
                        left join service20_cm_surv_h st2 on (st2.pgm_id = st1.pgm_id and st2.surv_seq = st1.surv_seq and st2.ansr_id = st1.ansr_id)
                        left join service20_cm_surv_p st3 on (st3.pgm_id = st1.pgm_id)
                        where st3.spc_no = t1.spc_no
                        AND st1.ansr_id = t2.apl_id) AS sati_status
                    , t1.atc_file_url as atc_file_url
                FROM service20_mp_spc t1
                LEFT JOIN service20_mp_spc_mtr t2 on (t2.mp_id = t1.mp_id AND t2.spc_no = t1.spc_no)
                LEFT JOIN service20_mpgm t3 ON (t3.mp_id = t1.mp_id)
                LEFT JOIN service20_mp_att t4 ON (t4.mp_id = t1.mp_id AND t4.apl_no = t2.apl_no and t4.spc_no = t1.spc_no)
                LEFT JOIN service20_com_cdd t5 ON (t5.std_grp_code = 'MP0084' AND t5.std_detl_code = t1.status)
                LEFT JOIN service20_com_cdd t6 ON (t6.std_grp_code = 'MP0099' AND t6.std_detl_code = t2.cncl_rsn)
                WHERE t1.yr = '{l_yr}'
                AND t1.apl_term = '{l_apl_term}'
                AND t1.spc_div LIKE ifnull(NULLIF('{l_spc_div}', ''), '%%')
                AND t1.status LIKE ifnull(NULLIF('{l_status}', ''), '%%')
                AND t2.apl_id = TRIM('{l_apl_id}')
                order by t1.mp_id desc
        """

        print(query)
        queryset = mp_spc.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학습외신청(멘티) 리스트 ###################################################
class MP0102M_mentee_list_Serializer(serializers.ModelSerializer):

    mnte_nm = serializers.SerializerMethodField()
    sati_status = serializers.SerializerMethodField()
    spc_status = serializers.SerializerMethodField()

    class Meta:
        model = mp_spc_mte
        fields = '__all__'

    def get_mnte_nm(self, obj):
        return obj.mnte_nm
    def get_sati_status(self, obj):
        return obj.sati_status
    def get_spc_status(self, obj):
        return obj.spc_status

class MP0102M_mentee_list(generics.ListAPIView):
    queryset = mp_spc_mte.objects.all()
    serializer_class = MP0102M_mentee_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_spc_no = request.GET.get('spc_no', "")
        l_spc_apl_no = request.GET.get('spc_apl_no', "")
        
        queryset = self.get_queryset()

        query = f"""
                SELECT t1.id AS id
                    , t1.mp_id AS mp_id
                    , t1.mnte_id AS mnte_id
                    , t1.spc_no AS spc_no
                    , t1.spc_apl_no AS spc_apl_no
                    , t1.mnte_no AS mnte_no
                    , t1.status AS status
                    , t4.std_detl_code_nm as mte_status
                    , t1.appr_file AS appr_file
                    , t1.appr_dt AS appr_dt
                    , t2.mnte_nm AS mnte_nm
                    , (select st2.status
                        from service20_cm_surv_a st1
                        left join service20_cm_surv_h st2 on (st2.pgm_id = st1.pgm_id and st2.surv_seq = st1.surv_seq and st2.ansr_id = st1.ansr_id)
                        left join service20_cm_surv_p st3 on (st3.pgm_id = st1.pgm_id)
                        where st3.spc_no = t1.spc_no
                        AND st1.ansr_id = t1.mnte_id) AS sati_status
                    , t3.status as spc_status
                FROM service20_mp_spc_mte t1
                LEFT JOIN service20_mp_mte t2 ON (t2.mp_id = t1.mp_id AND t2.mnte_no = t1.mnte_no)
                LEFT JOIN service20_mp_spc t3 ON (t3.mp_id = t1.mp_id AND t3.spc_no = '{l_spc_no}')
                LEFT JOIN service20_com_cdd t4 ON (t4.std_detl_code = "MP0084" AND t4.std_detl_code = t3.status)
                WHERE t1.mp_id = '{l_mp_id}'
                AND t1.spc_no = '{l_spc_no}'
                AND t1.spc_apl_no = '{l_spc_apl_no}'
                AND t3.spc_div <> 'B'
        """

        print(query)
        queryset = mp_spc_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학습외신청(멘토) 학습외 신청 및 취소 ###################################################
@csrf_exempt
def MP0102M_mento_update(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = '/NANUM/www/img/spc/mtr/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_no = request.POST.get('mtr_no', "")
        l_mp_id = request.POST.get('mtr_mp_id', "")    
        l_apl_no = request.POST.get('mtr_apl_no', "")
        l_spc_no = request.POST.get('mtr_spc_no', "")
        l_spc_apl_no = request.POST.get('mtr_spc_apl_no', "")
        l_spc_status = request.POST.get('mtr_spc_status', "")
        l_cncl_rsn = request.POST.get('mtr_cncl_rsn', "")

        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")

        client_ip = request.META['REMOTE_ADDR']
        
        try:
            file = request.FILES['mtr_appr_file' + str(l_no)]
        except MultiValueDictKeyError:
            file = False

        if file != False:
            # 불참
            if l_spc_status == '49':
                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/spc/mtr/"+ str(n_filename)

                query = " /* 학습외 신청 불참 */ "
                query += " update service20_mp_spc_mtr "
                query += "   set status = '" + l_spc_status + "' "
                query += "     , mgr_dt = null "
                query += "     , appr_file = null "
                query += "     , upd_id = '" + upd_id + "' "
                query += "     , upd_ip = '" + client_ip + "' "
                query += "     , upd_dt = now() "
                query += "     , upd_pgm = '" + upd_pgm + "' "
                query += " where mp_id = '" + l_mp_id + "' "
                query += "   and apl_no = '" + l_apl_no + "' "
                query += "   and spc_no = '" + l_spc_no + "' "
                query += "   and spc_apl_no = '" + l_spc_apl_no + "' "

                cursor.execute(query)
            else:
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_apl_no) + str(l_spc_no) + str(l_spc_apl_no) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
            
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/spc/mtr/"+ str(n_filename)

                query = " /* 학습외 신청 및 취소 */ "
                query += " update service20_mp_spc_mtr "
                query += "   set status = '" + l_spc_status + "' "
                query += "     , cncl_rsn = '" + l_cncl_rsn + "' "
                query += "     , appr_file = '" + str(fullFile) + "' "
                query += "     , upd_id = '" + upd_id + "' "
                query += "     , upd_ip = '" + client_ip + "' "
                query += "     , upd_dt = now() "
                query += "     , upd_pgm = '" + upd_pgm + "' "
                query += " where mp_id = '" + l_mp_id + "' "
                query += "   and apl_no = '" + l_apl_no + "' "
                query += "   and spc_no = '" + l_spc_no + "' "
                query += "   and spc_apl_no = '" + l_spc_apl_no + "' "

                cursor.execute(query)
        else:
            cursor = connection.cursor()

            query = " /* 학습외 신청 및 취소 */ "
            query += " update service20_mp_spc_mtr "
            query += "   set status = '" + l_spc_status + "' "
            query += "     , cncl_rsn = '" + l_cncl_rsn + "' "
            query += "     , mgr_dt = null "
            query += "     , appr_file = null "
            query += "     , upd_id = '" + upd_id + "' "
            query += "     , upd_ip = '" + client_ip + "' "
            query += "     , upd_dt = now() "
            query += "     , upd_pgm = '" + upd_pgm + "' "
            query += " where mp_id = '" + l_mp_id + "' "
            query += "   and apl_no = '" + l_apl_no + "' "
            query += "   and spc_no = '" + l_spc_no + "' "
            query += "   and spc_apl_no = '" + l_spc_apl_no + "' "
            
            cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 학습외신청(멘티) 학습외 신청 및 취소 ###################################################
@csrf_exempt
def MP0102M_mentee_update(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = '/NANUM/www/img/spc/mte/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_no = request.POST.get('mte_no', "")
        l_mp_id = request.POST.get('mte_mp_id', "")
        l_mnte_no = request.POST.get('mte_mnte_no', "")
        l_spc_no = request.POST.get('mte_spc_no', "")
        l_spc_apl_no = request.POST.get('mte_spc_apl_no', "")
        l_spc_status = request.POST.get('mte_spc_status', "")
        # l_cncl_rsn = request.POST.get('cncl_rsn', "")

        ins_id = request.POST.get('ins_id', "")
        ins_ip = request.POST.get('ins_ip', "")
        ins_dt = request.POST.get('ins_dt', "")
        ins_pgm = request.POST.get('ins_pgm', "")
        upd_id = request.POST.get('upd_id', "")
        upd_ip = request.POST.get('upd_ip', "")
        upd_dt = request.POST.get('upd_dt', "")
        upd_pgm = request.POST.get('upd_pgm', "")

        client_ip = request.META['REMOTE_ADDR']

        try:
            file = request.FILES['appr_file' + str(l_no)]
        except MultiValueDictKeyError:
            file = False

        if file != False:
            # 불참
            if l_spc_status == '49':
                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/spc/mte/"+ str(n_filename)

                query = " /* 학습외 신청 */ "
                query += " update service20_mp_spc_mte "
                query += "   set status = '" + l_spc_status + "' "
                query += "     , appr_id = null "
                query += "     , appr_nm = null "
                query += "     , appr_dt = null "
                query += "     , appr_file = null "
                query += "     , upd_id = '" + upd_id + "' "
                query += "     , upd_ip = '" + client_ip + "' "
                query += "     , upd_dt = now() "
                query += "     , upd_pgm = '" + upd_pgm + "' "
                query += " where mp_id = '" + l_mp_id + "' "
                query += "   and mnte_no = '" + l_mnte_no + "' "
                query += "   and spc_no = '" + l_spc_no + "' "
                query += "   and spc_apl_no = '" + l_spc_apl_no + "' "

                cursor.execute(query)
            else:
                print(file)
                filename = file._name
                n_filename = str(l_mp_id) + str(l_mnte_no) + str(l_spc_no) + str(l_spc_apl_no) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
            
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/spc/mte/"+ str(n_filename)

                query = " /* 학습외 신청 */ "
                query += " update service20_mp_spc_mte "
                query += "   set status = '" + l_spc_status + "' "
                query += "     , appr_id = (select grd_id from service20_mp_mte where mp_id = '" + l_mp_id + "' and mnte_no = '" + l_mnte_no + "') "
                query += "     , appr_nm = (select grd_nm from service20_mp_mte where mp_id = '" + l_mp_id + "' and mnte_no = '" + l_mnte_no + "') "
                query += "     , appr_dt = now() "
                query += "     , appr_file = '" + str(fullFile) + "' "
                query += "     , upd_id = '" + upd_id + "' "
                query += "     , upd_ip = '" + client_ip + "' "
                query += "     , upd_dt = now() "
                query += "     , upd_pgm = '" + upd_pgm + "' "
                query += " where mp_id = '" + l_mp_id + "' "
                query += "   and mnte_no = '" + l_mnte_no + "' "
                query += "   and spc_no = '" + l_spc_no + "' "
                query += "   and spc_apl_no = '" + l_spc_apl_no + "' "

                cursor.execute(query)
        else:
            cursor = connection.cursor()

            query = " /* 학습외 취소 */ "
            query += " update service20_mp_spc_mte "
            query += "   set status = '" + l_spc_status + "' "
            query += "     , appr_id = null "
            query += "     , appr_nm = null "
            query += "     , appr_dt = null "
            query += "     , appr_file = null "
            query += "     , upd_id = '" + upd_id + "' "
            query += "     , upd_ip = '" + client_ip + "' "
            query += "     , upd_dt = now() "
            query += "     , upd_pgm = '" + upd_pgm + "' "
            query += " where mp_id = '" + l_mp_id + "' "
            query += "   and mnte_no = '" + l_mnte_no + "' "
            query += "   and spc_no = '" + l_spc_no + "' "
            query += "   and spc_apl_no = '" + l_spc_apl_no + "' "
            
            cursor.execute(query)

    print(query)

    return HttpResponse('File Uploaded')

# 학습외신청(멘토) 보호자 승인 양식 detail set ###################################################
class MP0102M_mento_report_Serializer(serializers.ModelSerializer):

    grd_rel = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    t_gen = serializers.SerializerMethodField()
    m_gen = serializers.SerializerMethodField()
    t_mob_no = serializers.SerializerMethodField()
    m_mob_no = serializers.SerializerMethodField()
    spc_name = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = '__all__'

    def get_grd_rel(self, obj):
        return obj.grd_rel
    def get_apl_id(self, obj):
        return obj.apl_id
    def get_apl_nm(self, obj):
        return obj.apl_nm
    def get_mnte_nm(self, obj):
        return obj.mnte_nm
    def get_t_gen(self, obj):
        return obj.t_gen
    def get_m_gen(self, obj):
        return obj.m_gen
    def get_t_mob_no(self, obj):
        return obj.t_mob_no
    def get_m_mob_no(self, obj):
        return obj.m_mob_no
    def get_spc_name(self, obj):
        return obj.spc_name
    def get_dept_nm(self, obj):
        return obj.dept_nm
    def get_mp_name(self, obj):
        return obj.mp_name

class MP0102M_mento_report(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = MP0102M_mento_report_Serializer

    # mp_spc

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_mnte_no = request.GET.get('mnte_no', "")
        l_spc_no = request.GET.get('spc_no', "")
        l_spc_apl_no = request.GET.get('spc_apl_no', "")
        
        queryset = self.get_queryset()
        
        query = "/* 보호자승인  확인서 */ "
        query += " select t4.id as id "
        query += "     , t1.mp_id as mp_id "
        query += "     , t1.mnte_no as mnte_no "
        query += "     , t1.mnte_id as mnte_id "
        query += "     , t4.mnte_nm as mnte_nm "
        query += "     , t4.mnte_nm_e as mnte_nm_e "
        query += "     , t5.dept_nm as dept_nm "
        query += "     , t4.sch_nm as sch_nm "
        query += "     , t4.sch_yr as sch_yr "
        query += "     , t4.mob_no as t_mob_no "
        query += "     , t4.h_addr as h_addr "
        query += "     , case when t4.gen = 'm' then '남' "
        query += "            else '여' end as t_gen "
        query += "     , t4.grd_tel as grd_tel "
        query += "     , t6.std_detl_code_nm as grd_rel "
        query += "     , t2.apl_no as apl_no "
        query += "     , t2.apl_id as apl_id "
        query += "     , t5.apl_nm as apl_nm "
        query += "     , t5.mob_no as m_mob_no "
        query += "     , case when t5.gen = 'm' then '남' "
        query += "            else '여' end as m_gen "
        query += "     , t3.spc_name as spc_name "
        query += "     , t7.mp_name as mp_name "
        query += "     , t4.yr as yr "
        query += "  from service20_mp_spc_mte t1 "
        query += "  left join service20_mp_spc_mtr t2 on (t2.mp_id = t1.mp_id and t2.apl_no = t1.apl_no and t2.spc_no = t1.spc_no and t2.spc_apl_no = t1.spc_apl_no) "
        query += "  left join service20_mp_spc t3 on (t3.mp_id = t1.mp_id and t3.spc_no = t1.spc_no) "
        query += "  left join service20_mp_mte t4 on (t4.mp_id = t1.mp_id and t4.mnte_no = t1.mnte_no and t4.apl_no = t1.apl_no) "
        query += "  left join service20_mp_mtr t5 on (t5.mp_id = t1.mp_id and t5.apl_no = t1.apl_no) "
        query += "  left join service20_com_cdd t6 on (t6.std_grp_code = 'MP0047' and t6.std_detl_code = t4.grd_rel) "
        query += "  left join service20_mpgm t7 on (t7.mp_id = t1.mp_id) "
        query += " where t1.mp_id = '" + l_mp_id + "' "
        query += "   and t1.mnte_no = '" + l_mnte_no + "' "
        query += "   and t1.spc_no = '" + l_spc_no + "' "
        query += "   and t1.spc_apl_no = '" + l_spc_apl_no + "' "

        print(query)

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 학습외신청(멘토) 취소사유 콤보 ###################################################
class MP0102M_mento_cncl_Serializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = com_cdd
        fields = '__all__'

    def get_testField(self, obj):
        return 'test'     


class MP0102M_mento_cncl(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0102M_mento_cncl_Serializer

    # mp_spc

    def list(self, request):
        queryset = self.get_queryset()
        
        query = "select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm "
        query += "union "
        query += "select id, std_detl_code, std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0099'; "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

######################################################################

#####################################################################################
# MP0102M - END
#####################################################################################


#####################################################################################
# MP0103M - START
#####################################################################################

# 프로그램 수행계획서 리스트 ###################################################
class MP0103M_v1_Serializer(serializers.ModelSerializer):

    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mpgm
        fields = ('mp_id','mnt_fr_dt','mnt_to_dt')
      


class MP0103M_v1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_v1_Serializer

    def list(self, request):
        mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query = " select t1.mp_id,t1.mnt_fr_dt"
        query += "      , t1.mnt_to_dt"
        query += "   from service20_mpgm t1"
        query += "  where t1.mp_id  = '" + mp_id +"'"

        

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 리스트 ###################################################
class MP0103M_list_Serializer(serializers.ModelSerializer):

    mnte_nm = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    pln_dt = serializers.SerializerMethodField()
    appr_nm = serializers.SerializerMethodField()
    appr_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    pln_dt = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    pln_sedt = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_sedt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = '__all__'
    
    def get_mnte_nm(self,obj):
        return obj.mnte_nm  
    def get_sch_nm(self,obj):
        return obj.sch_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_pln_dt(self,obj):
        return obj.pln_dt
    def get_appr_nm(self,obj):
        return obj.appr_nm
    def get_appr_dt(self,obj):
        return obj.appr_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_mgr_dt(self,obj):
        return obj.mgr_dt
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_tchr_nm(self,obj):
        return obj.tchr_nm
    def get_pln_dt(self,obj):
        return obj.pln_dt
    def get_mtr_sub(self,obj):
        return obj.mtr_sub
    def get_pln_sedt(self,obj):
        return obj.pln_sedt
    def get_apl_no(self,obj):
        return obj.apl_no    
    def get_status(self,obj):
        return obj.status  
    


class MP0103M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_list_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query = " select b.mp_id      AS mp_id "
        query += " , b.mp_name    AS mp_name "
        query += " , b.apl_term   AS apl_term "
        query += " , b.yr_seq     AS yr_seq "
        query += " , c.mnte_nm    AS mnte_nm "
        query += " , c.sch_nm     AS sch_nm "
        query += " , c.sch_yr     AS sch_yr "
        query += " , a.pln_dt     AS pln_dt "
        query += " , a.appr_nm    AS appr_nm "
        query += " , a.appr_dt    AS appr_dt "
        query += " , a.mgr_id     AS mgr_id "
        query += " , b.mgr_nm     AS mgr_nm "
        query += " , a.mgr_dt     AS mgr_dt "
        query += " , d.apl_id     AS apl_id "
        query += " , d.apl_nm     AS apl_nm "
        query += " , c.tchr_nm    AS tchr_nm "
        query += " , a.mtr_sub     AS mtr_sub "
        query += " , d.apl_no     AS apl_no "
        query += " , a.status     AS status "
        query += " , (SELECT concat(pln_sdt, CONCAT('~', pln_edt)) FROM service20_mp_plnd WHERE mp_id = a.mp_id AND apl_no = a.apl_no LIMIT 1) AS pln_sedt "
        query += " from service20_mp_plnh a "
        query += " , service20_mpgm b "
        query += " , service20_mp_mte c "
        query += " , (SELECT mp_id "
        query += " , apl_no "
        query += " , apl_id "
        query += " , apl_nm "
        query += " FROM service20_mp_mtr "
        query += " WHERE (mntr_id = '"+l_user_id+"' or apl_id = '"+l_user_id+"') "
        query += " AND mp_id like Ifnull(Nullif('"+str(l_mp_id)+"', ''), '%%') ) d "
        query += " WHERE a.mp_id = b.mp_id "
        query += " AND a.mp_id = c.mp_id "
        query += " AND a.mp_id = d.mp_id "
        query += " AND a.apl_no = d.apl_no "
        query += " AND d.apl_no = c.apl_no "

        

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 상세 ###################################################
class MP0103M_Detail_Serializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = mp_plnd
        fields = '__all__'

    def get_status(self, obj):
        return obj.status


class MP0103M_Detail(generics.ListAPIView):
    queryset = mp_plnd.objects.all()
    serializer_class = MP0103M_Detail_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        

        query = " select b.id as id"
        query += "     , b.pln_no     AS pln_no"
        query += "     , b.mtr_desc   AS mtr_desc"
        query += "     , a.status AS status"
        query += " from service20_mp_plnh a"
        query += " , service20_mp_plnd b"
        query += " , (SELECT mp_id"
        query += " , apl_no"
        query += " FROM service20_mp_mtr"
        query += " WHERE mp_id = '"+l_mp_id+"'"
        query += " AND ( apl_id = '"+l_user_id+"') ) c"
        query += " WHERE a.mp_id = b.mp_id"
        query += "    AND a.mp_id = c.mp_id"
        query += "    AND a.apl_no = b.apl_no"
        query += "    AND a.apl_no = c.apl_no"

        print(query)
        queryset = mp_plnd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 프로그램 수행계획서 작성 폼 데이터 ###################################################
class MP0103M_Detail_v2_Serializer(serializers.ModelSerializer):

    tchr_nm = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    pln_time  = serializers.SerializerMethodField()
    appr_nm  = serializers.SerializerMethodField()
    appr_dt  = serializers.SerializerMethodField()
    mgr_nm  = serializers.SerializerMethodField()
    mgr_dt  = serializers.SerializerMethodField()
    status  = serializers.SerializerMethodField()
    mnte_nm  = serializers.SerializerMethodField()
    min_len_mp_plnd_mtr_desc  = serializers.SerializerMethodField()
    max_len_mp_plnd_mtr_desc  = serializers.SerializerMethodField() 

    class Meta:
        model = mp_mtr
        fields = ('apl_no', 'apl_nm','apl_id','tchr_nm','sch_nm','mtr_sub','pln_time', 'appr_nm', 'appr_dt', 'mgr_nm', 'mgr_dt', 'status', 'mnte_nm', 'min_len_mp_plnd_mtr_desc', 'max_len_mp_plnd_mtr_desc')
      
    def get_tchr_nm(self, obj):
        return obj.tchr_nm
    def get_sch_nm(self, obj):
        return obj.sch_nm
    def get_mtr_sub(self, obj):
        return obj.mtr_sub
    def get_pln_time(self, obj):
        return obj.pln_time
    def get_appr_nm(self, obj):
        return obj.appr_nm
    def get_appr_dt(self, obj):
        return obj.appr_dt
    def get_mgr_nm(self, obj):
        return obj.mgr_nm
    def get_mgr_dt(self, obj):
        return obj.mgr_dt
    def get_status(self, obj):
        return obj.status
    def get_mnte_nm(self, obj):
        return obj.mnte_nm
    def get_min_len_mp_plnd_mtr_desc(self, obj):
        return obj.min_len_mp_plnd_mtr_desc
    def get_max_len_mp_plnd_mtr_desc(self, obj):
        return obj.max_len_mp_plnd_mtr_desc

class MP0103M_Detail_v2(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0103M_Detail_v2_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        # apl_id = request.GET.get('apl_id', "")
        apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()
    
        query = " /* 프로그램 수행계획서 작성 폼 데이터 */ "
        query += " select t1.id as id "
        query += "      , t4.apl_id as apl_id "
        query += "      , t4.apl_no as apl_no "
        query += "      , t4.apl_nm as apl_nm "
        query += "      , t3.tchr_nm as tchr_nm "
        query += "      , t3.sch_nm as sch_nm "
        query += "      , t1.mtr_sub as mtr_sub "
        query += "      , t5.att_val as pln_time "
        query += "      , t1.appr_nm as appr_nm "
        query += "      , date_format(t1.appr_dt, '%%y-%%m-%%d %%h:%%i:%%s') as appr_dt "
        query += "      , t2.mgr_nm as mgr_nm "
        query += "      , date_format(t1.mgr_dt, '%%y-%%m-%%d %%h:%%i:%%s') as mgr_dt "
        query += "      , t1.status as status "
        query += "      , fn_mp_mte_select_01(t1.mp_id, t1.apl_no) AS mnte_nm "
        query += "      , fn_mp_sub_att_val_select_01(t1.mp_id, 'CL0001', 'MS0028', '10') min_len_mp_plnd_mtr_desc /* 멘토링 내용(MTR_DESC) - 프로그램 수행 계획서 상세(MP_PLND) */ "
        query += "      , fn_mp_sub_att_val_select_01(t1.mp_id, 'CL0001', 'MS0029', '10') max_len_mp_plnd_mtr_desc /* 멘토링 내용(MTR_DESC) - 프로그램 수행 계획서 상세(MP_PLND) */ "
        query += "   from service20_mp_plnh t1 "
        query += "   left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += "   left join service20_mp_mte t3 on (t3.mp_id = t1.mp_id and t3.apl_no = t1.apl_no) "
        query += "   left join service20_mp_mtr t4 on (t4.mp_id = t1.mp_id and t4.apl_no = t1.apl_no) "
        query += "   left join service20_mp_sub t5 on (t5.mp_id = t1.mp_id and t5.att_id = 'MP0007' and att_cdh = 'MP0007' and att_cdd = '10') "
        query += "  where t1.mp_id = '" + l_mp_id + "' "
        query += "    and t4.apl_id = '" + apl_id + "' "

        print(query)

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 계획서 최초 작성 시 주차 수를 셋팅
class MP0103M_list_v1_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = mp_sub
        fields = ('id','mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq')
    

class MP0103M_list_v1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_list_v1_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query = " select t2.id,t2.att_val AS att_val "
        query += " FROM service20_mp_mtr t1 "
        query += " LEFT JOIN service20_mp_sub t2 ON (t2.mp_id = t1.mp_id "
        query += " AND t2.att_id= 'MP0013' "
        query += " AND t2.att_cdh = 'MP0013' "
        query += " AND t2.att_cdd = '20') "
        query += " WHERE t1.mp_id = '"+l_mp_id+"' "
        query += " AND t1.apl_id='"+l_apl_id+"' "

        print(query)
        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 Insert
@csrf_exempt
@transaction.atomic
def MP0103M_Insert(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    pln_no = request.POST.get('pln_no', 0)
    pln_sdt = request.POST.get('pln_sdt', "")
    pln_edt = request.POST.get('pln_edt', "")
    mtr_desc = request.POST.get('mtr_desc', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    mnt_fr_dt = request.POST.get('mnt_fr_dt', "")
    mnt_to_dt = request.POST.get('mnt_to_dt', "")

    maxRow = request.POST.get('maxRow', 0)              # 1번 insert
    
    client_ip = request.META['REMOTE_ADDR']

    row_max = int(maxRow)
    insert_text = ""
    try:
        with transaction.atomic():
            update_text = " update service20_mp_plnh a "
            update_text += " , service20_mpgm b "
            update_text += " , service20_mp_mte c "
            update_text += " , (SELECT mp_id "
            update_text += " , apl_no "
            update_text += " , apl_id "
            update_text += " , apl_nm "
            update_text += " FROM service20_mp_mtr "
            update_text += " WHERE apl_id = '"+apl_id+"' "
            update_text += " AND apl_no = '"+apl_no+"') d "
            update_text += " SET a.pln_dt = NOW() "
            update_text += "   , a.status = '10' "
            update_text += "   , a.upd_id = '" + upd_id + "' "
            update_text += "   , a.upd_ip = '" + client_ip + "' "
            update_text += "   , a.upd_pgm = '" + upd_pgm + "' "
            update_text += "   , a.upd_dt = now() "
            update_text += " WHERE a.mp_id = b.mp_id "
            update_text += " AND a.mp_id = c.mp_id "
            update_text += " AND a.mp_id = d.mp_id "
            update_text += " AND a.apl_no = d.apl_no "
            update_text += " AND d.apl_no = c.apl_no "
            
            cursor = connection.cursor()
            query_result = cursor.execute(update_text)

            for i in range(0,row_max):
            
                # pln_no_max = mp_plnd.objects.all().aggregate(vlMax=Max('pln_no'))
                
                # apl_no = 0
                
                # max_no = mp_plnd_max['vlMax']    

                # if max_no == None:
                #     apl_no = 0
                # else:
                #     apl_no = mp_plnd_max['vlMax']
                #     apl_no = apl_no + 1

                mtr_desc = request.POST.get('mtr_desc'+str(i), "")
                pln_no = request.POST.get('pln_no'+str(i+1), "")

                insert_text = f"""
                                insert into service20_mp_plnd (
                                mp_id 
                                , apl_no
                                , pln_no 
                                , pln_sdt 
                                , pln_edt 
                                /*, mtr_desc*/
                                , ins_id 
                                , ins_ip 
                                , ins_dt 
                                , ins_pgm 
                                , upd_id 
                                , upd_ip 
                                , upd_dt 
                                , upd_pgm 
                                ) 
                                ( select 
                                '{mp_id}' 
                                , '{apl_no}' 
                                , '{pln_no}' 
                                , adddate(t2.mnt_fr_dt, 7*({pln_no}*1-1) + 0) pln_sdt 
                                , adddate(t2.mnt_fr_dt, 7*({pln_no}*1-1) + 6) pln_edt 
                                /*, '{mtr_desc}'*/
                                , '{apl_id}' 
                                , '{client_ip}' 
                                , now() 
                                , '{ins_pgm}' 
                                , '{apl_id}' 
                                , '{client_ip}' 
                                , now() 
                                , '{upd_pgm}'
                                from service20_mp_mtr t1 
                                left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) 
                                where t1.mp_id = '{mp_id}' 
                                and apl_id = '{apl_id}' 
                                );
                """
                # insert_text += " insert into service20_mp_plnd ( "
                # insert_text += " mp_id "
                # insert_text += " , apl_no "
                # insert_text += " , pln_no "
                # insert_text += " , pln_sdt "
                # insert_text += " , pln_edt "
                # insert_text += " , mtr_desc "
                # insert_text += " , ins_id "
                # insert_text += " , ins_ip "
                # insert_text += " , ins_dt "
                # insert_text += " , ins_pgm "
                # insert_text += " , upd_id "
                # insert_text += " , upd_ip "
                # insert_text += " , upd_dt "
                # insert_text += " , upd_pgm "
                # insert_text += " ) "
                # insert_text += "  ( select "
                # insert_text += " '"+str(mp_id)+"' "
                # insert_text += " , '"+str(apl_no)+"' "
                # insert_text += " , '"+str(pln_no)+"' "
                # insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 0) pln_sdt "
                # insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 6) pln_edt "
                # insert_text += " , '"+str(mtr_desc)+"' "
                # insert_text += " , '"+str(apl_id)+"' "
                # insert_text += " , '"+str(client_ip)+"' "
                # insert_text += " , now() "
                # insert_text += " , '"+str(ins_pgm)+"' "
                # insert_text += " , '"+str(apl_id)+"' "
                # insert_text += " , '"+str(client_ip)+"' "
                # insert_text += " , now() "
                # insert_text += " , '"+str(upd_pgm)+"' "
                # insert_text += " from service20_mp_mtr t1 "
                # insert_text += " left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
                # insert_text += " where t1.mp_id = '"+str(mp_id)+"' "
                # insert_text += " and apl_id = '"+str(apl_id)+"' "
                # insert_text += " ) "
                print(insert_text)

                cursor = connection.cursor()
                query_result = cursor.execute(insert_text)    

                mp_plnd.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),pln_no=str(pln_no)).update(mtr_desc=str(mtr_desc))
        
        context = {'message': 'true'}
    except Exception:
        context = {'message': 'false'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


# 프로그램 수행계획서 Update
@csrf_exempt
@transaction.atomic
def MP0103M_Update(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    pln_no = request.POST.get('pln_no', 0)

    mtr_desc = request.POST.get('mtr_desc', "")
    mtr_sub = request.POST.get('mtr_sub', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    

    maxRow = request.POST.get('maxRow', 0)
    client_ip = request.META['REMOTE_ADDR']

    row_max = int(maxRow)

    try:
        with transaction.atomic():
            ####################################
            # 1번쿼리
            ####################################
            update_text = " update service20_mp_plnh "
            # update_text += " SET mtr_sub = '"+str(mtr_sub)+"' "
            # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
            # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
            update_text += " set pln_dt = now() "
            update_text += " , upd_id = '"+str(apl_id)+"' "
            update_text += " , upd_ip = '"+str(client_ip)+"' "
            update_text += " , upd_dt = now() "
            update_text += " , upd_pgm = '"+str(upd_pgm)+"' "
            update_text += " WHERE mp_id = '"+str(mp_id)+"' "
            # update_text += " AND apl_no = '"+str(apl_no)+"' "
            update_text += " AND apl_no = '"+str(apl_no)+"' "

            mp_plnh.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no)).update(mtr_sub=str(mtr_sub))

            print(update_text)
            cursor = connection.cursor()
            query_result = cursor.execute(update_text)    
            
            ####################################
            # 1번쿼리
            ####################################

            update_text = ""
            for i in range(0,row_max):

                mtr_desc = request.POST.get('mtr_desc'+str(i), "")
                pln_no = request.POST.get('pln_no'+str(i+1), "")

                ####################################
                # 2번쿼리
                ####################################
                update_text = f"""
                            update service20_mp_plnd 
                            /*SET mtr_desc = '{mtr_desc}' */
                                set upd_id = '{apl_id}' 
                                , upd_ip = '{client_ip}' 
                                , upd_dt = now() 
                                , upd_pgm = '{upd_pgm}' 
                            WHERE mp_id = '{mp_id}' 
                            AND apl_no = '{apl_no}' 
                            AND pln_no = '{pln_no}'
                            ;
                """
                # update_text += " update service20_mp_plnd "
                # update_text += " SET mtr_desc = '"+str(mtr_desc)+"' "
                # # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
                # # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "        
                # update_text += " , upd_id = '"+str(apl_id)+"' "
                # update_text += " , upd_ip = '"+str(client_ip)+"' "
                # update_text += " , upd_dt = now() "
                # update_text += " , upd_pgm = '"+str(upd_pgm)+"' "
                # update_text += " WHERE mp_id = '"+str(mp_id)+"' "
                # # update_text += " AND apl_no = '"+str(apl_no)+"' "
                # update_text += " AND apl_no = '"+str(apl_no)+"' "
                # update_text += " AND pln_no = '"+str(pln_no)+"' "

                print(update_text)
                cursor = connection.cursor()
                query_result = cursor.execute(update_text)    
                ####################################
                # 2번쿼리
                ####################################
                
                mp_plnd.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),pln_no=str(pln_no)).update(mtr_desc=str(mtr_desc))   

        context = {'message': 'true'}
    except Exception:
        context = {'message': 'false'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
######################################################################

# 프로그램 수행계획서 승인요청
@csrf_exempt
def MP0103M_Approval(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    status = request.POST.get('status', "")
    mtr_sub = request.POST.get('mtr_sub', "")

    mnt_dt_cnt = request.POST.get('mnt_dt_cnt', 0)      # 보고서 최초 생성
    rep_ym = request.POST.get('rep_ym', "")
    mnt_fr_dt = request.POST.get('mnt_fr_dt', "")
    mnt_to_dt = request.POST.get('mnt_to_dt', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    
    client_ip = request.META['REMOTE_ADDR']

    update_text = " update service20_mp_plnh a "
    update_text += " , service20_mpgm b "
    update_text += " , service20_mp_mte c "
    update_text += " , (SELECT mp_id "
    update_text += " , apl_no "
    update_text += " , apl_id "
    update_text += " , apl_nm "
    update_text += " FROM service20_mp_mtr "
    update_text += " WHERE apl_id = '"+apl_id+"' "
    update_text += " AND apl_no = '"+apl_no+"') d "
    update_text += " SET a.req_dt = NOW() "
    update_text += "   , a.status = '20' "
    update_text += "   , a.mtr_sub = '" + str(mtr_sub) + "' "
    update_text += "   , a.upd_id = '" + upd_id + "' "
    update_text += "   , a.upd_ip = '" + client_ip + "' "
    update_text += "   , a.upd_pgm = '" + upd_pgm + "' "
    update_text += "   , a.upd_dt = now() "
    update_text += " WHERE a.mp_id = b.mp_id "
    update_text += " AND a.mp_id = c.mp_id "
    update_text += " AND a.mp_id = d.mp_id "
    update_text += " AND a.apl_no = d.apl_no "
    update_text += " AND d.apl_no = c.apl_no "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    row_mnt_dt_cnt = int(mnt_dt_cnt)
    # for i in range(1,row_mnt_dt_cnt):
    #     # /* 계획서 최초 작성 시 보고서 insert */
    #     # /* 화면으로부터 넘겨받은 mnt_dt_cnt로 for(i = 1 i < mnt_dt_cnt i++) */
    #     # /* MP0103M/approval 시 같이 수행되게 해주세요 */
    #     query = " insert into service20_mp_rep ("
    #     query += "  mp_id"
    #     query += ", apl_no"
    #     query += ", rep_no"
    #     query += ", rep_div"
    #     query += ", rep_ym"
    #     query += ", mnte_id"
    #     query += ", mnte_nm"
    #     query += ", tchr_id"
    #     query += ", tchr_nm"
    #     # query += ", grd_id"
    #     # query += ", grd_nm"
    #     query += ", sch_nm"
    #     query += ", mtr_sub"
    #     query += ", att_desc"
    #     query += ", rep_ttl"
    #     query += ", mtr_obj"
    #     query += ", rep_dt"
    #     query += ", req_dt"
    #     query += ", mtr_desc"
    #     query += ", coatching"
    #     query += ", spcl_note"
    #     query += ", mtr_revw"
    #     query += ", appr_id"
    #     query += ", appr_nm"
    #     query += ", appr_dt"
    #     query += ", mgr_id"
    #     query += ", mgr_dt"
    #     query += ", status"
    #     query += ", ins_id"
    #     query += ", ins_ip"
    #     query += ", ins_dt"
    #     query += ", ins_pgm"
    #     query += ", upd_id"
    #     query += ", upd_ip"
    #     query += ", upd_dt"
    #     query += ", upd_pgm"
    #     query += ")"
    #     query += "select t1.mp_id  as mp_id"
    #     query += "     , t1.apl_no as apl_no"
    #     query += "     , '" + str(i) + "'        as rep_no /* {!i} */"
    #     query += "     , 'M'       as rep_div /*m - 교육 */"
    #     #query += "     , '" + str(rep_ym) + "'  as rep_ym /* {!rep_ym} */"
    #     query += "     , date_format(date_add(STR_TO_DATE(CONCAT('" + str(rep_ym) + "','01'), '%%Y%%m%%d'),interval+"+(i-1)+" month), '%%Y%%m')  as rep_ym /* {!rep_ym} */"
    #     #

    #     query += "     , null      as mnte_id"
    #     query += "     , null      as mnte_nm"
    #     query += "     , null      as tchr_id"
    #     query += "     , null      as tchr_nm"
    #     # query += "     , ' '      as grd_id"
    #     # query += "     , null      as grd_nm"
    #     query += "     , null      as sch_nm"
    #     query += "     , null      as mtr_sub"
    #     query += "     , null      as att_desc"
    #     #query += "     , concat(date_format(date( '" + str(mnt_fr_dt) + "' + interval " + str(i) + "-1 month), '%Y'), '년 ', date_format(date( '" + str(mnt_fr_dt) + "' + interval " + str(i) + "-1 month), '%m'), '월 보고서') as rep_ttl"
    #     query += "     , date_format(date_add(STR_TO_DATE(CONCAT('" + str(rep_ym) + "','01'), '%%Y%%m%%d'),interval+"+(i-1)+" month), '%%Y년 %%m월 보고서')  as rep_ttl"

    #     query += "     , null      as mtr_obj"
    #     query += "     , null      as rep_dt"
    #     query += "     , null      as req_dt"
    #     query += "     , null      as mtr_desc"
    #     query += "     , null      as coatching"
    #     query += "     , null      as spcl_note"
    #     query += "     , null      as mtr_revw"
    #     query += "     , null      as appr_id"
    #     query += "     , null      as appr_nm"
    #     query += "     , null      as appr_dt"
    #     query += "     , null      as mgr_id"
    #     query += "     , null      as mgr_dt"
    #     query += "     , '00'      as status"
    #     query += "     , '" + str(apl_id) + "' as ins_id   /* {!login_id} */"
    #     query += "     , '" + str(client_ip) + "' as ins_ip   /* {!ins_ip} */"
    #     query += "     , now()     as ins_dt"
    #     query += "     , '" + str(ins_pgm) + "'   as ins_pgm  /* {!ins_pgm} */"
    #     query += "     , '" + str(apl_id) + "' as upd_id"
    #     query += "     , '" + str(client_ip) + "' as upd_ip"
    #     query += "     , now() as upd_dt"
    #     query += "     , '" + str(upd_pgm) + "' as upd_pgm"
    #     query += "  from service20_mp_mtr t1"
    #     query += " where t1.mp_id  = '" + str(mp_id) + "'"
    #     query += "   and t1.apl_id = '" + str(apl_id) + "' /* {!apl_id} */"
    #     print("query_"+str(i))
    #     print(query)
    #     cursor = connection.cursor()
    #     query_result = cursor.execute(query)

        # rep_ym = int(rep_ym) + 1
        # if int(str(rep_ym)[4:]) > 12:
        #     rep_ym = str(rep_ym)[:4] + "01"

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#####################################################################################
# MP0103M - END 
#####################################################################################


#####################################################################################
# MP0104M - START
#####################################################################################

# 출석관리 리스트 ###################################################
class MP0104M_list_Serializer(serializers.ModelSerializer):

    apl_no = serializers.SerializerMethodField()
    sum_elap_tm = serializers.SerializerMethodField()
    sum_appr_tm = serializers.SerializerMethodField()
    sum_exp_amt = serializers.SerializerMethodField()
    cum_appr_tm = serializers.SerializerMethodField()
    att_ym = serializers.SerializerMethodField()
    att_sdt = serializers.SerializerMethodField()
    
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # pln_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # pln_sedt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mp_mtr
        fields = '__all__'
    
    def get_apl_no(self,obj):
        return obj.apl_no
    def get_sum_elap_tm(self,obj):
        return obj.sum_elap_tm
    def get_sum_appr_tm(self,obj):
        return obj.sum_appr_tm
    def get_sum_exp_amt(self,obj):
        return obj.sum_exp_amt
    def get_cum_appr_tm(self,obj):
        return obj.cum_appr_tm
    def get_att_ym(self,obj):
        return obj.att_ym
    def get_att_sdt(self,obj):
        return obj.att_sdt


class MP0104M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0104M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_term_div = request.GET.get('term_div', "")
        l_month  = request.GET.get('month', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_appr_yn = request.GET.get('appr_yn', "")
        l_mgr_yn = request.GET.get('mgr_yn', "")

        l_month1 = l_month
        l_month2 = l_month

        if not l_month:
            print("month:::" + l_month)
            l_month1 = '01'
            l_month2 = '12'

        queryset = self.get_queryset()

        # query = " select t3.id,t3.mp_id     /* 멘토링 프로그램id*/ "
        # query += " , t1.apl_no    /* 멘토 지원 no*/ "
        # query += " , t3.mntr_id         /* 멘토id*/ "
        # query += " , t3.apl_nm          /* 지원자(멘토,학생) 명*/ "
        # query += " , t3.unv_nm          /* 지원자 대학교 명*/ "
        # query += " , t3.cllg_nm         /* 지원자 대학 명*/ "
        # query += " , t3.dept_nm         /* 지원자 학부/학과 명*/ "
        # query += " , t3.sch_yr          /* 학년 */"
        # query += " , substring(t1.att_sdt, 1, 7) AS att_ym"
        # query += " , sec_to_time(sum(time_to_sec(t1.elap_tm))) sum_elap_tm  /* 경과시간*/ "
        # query += " , sum(t1.appr_tm)   sum_appr_tm /* 인정시간*/ "
        # query += " , sum(t1.exp_amt)   sum_exp_amt /* 지급 활동비 */"
        # query += " , sum(t1.appr_tm)   cum_appr_tm /* 누적시간*/ "
        # query += " , t3.bank_nm         /* 은행 명*/ "
        # query += " , t3.bank_acct       /* 은행 계좌 번호*/ "
        # query += " , t3.apl_id "
        # query += " from service20_mp_att t1     /* 프로그램 출석부(멘토)*/ "
        # query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id "
        # query += " and t3.apl_no   = t1.apl_no) "
        # query += " where 1=1 "
        # query += " and t3.yr    = '" + l_yr + "'    /* 년도 */ "        
        # query += " and t3.term_div    = '" + l_term_div + "'    /* 학기 */ "        
        # query += " and t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */ "
        # query += " and t3.apl_id   = '" + l_apl_id + "'   "
        # query += " and t1.appr_div   = '" + l_appr_yn + "'   "
        # query += " and t1.mgr_div   = '" + l_mgr_yn + "'   "
        # # query += " and (('" + l_appr_yn + "' = 'Y' and t1.appr_dt IS NOT NULL) OR ('" + l_appr_yn + "' <> 'Y' and t1.appr_dt IS NULL))"
        # # query += " and (('" + l_mgr_yn + "' = 'Y' and t1.mgr_dt IS NOT NULL) OR ('" + l_mgr_yn + "' <> 'Y' and t1.mgr_dt IS NULL))"
        # query += " and (t1.att_sdt >= CONCAT('" + l_yr + "-" + l_month1 + "', '-01') AND t1.att_sdt < ADDDATE(LAST_DAY(CONCAT('" + l_yr + "-" + l_month2 + "', '-01')), 1))"
        # query += " group by t1.mp_id     /* 멘토링 프로그램id */ "
        # query += " , substring(t1.att_sdt, 1, 7) "
        # query += " , t1.apl_no    /* 멘토 지원 no */ "
        # query += " , t3.mntr_id         /* 멘토id  */ "
        # query += " , t3.apl_nm          /* 지원자(멘토,학생) 명 */ "
        # query += " , t3.unv_nm          /* 지원자 대학교 명 */ "
        # query += " , t3.cllg_nm         /* 지원자 대학 명 */ "
        # query += " , t3.dept_nm         /* 지원자 학부/학과 명 */ "
        # query += " , t3.sch_yr          /* 학년 */ "
        # query += " , t3.bank_nm         /* 은행 명 */ "
        # query += " , t3.bank_acct "

        query = " select t1.id,t1.mp_id     /* 멘토링 프로그램id*/ "
        query += " , t1.apl_no    /* 멘토 지원 no*/ "
        query += " , t1.mntr_id         /* 멘토id*/ "
        query += " , t1.apl_nm          /* 지원자(멘토,학생) 명*/ "
        query += " , t1.unv_nm          /* 지원자 대학교 명*/ "
        query += " , t1.cllg_nm         /* 지원자 대학 명*/ "
        query += " , t1.dept_nm         /* 지원자 학부/학과 명*/ "
        query += " , t1.sch_yr          /* 학년 */"
        query += " , substring(t2.att_sdt, 1, 7) AS att_ym"
        query += " , sec_to_time(sum(time_to_sec(t2.elap_tm))) sum_elap_tm  /* 경과시간*/ "
        query += " , sum(t2.appr_tm)   sum_appr_tm /* 인정시간*/ "
        query += " , sum(t2.exp_amt)   sum_exp_amt /* 지급 활동비 */"
        query += " , sum(t2.appr_tm)   cum_appr_tm /* 누적시간*/ "
        query += " , t1.bank_nm         /* 은행 명*/ "
        query += " , t1.bank_acct       /* 은행 계좌 번호*/ "
        query += " , t1.apl_id "
        query += " , substring(t2.att_sdt,1, 7) as att_sdt "
        query += " from service20_mp_mtr t1     /* 프로그램 출석부(멘토)*/ "
        query += " left join service20_mp_att t2 on (t2.mp_id    = t1.mp_id "
        query += " and t2.apl_no   = t1.apl_no  "
        query += " and t2.apl_no   = t1.apl_no "
        query += " )"
        query += " where 1=1 "
        query += " and t1.yr    = '" + l_yr + "'    /* 년도 */ "        
        query += " and t1.term_div    = '" + l_term_div + "'    /* 학기 */ "        
        query += " and t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */ "
        query += " and t1.apl_id   = trim('" + l_apl_id + "')   "
        query += " and (t2.att_sdt >= CONCAT('" + l_yr + "-" + l_month1 + "', '-01') AND t2.att_sdt < ADDDATE(LAST_DAY(CONCAT('" + l_yr + "-" + l_month2 + "', '-01')), 1))"
        # query += " and t2.appr_div   = '" + l_appr_yn + "'   "
        # query += " and t2.mgr_div   = '" + l_mgr_yn + "'   "
        # query += " and (('" + l_appr_yn + "' = 'Y' and t1.appr_dt IS NOT NULL) OR ('" + l_appr_yn + "' <> 'Y' and t1.appr_dt IS NULL))"
        # query += " and (('" + l_mgr_yn + "' = 'Y' and t1.mgr_dt IS NOT NULL) OR ('" + l_mgr_yn + "' <> 'Y' and t1.mgr_dt IS NULL))"
        # query += " and (t2.att_sdt >= CONCAT('" + l_yr + "-" + l_month1 + "', '-01') AND t2.att_sdt < ADDDATE(LAST_DAY(CONCAT('" + l_yr + "-" + l_month2 + "', '-01')), 1))"
        query += " group by t1.mp_id     /* 멘토링 프로그램id */ "
        query += " , substring(t2.att_sdt, 1, 7) "
        query += " , t1.apl_no    /* 멘토 지원 no */ "
        query += " , t1.mntr_id         /* 멘토id  */ "
        query += " , t1.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += " , t1.unv_nm          /* 지원자 대학교 명 */ "
        query += " , t1.cllg_nm         /* 지원자 대학 명 */ "
        query += " , t1.dept_nm         /* 지원자 학부/학과 명 */ "
        query += " , t1.sch_yr          /* 학년 */ "
        query += " , t1.bank_nm         /* 은행 명 */ "
        query += " , t1.bank_acct "

        print(query)
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석관리 리스트 상세 ###################################################
class MP0104M_Detail_Serializer(serializers.ModelSerializer):

    mp_div_nm = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    expl_yn = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    att_etm = serializers.SerializerMethodField()
    att_stm = serializers.SerializerMethodField()
    mnte_no = serializers.SerializerMethodField()
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mp_att
        fields = '__all__'
    
    def get_mp_div_nm(self,obj):
        return obj.mp_div_nm
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_expl_yn(self,obj):
        return obj.expl_yn
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_att_etm(self,obj):
        return obj.att_etm
    def get_att_stm(self,obj):
        return obj.att_stm  
    def get_mnte_no(self,obj):
        return obj.mnte_no  


class MP0104M_Detail(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0104M_Detail_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_term_div = request.GET.get('term_div', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_month  = request.GET.get('month', "")
        l_appr_yn = request.GET.get('appr_yn', "")
        l_mgr_yn = request.GET.get('mgr_yn', "")

        l_month1 = l_month
        l_month2 = l_month

        if not l_month:
            print("month:::" + l_month)
            l_month1 = '01'
            l_month2 = '12'

        queryset = self.get_queryset()

        query = " select distinct t1.id,t1.mp_id     /* 멘토링 프로그램id */  "
        query += " , t1.apl_no    /* 멘토 지원 no */  "
        query += " , t1.att_no    /* 출석순서(seq) */  "
        query += " , t1.mp_div    /* 교육구분(mp0059) */  "
        query += " , c1.std_detl_code_nm   as mp_div_nm "
        query += " , t2.mnte_id     /* 멘티id */  "
        query += " , t5.mnte_no     /* 멘티지원No */  "
        query += " , t2.mnte_nm     /* 멘티명 */  "
        query += " , substring(t1.att_sdt, 1, 10) as att_sdt   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_sdt, 12, 5) as att_stm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_edt, 12, 5) as att_etm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.elap_tm, 1, 5)  as elap_tm   /* 경과시간 */  "
        query += " , t1.appr_tm   /* 인정시간 */  "
        query += " , t1.mtr_desc  /* 멘토링 내용(보고서) */  "
        query += " , t1.appr_id   /* 승인자id */  "
        query += " , t1.appr_nm   /* 승인자명 */  "
        query += " , substring(t1.appr_dt, 1, 16)  as appr_dt  /* 보호자 승인일시 */  "
        query += " , t1.mgr_id    /* 관리자id */  "
        query += " , t4.mgr_nm    /* 관리자명 */  "
        query += " , substring(t1.mgr_dt, 1, 16)  as mgr_dt   /* 관리자 승인일시 */  "
        query += " , t1.expl_yn as expl_yn   /* 소명상태 */  "
        query += " , t1.exp_amt   /* 지급 활동비 */  "
        query += " , t3.apl_id /* 학번 */ "
        query += " from service20_mp_att t1     /* 프로그램 출석부(멘토) */ "
        query += " left join service20_mp_att_mte t5 on (t5.mp_id = t1.mp_id and t5.apl_no = t1.apl_no and t5.att_no = t1.att_no)  "
        query += " left join service20_mp_mte t2  on (t2.mp_id  = t1.mp_id and t2.apl_no = t1.apl_no and t2.mnte_no = t5.mnte_no)  "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id and t3.apl_no   = t1.apl_no) "
        query += " left join service20_mpgm   t4 on (t4.mp_id    = t1.mp_id) "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'mp0059' and c1.std_detl_code = t1.mp_div) "
        query += " where 1=1 "
        query += " and t3.yr    = '" + l_yr + "'    /* 년도 */ "        
        query += " and t3.term_div    = '" + l_term_div + "'    /* 학기 */ "      
        query += " and t1.mp_id    = '" + l_mp_id + "'   /* 멘토링 프로그램id */ "
        query += " and t3.apl_id   = '" + l_apl_id + "' "
        query += " and t1.appr_div   like ifnull(nullif('" + l_appr_yn + "', ''), '%%')   "
        query += " and t1.mgr_div   like ifnull(nullif('" + l_mgr_yn + "', ''), '%%')   "
        # query += " and (('" + l_appr_yn + "' = 'Y' and t1.appr_dt IS NOT NULL) OR ('" + l_appr_yn + "' <> 'Y' and t1.appr_dt IS NULL))"
        # query += " and (('" + l_mgr_yn + "' = 'Y' and t1.mgr_dt IS NOT NULL) OR ('" + l_mgr_yn + "' <> 'Y' and t1.mgr_dt IS NULL))"
        query += " and (t1.att_sdt >= CONCAT('" + l_yr + "-" + l_month1 + "', '-01') AND t1.att_sdt < ADDDATE(LAST_DAY(CONCAT('" + l_yr + "-" + l_month2 + "', '-01')), 1))"
        query += " order by t1.att_no DESC    /* 출석순서(seq) */ "
        
        print(query)

        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#####################################################################################
# MP0104M - END
#####################################################################################

#####################################################################################
# MP01041M - START
#####################################################################################

# 멘토 리스트 ###################################################
class MP01041M_mtr_Serializer(serializers.ModelSerializer):

    min_len_mp_att_mtr_desc = serializers.SerializerMethodField()
    max_len_mp_att_mtr_desc = serializers.SerializerMethodField()
    min_len_mp_att_req_desc = serializers.SerializerMethodField()
    max_len_mp_att_req_desc = serializers.SerializerMethodField()
    att_val = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_min_len_mp_att_mtr_desc(self,obj):
        return obj.min_len_mp_att_mtr_desc
    def get_max_len_mp_att_mtr_desc(self,obj):
        return obj.max_len_mp_att_mtr_desc
    def get_min_len_mp_att_req_desc(self,obj):
        return obj.min_len_mp_att_req_desc
    def get_max_len_mp_att_req_desc(self,obj):
        return obj.max_len_mp_att_req_desc
    def get_att_val(self,obj):
        return obj.att_val

class MP01041M_mtr(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP01041M_mtr_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        query = "/* 멘토 그리드 */"
        query += " select t1.id as id "
        query += "     , t1.mp_id as mp_id"
        query += "     , t1.apl_no as apl_no"
        query += "     , t1.mntr_id as mntr_id"
        query += "     , t1.apl_nm as apl_nm"
        query += "     , t1.unv_nm as unv_nm"
        query += "     , t1.dept_nm as dept_nm"
        query += "     , t1.sch_yr as sch_yr"
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0003', 'MS0028', '10') min_len_mp_att_mtr_desc /* 멘토링 내용(보고서)(MTR_DESC) - 프로그램 출석부(멘토)(MP_ATT) */ "
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0003', 'MS0029', '10') max_len_mp_att_mtr_desc /* 멘토링 내용(보고서)(MTR_DESC) - 프로그램 출석부(멘토)(MP_ATT) */ "
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0018', 'MS0028', '10') min_len_mp_att_req_desc /* 소명 내용(보고서)(MTR_DESC) - 프로그램 출석부(멘토)(MP_ATT) */ "
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0018', 'MS0029', '10') max_len_mp_att_req_desc /* 소명 내용(보고서)(MTR_DESC) - 프로그램 출석부(멘토)(MP_ATT) */ "
        query += "     , t2.att_val as att_val"
        query += "  from service20_mp_mtr t1"
        query += "  left join service20_mp_sub t2 on (t2.mp_id = t1.mp_id and t2.att_id = 'MP0094' and t2.att_cdh = 'MP0094' and t2.att_cdd = '1') "
        query += " where t1.mp_id = '" + l_mp_id + "'"
        query += "   and t1.apl_id = '" + l_apl_id + "'"

        print(query)
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘티 리스트 소명 ###################################################
class MP01041M_mte_req_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mte
        fields = '__all__'

class MP01041M_mte_req(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = MP01041M_mte_req_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()

        query = "/* 멘티 그리드 */"
        query += " select id as id "
        query += "     , mp_id as mp_id"
        query += "     , mnte_no as mnte_no"
        query += "     , apl_no as apl_no"
        query += "     , mnte_id as mnte_id"
        query += "     , mnte_nm as mnte_nm"
        query += "     , sch_nm as sch_nm"
        query += "     , sch_yr as sch_yr"
        query += "  from service20_mp_mte"
        query += " where mp_id = '" + l_mp_id + "'"
        query += "   and apl_no = '" + l_apl_no + "'"

        print(query)

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘티 리스트 콤보 추가 ###################################################
class MP01041M_combo_mte_att_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = ('std_detl_code', 'std_detl_code_nm')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP01041M_combo_mte_att(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = MP01041M_combo_mte_att_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()
        
        query = " select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm from dual union"
        query += " select id as id"
        query += "     , mnte_no as std_detl_code"
        query += "     , mnte_nm as std_detl_code_nm"
        query += "  from service20_mp_mte"
        query += " where mp_id = '" + l_mp_id + "'"
        query += "   and apl_no = '" + l_apl_no + "'"

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘티 리스트 추가 상세 ###################################################
class MP01041M_mte_att_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mte
        fields = '__all__'

class MP01041M_mte_att(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = MP01041M_mte_att_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_mnte_no = request.GET.get('mnte_no', "")

        queryset = self.get_queryset()

        query = " select id as id"
        query += "     , mnte_id as mnte_id"
        query += "     , mnte_nm as mnte_nm"
        query += "     , mnte_no as mnte_no"
        query += "     , sch_nm as sch_nm"
        query += "     , sch_yr as sch_yr"
        query += "     , mp_id as mp_id"
        query += "     , apl_no as apl_no"
        query += "     , apl_id as apl_id"
        query += "  from service20_mp_mte"
        query += " where mp_id = '" + l_mp_id + "'"
        query += "   and mnte_no = '" + l_mnte_no + "'"

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토에 따른 멘티 리스트 ###################################################
class MP01041M_mtr_mte_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mte
        fields = '__all__'

class MP01041M_mtr_mte(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = MP01041M_mtr_mte_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()

        query = "select t1.id as id "
        query += "     , t1.mp_id as mp_id "
        query += "     , t1.mnte_no as mnte_no "
        query += "     , t1.apl_no as apl_no "
        query += "     , t1.mnte_id as mnte_id "
        query += "     , t1.mnte_nm as mnte_nm "
        query += "     , t1.sch_nm as sch_nm "
        query += "     , t1.sch_yr as sch_yr "
        query += "  from service20_mp_mte t1 "
        query += "  left join service20_mp_mtr t2 on (t2.mp_id = t1.mp_id and t2.apl_no = t1.apl_no) "
        query += " where t1.mp_id = '" + l_mp_id + "' "
        query += "   and t1.apl_no = '" + l_apl_no + "' "

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 프로그램 리스트 콤보 추가 ###################################################
class MP01041M_combo_mpgm_att_Serializer(serializers.ModelSerializer):
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = ('std_detl_code', 'std_detl_code_nm')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

class MP01041M_combo_mpgm_att(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP01041M_combo_mpgm_att_Serializer

    def list(self, request):
        l_apl_id = request.GET.get('apl_id', "")
        l_status = request.GET.get('status', "")

        queryset = self.get_queryset()

        query = " select '0' as mp_id, '' as std_detl_code, '선택' as std_detl_code_nm from dual union"
        query += " select t2.mp_id as mp_id"
        query += "     , t2.mp_id as std_detl_code"
        query += "     , t2.mp_name as std_detl_code_nm"   
        query += "  from service20_mp_mtr t1"
        query += "  left join service20_mpgm t2 on (t2.mp_id = t1.mp_id)"
        query += " where t1.apl_id = '"+ l_apl_id + "'"
        query += "   and t1.status = '" + l_status + "'"

        print(query)
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석 상세 ###################################################
class MP01041M_att_Serializer(serializers.ModelSerializer):
    req_no = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    att_stm = serializers.SerializerMethodField()
    att_etm = serializers.SerializerMethodField()
    mp_div_nm = serializers.SerializerMethodField()
    att_div_nm = serializers.SerializerMethodField()
    att_sts_nm = serializers.SerializerMethodField()
    req_desc = serializers.SerializerMethodField()

    class Meta:
        model = mp_att
        fields = '__all__'

    def get_req_no(self,obj):
        return obj.req_no
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_mp_name(self,obj):
        return obj.mp_name
    def get_att_stm(self,obj):
        return obj.att_stm
    def get_att_etm(self,obj):
        return obj.att_etm
    def get_mp_div_nm(self,obj):
        return obj.mp_div_nm
    def get_att_div_nm(self,obj):
        return obj.att_div_nm
    def get_att_sts_nm(self,obj):
        return obj.att_sts_nm
    def get_req_desc(self,obj):
        return obj.req_desc

class MP01041M_att(generics.ListAPIView):
    queryset = mp_att.objects.all()
    serializer_class = MP01041M_att_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")
        l_att_no = request.GET.get('att_no', "")

        queryset = self.get_queryset()

        # query = "/* 출석 상세 그리드 */"
        # query += " select t1.id as id "
        # query += "     , t1.mp_id as mp_id"
        # query += "     , t1.apl_no as apl_no"
        # query += "     , t1.att_no as att_no"
        # query += "     , t2.mp_name as mp_name"
        # query += "     , t1.mp_div as mp_div"
        # query += "     , t5.std_detl_code_nm AS mp_div_nm"
        # query += "     , t1.att_div AS att_div"     
        # query += "     , t4.std_detl_code_nm AS att_div_nm"     
        # query += "     , t1.att_sts AS att_sts"
        # query += "     , t3.std_detl_code_nm AS att_sts_nm"
        # query += "     , t1.mtr_desc as mtr_desc"
        # query += "     , t1.mtr_pic as mtr_pic"
        # query += "     , t1.att_saddr as att_saddr"
        # query += "     , t1.att_eaddr as att_eaddr"
        # query += "     , substring(t1.att_sdt, 1, 11) as att_sdt"
        # query += "     , substring(t1.att_sdt, 12, 8) as att_stm"
        # query += "     , substring(t1.att_edt, 1, 11) as att_edt"
        # query += "     , substring(t1.att_edt, 12, 8) as att_etm"
        # query += "     , substring(t1.elap_tm, 1, 5) as elap_tm"
        # query += "     , t1.appr_tm as appr_tm"
        # query += "     , t1.exp_amt as exp_amt"
        # query += "     , t1.appr_nm as appr_nm"
        # query += "     , t2.mgr_nm as mgr_nm"
        # query += "  from service20_mp_att t1"
        # query += "  left join service20_mpgm t2 on (t2.mp_id = t1.mp_id)"
        # query += "  LEFT JOIN service20_com_cdd t3 ON (t3.std_grp_code = 'MP0060' AND t3.std_detl_code = t1.att_sts)"
        # query += "  LEFT JOIN service20_com_cdd t4 ON (t4.std_grp_code = 'MP0063' AND t4.std_detl_code = t1.att_div)"
        # query += "  LEFT JOIN service20_com_cdd t5 ON (t5.std_grp_code = 'MP0059' AND t5.std_detl_code = t1.mp_div)"
        # query += " where t1.mp_id = '" + l_mp_id + "'"
        # query += "   and t1.apl_no = '" + l_apl_no + "'"
        # query += "   and t1.att_no = '" + l_att_no + "'"

        query = "/* 출석 상세 그리드 */"
        query += " select t1.id as id"
        query += "     , t1.mp_id as mp_id"
        query += "     , t1.apl_no as apl_no"
        query += "     , t2.req_no as req_no"
        query += "     , t1.att_no as att_no"
        query += "     , t3.mp_name as mp_name"
        query += "     , t1.mp_div as mp_div"
        query += "     , t6.std_detl_code_nm as mp_div_nm"
        query += "     , t1.att_div as att_div"
        query += "     , t5.std_detl_code_nm as att_div_nm"
        query += "     , t1.att_sts as att_sts"
        query += "     , t4.std_detl_code_nm as att_sts_nm"
        query += "     , t1.att_saddr as att_saddr"
        query += "     , t1.att_eaddr as att_eaddr"
        query += "     , t1.mtr_desc as mtr_desc"
        query += "     , t1.mtr_pic as mtr_pic"
        query += "     , t1.mtr_pic2 as mtr_pic2"
        query += "     , t1.mtr_pic3 as mtr_pic3"
        query += "     , t1.mtr_pic4 as mtr_pic4"
        query += "     , t1.mtr_pic5 as mtr_pic5"
        query += "     , substring(t1.att_sdt, 1, 10) as att_sdt"
        query += "     , substring(t1.att_sdt, 12, 8) as att_stm"
        query += "     , substring(t1.att_edt, 1, 10) as att_edt"
        query += "     , substring(t1.att_edt, 12, 8) as att_etm"
        query += "     , t1.elap_tm as elap_tm"
        query += "     , t1.appr_tm as appr_tm"
        query += "     , t1.exp_amt as exp_amt"
        query += "     , t1.appr_nm as appr_nm"
        query += "     , t3.mgr_nm as mgr_nm"
        query += "     , t2.t_req_desc as req_desc"
        query += "     , t1.att_slat as att_slat"
        query += "     , t1.att_slon as att_slon"
        query += "     , t1.att_slat as att_elat"
        query += "     , t1.att_slon as att_elon"
        query += "     , t1.appr_ret_desc as appr_ret_desc"
        query += "     , t1.mgr_ret_desc as mgr_ret_desc"
        query += "     , t1.appr_div as appr_div"
        query += "     , t1.mgr_div as mgr_div"
        query += "     , t1.qr_div as qr_div"
        query += "     , substring(t1.appr_dt, 1, 10) as appr_dt"
        query += "     , substring(t1.mgr_dt, 1, 10) as mgr_dt"
        query += "  from service20_mp_att t1"
        query += "  left join service20_mp_att_req t2 on (t2.mp_id = t1.mp_id and t2.apl_no = t1.apl_no and t2.att_no = t1.att_no)"
        query += "  left join service20_mpgm t3 on (t3.mp_id = t1.mp_id)"
        query += "  left join service20_com_cdd t4 on (t4.std_grp_code = 'MP0060' and t4.std_detl_code = t1.att_sts)"
        query += "  left join service20_com_cdd t5 on (t5.std_grp_code = 'MP0063' and t5.std_detl_code = t1.att_div)"
        query += "  left join service20_com_cdd t6 on (t6.std_grp_code = 'MP0059' and t6.std_detl_code = t1.mp_div)"
        query += " where t1.mp_id = '" + l_mp_id + "'"
        query += "   and t1.apl_no = '" + l_apl_no + "'"
        query += "   and t1.att_no = '" + l_att_no + "'"

        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석 추가 ###################################################
@csrf_exempt
def MP01041M_Insert(request):
    l_mp_id = request.POST.get('u_mp_id', "")
    l_apl_no = request.POST.get('u_apl_no', "")
    l_att_no = request.POST.get('u_att_no', "")
    l_mp_div = request.POST.get('u_mp_div', "")
    l_att_div = request.POST.get('u_att_div', "")
    l_mtr_desc = request.POST.get('u_mtr_desc', "")
    l_mtr_pic = request.POST.get('u_mtr_pic', "")
    l_att_saddr = request.POST.get('u_att_saddr', "")
    l_att_eaddr = request.POST.get('u_att_eaddr', "")
    l_att_sdt = request.POST.get('u_att_sdt', "")
    l_att_stm_h = request.POST.get('u_att_stm_h', "")
    l_att_stm_m = request.POST.get('u_att_stm_m', "")
    l_att_edt = request.POST.get('u_att_edt', "")
    l_att_etm_h = request.POST.get('u_att_etm_h', "")
    l_att_etm_m = request.POST.get('u_att_etm_m', "")
    l_elap_tm = request.POST.get('u_elap_tm', "")
    l_appr_tm = request.POST.get('u_appr_tm', "")
    l_exp_amt = request.POST.get('u_exp_amt', "")
    l_appr_nm = request.POST.get('u_appr_nm', "")
    l_mgr_nm = request.POST.get('u_mgr_nm', "")
    l_req_desc = request.POST.get('u_req_desc', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']
    
    att_query = "select ifnull(max(att_no), 0) + 1 as att_no from service20_mp_att t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "'"
    cursor = connection.cursor()
    cursor.execute(att_query)    
    results = namedtuplefetchall(cursor)    
    att_no = int(results[0].att_no)

    req_query = "select ifnull(max(req_no), 0) + 1 as req_no from service20_mp_att_req t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "'"
    cursor = connection.cursor()
    cursor.execute(req_query)    
    results = namedtuplefetchall(cursor)    
    req_no = int(results[0].req_no)

    query = f"""
            /* 출석 추가 */
            insert into service20_mp_att (
               mp_id
               , apl_no
               , att_no
               , mp_div
               , spc_no
               , att_div
               , att_sts
               , att_sdt
               , att_saddr
               , att_slat
               , att_slon
               , att_sdist
               , att_edt
               , att_eaddr
               , att_elat
               , att_elon
               , att_edist
               , elap_tm
               , appr_tm
               /*, mtr_desc*/
               , mtr_pic
               , appr_id
               , appr_nm
               , appr_dt
               , mgr_id
               , mgr_dt
               , expl_yn
               , rep_no
               , exp_div
               , exp_no
               , exp_dt
               , exp_amt
               , ins_id
               , ins_ip
               , ins_dt
               , ins_pgm
               , upd_id
               , upd_ip
               , upd_dt
               , upd_pgm
            ) values (
               '{l_mp_id}'
               , '{l_apl_no}'
               , {att_no}
               , '{l_mp_div}'
               , 0
               , '{l_att_div}'
               , 'B'
               , concat('{l_att_sdt}', ' {l_att_stm_h}', ':', '{l_att_stm_m}', ':00')
               , '{l_att_saddr}'
               , null
               , null
               , null
               , concat('{l_att_edt}', ' {l_att_etm_h}', ':', '{l_att_etm_m}', ':00')
               , '{l_att_eaddr}'
               , null
               , null
               , null
               , concat('{l_elap_tm}', ':00')
               , '{l_appr_tm}'
               /*, '{l_mtr_desc}'*/
               , '{l_mtr_pic}'
               , null
               , null
               , null
               , null
               , null
               , 'N'
               , null
               , 'N'
               , (select exp_no from service20_mp_exp where mp_id = '{l_mp_id}' and apl_no = '{l_apl_no}' and exp_mon = substring(replace('{l_att_sdt}', '-', ''), 1, 6))
               , null
               , null
               , '{ins_id}'
               , '{client_ip}'
               , now()
               , '{ins_pgm}'
               , '{upd_id}'
               , '{client_ip}'
               , now()
               , '{upd_pgm}'
            );
    """
    print(query)
    cursor = connection.cursor()
    query_result = cursor.execute(query)
    mp_att.objects.filter(mp_id=str(l_mp_id),apl_no=str(l_apl_no),att_no=str(att_no)).update(mtr_desc=str(l_mtr_desc))    

    query = f"""
            /* 소명 추가 */
            insert into service20_mp_att_req (
               mp_id
               , apl_no
               , req_no
               , att_no
               , mp_div
               , spc_no
               , f_att_div
               , f_att_sts
               , f_att_sdt
               , f_att_saddr
               , f_att_slat
               , f_att_slon
               , f_att_sdist
               , f_att_edt
               , f_att_eaddr
               , f_att_elat
               , f_att_elon
               , f_att_edist
               , f_elap_tm
               , f_appr_tm
               /*, f_mtr_desc*/
               , f_mtr_pic
               , f_mtr_pic2
               , f_mtr_pic3
               , f_mtr_pic4
               , f_mtr_pic5
               , f_appr_id
               , f_appr_nm
               , f_appr_dt
               , f_mgr_id
               , f_mgr_dt
               /*, t_req_desc*/
               , t_att_div
               , t_att_sts
               , t_att_sdt
               , t_att_saddr
               , t_att_slat
               , t_att_slon
               , t_att_sdist
               , t_att_edt
               , t_att_eaddr
               , t_att_elat
               , t_att_elon
               , t_att_edist
               , t_elap_tm
               , t_appr_tm
               /*, t_mtr_desc*/
               , t_mtr_pic
               , t_mtr_pic2
               , t_mtr_pic3
               , t_mtr_pic4
               , t_mtr_pic5
               , t_appr_id
               , t_appr_nm
               , t_appr_dt
               , t_mgr_id
               , t_mgr_dt
               , ins_id
               , ins_ip
               , ins_dt
               , ins_pgm
               , upd_id
               , upd_ip
               , upd_dt
               , upd_pgm
            )
            select mp_id as mp_id
                , apl_no as apl_no
                , {req_no} as req_no
                , att_no as att_no
                , '{l_mp_div}' as mp_div
                , 0 as spc_no 
                , '{l_att_div}' as f_att_div 
                , 'B' as f_att_sts
                , concat('{l_att_sdt}', ' {l_att_stm_h}', ':', '{l_att_stm_m}', ':00') as f_att_sdt
                , att_saddr as f_att_saddr
                , att_slat as f_att_slat
                , att_slon as f_att_slon
                , att_sdist as f_att_sdist
                , concat('{l_att_edt}', ' {l_att_etm_h}', ':', '{l_att_etm_m}', ':00') as f_att_edt
                , att_eaddr as f_att_eaddr
                , att_elat as f_att_elat
                , att_elon as f_att_elon
                , att_edist as f_att_edist
                , '{l_elap_tm}' as f_elap_tm
                , '{l_appr_tm}' as f_appr_tm
                /*, '{l_mtr_desc}' as f_mtr_desc*/
                , mtr_pic as f_mtr_pic
                , mtr_pic2 as f_mtr_pic2
                , mtr_pic3 as f_mtr_pic3
                , mtr_pic4 as f_mtr_pic4
                , mtr_pic5 as f_mtr_pic5
                , null as f_appr_id
                , null as f_appr_nm
                , null as f_appr_dt
                , null as f_mgr_id
                , null as f_mgr_dt
                /*, '{l_req_desc}' as t_req_desc*/
                , '{l_att_div}' as t_att_div 
                , 'B' as t_att_sts
                , concat('{l_att_sdt}', ' {l_att_stm_h}', ':', '{l_att_stm_m}', ':00') as t_att_sdt
                , att_saddr as t_att_saddr
                , att_slat as t_att_slat
                , att_slon as t_att_slon
                , att_sdist as t_att_sdist
                , concat('{l_att_edt}', ' {l_att_etm_h}', ':', '{l_att_etm_m}', ':00') as t_att_edt
                , att_eaddr as t_att_eaddr
                , att_elat as t_att_elat
                , att_elon as t_att_elon
                , att_edist as t_att_edist
                , '{l_elap_tm}' as t_elap_tm
                , '{l_appr_tm}' as t_appr_tm
                /*, '{l_mtr_desc}' as t_mtr_desc*/
                , null as t_mtr_pic
                , null as t_mtr_pic2
                , null as t_mtr_pic3
                , null as t_mtr_pic4
                , null as t_mtr_pic5
                , null as t_appr_id
                , null as t_appr_nm
                , null as t_appr_dt
                , null as t_mgr_id
                , null as t_mgr_dt
                , '{ins_id}' as ins_id
                , '{client_ip}' as ins_ip
                , now() as ins_dt
                , '{ins_pgm}' as ins_pgm
                , '{upd_id}' as upd_id
                , '{client_ip}' as upd_ip
                , now() as upd_dt
                , '{upd_pgm}' as upd_pgm
             from service20_mp_att
            where mp_id = '{l_mp_id}'
              and apl_no = '{l_apl_no}'
              and att_no = {att_no}
            ;
    """
    print(query)
    cursor = connection.cursor()
    query_result = cursor.execute(query)
    mp_att_req.objects.filter(mp_id=str(l_mp_id),apl_no=str(l_apl_no),req_no=str(req_no),att_no=str(att_no)).update(f_mtr_desc=str(l_mtr_desc),t_mtr_desc=str(l_mtr_desc),t_req_desc=str(l_req_desc))
    
    # 출석 추가
    # query = "/* 출석 추가 */"
    # query += " insert into service20_mp_att ("
    # query += "    mp_id"
    # query += "    , apl_no"
    # query += "    , att_no"
    # query += "    , mp_div"
    # query += "    , spc_no"
    # query += "    , att_div"
    # query += "    , att_sts"
    # query += "    , att_sdt"
    # query += "    , att_saddr"
    # query += "    , att_slat"
    # query += "    , att_slon"
    # query += "    , att_sdist"
    # query += "    , att_edt"
    # query += "    , att_eaddr"
    # query += "    , att_elat"
    # query += "    , att_elon"
    # query += "    , att_edist"
    # query += "    , elap_tm"
    # query += "    , appr_tm"
    # query += "    , mtr_desc"
    # query += "    , mtr_pic"
    # query += "    , appr_id"
    # query += "    , appr_nm"
    # query += "    , appr_dt"
    # query += "    , mgr_id"
    # query += "    , mgr_dt"
    # query += "    , expl_yn"
    # query += "    , rep_no"
    # query += "    , exp_div"
    # query += "    , exp_no"
    # query += "    , exp_dt"
    # query += "    , exp_amt"
    # query += "    , ins_id"
    # query += "    , ins_ip"
    # query += "    , ins_dt"
    # query += "    , ins_pgm"
    # query += "    , upd_id"
    # query += "    , upd_ip"
    # query += "    , upd_dt"
    # query += "    , upd_pgm"
    # query += " ) values ("
    # query += "    '" + str(l_mp_id) + "'"
    # query += "    , '" + str(l_apl_no) + "'"
    # # query += "    , (select ifnull(max(att_no), 0) + 1 from service20_mp_att t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "')"
    # query += "    , " + att_no
    # query += "    , '" + str(l_mp_div) + "'"
    # query += "    , 0"
    # query += "    , '" + str(l_att_div) + "'"
    # query += "    , 'B'"
    # query += "    , concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00')"
    # query += "    , '" + l_att_saddr + "'"
    # query += "    , null"
    # query += "    , null"
    # query += "    , null"
    # query += "    , concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00')"
    # query += "    , '" + l_att_eaddr + "'"
    # query += "    , null"
    # query += "    , null"
    # query += "    , null"
    # query += "    , concat('" + str(l_elap_tm) + "', ':00')"
    # query += "    , '" + str(l_appr_tm) + "'"
    # query += "    , '" + str(l_mtr_desc) + "'"
    # query += "    , '" + str(l_mtr_pic) + "'"
    # query += "    , null"
    # query += "    , null"
    # query += "    , null"
    # query += "    , null"
    # query += "    , null"
    # query += "    , 'N'"
    # query += "    , null"
    # query += "    , 'Y'"
    # query += "    , (select exp_no from service20_mp_exp where mp_id = '" + str(l_mp_id) + "' and apl_no = '" + str(l_apl_no) + "' and exp_mon = substring(replace('" + str(l_att_sdt) + "', '-', ''), 1, 6))"
    # query += "    , null"
    # query += "    , null"
    # query += "    , '" + str(ins_id) + "'"
    # query += "    , '" + str(client_ip) + "'"
    # query += "    , now()"
    # query += "    , '" + str(ins_pgm) + "'"
    # query += "    , '" + str(upd_id) + "'"
    # query += "    , '" + str(client_ip) + "'"
    # query += "    , now()"
    # query += "    , '" + str(upd_pgm) + "'"
    # query += " )"

    # cursor = connection.cursor()
    # query_result = cursor.execute(query)

    # # 소명 최초 추가
    # query = "/* 소명 추가 */"
    # query += " insert into service20_mp_att_req ("
    # query += "    mp_id"
    # query += "    , apl_no"
    # query += "    , req_no"
    # query += "    , att_no"
    # query += "    , mp_div"
    # query += "    , spc_no"
    # query += "    , f_att_div"
    # query += "    , f_att_sts"
    # query += "    , f_att_sdt"
    # query += "    , f_att_saddr"
    # query += "    , f_att_slat"
    # query += "    , f_att_slon"
    # query += "    , f_att_sdist"
    # query += "    , f_att_edt"
    # query += "    , f_att_eaddr"
    # query += "    , f_att_elat"
    # query += "    , f_att_elon"
    # query += "    , f_att_edist"
    # query += "    , f_elap_tm"
    # query += "    , f_appr_tm"
    # query += "    , f_mtr_desc"
    # query += "    , f_mtr_pic"
    # query += "    , f_mtr_pic2"
    # query += "    , f_mtr_pic3"
    # query += "    , f_mtr_pic4"
    # query += "    , f_mtr_pic5"
    # query += "    , f_appr_id"
    # query += "    , f_appr_nm"
    # query += "    , f_appr_dt"
    # query += "    , f_mgr_id"
    # query += "    , f_mgr_dt"
    # query += "    , t_req_desc"
    # query += "    , t_att_div"
    # query += "    , t_att_sts"
    # query += "    , t_att_sdt"
    # query += "    , t_att_saddr"
    # query += "    , t_att_slat"
    # query += "    , t_att_slon"
    # query += "    , t_att_sdist"
    # query += "    , t_att_edt"
    # query += "    , t_att_eaddr"
    # query += "    , t_att_elat"
    # query += "    , t_att_elon"
    # query += "    , t_att_edist"
    # query += "    , t_elap_tm"
    # query += "    , t_appr_tm"
    # query += "    , t_mtr_desc"
    # query += "    , t_mtr_pic"
    # query += "    , t_mtr_pic2"
    # query += "    , t_mtr_pic3"
    # query += "    , t_mtr_pic4"
    # query += "    , t_mtr_pic5"
    # query += "    , t_appr_id"
    # query += "    , t_appr_nm"
    # query += "    , t_appr_dt"
    # query += "    , t_mgr_id"
    # query += "    , t_mgr_dt"
    # query += "    , ins_id"
    # query += "    , ins_ip"
    # query += "    , ins_dt"
    # query += "    , ins_pgm"
    # query += "    , upd_id"
    # query += "    , upd_ip"
    # query += "    , upd_dt"
    # query += "    , upd_pgm"
    # query += " )"
    # query += " select mp_id as mp_id"
    # query += "     , apl_no as apl_no"
    # query += "     , (select ifnull(max(req_no), 0) + 1 from service20_mp_att_req t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "') as req_no"
    # query += "     , att_no as att_no"
    # query += "     , '" + str(l_mp_div) + "' as mp_div"
    # query += "     , 0 as spc_no "
    # query += "     , '" + l_att_div + "' as f_att_div "
    # query += "     , 'B' as f_att_sts"
    # query += "     , concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00') as f_att_sdt"
    # query += "     , att_saddr as f_att_saddr"
    # query += "     , att_slat as f_att_slat"
    # query += "     , att_slon as f_att_slon"
    # query += "     , att_sdist as f_att_sdist"
    # query += "     , concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00') as f_att_edt"
    # query += "     , att_eaddr as f_att_eaddr"
    # query += "     , att_elat as f_att_elat"
    # query += "     , att_elon as f_att_elon"
    # query += "     , att_edist as f_att_edist"
    # query += "     , '" + l_elap_tm + "' as f_elap_tm"
    # query += "     , '" + l_appr_tm + "' as f_appr_tm"
    # query += "     , '" + l_mtr_desc + "' as f_mtr_desc"
    # query += "     , mtr_pic as f_mtr_pic"
    # query += "     , mtr_pic2 as f_mtr_pic2"
    # query += "     , mtr_pic3 as f_mtr_pic3"
    # query += "     , mtr_pic4 as f_mtr_pic4"
    # query += "     , mtr_pic5 as f_mtr_pic5"
    # query += "     , null as f_appr_id"
    # query += "     , null as f_appr_nm"
    # query += "     , null as f_appr_dt"
    # query += "     , null as f_mgr_id"
    # query += "     , null as f_mgr_dt"
    # query += "     , '" + l_req_desc + "' as t_req_desc"
    # query += "     , '" + l_att_div + "' as t_att_div "
    # query += "     , 'B' as t_att_sts"
    # query += "     , concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00') as t_att_sdt"
    # query += "     , att_saddr as t_att_saddr"
    # query += "     , att_slat as t_att_slat"
    # query += "     , att_slon as t_att_slon"
    # query += "     , att_sdist as t_att_sdist"
    # query += "     , concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00') as t_att_edt"
    # query += "     , att_eaddr as t_att_eaddr"
    # query += "     , att_elat as t_att_elat"
    # query += "     , att_elon as t_att_elon"
    # query += "     , att_edist as t_att_edist"
    # query += "     , '" + l_elap_tm + "' as t_elap_tm"
    # query += "     , '" + l_appr_tm + "' as t_appr_tm"
    # query += "     , '" + l_mtr_desc + "' as t_mtr_desc"
    # query += "     , null as t_mtr_pic"
    # query += "     , null as t_mtr_pic2"
    # query += "     , null as t_mtr_pic3"
    # query += "     , null as t_mtr_pic4"
    # query += "     , null as t_mtr_pic5"
    # query += "     , null as t_appr_id"
    # query += "     , null as t_appr_nm"
    # query += "     , null as t_appr_dt"
    # query += "     , null as t_mgr_id"
    # query += "     , null as t_mgr_dt"
    # query += "     , '" + str(ins_id) + "' as ins_id"
    # query += "     , '" + str(client_ip) + "' as ins_ip"
    # query += "     , now() as ins_dt"
    # query += "     , '" + str(ins_pgm) + "' as ins_pgm"
    # query += "     , '" + str(upd_id) + "' as upd_id"
    # query += "     , '" + str(client_ip) + "' as upd_ip"
    # query += "     , now() as upd_dt"
    # query += "     , '" + str(upd_pgm) + "' as upd_pgm"
    # query += "  from service20_mp_att"
    # query += " where mp_id = '" + str(l_mp_id) + "'"
    # query += "   and apl_no = '" + str(l_apl_no) + "'"
    # query += "   and att_no = (select max(att_no) from service20_mp_att where mp_id = '" + str(l_mp_id) + "' and apl_no = '" + str(l_apl_no) + "')"
    # query += "   and att_no in (select max(att_no) from service20_mp_att where mp_id = '" + str(l_mp_id) + "' and apl_no = '" + str(l_apl_no) + "')"

    # print(query)
    # cursor = connection.cursor()
    # query_result = cursor.execute(query)    

    context = {'att_no': str(att_no), 'req_no': str(req_no)}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 출석 소명 수정 ###################################################
@csrf_exempt
def MP01041M_req(request):
    l_mp_id = request.POST.get('u_mp_id', "")
    l_apl_no = request.POST.get('u_apl_no', "")
    l_req_no = request.POST.get('u_req_no', "")
    l_att_no = request.POST.get('u_att_no', "")
    l_mp_div = request.POST.get('u_mp_div', "")
    l_att_div = request.POST.get('u_att_div', "")
    l_mtr_desc = request.POST.get('u_mtr_desc', "")
    # l_mtr_pic[i] = request.POST.get('u_mtr_pic' + str(i), "")
    l_att_saddr = request.POST.get('u_att_saddr', "")
    l_att_eaddr = request.POST.get('u_att_eaddr', "")
    l_att_sdt = request.POST.get('u_att_sdt', "")
    l_att_stm_h = request.POST.get('u_att_stm_h', "")
    l_att_stm_m = request.POST.get('u_att_stm_m', "")
    l_att_edt = request.POST.get('u_att_edt', "")
    l_att_etm_h = request.POST.get('u_att_etm_h', "")
    l_att_etm_m = request.POST.get('u_att_etm_m', "")
    l_elap_tm = request.POST.get('u_elap_tm', "")
    l_appr_tm = request.POST.get('u_appr_tm', "")
    l_exp_amt = request.POST.get('u_exp_amt', "")
    l_appr_nm = request.POST.get('u_appr_nm', "")
    l_mgr_nm = request.POST.get('u_mgr_nm', "")
    l_req_desc = request.POST.get('u_req_desc', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    req_query = "select ifnull(max(req_no), 0) + 1 as req_no from service20_mp_att_req t1 where t1.mp_id = '" + str(l_mp_id) + "' and t1.apl_no = '" + str(l_apl_no) + "'"
    cursor = connection.cursor()
    cursor.execute(req_query)    
    results = namedtuplefetchall(cursor)    
    req_no = int(results[0].req_no)


    # 소명 최초 추가
    query = "/* 소명 추가 */"
    query += " insert into service20_mp_att_req ("
    query += "    mp_id"
    query += "    , apl_no"
    query += "    , req_no"
    query += "    , att_no"
    query += "    , mp_div"
    query += "    , spc_no"
    query += "    , f_att_div"
    query += "    , f_att_sts"
    query += "    , f_att_sdt"
    query += "    , f_att_saddr"
    query += "    , f_att_slat"
    query += "    , f_att_slon"
    query += "    , f_att_sdist"
    query += "    , f_att_edt"
    query += "    , f_att_eaddr"
    query += "    , f_att_elat"
    query += "    , f_att_elon"
    query += "    , f_att_edist"
    query += "    , f_elap_tm"
    query += "    , f_appr_tm"
    # query += "    , f_mtr_desc"
    query += "    , f_mtr_pic"
    query += "    , f_mtr_pic2"
    query += "    , f_mtr_pic3"
    query += "    , f_mtr_pic4"
    query += "    , f_mtr_pic5"
    query += "    , f_appr_id"
    query += "    , f_appr_nm"
    query += "    , f_appr_dt"
    query += "    , f_mgr_id"
    query += "    , f_mgr_dt"
    # query += "    , t_req_desc"
    query += "    , t_att_div"
    query += "    , t_att_sts"
    query += "    , t_att_sdt"
    query += "    , t_att_saddr"
    query += "    , t_att_slat"
    query += "    , t_att_slon"
    query += "    , t_att_sdist"
    query += "    , t_att_edt"
    query += "    , t_att_eaddr"
    query += "    , t_att_elat"
    query += "    , t_att_elon"
    query += "    , t_att_edist"
    query += "    , t_elap_tm"
    query += "    , t_appr_tm"
    # query += "    , t_mtr_desc"
    query += "    , t_mtr_pic"
    query += "    , t_mtr_pic2"
    query += "    , t_mtr_pic3"
    query += "    , t_mtr_pic4"
    query += "    , t_mtr_pic5"
    query += "    , t_appr_id"
    query += "    , t_appr_nm"
    query += "    , t_appr_dt"
    query += "    , t_mgr_id"
    query += "    , t_mgr_dt"
    query += "    , ins_id"
    query += "    , ins_ip"
    query += "    , ins_dt"
    query += "    , ins_pgm"
    query += "    , upd_id"
    query += "    , upd_ip"
    query += "    , upd_dt"
    query += "    , upd_pgm"
    query += " )"
    query += " select mp_id as mp_id"
    query += "     , apl_no as apl_no"
    query += "     , '" + str(req_no) + "' "
    query += "     , att_no as att_no"
    query += "     , '" + str(l_mp_div) + "' as mp_div"
    query += "     , 0 as spc_no "
    query += "     , '" + str(l_att_div) + "' as f_att_div "
    query += "     , 'B' as f_att_sts"
    query += "     , concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00') as f_att_sdt"
    query += "     , att_saddr as f_att_saddr"
    query += "     , att_slat as f_att_slat"
    query += "     , att_slon as f_att_slon"
    query += "     , att_sdist as f_att_sdist"
    query += "     , concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00') as f_att_edt"
    query += "     , att_eaddr as f_att_eaddr"
    query += "     , att_elat as f_att_elat"
    query += "     , att_elon as f_att_elon"
    query += "     , att_edist as f_att_edist"
    query += "     , '" + l_elap_tm + "' as f_elap_tm"
    query += "     , '" + l_appr_tm + "' as f_appr_tm"
    # query += "     , '" + l_mtr_desc + "' as f_mtr_desc"
    query += "     , mtr_pic as f_mtr_pic"
    query += "     , mtr_pic2 as f_mtr_pic2"
    query += "     , mtr_pic3 as f_mtr_pic3"
    query += "     , mtr_pic4 as f_mtr_pic4"
    query += "     , mtr_pic5 as f_mtr_pic5"
    query += "     , null as f_appr_id"
    query += "     , null as f_appr_nm"
    query += "     , null as f_appr_dt"
    query += "     , null as f_mgr_id"
    query += "     , null as f_mgr_dt"
    # query += "     , '" + l_req_desc + "' as t_req_desc"
    query += "     , '" + l_att_div + "' as t_att_div "
    query += "     , 'B' as t_att_sts"
    query += "     , concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00') as t_att_sdt"
    query += "     , att_saddr as t_att_saddr"
    query += "     , att_slat as t_att_slat"
    query += "     , att_slon as t_att_slon"
    query += "     , att_sdist as t_att_sdist"
    query += "     , concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00') as t_att_edt"
    query += "     , att_eaddr as t_att_eaddr"
    query += "     , att_elat as t_att_elat"
    query += "     , att_elon as t_att_elon"
    query += "     , att_edist as t_att_edist"
    query += "     , '" + l_elap_tm + "' as t_elap_tm"
    query += "     , '" + l_appr_tm + "' as t_appr_tm"
    # query += "     , '" + l_mtr_desc + "' as t_mtr_desc"
    query += "     , null as t_mtr_pic"
    query += "     , null as t_mtr_pic2"
    query += "     , null as t_mtr_pic3"
    query += "     , null as t_mtr_pic4"
    query += "     , null as t_mtr_pic5"
    query += "     , null as t_appr_id"
    query += "     , null as t_appr_nm"
    query += "     , null as t_appr_dt"
    query += "     , null as t_mgr_id"
    query += "     , null as t_mgr_dt"
    query += "     , '" + str(ins_id) + "' as ins_id"
    query += "     , '" + str(client_ip) + "' as ins_ip"
    query += "     , now() as ins_dt"
    query += "     , '" + str(ins_pgm) + "' as ins_pgm"
    query += "     , '" + str(upd_id) + "' as upd_id"
    query += "     , '" + str(client_ip) + "' as upd_ip"
    query += "     , now() as upd_dt"
    query += "     , '" + str(upd_pgm) + "' as upd_pgm"
    query += "  from service20_mp_att"
    query += " where mp_id = '" + str(l_mp_id) + "'"
    query += "   and apl_no = '" + str(l_apl_no) + "'"
    query += "   and att_no = '" + str(l_att_no) +  "' "
    # query += "   and att_no in (select max(att_no) from service20_mp_att where mp_id = '" + str(l_mp_id) + "' and apl_no = '" + str(l_apl_no) + "')"

    print(query)
    cursor = connection.cursor()
    query_result = cursor.execute(query)    
    mp_att_req.objects.filter(mp_id=str(l_mp_id),apl_no=str(l_apl_no),req_no=str(req_no),att_no=str(l_att_no)).update(f_mtr_desc=str(l_mtr_desc),t_mtr_desc=str(l_mtr_desc),t_req_desc=str(l_req_desc))

    # 출석 소명 수정
    # query = "/* 출석 소명 수정 */"
    # query += " update service20_mp_att_req"
    # query += "   set t_req_desc = '" + str(l_req_desc) + "'"
    # query += "     , t_att_sdt = concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00')"
    # query += "     , t_att_edt = concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00')"
    # query += "     , t_elap_tm = concat('" + str(l_elap_tm) + "', ':00')"
    # query += "     , t_appr_tm = '" + str(l_appr_tm) + "'"
    # query += "     , t_mtr_desc = '" + str(l_mtr_desc) + "'"
    # # if i > 0:
    # #     if not l_mtr_pic[i]:
    # #         query += "     , t_mtr_pic = '" + str(i+1) + str(l_mtr_pic[i]) + "'"
    # # else:
    # #     query += "     , t_mtr_pic = '" + str(l_mtr_pic[i]) + "'"
    # query += "     , upd_id = '" + str(upd_id) + "'"
    # query += "     , upd_ip = '" + str(client_ip) + "'"
    # query += "     , upd_dt = now()"
    # query += "     , upd_pgm = '" + str(upd_pgm) + "'"
    # query += " where mp_id = '" + str(l_mp_id) + "'"
    # query += "   and apl_no = '" + str(l_apl_no) + "'"
    # query += "   and req_no = '" + str(l_req_no) + "'"

    # print(query)
    # cursor = connection.cursor()
    # query_result = cursor.execute(query)

    # 출석 원본 수정
    query = "/* 출석 원본 수정 */"
    query += " update service20_mp_att"
    query += "   set att_sdt = concat('" + str(l_att_sdt) + "', ' " + str(l_att_stm_h) + "', ':', '" + str(l_att_stm_m) + "', ':00')"
    query += "     , att_edt = concat('" + str(l_att_edt) + "', ' " + str(l_att_etm_h) + "', ':', '" + str(l_att_etm_m) + "', ':00')"
    query += "     , elap_tm = concat('" + str(l_elap_tm) + "', ':00')"
    query += "     , appr_tm = '" + str(l_appr_tm) + "'"
    # query += "     , mtr_desc = '" + str(l_mtr_desc) + "'"
    # if i > 0:
    #     if not l_mtr_pic[i]:
    #         query += "     , mtr_pic = '" + str(i+1) + str(l_mtr_pic[i]) + "'"
    # else:
    #     query += "     , mtr_pic = '" + str(l_mtr_pic[i]) + "'"
    query += "     , expl_yn = 'Y'"
    query += " where mp_id = '" + str(l_mp_id) + "'"
    query += "   and apl_no = '" + str(l_apl_no) + "'"
    query += "   and att_no = '" + str(l_att_no) + "'"

    print(query)
    cursor = connection.cursor()
    query_result = cursor.execute(query)
    mp_att.objects.filter(mp_id=str(l_mp_id),apl_no=str(l_apl_no),att_no=str(l_att_no)).update(mtr_desc=str(l_mtr_desc))

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 출석 소명 insert 후 max att_no, req_no 가져오기 ###################################################
class MP01041M_att_max_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    req_no = serializers.SerializerMethodField()

    class Meta:
        model = mp_att
        fields = '__all__'

    def get_req_no(self,obj):
        return obj.req_no
    def get_id(self,obj):
        return obj.id

class MP01041M_att_max(generics.ListAPIView):
    queryset = mp_att.objects.all()
    serializer_class = MP01041M_att_max_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()

        query = " select t1.id as id"
        query += "     , t1.att_no as att_no"
        query += "     , t2.req_no as req_no"
        query += "  from (select id as id, max(att_no) as att_no from service20_mp_att where mp_id = '" + l_mp_id + "' and apl_no = '" + l_apl_no + "') t1"
        query += "     , (select max(req_no) as req_no from service20_mp_att_req where mp_id = '" + l_mp_id + "' and apl_no = '" + l_apl_no + "') t2"

        print(query)
        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 사진 업로드 ###################################################
@csrf_exempt
def MP01041M_upload(request):
    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/MP01041M/'
    UPLOAD_DIR = '/NANUM/www/img/mp_attend/'
    # UPLOAD_DIR = 'img'
    
    if request.method == 'POST':
        l_mp_id = request.POST.get("u_mp_id")
        l_apl_no = request.POST.get("u_apl_no")
        l_att_no = request.POST.get("u_att_no")
        l_req_no = request.POST.get("u_req_no")
        l_user_id = request.POST.get("user_id")
        
        l_req_no_yn = 'Y'
        if not l_req_no:
            l_req_no_yn = 'N'

        print(l_mp_id)
        print(l_apl_no)
        print(l_att_no)
        print(l_user_id)

        pic_num = 0
        for i in range(0,5):
            try:
                file = request.FILES['mtr_pic' + str(i)]
            except MultiValueDictKeyError:
                file = False

            if file != False:
                print(file)
                filename = file._name
                n_filename = str(l_user_id) + str(l_mp_id) + str(l_apl_no) + str(l_att_no) + str(l_req_no) + str((i+1)) + os.path.splitext(filename)[1]
                print(n_filename)
                print (UPLOAD_DIR)
                
                fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')

                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()

                cursor = connection.cursor()
                fullFile = str(UPLOAD_DIR) + str(n_filename)
                fullFile = "/img/mp_attend/"+ str(n_filename)

                if i == 0:
                    pic_num = ""
                else:
                    pic_num = (i+1)

                query = " update service20_mp_att"
                query += "   set mtr_pic" + str(pic_num) + " = '" + str(fullFile) + "'"
                query += " where mp_id = '" + str(l_mp_id) + "'"
                query += "   and apl_no = '" + str(l_apl_no) + "'"
                query += "   and (('" + str(l_req_no_yn) + "' = 'N' and att_no in ( select * from (select max(att_no)"
                query += "                                                                 from service20_mp_att"
                query += "                                                                where mp_id = '" + str(l_mp_id) + "'"
                query += "                                                                  and apl_no = '" + str(l_apl_no) + "') as att_no))"
                query += "       or ('" + str(l_req_no_yn) + "' = 'Y' and att_no = '" + str(l_att_no) + "'))"

                print(query)
                cursor.execute(query)

                query = " update service20_mp_att_req"
                query += " set t_mtr_pic" + str(pic_num) + " = '" + str(fullFile) + "'"
                query += " where mp_id = '" + str(l_mp_id) + "'"
                query += "  and apl_no = '" + str(l_apl_no) + "'"
                query += "  and (('" + str(l_req_no_yn) + "' = 'N' and req_no in ( select * from (select max(req_no)"
                query += "                                                    from service20_mp_att_req"
                query += "                                                   where mp_id = '" + str(l_mp_id) + "'"
                query += "                                                     and apl_no = '" + str(l_apl_no) + "') as req_no))"
                query += "      or ('" + str(l_req_no_yn) + "' = 'Y' and req_no = '" + str(l_req_no) + "'))"

                print(query)
                cursor.execute(query)
        
        return HttpResponse('File Uploaded')


#####################################################################################
# MP01041M - END
#####################################################################################

#####################################################################################
# MP0105M - START
#####################################################################################

# 보고서 현황 리스트 ###################################################
class MP0105M_combo_1_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','mp_name')

    def get_mp_name(self,obj):
        return obj.mp_name

class MP0105M_combo_1(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_combo_1_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")


        queryset = self.get_queryset()

        query = " select A.id "
        query += " , A.mp_id "
        query += " , A.apl_no "
        query += " , B.mp_name "
        query += " FROM service20_mp_mtr A "
        query += " , service20_mpgm B "
        query += " WHERE apl_id = '"+l_apl_id+"' "
        query += " AND mntr_id IS NOT null "
        query += " AND A.mp_id = B.mp_id "

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 보고서 현황 콤보1 ###################################################
class MP0105M_list_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    unv_nm = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    rep_div_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    req_dt_sub = serializers.SerializerMethodField()
    appr_dt_sub = serializers.SerializerMethodField()
    mgr_dt_sub = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','unv_nm','cllg_nm','dept_nm','apl_id','apl_nm','rep_div_nm','status_nm','req_dt_sub','appr_dt_sub','mgr_dt_sub','rep_ym')
    
    def get_unv_nm(self,obj):
        return obj.unv_nm  
    def get_cllg_nm(self,obj):
        return obj.cllg_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_appr_id(self,obj):
        return obj.appr_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_req_dt_sub(self,obj):
        return obj.req_dt_sub
    def get_appr_dt_sub(self,obj):
        return obj.appr_dt_sub
    def get_mgr_dt_sub(self,obj):
        return obj.mgr_dt_sub


class MP0105M_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_list_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")




        queryset = self.get_queryset()

        query = " select t1.id "
        query += " , t1.mp_id     /* 멘토링 프로그램id */ "
        query += " , t2.unv_nm          /* 지원자 대학교 명 */ "
        query += " , t2.cllg_nm         /* 지원자 대학 명 */ "
        query += " , t2.dept_nm         /* 지원자 학부/학과 명 */ "
        query += " , t2.apl_id          /* 지원자(멘토,학생) 학번 */ "
        query += " , t2.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += " , t1.rep_div         /* 보고서 구분(mp0062) */ "
        query += " , c2.std_detl_code_nm   as rep_div_nm "
        query += " , t1.status          /* 상태(mp0070) */ "
        query += " , c1.std_detl_code_nm   as status_nm "
        query += " , substring(t1.req_dt,  1, 10) req_dt_sub    /* 승인요청일 */ "
        query += " , substring(t1.appr_dt, 1, 10) appr_dt_sub   /* 보호자 승인일시 */ "
        query += " , substring(t1.mgr_dt,  1, 10) mgr_dt_sub   /* 관리자 승인일시 */ "
        query += " , t1.rep_ttl   /* 보고서 제목 : 내용 */ "
        query += " , t1.apl_no    /* 멘토 지원 no */ "
        query += " , t1.rep_no    /* 보고서 no */ "
        query += " , t1.rep_div   /* 보고서 구분(mp0062) */ "
        query += " , t1.rep_ttl   /* 보고서 제목 */ "
        query += " , t1.mtr_obj   /* 학습목표 */ "
        query += " , t1.rep_dt    /* 보고서작성일 */ "
        query += " , t1.req_dt    /* 승인요청일 */ "
        query += " , t1.mtr_desc  /* 학습내용 */ "
        query += " , t1.coatching /* 학습외 지도(상담) */ "
        query += " , t1.spcl_note /* 특이사항 */ "
        query += " , t1.mtr_revw  /* 소감문 */ "
        query += " , t1.appr_id   /* 승인자id */ "
        query += " , t1.appr_nm   /* 승인자명 */ "
        query += " , t1.appr_dt   /* 보호자 승인일시 */ "
        query += " , t1.mgr_id    /* 관리자id */ "
        query += " , t1.mgr_dt    /* 관리자 승인일시 */ "
        query += " , t1.rep_ym     "
        query += " from service20_mp_rep t1     /* 프로그램 보고서 */ "
        query += " left join service20_mp_mtr t2 on (t2.mp_id   = t1.mp_id "
        query += " and t2.apl_no = t1.apl_no)       /* 지원 멘토 */ "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  /* 상태(mp0070) */ "
        query += " and c1.std_detl_code = t1.status) "
        query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  /* 보고서 구분(mp0062) */ "
        query += " and c2.std_detl_code = t1.rep_div) "
        query += " where 1=1 "
        query += " and t1.rep_ym    <= date_format(now(), '%%Y%%m') "
        query += " and t1.mp_id     = '"+l_mp_id+"'     /* 멘토링 프로그램id */ "
        # query += " and t1.rep_div   = 'M' "
        # query += " and t1.status    =  '20' /* 제출, 40 완료 */ "
        query += " and t2.apl_id    =  '"+l_apl_id+"' "

        
        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)  

class MP0105M_detail_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    rep_div_nm  = serializers.SerializerMethodField()  
    apl_m  = serializers.SerializerMethodField()
    teacher  = serializers.SerializerMethodField()     
    mte_nm  = serializers.SerializerMethodField()     
    sch_yr  = serializers.SerializerMethodField()     
    obj_sub  = serializers.SerializerMethodField()     
    aaa  = serializers.SerializerMethodField()        
    status_nm  = serializers.SerializerMethodField() 
    unv_nm  = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    tchr_id = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    appr_yn = serializers.SerializerMethodField()
    last_day = serializers.SerializerMethodField()
    att = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = '__all__'
    
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm   
    def get_apl_m(self,obj):
        return obj.apl_m
    def get_teacher(self,obj):      
        return obj.teacher
    def get_mte_nm(self,obj):      
        return obj.mte_nm
    def get_sch_yr(self,obj):      
        return obj.sch_yr
    def get_obj_sub(self,obj):      
        return obj.obj_sub
    def get_aaa(self,obj):         
        return obj.aaa
    def get_status_nm(self,obj):   
        return obj.status_nm
    def get_unv_nm(self,obj):
        return obj.unv_nm
    def get_cllg_nm(self,obj):
        return obj.cllg_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_tchr_id(self,obj):    
        return obj.tchr_id
    def get_mnte_id(self,obj):    
        return obj.mnte_id    
    def get_appr_yn(self,obj):    
        return obj.appr_yn  
    def get_last_day(self,obj):    
        return obj.last_day  
    def get_att(self,obj):    
        return obj.att  

class MP0105M_detail(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_detail_Serializer


    def list(self, request):
        
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_rep_ym = request.GET.get('rep_ym', "")

        queryset = self.get_queryset()

                # /*보고서 상세*/
        # query = " select t1.id,t1.mp_id                                         /* 멘토링 프로그램id   */ "
        # query += " , t1.rep_div                                       /* 보고서 구분(mp0062) */ "
        # query += " , t1.rep_ttl                                       /* 보고서 제목 : 내용  */ "
        # query += " , c2.std_detl_code_nm               as rep_div_nm    "
        # query += " , concat(t2.apl_id, '/', t2.apl_nm) as apl_m       /* 지원자(멘토,학생) 명*/ "
        
        # query += " , t1.tchr_id                                       /* 담당멘티id*/ "
        # query += " , t1.tchr_nm                        as teacher     /* 담당멘티명*/ "
        # query += " , t1.mnte_id                                       /* 담당멘티id*/ "
        # query += " , fn_mp_mte_select_01(t1.mp_id, t1.apl_no) mte_nm        /* 담당멘티명*/ "
        # # query += " , t1.mnte_nm                        as mte_nm        /* 담당멘티명*/ "
        # query += " , t1.sch_nm                         as sch_yr        /* 학교명*/ "
        # query += " , t1.mtr_sub                        as obj_sub     /* 지도과목*/ " 

        # query += " , t1.att_desc                       as aaa          /* 출석현황*/ "

        # query += " , substring(t1.rep_dt,  1, 10)      as rep_dt      /* 보고서작성일         */ "
        # query += " , substring(t1.req_dt,  1, 10)      as req_dt      /* 승인요청일         */ "
        # query += " , t1.appr_nm                                       /* 승인자명            */ "
        # query += " , substring(t1.appr_dt,  1, 10)     as appr_dt     /* 보호자 승인일시      */ "
        # query += " , t1.mgr_id                         as mgr_id      /* 관리자id            */ "
        # query += " , (select mgr_nm from service20_mpgm where mp_id = t1.mp_id) as mgr_nm "
        # query += " , substring(t1.mgr_dt,  1, 10)      as mgr_dt      /* 관리자 승인일시      */ "
        # query += " , t1.status                                        /* 상태(mp0070)         */ "
        # query += " , c1.std_detl_code_nm               as status_nm    "
        # query += " , t1.mtr_obj                                       /* 학습목표            */ "
        # query += " , t1.mtr_desc                                      /* 학습내용            */ "
        # query += " , t1.coatching                                     /* 학습외 지도(상담)   */ "
        # query += " , t1.spcl_note                                     /* 특이사항            */ "
        # query += " , t1.mtr_revw                                      /* 소감문            */ "
        # query += " , t2.unv_nm                                        /* 지원자 대학교 명      */ "
        # query += " , t2.cllg_nm                                       /* 지원자 대학 명      */ "
        # query += " , t2.dept_nm                                       /* 지원자 학부/학과 명 */       "                                    
        # query += " , t1.apl_no                                        /* 멘토 지원 no         */ "
        # query += " , t1.rep_no                                        /* 보고서 no         */ "
        # query += " , t1.rep_div                                       /* 보고서 구분(mp0062) */ "
        # query += " , t1.rep_ttl                                       /* 보고서 제목         */ "
        # query += " , t1.appr_id                                       /* 승인자id            */ "
        # query += " , (case when date_format(last_day(concat(t1.rep_ym,'01')),'%%Y%%m%%d') > date_format(now(),'%%Y%%m%%d') then 'N' else 'Y' end) as appr_yn "        
        # query += " , last_day(concat(t1.rep_ym,'01')) as last_day "        
        # query += " , fn_mp_att_select_01(t2.mp_id, t2.apl_id, t1.rep_ym ) AS att "
        # query += " from service20_mp_rep t1                              /* 프로그램 보고서      */ "
        # query += " left join service20_mp_mtr t2  on (t2.mp_id   = t1.mp_id and t2.apl_no = t1.apl_no) "
        # query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  and c1.std_detl_code = t1.status)  "
        # query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  and c2.std_detl_code = t1.rep_div)  "
        # query += " where 1=1 "
        # query += " and t1.mp_id     = '"+l_mp_id+"'     "
        # query += " and t2.apl_id    =  '"+l_apl_id+"' "
        # query += " and t1.rep_ym    = '"+l_rep_ym+"' "       

        query = f"""
                SELECT t1.id
                    , t1.mp_id /* 멘토링 프로그램id   */
                    , t1.rep_div /* 보고서 구분(mp0062) */
                    , t1.rep_ttl /* 보고서 제목 : 내용  */
                    , c2.std_detl_code_nm AS rep_div_nm
                    , CONCAT(t2.apl_id, '/', t2.apl_nm) AS apl_m /* 지원자(멘토,학생) 명*/
                    , t1.tchr_id /* 담당멘티id*/
                    , t1.tchr_nm AS teacher /* 담당멘티명*/
                    , t1.mnte_id /* 담당멘티id*/
                    , fn_mp_mte_select_01(t1.mp_id, t1.apl_no) mte_nm /* 담당멘티명*/
                    , t1.sch_nm AS sch_yr /* 학교명*/
                    , t1.mtr_sub AS obj_sub /* 지도과목*/
                    , CASE WHEN t1.rep_div = 'F' THEN (SELECT CONCAT(COUNT(*), '회 ', ifnull(SUM(s1.appr_tm), 0), '시간')
                                                        FROM service20_mp_att s1 
                                                        WHERE s1.mp_id = t1.mp_id
                                                        AND s1.apl_no = t1.apl_no) /*출석현황*/
                            else (SELECT CONCAT(COUNT(*), '회 ', ifnull(SUM(s1.appr_tm), 0), '시간')
                                    FROM service20_mp_att s1 
                                WHERE s1.mp_id = t1.mp_id
                                    AND s1.apl_no = t1.apl_no
                                    AND ( s1.att_sdt >= CONCAT(t1.rep_ym, '01') AND s1.att_sdt < CONCAT(DATE_FORMAT(DATE(CONCAT(t1.rep_ym, '01') + INTERVAL 1 MONTH), '%%y%%m'), '01'))) END AS aaa
                    , t1.att_desc AS aaa2 /* 출석현황*/
                    , SUBSTRING(t1.rep_dt, 1, 10) AS rep_dt /* 보고서작성일         */
                    , SUBSTRING(t1.req_dt, 1, 10) AS req_dt /* 승인요청일         */
                    , t1.appr_nm /* 승인자명            */
                    , SUBSTRING(t1.appr_dt, 1, 10) AS appr_dt /* 보호자 승인일시      */
                    , t1.mgr_id AS mgr_id /* 관리자id            */
                    , ( SELECT mgr_nm
                        FROM service20_mpgm 
                        WHERE mp_id = t1.mp_id ) AS mgr_nm
                    , SUBSTRING(t1.mgr_dt, 1, 10) AS mgr_dt /* 관리자 승인일시      */
                    , t1.status /* 상태(mp0070)         */
                    , c1.std_detl_code_nm AS status_nm
                    , t1.mtr_obj /* 학습목표            */
                    , t1.mtr_desc /* 학습내용            */
                    , t1.coatching /* 학습외 지도(상담)   */
                    , t1.spcl_note /* 특이사항            */
                    , t1.mtr_revw /* 소감문            */
                    , t2.unv_nm /* 지원자 대학교 명      */
                    , t2.cllg_nm /* 지원자 대학 명      */
                    , t2.dept_nm /* 지원자 학부/학과 명 */
                    , t1.apl_no /* 멘토 지원 no         */
                    , t1.rep_no /* 보고서 no         */
                    , t1.rep_div /* 보고서 구분(mp0062) */
                    , t1.rep_ttl /* 보고서 제목         */
                    , t1.appr_id /* 승인자id            */
                    , (CASE WHEN DATE_FORMAT(last_day(CONCAT(t1.rep_ym, '01')), '%%Y%%m%%d') > DATE_FORMAT(NOW(), '%%Y%%m%%d') THEN 'N'
                            ELSE 'Y' END) AS appr_yn
                    , last_day(CONCAT(t1.rep_ym, '01')) AS last_day
                    , fn_mp_att_select_01(t2.mp_id, t2.apl_id, t1.rep_ym) AS att
                FROM service20_mp_rep t1 /* 프로그램 보고서      */
                LEFT JOIN service20_mp_mtr t2 ON (t2.mp_id = t1.mp_id AND t2.apl_no = t1.apl_no)
                LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code = 'MP0070' AND c1.std_detl_code = t1.status)
                LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code = 'MP0062' AND c2.std_detl_code = t1.rep_div)
                WHERE 1 = 1
                AND t1.mp_id = '{l_mp_id}'
                AND t2.apl_id = '{l_apl_id}'
                AND t1.rep_ym = '{l_rep_ym}';
        """

        print(query)
        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)     

class MP0105M_detail_2_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_id = serializers.SerializerMethodField()
    rep_div_nm = serializers.SerializerMethodField()
    apl_m = serializers.SerializerMethodField()
    tchr_id = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    att_desc = serializers.SerializerMethodField()
    rep_dt = serializers.SerializerMethodField()
    req_dt = serializers.SerializerMethodField()
    appr_id = serializers.SerializerMethodField()
    appr_nm = serializers.SerializerMethodField()
    appr_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    mtr_desc = serializers.SerializerMethodField()
    coatching = serializers.SerializerMethodField()
    spcl_note = serializers.SerializerMethodField()
    mtr_revw = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    mte_nm = serializers.SerializerMethodField()
    obj_sub = serializers.SerializerMethodField()
    aaa = serializers.SerializerMethodField()
    grd_id = serializers.SerializerMethodField()
    grd_nm = serializers.SerializerMethodField()
    att = serializers.SerializerMethodField()
    appr_yn = serializers.SerializerMethodField()
    last_day = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = '__all__'
    
    def get_mp_id(self,obj):
        return obj.mp_id
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm
    def get_apl_m(self,obj):
        return obj.apl_m
    def get_tchr_id(self,obj):
        return obj.tchr_id
    def get_tchr_nm(self,obj):
        return obj.tchr_nm
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_mtr_sub(self,obj):
        return obj.mtr_sub
    def get_att_desc(self,obj):
        return obj.att_desc
    def get_rep_dt(self,obj):
        return obj.rep_dt
    def get_req_dt(self,obj):
        return obj.req_dt
    def get_appr_id(self,obj):
        return obj.appr_id
    def get_appr_nm(self,obj):
        return obj.appr_nm
    def get_appr_dt(self,obj):
        return obj.appr_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_mgr_dt(self,obj):
        return obj.mgr_dt
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_mtr_desc(self,obj):
        return obj.mtr_desc
    def get_coatching(self,obj):
        return obj.coatching
    def get_spcl_note(self,obj):
        return obj.spcl_note
    def get_mtr_revw(self,obj):
        return obj.mtr_revw
    def get_apl_no(self,obj):
        return obj.apl_no
    def get_apl_id(self,obj):
        return obj.apl_id   
    def get_teacher(self,obj):
        return obj.teacher
    def get_mte_nm(self,obj):
        return obj.mte_nm
    def get_obj_sub(self,obj):
        return obj.obj_sub
    def get_aaa(self,obj):    
        return obj.aaa 
    def get_grd_id(self,obj):
        return obj.grd_id       
    def get_grd_nm(self,obj):
        return obj.grd_nm
    def get_att(self,obj):
        return obj.att        
    def get_appr_yn(self,obj):
        return obj.appr_yn  
    def get_last_day(self,obj):
        return obj.last_day          

class MP0105M_detail_2(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_detail_2_Serializer


    def list(self, request):
        mp_id = request.GET.get('mp_id', "")
        apl_id = request.GET.get('apl_id', "")
        rep_ym = request.GET.get('rep_ym', "")

        queryset = self.get_queryset()

        # /*보고서 상세*/
        # query = "select t2.id,t1.mp_id       /* 멘토링 프로그램id   */ "
        # query += "     , t2.rep_div     /* 보고서 구분(mp0062) */"
        # query += "     , t2.rep_ttl     /* 보고서 제목 : 내용  */"
        # query += "     , (select std_detl_code_nm "
        # query += "          from service20_com_cdd "
        # query += "         where std_grp_code  = 'mp0062' "
        # query += "           and std_detl_code = t2.rep_div)   as rep_div_nm     "
        # query += "     , concat(t1.apl_id, '/', t1.apl_nm)     as apl_m       /* 지원자(멘토,학생) 명*/ "
        # query += "     , t3.tchr_id     /* 지도교사 id */"
        # query += "     , t3.tchr_nm  as teacher   /* 지도교사 명 */     "
        # query += "     , t3.mnte_id     /* 멘티id */ "
        # query += "     , t3.mnte_nm  as mte_nm"
        # query += "     , t3.sch_yr      /* 학교명/학년 */ "
        # query += "     , t3.mtr_sub  as obj_sub   /* 지도과목 */ "
        # query += "     , (select concat(count(*), '회 ', ifnull(sum(s1.appr_tm), 0), '시간') "
        # query += "         from service20_mp_att s1 "
        # query += "        where s1.mp_id = t1.mp_id "
        # query += "          and s1.apl_no = t1.apl_no "
        # query += "          and "
        # query += "              ("
        # query += "                  s1.att_sdt >= concat(t2.rep_ym, '01') "
        # query += "              and s1.att_sdt  < concat(date_format(date(concat(t2.rep_ym, '01') + interval 1 month), '%%y%%m'), '01')"
        # query += "              ) "
        # query += "       ) as aaa   /*출석현황*/  "
        # query += "     , null as rep_dt "
        # query += "     , null as req_dt              "
        # query += "     , t3.mp_plc "
        # query += "     , case when t3.mp_plc = 'b' then t3.grd_id else t3.tchr_id end as appr_id /*장소가 멘티가정이면 승인자는 보호자, 그렇지 않으면 교사*/";
        # query += "     , case when t3.mp_plc = 'b' then t3.grd_nm else t3.tchr_nm end as appr_nm";
        # query += "     , null       as appr_dt "
        # query += "     , t4.mgr_id  as mgr_id "
        # query += "     , t4.mgr_nm  as mgr_nm "
        # query += "     , null       as mgr_dt"
        # query += "     , t2.status "
        # query += "     , c1.std_detl_code_nm as status_nm     "
        # query += "     , t2.mtr_obj "
        # query += "     , t2.mtr_desc as mtr_desc ";
        # query += "     , t2.coatching as coatching "
        # query += "     , t2.spcl_note as spcl_note "
        # query += "     , t2.mtr_revw as mtr_revw    "
        # query += "     , fn_mp_att_select_01(t1.mp_id, t1.apl_id, t2.rep_ym ) AS att "
        # query += "     , t1.apl_no "
        # query += "     , t1.apl_id "
        # query += "     , t2.rep_no "
        # query += "     , t2.rep_ym "
        # query += "     , t3.grd_id    /*주보호자id*/";
        # query += "     , t3.grd_nm    /*보호자명*/";
        # query += "     , (case when date_format(last_day(concat(t2.rep_ym,'01')),'%%Y%%m%%d') > date_format(now(),'%%Y%%m%%d') then 'N' else 'Y' end) as appr_yn "
        # query += "     , last_day(concat(t2.rep_ym,'01')) as last_day "
        # query += "  from service20_mp_mtr t1 "
        # query += "   left join service20_mp_rep t2 "
        # query += "       on ("
        # query += "           t2.mp_id = t1.mp_id "
        # query += "       and t2.apl_no = t1.apl_no"
        # query += "       ) "
        # query += "   left join service20_mpgm t4 "
        # query += "       on ("
        # query += "           t4.mp_id = t1.mp_id"
        # query += "       ) "
        # query += "   left join "
        # query += "       (select distinct s2.tchr_id  "
        # query += "            , s2.tchr_nm  "
        # query += "            , s2.mnte_id  "
        # query += "            , s2.mnte_nm "
        # query += "            , concat(s2.sch_nm, '/', s2.sch_yr, '학년') as sch_yr /* 학교명/학년 */ "
        # query += "            , s3.mtr_sub /* 지도과목 */"
        # query += "            , truncate(rand()*7 + 1, 0) as att_desc  "
        # query += "            , s3.mtr_obj "
        # query += "            , s1.mp_id "
        # query += "            , s1.apl_no "
        # query += "            , s1.apl_id "
        # query += "            , s2.grd_id "
        # query += "            , s2.grd_nm "
        # query += "            , s2.mp_plc "
        # query += "         from service20_mp_mtr s1 "
        # query += "          left join service20_mp_mte s2 "
        # query += "              on ("
        # query += "                  s2.mp_id = s1.mp_id "
        # query += "              and s2.apl_no = s1.apl_no"
        # query += "              ) "
        # query += "          left join service20_mp_plnh s3 "
        # query += "              on ("
        # query += "                  s3.mp_id = s1.mp_id "
        # query += "              and s3.apl_no = s1.apl_no"
        # query += "              ) "
        # query += "       ) t3 "
        # query += "       on ("
        # query += "           t3.mp_id = t1.mp_id "
        # query += "       and t3.apl_no = t1.apl_no"
        # query += "       ) "
        # query += "   left join service20_com_cdd c1 "
        # query += "       on ("
        # query += "           c1.std_grp_code = 'mp0070'  "
        # query += "       and c1.std_detl_code = t2.status"
        # query += "       ) "
        # query += " where t1.mp_id = '"+str(mp_id)+"' "
        # query += "   and t1.apl_id = '"+str(apl_id)+"' "
        # # query += "   and t2.status = '00' "
        # query += "   and t2.rep_ym = '"+str(rep_ym)+"'"

        query = f"""
                SELECT t2.id
                    , t1.mp_id /* 멘토링 프로그램id   */
                    , t2.rep_div /* 보고서 구분(mp0062) */
                    , t2.rep_ttl /* 보고서 제목 : 내용  */
                    , ( SELECT std_detl_code_nm
                        FROM service20_com_cdd
                        WHERE std_grp_code = 'MP0062'
                            AND std_detl_code = t2.rep_div) AS rep_div_nm
                    , CONCAT(t1.apl_id, '/', t1.apl_nm) AS apl_m /* 지원자(멘토,학생) 명*/
                    , t3.tchr_id /* 지도교사 id */
                    , t3.tchr_nm AS teacher /* 지도교사 명 */
                    , t3.mnte_id /* 멘티id */
                    , t3.mnte_nm AS mte_nm
                    , t3.sch_yr /* 학교명/학년 */
                    , t3.mtr_sub AS obj_sub /* 지도과목 */
                    , CASE WHEN t2.rep_div = 'F' THEN (SELECT CONCAT(COUNT(*), '회 ', ifnull(SUM(s1.appr_tm), 0), '시간')
                                                        FROM service20_mp_att s1 
                                                        WHERE s1.mp_id = t1.mp_id
                                                        AND s1.apl_no = t1.apl_no) /*출석현황*/
                            else (SELECT CONCAT(COUNT(*), '회 ', ifnull(SUM(s1.appr_tm), 0), '시간')
                                    FROM service20_mp_att s1 
                                WHERE s1.mp_id = t1.mp_id
                                    AND s1.apl_no = t1.apl_no
                                    AND ( s1.att_sdt >= CONCAT(t2.rep_ym, '01') AND s1.att_sdt < CONCAT(DATE_FORMAT(DATE(CONCAT(t2.rep_ym, '01') + INTERVAL 1 MONTH), '%%y%%m'), '01'))) END AS aaa
                    , NULL AS rep_dt
                    , NULL AS req_dt
                    , t3.mp_plc
                    , CASE WHEN t3.mp_plc = 'b' THEN t3.grd_id
                            ELSE t3.tchr_id END AS appr_id /*장소가 멘티가정이면 승인자는 보호자, 그렇지 않으면 교사*/
                    , CASE WHEN t3.mp_plc = 'b' THEN t3.grd_nm
                            ELSE t3.tchr_nm END AS appr_nm
                    , NULL AS appr_dt
                    , t4.mgr_id AS mgr_id
                    , t4.mgr_nm AS mgr_nm
                    , NULL AS mgr_dt
                    , t2.status
                    , c1.std_detl_code_nm AS status_nm
                    , t2.mtr_obj
                    , t2.mtr_desc AS mtr_desc
                    , t2.coatching AS coatching
                    , t2.spcl_note AS spcl_note
                    , t2.mtr_revw AS mtr_revw
                    , fn_mp_att_select_01(t1.mp_id, t1.apl_id, t2.rep_ym ) AS att
                    , t1.apl_no
                    , t1.apl_id
                    , t2.rep_no
                    , t2.rep_ym
                    , t3.grd_id /*주보호자id*/
                    , t3.grd_nm /*보호자명*/
                    , (CASE WHEN DATE_FORMAT(last_day(CONCAT(t2.rep_ym, '01')), '%%Y%%m%%d') > DATE_FORMAT(NOW(), '%%Y%%m%%d') THEN 'N'
                            ELSE 'Y' END) AS appr_yn
                    , last_day(CONCAT(t2.rep_ym, '01')) AS last_day
                FROM service20_mp_mtr t1
                LEFT JOIN service20_mp_rep t2 ON (t2.mp_id = t1.mp_id AND t2.apl_no = t1.apl_no)
                LEFT JOIN service20_mpgm t4 ON (t4.mp_id = t1.mp_id)
                LEFT JOIN (   SELECT
                            DISTINCT s2.tchr_id
                                    , s2.tchr_nm
                                    , s2.mnte_id
                                    , s2.mnte_nm
                                    , CONCAT(s2.sch_nm, '/', s2.sch_yr, '학년') AS sch_yr /* 학교명/학년 */
                                    , s3.mtr_sub /* 지도과목 */
                                    , TRUNCATE (RAND()* 7 + 1, 0) AS att_desc
                                    , s3.mtr_obj
                                    , s1.mp_id
                                    , s1.apl_no
                                    , s1.apl_id
                                    , s2.grd_id
                                    , s2.grd_nm
                                    , s2.mp_plc
                                FROM service20_mp_mtr s1
                                LEFT JOIN service20_mp_mte s2 ON (s2.mp_id = s1.mp_id AND s2.apl_no = s1.apl_no)
                                LEFT JOIN service20_mp_plnh s3 ON (s3.mp_id = s1.mp_id AND s3.apl_no = s1.apl_no) ) t3 ON (t3.mp_id = t1.mp_id AND t3.apl_no = t1.apl_no)
                LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code = 'MP0070' AND c1.std_detl_code = t2.status )
                WHERE t1.mp_id = '{mp_id}'
                AND t1.apl_id = '{apl_id}'
                AND t2.rep_ym = '{rep_ym}'
        """
        print(query)
        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)          

# 보고서 멘토 정보 조회 ###################################################
class MP0105M_listMento_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mtr
        fields = '__all__'


class MP0105M_listMento(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0105M_listMento_Serializer


    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")


        queryset = self.get_queryset()

        query  = "select * "
        query += "  from service20_mp_mtr "
        query += " where mp_id = '"+l_mp_id+"' "
        query += "   and apl_id = '"+l_user_id+"' "

        
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)      

# 보고서 현황 save
@csrf_exempt
def MP0105M_update(request,pk):


    mp_id     = request.POST.get('mp_id', "")
    apl_no    = request.POST.get('apl_no', 0)
    rep_no    = request.POST.get('rep_no', 0)
    rep_div   = request.POST.get('rep_div', "")
    mnte_id   = request.POST.get('mnte_id', "")
    mnte_nm   = request.POST.get('mnte_nm', "")
    tchr_id   = request.POST.get('tchr_id', "")
    tchr_nm   = request.POST.get('tchr_nm', "")
    sch_nm    = request.POST.get('sch_nm', "")
    mtr_sub   = request.POST.get('mtr_sub', "")
    att_desc  = request.POST.get('att_desc', "")
    rep_ttl   = request.POST.get('rep_ttl', "")
    mtr_obj   = request.POST.get('mtr_obj', "")
    rep_dt    = request.POST.get('rep_dt', "")
    req_dt    = request.POST.get('req_dt', "")
    mtr_desc  = request.POST.get('mtr_desc', "")
    coatching = request.POST.get('coatching', "")
    spcl_note = request.POST.get('spcl_note', "")
    mtr_revw  = request.POST.get('mtr_revw', "")
    appr_id   = request.POST.get('appr_id', "")
    appr_nm   = request.POST.get('appr_nm', "")
    appr_dt   = request.POST.get('appr_dt', "")
    mgr_id    = request.POST.get('mgr_id', "")
    mgr_dt    = request.POST.get('mgr_dt', "")
    status    = request.POST.get('status', "")
    ins_id    = request.POST.get('ins_id', "")
    ins_dt    = request.POST.get('ins_dt', "")
    ins_pgm   = request.POST.get('ins_pgm', "")
    upd_id    = request.POST.get('upd_id', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")

    teacher   = request.POST.get('teacher', "")
    sch_yr    = request.POST.get('sch_yr', "")
    obj_sub   = request.POST.get('obj_sub', "")
    aaa       = request.POST.get('aaa', "")
    mte_nm   = request.POST.get('mte_nm', "")
    status   = request.POST.get('status', "")
    appr_id  = request.POST.get('appr_id', "")
    appr_nm  = request.POST.get('appr_nm', "")
    mgr_id   = request.POST.get('mgr_id', "")
    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    if pk == 1:
        # /*보고서현황작성_승인요청*/
        update_text = " update service20_mp_rep "
        update_text += " set mnte_id    = '" +mnte_id+"'      /*담당멘티id*/ "
        update_text += " , mnte_nm     = '" +mte_nm+"'      /*담당멘티명*/ "
        update_text += " , tchr_id     = '" +tchr_id+"'      /*담당교사id*/ "
        update_text += " , tchr_nm     = '" +teacher+"'      /*담당교사명*/ "
        update_text += " , sch_nm      = '" +sch_yr+"'       /*학교명*/ "
        update_text += " , mtr_sub     = '" +obj_sub+"'      /*지도과목*/ "
        update_text += " , att_desc    = '" +aaa+"'          /*출석현황*/   "
        update_text += " , status    = '10'          /*status - 제출*/   "
        update_text += " , appr_id     = '" +str(appr_id)+"'       "
        update_text += " , appr_nm     = '" +str(appr_nm)+"'       "
        update_text += " , mgr_id      = '" +str(mgr_id)+"'        "
        # update_text += " , rep_dt      = now()    /*보고서작성일*/     "    
        update_text += " , upd_id      = '"+str(upd_id)   +"'    /*수정자id*/         "    
        update_text += " , upd_ip      = '"+str(client_ip)   +"'    /*수정자ip*/         "    
        update_text += " , upd_dt      = now()    /*수정일시*/         "    
        update_text += " , upd_pgm     = '"+str(upd_pgm)  +"'    /*수정프로그램id*/   "    
        update_text += " where 1=1 "
        update_text += " and mp_id  = '" +mp_id+"' "
        update_text += " and apl_no = '"+str(apl_no)+"' "
        update_text += " and rep_no = '"+str(rep_no)+"' "

        # 따옴표 처리(학습목표, 학습내용, 학습외 지도(상담), 특이사항, 소감문)
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_obj=str(mtr_obj))        
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_desc=str(mtr_desc))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(coatching=str(coatching))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(spcl_note=str(spcl_note))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_revw=str(mtr_revw))
    elif pk == 2:
        # /*보고서현황작성_승인요청*/
        update_text = " update service20_mp_rep "
        update_text += " set mnte_id    = '" +mnte_id+"'      /*담당멘티id*/ "
        update_text += " , mnte_nm     = '" +mte_nm+"'      /*담당멘티명*/ "
        update_text += " , tchr_id     = '" +tchr_id+"'      /*담당교사id*/ "
        update_text += " , tchr_nm     = '" +teacher+"'      /*담당교사명*/ "
        update_text += " , sch_nm      = '" +sch_yr+"'       /*학교명*/ "
        update_text += " , mtr_sub     = '" +obj_sub+"'      /*지도과목*/ "
        update_text += " , att_desc    = '" +aaa+"'          /*출석현황*/   "
        update_text += " , status    = '20'          /*status - 제출*/   "
        update_text += " , appr_id     = '" +str(appr_id)+"'       "
        update_text += " , appr_nm     = '" +str(appr_nm)+"'       "
        update_text += " , mgr_id      = '" +str(mgr_id)+"'        "
        update_text += " , req_dt      = now()    /*승인요청일*/       "
        update_text += " , upd_id      = '"+str(upd_id)   +"'    /*수정자id*/         "    
        update_text += " , upd_ip      = '"+str(client_ip)   +"'    /*수정자ip*/         "    
        update_text += " , upd_dt      = now()    /*수정일시*/         "    
        update_text += " , upd_pgm     = '"+str(upd_pgm)  +"'    /*수정프로그램id*/   "    
        update_text += " where 1=1 "
        update_text += " and mp_id  = '" +mp_id+"' "
        update_text += " and apl_no = '"+str(apl_no)+"' "
        update_text += " and rep_no = '"+str(rep_no)+"' "

        # 따옴표 처리(학습목표, 학습내용, 학습외 지도(상담), 특이사항, 소감문)
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_obj=str(mtr_obj))        
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_desc=str(mtr_desc))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(coatching=str(coatching))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(spcl_note=str(spcl_note))
        mp_rep.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no),rep_no=str(rep_no)).update(mtr_revw=str(mtr_revw)) 
    
    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
 
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 보고서 생성 버튼 ###################################################
class MP0105M_listBtn_Serializer(serializers.ModelSerializer):

    mpgm_month  = serializers.SerializerMethodField()  
    mpgm_month2 = serializers.SerializerMethodField()
    rep_status = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = '__all__'
    
    def get_mpgm_month(self,obj):
        return obj.mpgm_month  
    def get_mpgm_month2(self,obj):
        return obj.mpgm_month2          
    def get_rep_status(self,obj):
        return obj.rep_status

class MP0105M_listBtn(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0105M_listBtn_Serializer


    def list(self, request):
        
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_no = request.GET.get('apl_no', "")

        queryset = self.get_queryset()

        query  = "select t3.*, t4.status as mtr_status"
        query += "     , case when t3.mpgm_month2 = substring(REPLACE(t5.mnt_to_dt, '-', ''), 1, 6) THEN 'F' ELSE 'M' END AS rep_status"
        query += " from ( "    
        query += "    select date_format(date_table.date,'%%Y-%%m') as mpgm_month "   
        query += "         , date_format(date_table.date,'%%Y%%m') as mpgm_month2 " 
        query += "         , 'id' as mp_id "  
        query += "    from ( "    
        query += "        select sub_a.mnt_to_dt - interval (a.a + (10 * b.a) + (100 * c.a)) day as date "    
        query += "        from service20_mpgm sub_a,(select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as a "    
        query += "        cross join (select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as b "    
        query += "        cross join (select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as c "    
        query += "        where sub_a.mp_id = '"+l_mp_id+"' "    
        query += "    ) date_table, service20_mpgm b "    
        query += "    where date(date_table.date) between date(b.mnt_fr_dt) and date(b.mnt_to_dt) "    
        query += "    and b.mp_id = '"+l_mp_id+"'     "    
        query += "    and b.status = '60'     "  
        query += "    group by date_format(date_table.date,'%%Y-%%m') "    
        query += ") as t3 "    
        query += " left join service20_mp_mtr t4 on (t4.mp_id = '" + l_mp_id + "' and t4.apl_no = '" + l_apl_no + "')"
        query += " left join service20_mpgm t5 on (t5.mp_id = '" + l_mp_id + "')"
        query += "where t3.mpgm_month2 not in ( "    
        query += "    select ifnull(sub_t2.rep_ym,'') "    
        query += "      from service20_mpgm as sub_t1 left join (select * "    
        query += "                                                  from service20_mp_rep "    
        query += "                                                 where mp_id = '"+l_mp_id+"' "    
        query += "                                                   and apl_no = '"+l_apl_no+"' "    
        query += "                                               ) as sub_t2 on (sub_t1.mp_id = sub_t2.mp_id) "    
        query += "    where sub_t1.mp_id = '"+l_mp_id+"' "    
        query += ") "    
        query += "and t3.mpgm_month <= date_format(now(), '%%Y-%%m') "       
        query += "and t3.mpgm_month2 <> '201903' " ## 201903은 첫시작단계라 월별보고서 제외. 추후 필요하다고 하면 삭제하면 됨.

        print(query)
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)   

# 보고서 생성
@csrf_exempt
def MP0105M_insert(request):

    mp_id    = request.POST.get('mp_id', "")
    apl_no    = request.POST.get('apl_no', "")
    rep_ym    = request.POST.get('rep_ym', "")
    rep_div    = request.POST.get('rep_div', "")

    upd_id    = request.POST.get('upd_id', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    update_text += "insert into service20_mp_rep     /* 프로그램 보고서 */ "    
    update_text += "     ( mp_id     /* 멘토링 프로그램id */ "    
    update_text += "     , apl_no    /* 멘토 지원 no */ "    
    update_text += "     , rep_no    /* 보고서 no */ "    
    update_text += "     , rep_div   /* 보고서 구분(mp0062) */ "    
    update_text += "     , rep_ym    /* 보고서 연월(월보고) */ "    
    update_text += "     , mnte_id   /* 담당멘티id */ "    
    update_text += "     , mnte_nm   /* 담당멘티명 */ "    
    update_text += "     , tchr_id   /* 담당교사id */ "    
    update_text += "     , tchr_nm   /* 담당교사명 */ "    
    update_text += "     , sch_nm    /* 학교명 */ "    
    update_text += "     , mtr_sub   /* 지도과목 */ "    
    update_text += "     , att_desc  /* 출석현황 */ "    
    update_text += "     , rep_ttl   /* 보고서 제목 */ "    
    update_text += "     , mtr_obj   /* 학습목표 */ "    
    update_text += "     , rep_dt    /* 보고서작성일 */ "    
    update_text += "     , req_dt    /* 승인요청일 */ "    
    update_text += "     , mtr_desc  /* 학습내용 */ "    
    update_text += "     , coatching /* 학습외 지도(상담) */ "    
    update_text += "     , spcl_note /* 특이사항 */ "    
    update_text += "     , mtr_revw  /* 소감문 */ "    
    update_text += "     , appr_id   /* 승인자id */ "    
    update_text += "     , appr_nm   /* 승인자명 */ "    
    update_text += "     , appr_dt   /* 보호자 승인일시 */ "    
    update_text += "     , mgr_id    /* 관리자id */ "    
    update_text += "     , mgr_dt    /* 관리자 승인일시 */ "    
    update_text += "     , status    /* 상태(mp0070) */ "    
    update_text += "     , ins_id    /* 입력자id */ "    
    update_text += "     , ins_ip    /* 입력자ip */ "    
    update_text += "     , ins_dt    /* 입력일시 */ "    
    update_text += "     , ins_pgm   /* 입력프로그램id */ "    
    update_text += "     , upd_id    /* 수정자id */ "    
    update_text += "     , upd_ip    /* 수정자ip */ "    
    update_text += "     , upd_dt    /* 수정일시 */ "    
    update_text += "     , upd_pgm   /* 수정프로그램id */ "    
    update_text += ") "    
    update_text += "select a.mp_id     /* 멘토링 프로그램id */ "    
    update_text += "     , a.apl_no    /* 멘토 지원 no */ "    
    update_text += "     , (select ifnull(max(rep_no),0)+1 from service20_mp_rep where mp_id = a.mp_id and apl_no = a.apl_no) rep_no "    
    update_text += "     , '" + str(rep_div) + "'   /* 보고서 구분(mp0062) */ "    
    update_text += "     , '"+str(rep_ym)+"'    /* 보고서 연월(월보고) */ "    
    update_text += "     , null   /* 담당멘티id */ "    
    update_text += "     , null   /* 담당멘티명 */ "    
    update_text += "     , null   /* 담당교사id */ "    
    update_text += "     , null   /* 담당교사명 */ "    
    update_text += "     , null    /* 학교명 */ "    
    update_text += "     , null   /* 지도과목 */ "    
    update_text += "     , null  /* 출석현황 */ "    
    update_text += "     , concat(SUBSTRING('"+str(rep_ym)+"',1,4),'년 ',SUBSTRING('"+str(rep_ym)+"',5,2),'월 보고서')   /* 보고서 제목 */ "    
    update_text += "     , null   /* 학습목표 */ "    
    update_text += "     , now()    /* 보고서작성일 */ "    
    update_text += "     , null    /* 승인요청일 */ "    
    update_text += "     , null  /* 학습내용 */ "    
    update_text += "     , null /* 학습외 지도(상담) */ "    
    update_text += "     , null /* 특이사항 */ "    
    update_text += "     , null  /* 소감문 */ "    
    update_text += "     , null   /* 승인자id */ "    
    update_text += "     , null   /* 승인자명 */ "    
    update_text += "     , null   /* 보호자 승인일시 */ "    
    update_text += "     , null    /* 관리자id */ "    
    update_text += "     , null    /* 관리자 승인일시 */ "    
    update_text += "     , '00'    /* 상태(mp0070) */ "    
    update_text += "     , '"+str(upd_id)   +"'     /* 입력자id */ "    
    update_text += "     , '"+str(client_ip)   +"'    /* 입력자ip */ "    
    update_text += "     , now()    /* 입력일시 */ "    
    update_text += "     , '"+str(upd_pgm)   +"'   /* 입력프로그램id */ "    
    update_text += "     , '"+str(upd_id)   +"'     /* 수정자id */ "    
    update_text += "     , '"+str(client_ip)   +"'    /* 수정자ip */ "    
    update_text += "     , now()    /* 수정일시 */ "    
    update_text += "     , '"+str(upd_pgm)   +"'   /* 수정프로그램id */ "    
    update_text += "  from service20_mp_plnh a "    
    update_text += " where 1=1 "    
    update_text += "   and a.mp_id = '"+str(mp_id)+"' "    
    update_text += "   and a.apl_no = '"+str(apl_no)+"' "    
    
    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
 
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 보고서 Min, Max ###################################################
class MP0105M_detail_min_max_Serializer(serializers.ModelSerializer):

    min_len_mp_rep_mtr_obj = serializers.SerializerMethodField()
    max_len_mp_rep_mtr_obj = serializers.SerializerMethodField()
    min_len_mp_rep_mtr_desc = serializers.SerializerMethodField()
    max_len_mp_rep_mtr_desc = serializers.SerializerMethodField()
    min_len_mp_rep_coatching = serializers.SerializerMethodField()
    max_len_mp_rep_coatching = serializers.SerializerMethodField()
    min_len_mp_rep_spcl_note = serializers.SerializerMethodField()
    max_len_mp_rep_spcl_note = serializers.SerializerMethodField()
    min_len_mp_rep_mtr_revw = serializers.SerializerMethodField()
    max_len_mp_rep_mtr_revw = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = '__all__'

    def get_min_len_mp_rep_mtr_obj(self,obj):
        return obj.min_len_mp_rep_mtr_obj
    def get_max_len_mp_rep_mtr_obj(self,obj):
        return obj.max_len_mp_rep_mtr_obj
    def get_min_len_mp_rep_mtr_desc(self,obj):
        return obj.min_len_mp_rep_mtr_desc
    def get_max_len_mp_rep_mtr_desc(self,obj):
        return obj.max_len_mp_rep_mtr_desc
    def get_min_len_mp_rep_coatching(self,obj):
        return obj.min_len_mp_rep_coatching
    def get_max_len_mp_rep_coatching(self,obj):
        return obj.max_len_mp_rep_coatching
    def get_min_len_mp_rep_spcl_note(self,obj):
        return obj.min_len_mp_rep_spcl_note
    def get_max_len_mp_rep_spcl_note(self,obj):
        return obj.max_len_mp_rep_spcl_note
    def get_min_len_mp_rep_mtr_revw(self,obj):
        return obj.min_len_mp_rep_mtr_revw
    def get_max_len_mp_rep_mtr_revw(self,obj):
        return obj.max_len_mp_rep_mtr_revw

class MP0105M_detail_min_max(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0105M_detail_min_max_Serializer


    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = f"""
                select '0' as id, '' as mp_id
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0004', 'MS0028', '10') min_len_mp_rep_mtr_obj /* 학습목표(MTR_OBJ) - 프로그램 보고서(MP_REP) */  
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0004', 'MS0029', '10') max_len_mp_rep_mtr_obj /* 학습목표(MTR_OBJ) - 프로그램 보고서(MP_REP) */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0005', 'MS0028', '10') min_len_mp_rep_mtr_desc /* 학습내용(MTR_DESC) - 프로그램 보고서(MP_REP) */  
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0005', 'MS0029', '10') max_len_mp_rep_mtr_desc /* 학습내용(MTR_DESC) - 프로그램 보고서(MP_REP) */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0006', 'MS0028', '10') min_len_mp_rep_coatching /* 학습외 지도(상담)(COATCHING) - 프로그램 보고서(MP_REP)   */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0006', 'MS0029', '10') max_len_mp_rep_coatching /* 학습외 지도(상담)(COATCHING) - 프로그램 보고서(MP_REP)   */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0007', 'MS0028', '10') min_len_mp_rep_spcl_note /* 특이사항(SPCL_NOTE) - 프로그램 보고서(MP_REP)   */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0007', 'MS0029', '10') max_len_mp_rep_spcl_note /* 특이사항(SPCL_NOTE) - 프로그램 보고서(MP_REP)    */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0008', 'MS0028', '10') min_len_mp_rep_mtr_revw /* 소감문(MTR_REVW) - 프로그램 보고서(MP_REP)   */
                    , fn_mp_sub_att_val_select_01('{l_mp_id}', 'CL0008', 'MS0029', '10') max_len_mp_rep_mtr_revw /* 소감문(MTR_REVW) - 프로그램 보고서(MP_REP)    */
        """
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)   

#####################################################################################
# MP0105M - END
#####################################################################################


#####################################################################################
# MP0106M - START
#####################################################################################

# 보고서 현황 리스트 ###################################################
class MP0106M_list_Serializer(serializers.ModelSerializer):

    bank_acct_mask = serializers.SerializerMethodField()
    exp_div_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_exp
        fields = '__all__'

    def get_bank_acct_mask(self,obj):
        return obj.bank_acct_mask
    def get_exp_div_nm(self,obj):
        return obj.exp_div_nm        

class MP0106M_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0106M_list_Serializer


    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")


        queryset = self.get_queryset()

        query = " select t1.id,t1.mp_id                              /*멘토링 프로그램id     */ "
        query += " , t1.apl_no                             /*멘토 지원 no        */ "
        query += " , t1.exp_no                             /*활동비 no        */ "
        query += " , substring(t1.exp_mon,5,2) as exp_mon  /*활동비 월        */ "
        query += " , t1.exp_div                            /*활동비 구분        */ "
        query += " , (select std_detl_code_nm from service20_com_cdd where t1.EXP_DIV = std_detl_code and std_grp_code = 'MP0102') as exp_div_nm /*활동비 구분명 */ "
        query += " , t1.exp_ttl                            /*활동비 제목        */ "
        query += " , t1.appr_tm                            /*인정시간 합계        */ "
        query += " , t1.sum_exp                            /*활동비=appr_tm * unit_price*/ "
        query += " , t1.bank_acct                          /*은행 계좌 번호        */ "
        query += " , t1.bank_cd                            /*은행 코드        */ "
        query += " , t1.bank_nm                            /*은행 명           */ "
        query += " , t1.bank_dpsr                          /*예금주           */ "
        query += ", concat(left(t1.bank_acct,2),repeat('*',length(t1.bank_acct)-4),right(t1.bank_acct,2))  as bank_acct_mask "
        query += " from service20_mp_exp t1                   /*프로그램 출석부(멘토)     */ "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id "
        query += " and t3.apl_no   = t1.apl_no) "
        query += " where 1=1 "
        query += " and t1.mp_id    = '"+l_mp_id+"'     "
        query += " and t3.apl_id   = '"+l_apl_id+"' "
        query += " order by t1.exp_mon "

        queryset = mp_exp.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#####################################################################################
# MP0106M - END
#####################################################################################

#####################################################################################
# MP0107 - START
#####################################################################################

# 활동중단 사유서 리스트 ###################################################
class MP0107_list_Serializer(serializers.ModelSerializer):

    mp_id = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    wirte_status = serializers.SerializerMethodField()
    wirte_status_nm = serializers.SerializerMethodField()
    wrt_dt = serializers.SerializerMethodField()
    sbm_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    base_hr = serializers.SerializerMethodField()
    act_hr = serializers.SerializerMethodField()
    stop_desc = serializers.SerializerMethodField()    
    stop_resp = serializers.SerializerMethodField()
    stop_resp_nm = serializers.SerializerMethodField()
    stop_tp = serializers.SerializerMethodField()
    stop_tp_nm = serializers.SerializerMethodField()
    min_len_mp_stop_req_stop_desc = serializers.SerializerMethodField()
    max_len_mp_stop_req_stop_desc = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_mp_id(self,obj):
        return obj.mp_id
    def get_mp_name(self,obj):
        return obj.mp_name
    def get_status(self,obj):
        return obj.status
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_wirte_status(self,obj):
        return obj.wirte_status
    def get_wirte_status_nm(self,obj):
        return obj.wirte_status_nm
    def get_wrt_dt(self,obj):
        return obj.wrt_dt
    def get_sbm_dt(self,obj):
        return obj.sbm_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_base_hr(self,obj):
        return obj.base_hr
    def get_act_hr(self,obj):
        return obj.act_hr
    def get_stop_desc(self,obj):
        return obj.stop_desc      
    def get_stop_resp(self,obj):
        return obj.stop_resp 
    def get_stop_resp_nm(self,obj):
        return obj.stop_resp_nm 
    def get_stop_tp(self,obj):
        return obj.stop_tp 
    def get_stop_tp_nm(self,obj):
        return obj.stop_tp_nm        
    def get_min_len_mp_stop_req_stop_desc(self,obj):
        return obj.min_len_mp_stop_req_stop_desc   
    def get_max_len_mp_stop_req_stop_desc(self,obj):
        return obj.max_len_mp_stop_req_stop_desc                                                                                                                      

class MP0107_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0107_list_Serializer


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = "select t1.id "
        query += "     , t2.mp_id "
        query += "     , t2.mp_name         /* 멘토링 프로그램명 */ "
        query += "     , t2.status          /* 프로그램상태*/ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.status and std_grp_code = 'mp0001') as status_nm "
        query += "     , t3.status as wirte_status          /* 작성상태*/ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.status and std_grp_code = 'mp0070') as wirte_status_nm "
        query += "     , SUBSTRING(t3.wrt_dt,1,10) as wrt_dt   /* 작성일 */ "
        query += "     , SUBSTRING(t3.sbm_dt,1,10) as sbm_dt    /* 제출일 */ "
        query += "     , t2.mgr_id    /*승인자id*/ "
        query += "     , t2.mgr_nm    /*승인자명*/ "
        query += "     , SUBSTRING(t3.mgr_dt,1,10) as mgr_dt    /* 관리자 승인일시 */    /*승인일시*/ "
        query += "     , t1.unv_nm          /* 지원자 대학교 명 */ "
        query += "     , t1.dept_nm         /* 지원자 학부/학과 명 */ "
        query += "     , t1.apl_no          /* 지원자(멘토,학생) no */ "
        query += "     , t1.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += "     , t1.apl_id          /* 지원자(멘토,학생) 학번 */ "
        query += "     , t1.mob_no          /* 휴대전화 */ "
        query += "     , (select ifnull(att_val,0) "
        query += "          from service20_mp_sub "
        query += "         where mp_id   = t1.mp_id "
        query += "           and att_id  = 'mp0007' "
        query += "           and att_cdh = 'mp0007' "
        query += "           and att_cdd = '10' ) as base_hr /* 활동 기준시간*/ "
        query += "     , (select ifnull(sum(appr_tm),0) "
        query += "          from service20_mp_att "
        query += "         where mp_id   = t1.mp_id "
        query += "           and apl_no  = t1.apl_no "
        query += "           and att_sts in ('d', 'e') ) as act_hr /* 관리자 승인, 활동비 지급 */  "
        query += "     , t3.stop_desc /* 중단 사유 */ "
        query += "     , t3.stop_resp /* 중단 귀책(ms0005) */   "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.stop_resp and std_grp_code = 'ms0005') as stop_resp_nm "
        query += "     , t3.stop_tp   /* 중단 유형(mp0095) */         "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.stop_tp and std_grp_code = 'mp0095') as stop_tp_nm "       
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0010', 'MS0028', '10') min_len_mp_stop_req_stop_desc /* 중단 사유(STOP_DESC) - 활동중단 사유서(MP_STOP_REQ) */ " 
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0010', 'MS0029', '10') max_len_mp_stop_req_stop_desc /* 중단 사유(STOP_DESC) - 활동중단 사유서(MP_STOP_REQ) */ "
        query += "  from service20_mp_mtr t1 "
        query += "    left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += "    left join service20_mp_stop_req t3 on (t3.mp_id = t1.mp_id and t1.apl_id = t3.apl_id) "
        query += " where t1.apl_id = '"+l_user_id+"' "
        query += "   and t2.yr = '"+l_yr+"' "
        query += "   and t2.apl_term = '"+l_apl_term+"' "
        query += "   and t1.mp_id like Ifnull(Nullif('" + str(l_mp_id) + "', ''), '%%')  "
        query += " order by t2.yr desc "
        query += "     , t2.apl_term desc "
        query += "     , t2.status "

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 보고서 현황 save
@csrf_exempt
def MP0107_update(request,pk):

    mp_id     = request.POST.get('mp_id', "")
    apl_no    = request.POST.get('apl_no', 0)
    apl_id    = request.POST.get('apl_id', "")
    apl_nm    = request.POST.get('apl_nm', "")
    base_hr   = request.POST.get('base_hr', 0)
    act_hr    = request.POST.get('act_hr', 0)
    mgr_id    = request.POST.get('mgr_id', "")
    stop_tp   = request.POST.get('stop_tp', "")
    stop_resp = request.POST.get('stop_resp', "")
    stop_desc = request.POST.get('stop_desc', "")
    upd_id    = request.POST.get('upd_id', "")
    upd_ip    = request.POST.get('upd_ip', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    if pk == 1:
        # /*중단사유서 저장*/
        update_text  = " insert into service20_mp_stop_req     /* 활동중단 사유서 */ "
        update_text += "      ( mp_id     /* 멘토링 프로그램id */ "
        update_text += "      , apl_no    /* 멘토 지원 no */ "
        update_text += "      , stop_seq  /* 미완료 소명 no */ "
        update_text += "      , apl_id    /* 멘토 학번 */ "
        update_text += "      , apl_nm    /* 멘토 이름 */ "
        update_text += "      , base_hr   /* 기준 시간 */ "
        update_text += "      , act_hr    /* 활동 시간 */ "
        update_text += "      , stop_dt   /* 중단일 */ "
        update_text += "      , wrt_dt    /* 작성일 */ "
        update_text += "      , sbm_dt    /* 제출일 */ "
        update_text += "      , appr_id   /* 승인자id */ "
        update_text += "      , appr_nm   /* 승인자명 */ "
        update_text += "      , appr_dt   /* 보호자 승인일시 */ "
        update_text += "      , mgr_id    /* 관리자id */ "
        update_text += "      , mgr_dt    /* 관리자 승인일시 */ "
        update_text += "      , status    /* 상태(mp0070) */ "
        update_text += "      , stop_tp   /* 중단 유형(mp0095) */ "
        update_text += "      , stop_resp /* 중단 귀책(ms0005) */ "
        # update_text += "      , stop_desc /* 중단 사유 */ "
        update_text += "      , ins_id    /* 입력자id */ "
        update_text += "      , ins_ip    /* 입력자ip */ "
        update_text += "      , ins_dt    /* 입력일시 */ "
        update_text += "      , ins_pgm   /* 입력프로그램id */ "
        update_text += "      , upd_id    /* 수정자id */ "
        update_text += "      , upd_ip    /* 수정자ip */ "
        update_text += "      , upd_dt    /* 수정일시 */ "
        update_text += "      , upd_pgm   /* 수정프로그램id */ "
        update_text += " ) "
        update_text += " values "
        update_text += "      ( '" + str(mp_id) + "'      /* 멘토링 프로그램id */ "
        update_text += "      , '" + str(apl_no) + "'     /* 멘토 지원 no */ "
        update_text += "      , 1                         /* 미완료 소명 no */ "
        update_text += "      , '" + str(apl_id) + "'     /* 멘토 학번 */ "
        update_text += "      , '" + str(apl_nm) + "'     /* 멘토 이름 */ "
        update_text += "      , '" + str(base_hr) + "'    /* 기준 시간 */ "
        update_text += "      , '" + str(act_hr) + "'     /* 활동 시간 */ "
        update_text += "      , now()                     /* 중단일 */ "
        update_text += "      , now()                     /* 작성일 */ "
        update_text += "      , null                      /* 제출일 */ "
        update_text += "      , null                      /* 승인자id */ "
        update_text += "      , null                      /* 승인자명 */ "
        update_text += "      , null                      /* 보호자 승인일시 */ "
        update_text += "      , '" + str(mgr_id) + "'     /* 관리자id */ "
        update_text += "      , null                      /* 관리자 승인일시 */ "
        update_text += "      , '10'                      /* 상태(mp0070) */ "
        update_text += "      , '99'                      /* 중단 유형(mp0095) */ "
        update_text += "      , 'M'                       /* 중단 귀책(ms0005) */ "
        # update_text += "      , '" + str(stop_desc) + "'  /* 중단 사유 */ "
        update_text += "      , '" + str(upd_id) + "'     /* 입력자id */ "
        update_text += "      , '" + str(client_ip) + "'  /* 입력자ip */ "
        update_text += "      , now()                     /* 입력일시 */ "
        update_text += "      , '" + str(upd_pgm) + "'    /* 입력프로그램id */ "
        update_text += "      , '" + str(upd_id) + "'     /* 수정자id */ "
        update_text += "      , '" + str(client_ip) + "'  /* 수정자ip */ "
        update_text += "      , now()                     /* 수정일시 */ "
        update_text += "      , '" + str(upd_pgm) + "'    /* 수정프로그램id */ "
        update_text += " ) on duplicate key update "
        update_text += "        stop_dt   =  now()                      /* 중단일 */ "
        update_text += "      , wrt_dt    =  now()                      /* 작성일 */ "
        update_text += "      , status    =  '10'                       /* 상태 */ "
        update_text += "      , stop_resp =  '" + str(stop_resp) + "'   /* 중단 귀책(ms0005) */ "
        update_text += "      , stop_tp   =  '" + str(stop_tp) + "'     /* 중단 유형(mp0095) */ "
        # update_text += "      , stop_desc =  '" + str(stop_desc) + "'   /* 중단 사유 */ "
        update_text += "      , upd_id    =  '" + str(upd_id) + "'      /* 수정자id */ "
        update_text += "      , upd_ip    =  '" + str(client_ip) + "'   /* 수정자ip */ "
        update_text += "      , upd_dt    =  now()                      /* 수정일시 */ "
        update_text += "      , upd_pgm   =  '" + str(upd_pgm) + "'     /* 수정프로그램id */ "  

    elif pk == 2:
        # /*중단사유서 제출*/
        update_text  = " insert into service20_mp_stop_req     /* 활동중단 사유서 */ "
        update_text += "      ( mp_id     /* 멘토링 프로그램id */ "
        update_text += "      , apl_no    /* 멘토 지원 no */ "
        update_text += "      , stop_seq  /* 미완료 소명 no */ "
        update_text += "      , apl_id    /* 멘토 학번 */ "
        update_text += "      , apl_nm    /* 멘토 이름 */ "
        update_text += "      , base_hr   /* 기준 시간 */ "
        update_text += "      , act_hr    /* 활동 시간 */ "
        update_text += "      , stop_dt   /* 중단일 */ "
        update_text += "      , wrt_dt    /* 작성일 */ "
        update_text += "      , sbm_dt    /* 제출일 */ "
        update_text += "      , appr_id   /* 승인자id */ "
        update_text += "      , appr_nm   /* 승인자명 */ "
        update_text += "      , appr_dt   /* 보호자 승인일시 */ "
        update_text += "      , mgr_id    /* 관리자id */ "
        update_text += "      , mgr_dt    /* 관리자 승인일시 */ "
        update_text += "      , status    /* 상태(mp0070) */ "
        update_text += "      , stop_tp   /* 중단 유형(mp0095) */ "
        update_text += "      , stop_resp /* 중단 귀책(ms0005) */ "
        update_text += "      , stop_desc /* 중단 사유 */ "
        update_text += "      , ins_id    /* 입력자id */ "
        update_text += "      , ins_ip    /* 입력자ip */ "
        update_text += "      , ins_dt    /* 입력일시 */ "
        update_text += "      , ins_pgm   /* 입력프로그램id */ "
        update_text += "      , upd_id    /* 수정자id */ "
        update_text += "      , upd_ip    /* 수정자ip */ "
        update_text += "      , upd_dt    /* 수정일시 */ "
        update_text += "      , upd_pgm   /* 수정프로그램id */ "
        update_text += " ) "
        update_text += " values "
        update_text += "      ( '" + str(mp_id) + "'      /* 멘토링 프로그램id */ "
        update_text += "      , '" + str(apl_no) + "'     /* 멘토 지원 no */ "
        update_text += "      , 1                         /* 미완료 소명 no */ "
        update_text += "      , '" + str(apl_id) + "'     /* 멘토 학번 */ "
        update_text += "      , '" + str(apl_nm) + "'     /* 멘토 이름 */ "
        update_text += "      , '" + str(base_hr) + "'    /* 기준 시간 */ "
        update_text += "      , '" + str(act_hr) + "'     /* 활동 시간 */ "
        update_text += "      , now()                     /* 중단일 */ "
        update_text += "      , now()                     /* 작성일 */ "
        update_text += "      , now()                     /* 제출일 */ "
        update_text += "      , null                      /* 승인자id */ "
        update_text += "      , null                      /* 승인자명 */ "
        update_text += "      , null                      /* 보호자 승인일시 */ "
        update_text += "      , '" + str(mgr_id) + "'     /* 관리자id */ "
        update_text += "      , null                      /* 관리자 승인일시 */ "
        update_text += "      , '20'                      /* 상태(mp0070) */ "
        update_text += "      , '99'                      /* 중단 유형(mp0095) */ "
        update_text += "      , 'M'                       /* 중단 귀책(ms0005) */ "
        update_text += "      , '" + str(stop_desc) + "'  /* 중단 사유 */ "
        update_text += "      , '" + str(upd_id) + "'     /* 입력자id */ "
        update_text += "      , '" + str(client_ip) + "'  /* 입력자ip */ "
        update_text += "      , now()                     /* 입력일시 */ "
        update_text += "      , '" + str(upd_pgm) + "'    /* 입력프로그램id */ "
        update_text += "      , '" + str(upd_id) + "'     /* 수정자id */ "
        update_text += "      , '" + str(client_ip) + "'  /* 수정자ip */ "
        update_text += "      , now()                     /* 수정일시 */ "
        update_text += "      , '" + str(upd_pgm) + "'    /* 수정프로그램id */ "
        update_text += " ) on duplicate key update "
        update_text += "        stop_dt   =  now()                      /* 중단일 */ "
        update_text += "      , wrt_dt    =  now()                      /* 작성일 */ "
        update_text += "      , sbm_dt    =  now()                      /* 제출일 */ "
        update_text += "      , status    =  '20'                       /* 상태 */ "
        update_text += "      , stop_resp =  '" + str(stop_resp) + "'   /* 중단 귀책(ms0005) */ "
        update_text += "      , stop_tp   =  '" + str(stop_tp) + "'     /* 중단 유형(mp0095) */ "
        update_text += "      , stop_desc =  '" + str(stop_desc) + "'   /* 중단 사유 */ "
        update_text += "      , upd_id    =  '" + str(upd_id) + "'      /* 수정자id */ "
        update_text += "      , upd_ip    =  '" + str(client_ip) + "'   /* 수정자ip */ "
        update_text += "      , upd_dt    =  now()                      /* 수정일시 */ "
        update_text += "      , upd_pgm   =  '" + str(upd_pgm) + "'     /* 수정프로그램id */ "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
    
    # 따옴표 처리(중단사유서)
    mp_stop_req.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no)).update(stop_desc=str(stop_desc))
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# MP0107 - END
#####################################################################################

#####################################################################################
# MP0108 - START
#####################################################################################

# 미완료 소명서 리스트 ###################################################
class MP0108_list_Serializer(serializers.ModelSerializer):

    mp_id = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    wirte_status = serializers.SerializerMethodField()
    wirte_status_nm = serializers.SerializerMethodField()
    wrt_dt = serializers.SerializerMethodField()
    sbm_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    base_hr = serializers.SerializerMethodField()
    act_hr = serializers.SerializerMethodField()
    uncmp_desc = serializers.SerializerMethodField()    
    uncmp_resp = serializers.SerializerMethodField()
    uncmp_resp_nm = serializers.SerializerMethodField()
    uncmp_tp = serializers.SerializerMethodField()
    uncmp_tp_nm = serializers.SerializerMethodField()
    min_len_mp_ucmp_req_uncmp_desc = serializers.SerializerMethodField()
    max_len_mp_ucmp_req_uncmp_desc = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = '__all__'

    def get_mp_id(self,obj):
        return obj.mp_id
    def get_mp_name(self,obj):
        return obj.mp_name
    def get_status(self,obj):
        return obj.status
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_wirte_status(self,obj):
        return obj.wirte_status
    def get_wirte_status_nm(self,obj):
        return obj.wirte_status_nm
    def get_wrt_dt(self,obj):
        return obj.wrt_dt
    def get_sbm_dt(self,obj):
        return obj.sbm_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_base_hr(self,obj):
        return obj.base_hr
    def get_act_hr(self,obj):
        return obj.act_hr
    def get_uncmp_desc(self,obj):
        return obj.uncmp_desc      
    def get_uncmp_resp(self,obj):
        return obj.uncmp_resp 
    def get_uncmp_resp_nm(self,obj):
        return obj.uncmp_resp_nm 
    def get_uncmp_tp(self,obj):
        return obj.uncmp_tp 
    def get_uncmp_tp_nm(self,obj):
        return obj.uncmp_tp_nm                      
    def get_min_len_mp_ucmp_req_uncmp_desc(self,obj):
        return obj.min_len_mp_ucmp_req_uncmp_desc 
    def get_max_len_mp_ucmp_req_uncmp_desc(self,obj):
        return obj.max_len_mp_ucmp_req_uncmp_desc                                                                                                      

class MP0108_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0108_list_Serializer


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query  = "select t1.id "
        query += "     , t2.mp_id "
        query += "     , t2.mp_name         /* 멘토링 프로그램명 */ "
        query += "     , t2.status          /* 프로그램상태*/ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t2.status and std_grp_code = 'mp0001') as status_nm "
        query += "     , t3.status as wirte_status          /* 작성상태*/ "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.status and std_grp_code = 'mp0070') as wirte_status_nm "
        query += "     , SUBSTRING(t3.wrt_dt,1,10) as wrt_dt   /* 작성일 */ "
        query += "     , SUBSTRING(t3.sbm_dt,1,10) as sbm_dt    /* 제출일 */ "
        query += "     , t2.mgr_id    /*승인자id*/ "
        query += "     , t2.mgr_nm    /*승인자명*/ "
        query += "     , SUBSTRING(t3.mgr_dt,1,10) as mgr_dt    /* 관리자 승인일시 */    /*승인일시*/ "
        query += "     , t1.unv_nm          /* 지원자 대학교 명 */ "
        query += "     , t1.dept_nm         /* 지원자 학부/학과 명 */ "
        query += "     , t1.apl_no          /* 지원자(멘토,학생) no */ "
        query += "     , t1.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += "     , t1.apl_id          /* 지원자(멘토,학생) 학번 */ "
        query += "     , t1.mob_no          /* 휴대전화 */ "
        query += "     , (select ifnull(att_val,0) "
        query += "          from service20_mp_sub "
        query += "         where mp_id   = t1.mp_id "
        query += "           and att_id  = 'mp0007' "
        query += "           and att_cdh = 'mp0007' "
        query += "           and att_cdd = '10' ) as base_hr /* 활동 기준시간*/ "
        query += "     , (select ifnull(sum(appr_tm),0) "
        query += "          from service20_mp_att "
        query += "         where mp_id   = t1.mp_id "
        query += "           and apl_no  = t1.apl_no "
        query += "           and att_sts in ('d', 'e') ) as act_hr /* 관리자 승인, 활동비 지급 */  "
        query += "     , t3.uncmp_desc /* 미완료 소명 사유 */ "
        query += "     , t3.uncmp_resp /* 미완료 귀책(ms0005) */   "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.uncmp_resp and std_grp_code = 'ms0005') as uncmp_resp_nm "
        query += "     , t3.uncmp_tp   /* 미완료 유형(mp0096) */   /* 중단 유형(mp0096) */         "
        query += "     , (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.uncmp_tp and std_grp_code = 'mp0096') as uncmp_tp_nm "       
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0009', 'MS0028', '10') min_len_mp_ucmp_req_uncmp_desc /* 미완료 소명 사유(UNCMP_DESC) - 미완료 소명서(MP_UCMP_REQ) */ "
        query += "     , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0009', 'MS0029', '10') max_len_mp_ucmp_req_uncmp_desc /* 미완료 소명 사유(UNCMP_DESC) - 미완료 소명서(MP_UCMP_REQ) */ "
        query += "  from service20_mp_mtr t1 "
        query += "    inner join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += "    inner join service20_mp_ucmp_req t3 on (t3.mp_id = t1.mp_id and t1.apl_id = t3.apl_id) "
        query += " where t1.apl_id = '"+l_user_id+"' "
        query += "   and t2.yr = '"+l_yr+"' "
        query += "   and t2.apl_term = '"+l_apl_term+"' "
        query += "   and t1.mp_id like Ifnull(Nullif('" + str(l_mp_id) + "', ''), '%%')  "
        query += " order by t2.yr desc "
        query += "     , t2.apl_term desc "
        query += "     , t2.status "

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 보고서 현황 save
@csrf_exempt
def MP0108_update(request,pk):

    uncmp_desc = request.POST.get('uncmp_desc', "")
    mp_id      = request.POST.get('mp_id', "")
    apl_no     = request.POST.get('apl_no', 0)
    upd_id     = request.POST.get('upd_id', "")
    upd_ip     = request.POST.get('upd_ip', "")
    upd_dt     = request.POST.get('upd_dt', "")
    upd_pgm    = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    if pk == 1:
        # /*미완료 소명서 저장*/
        update_text += "update service20_mp_ucmp_req     /* 미완료 소명서 */ "
        update_text += "   set wrt_dt     = now()                     /* 작성일 */ "
        update_text += "     , status     = '10'                      /* 상태(mp0070) */ "
        update_text += "     , uncmp_desc = '" + str(uncmp_desc) + "' /* 미완료 소명 사유 */ "
        update_text += "     , upd_id     = '" + str(upd_id) + "'     /* 수정자id */ "
        update_text += "     , upd_ip     = '" + str(client_ip) + "'  /* 수정자ip */ "
        update_text += "     , upd_dt     = now()                     /* 수정일시 */ "
        update_text += "     , upd_pgm    = '" + str(upd_pgm) + "'    /* 수정프로그램id */ "
        update_text += " where mp_id = '" + str(mp_id) + "' "
        update_text += "   and apl_no = '" + str(apl_no) + "' "

        # 따옴표 처리(미완료 소명서)
        mp_ucmp_req.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no)).update(uncmp_desc=str(uncmp_desc))    
         
    elif pk == 2:
        # /*미완료 소명서 제출*/
        update_text += "update service20_mp_ucmp_req     /* 미완료 소명서 */ "
        update_text += "   set wrt_dt     = now()                     /* 작성일 */ "
        update_text += "     , sbm_dt     = now()                     /* 작성일 */ "
        update_text += "     , status     = '20'                      /* 상태(mp0070) */ "
        update_text += "     , uncmp_desc = '" + str(uncmp_desc) + "' /* 미완료 소명 사유 */ "
        update_text += "     , upd_id     = '" + str(upd_id) + "'     /* 수정자id */ "
        update_text += "     , upd_ip     = '" + str(client_ip) + "'  /* 수정자ip */ "
        update_text += "     , upd_dt     = now()                     /* 수정일시 */ "
        update_text += "     , upd_pgm    = '" + str(upd_pgm) + "'    /* 수정프로그램id */ "
        update_text += " where mp_id = '" + str(mp_id) + "' "
        update_text += "   and apl_no = '" + str(apl_no) + "' "
 
        # 따옴표 처리(미완료 소명서)
        mp_ucmp_req.objects.filter(mp_id=str(mp_id),apl_no=str(apl_no)).update(uncmp_desc=str(uncmp_desc))

    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# MP0108 - END
#####################################################################################

#####################################################################################
# TE0201 - START
#####################################################################################

# 멘티의 프로그램 신청현황 리스트 ###################################################
class TE0201_list_Serializer(serializers.ModelSerializer):
    mp_hm = serializers.SerializerMethodField()
    mp_plc = serializers.SerializerMethodField()
    mp_addr = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_no = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = ('yr', 'apl_term', 'mp_id', 'mp_name', 'mp_hm', 'mp_plc', 'mp_addr', 'status', 'id', 'mnte_id', 'mnte_no')

    def get_mp_hm(self,obj):
        return obj.mp_hm
    def get_mp_plc(self,obj):
        return obj.mp_plc
    def get_mp_addr(self,obj):
        return obj.mp_addr
    def get_id(self,obj):
        return obj.id
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_no(self,obj):
        return obj.mnte_no

class TE0201_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = TE0201_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mnte_id = request.GET.get('mnte_id', "")

        queryset = self.get_queryset()

        # /* 멘티의 프로그램 신청현황 조회 TE0201/list */
        query = " select t1.yr as yr"
        query += "     , case when t1.apl_term = '10' then '1'"
        query += "            when t1.apl_term = '20' then '2'"
        query += "            else '' end as apl_term"
        query += "     , t1.mp_id as mp_id"
        query += "     , t1.mp_name as mp_name"
        query += "     , t2.mp_hm as mp_hm"
        query += "     , t2.mp_plc as mp_plc"
        query += "     , t2.mp_addr as mp_addr"
        query += "     , t2.status as status"
        query += "     , t2.id as id"
        query += "     , t2.mnte_id as mnte_id"
        query += "     , t2.mnte_no as mnte_no"
        query += "  from service20_mpgm t1"
        query += "  left join service20_mp_mte t2 on t1.mp_id = t2.mp_id"
        query += " where t1.yr = '" + l_yr + "'"
        query += "   and t1.apl_term like '" + l_apl_term + "'"
        query += "   and t1.mp_id = '" + l_mp_id + "'"
        query += "   and t2.mnte_id = '" + l_mnte_id + "'"

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘티의 프로그램 신청현황 리스트 ###################################################
class TE0201_detail_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mte
        fields = ('id', 'mp_id', 'mnte_id', 'mnte_nm', 'sch_cd', 'sch_nm', 'h_addr', 'brth_dt', 'sch_yr', 'mob_no', 'tel_no', 'grd_id', 'grd_nm', 'grd_rel', 'grd_rel', 'grd_rel', 'grd_rel', 'grd_rel', 'grd_rel', 'grd_tel', 'prnt_nat_cd', 'prnt_nat_nm', 'tchr_id', 'tchr_nm', 'tchr_tel', 'mnte_id')

class TE0201_detail(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = TE0201_detail_Serializer

    def list(self, request):

        l_mnte_id = request.GET.get('mnte_id', "")

        queryset = self.get_queryset()

        # /* 멘티의 프로그램 신청현황 멘티 상세 조회 TE0201/detail */
        query = " select t1.id as id"
        query += "     , t1.mp_id as mp_id"
        query += "     , t1.mnte_no as mnte_no"
        query += "     , t1.mnte_id as mnte_id"
        query += "     , t1.mnte_nm as mnte_nm"
        query += "     , t1.sch_cd as sch_cd"
        query += "     , t1.sch_nm as sch_nm"
        query += "     , t1.h_addr as h_addr"
        query += "     , t1.brth_dt as brth_dt"
        query += "     , t1.sch_yr as sch_yr"
        query += "     , t1.mob_no as mob_no"
        query += "     , t1.tel_no as tel_no"
        query += "     , t1.grd_id as grd_id"
        query += "     , t1.grd_nm as grd_nm"
        query += "     , case when t1.grd_rel = '11' then '부' "
        query += "            when t1.grd_rel = '12' then '모' "
        query += "            when t1.grd_rel = '21' then '조부' "
        query += "            when t1.grd_rel = '22' then '조모' "
        query += "            when t1.grd_rel = '31' then '삼촌' "
        query += "            when t1.grd_rel = '32' then '고모' "
        query += "            else '' end as grd_rel"
        query += "     , t1.grd_tel as grd_tel"
        query += "     , t1.prnt_nat_cd as prnt_nat_cd"
        query += "     , t1.prnt_nat_nm as prnt_nat_nm"
        query += "     , t1.tchr_id as tchr_id"
        query += "     , t1.tchr_nm as tchr_nm"
        query += "     , t1.tchr_tel as tchr_tel"
        query += "  from service20_mp_mte t1"
        query += " where t1.mnte_id = '" + l_mnte_id + "'"

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
#####################################################################################
# TE0201 - END
#####################################################################################

#####################################################################################
# TE0202 - START
#####################################################################################

# 멘티출석확인 멘티 리스트 ###################################################
class TE0202_list_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mp_mte
        fields = '__all__'

class TE0202_list(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = TE0202_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        # /* 멘티출석확인 멘티 리스트 조회 TE0202/list */
        query = " select t1.id as id "
        query += " , t1.mp_id as mp_id "
        query += "     , t1.mnte_no as mnte_no"
        query += "     , t1.mnte_id as mnte_id"
        query += "     , t1.mnte_nm as mnte_nm"
        query += "     , t1.sch_nm as sch_nm"
        query += "     , t1.sch_yr as sch_yr"
        query += "     , t1.tchr_id as tchr_id"
        query += "     , t1.grd_id as grd_id"
        query += "  from service20_mp_mte t1"
        query += " where t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */"
        query += "   and (t1.tchr_id = '" + l_user_id + "' or t1.grd_id = '" + l_user_id + "')"

        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#####################################################################################
# TE0202 - START
#####################################################################################

# 멘티출석확인 멘티 리스트 ###################################################
class TE0202_list_Serializer(serializers.ModelSerializer):
    apl_no = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_mte
        fields = '__all__'

    def get_apl_no(self,obj):
        return obj.apl_no
    def get_apl_nm(self,obj):
        return obj.apl_nm

class TE0202_list(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = TE0202_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        # /* 멘티출석확인 멘티 리스트 조회 TE0202/list */
        query = " select t1.id as id "
        query += " , t1.mp_id as mp_id "
        query += "     , t1.mnte_no as mnte_no"
        query += "     , t2.apl_no as apl_no"
        query += "     , t2.apl_nm as apl_nm"
        query += "     , t1.mnte_id as mnte_id"
        query += "     , t1.mnte_nm as mnte_nm"
        query += "     , t1.sch_nm as sch_nm"
        query += "     , t1.sch_yr as sch_yr"
        query += "     , t1.tchr_id as tchr_id"
        query += "     , t1.grd_id as grd_id"
        query += "  from service20_mp_mte t1"
        query += "  LEFT JOIN service20_mp_mtr t2 ON (t2.mp_id = t1.mp_id AND t2.apl_no = t1.apl_no)"
        query += " where t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */"
        query += "   and (t1.tchr_id = '" + l_user_id + "' or t1.grd_id = '" + l_user_id + "')"

        print(query)
        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘티출석확인 멘티에 따른 월별 멘토 리스트 ###################################################
class TE0202_detail_Serializer(serializers.ModelSerializer):
    att_ym = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    att_sdt = serializers.SerializerMethodField()
    att_stm = serializers.SerializerMethodField()
    att_etm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    # mnte_id = serializers.SerializerMethodField()
    mp_div_nm = serializers.SerializerMethodField()
    # mnte_nm = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()

    class Meta:
        model = mp_att
        fields = '__all__'

    def get_att_ym(self,obj):
        return obj.att_ym
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_att_sdt(self,obj):
        return obj.att_sdt
    def get_att_stm(self,obj):
        return obj.att_stm
    def get_att_etm(self,obj):
        return obj.att_etm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    # def get_mnte_id(self,obj):
    #     return obj.mnte_id
    def get_mp_div_nm(self,obj):
        return obj.mp_div_nm
    # def get_mnte_nm(self,obj):
    #     return obj.mnte_nm
    def get_apl_id(self,obj):
        return obj.apl_id

class TE0202_detail(generics.ListAPIView):
    queryset = mp_att.objects.all()
    serializer_class = TE0202_detail_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_no = request.GET.get('apl_no', "")
        l_month  = request.GET.get('month', "")
        l_mp_id = request.GET.get('mp_id', "")
        # l_mnte_id = request.GET.get('mnte_id', "")
        l_appr_yn = request.GET.get('appr_yn', "")
        l_mgr_yn = request.GET.get('mgr_yn', "")

        l_month1 = l_month
        l_month2 = l_month

        if not l_month:
            l_month1 = '01'
            l_month2 = '12'

        queryset = self.get_queryset()

        # /* 멘티출석확인 멘티에 따른 월별 멘토 리스트 조회 TE0202/detail */
        query = " select t1.id as id "
        query += "      , t1.mp_id as mp_id "
        query += "      , t1.apl_no as apl_no "
        query += "      , t2.apl_id as apl_id "
        query += "      , t1.att_no as att_no   /* 출석순서(seq) */"
        query += "     , t1.mp_div as mp_div"
        query += "     , c1.std_detl_code_nm   as mp_div_nm "
        query += "     , substring(t1.att_sdt, 1, 10) as att_ym"
        query += "     , t2.apl_nm as apl_nm"
        query += "     , substring(t1.att_sdt, 1, 10) as att_sdt   /* 출석일시(교육시작일시) */ "
        query += "     , substring(t1.att_sdt, 12, 5) as att_stm   /* 출석일시(교육시작일시) */"
        query += "     , substring(t1.att_edt, 12, 5) as att_etm   /* 출석일시(교육시작일시) */"
        query += "     , substring(t1.elap_tm, 1, 5)  as elap_tm   /* 경과시간 */"
        query += "     , t1.appr_tm as appr_tm  /* 인정시간 */"
        query += "     , t1.exp_amt as exp_amt  /* 지급 활동비 */"
        query += "     , t1.appr_id as appr_id  /* 승인자id */"
        query += "     , t1.appr_nm as appr_nm  /* 승인자명 */"
        query += "     , substring(t1.appr_dt, 1, 16)  as appr_dt  /* 보호자 승인일시 */"
        query += "     , t1.mgr_id as mgr_id    /* 관리자id */"
        query += "     , case when t1.mgr_dt is not null then t4.mgr_nm else null end as mgr_nm   /* 관리자명 */"
        query += "     , substring(t1.mgr_dt, 1, 16)  as mgr_dt   /* 관리자 승인일시 */"
        # query += "     , t3.mnte_id as mnte_id"
        query += "     , t1.att_sts as att_sts"
        # query += "     , t3.mnte_nm as mnte_nm"
        query += "  from service20_mp_att t1"
        query += "  left join service20_mp_mtr t2 on (t2.mp_id = t1.mp_id"
        query += "                                   and t2.apl_no = t1.apl_no)"
        # query += "  left join service20_mp_mte t3 on (t3.mp_id = t1.mp_id"
        # query += "                                   and t3.apl_no = t1.apl_no)"
        query += "  left join service20_mpgm   t4 on (t4.mp_id    = t1.mp_id)"
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'mp0059' and c1.std_detl_code = t1.mp_div) "
        query += " where t1.mp_id    = '" + l_mp_id + "'    /* 멘토링 프로그램id */"
        query += " and t1.apl_no = '" + l_apl_no + "'"
        query += " and t1.appr_div   like ifnull(nullif('" + l_appr_yn + "', ''), '%%')   "
        query += " and t1.mgr_div   like ifnull(nullif('" + l_mgr_yn + "', ''), '%%')   "
        # query += "   and (('" + l_appr_yn + "' = 'Y' and t1.appr_dt is not null) or ('" + l_appr_yn + "' <> 'Y' and t1.appr_dt is null))"
        # query += "   and (('" + l_mgr_yn + "' = 'Y' and t1.mgr_dt is not null) or ('" + l_mgr_yn + "' <> 'Y' and t1.mgr_dt is null))"
        query += " and (t1.att_sdt >= CONCAT('" + l_yr + "-" + l_month1 + "', '-01') AND t1.att_sdt < ADDDATE(LAST_DAY(CONCAT('" + l_yr + "-" + l_month2 + "', '-01')), 1))"
        # query += "   and t3.mnte_id = '" + l_mnte_id + "'"
        query += " order by t1.att_no"

        print(query)
        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘티출석확인 멘토 출석 승인 ###################################################
@csrf_exempt
def TE0202_Approval(request):
    l_mp_id = request.POST.get('upd_mp_id', "")
    # l_mnte_id = request.POST.get('upd_mnte_id', "")
    l_apl_no = request.POST.get('upd_apl_no', "")
    l_att_no = request.POST.get('upd_att_no', "")
    l_status = request.POST.get('upd_status', "")
    l_appr_yn = request.POST.get('upd_appr_yn', "")
    l_mgr_yn = request.POST.get('upd_mgr_yn', "")
    l_user_id = request.POST.get('upd_user_id', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    
    client_ip = request.META['REMOTE_ADDR']

    query = " update service20_mp_att t1"
    query += "   set t1.appr_dt = case when '" + l_status + "' = 'B' then now() else null end"
    query += "     , t1.appr_id = case when '" + l_status + "' = 'B' then '" + l_user_id + "' else null end"
    query += "     , t1.appr_nm = case when '" + l_status + "' = 'B' then (select tchr_nm from service20_teacher where tchr_id = '" + l_user_id + "')"
    query += "                         else null end"
    query += "     , t1.appr_div = 'Y'"
    query += "     , t1.att_sts = 'C'"
    # query += "     , t1.mgr_dt = case when '" + l_status + "' = 'C' then 'C' else null end"
    # query += "     , t1.mgr_id = case when '" + l_status + "' = 'C' then '" + l_user_id + "' else null end"
    # query += "     , t1.att_sts = case when '" + l_status + "' = 'B' then 'C' "
    # query += "                         when '" + l_status + "' = 'C' then 'D'"
    # query += "                         else 'B' end"
    # query += "                         else 'B' end"
    query += "     , upd_id = '" + upd_id + "'"
    query += "     , upd_ip = '" + client_ip + "'"
    query += "     , upd_dt = now()"
    query += "     , upd_pgm = '" + upd_pgm + "'"
    query += " where t1.mp_id = '" + l_mp_id + "'"
    # query += " and t1.appr_div   like ifnull(nullif('" + l_appr_yn + "', ''), '%%')   "
    # query += " and t1.mgr_div   like ifnull(nullif('" + l_mgr_yn + "', ''), '%%')   "
    # query += "    and (('" + l_appr_yn + "' = 'Y' and t1.appr_dt is not null) or ('" + l_appr_yn + "' <> 'Y' and t1.appr_dt is null))"
    # query += "   and (('" + l_mgr_yn + "' = 'Y' and t1.mgr_dt is not null) or ('" + l_mgr_yn + "' <> 'Y' and t1.mgr_dt is null))"
    query += "   and t1.apl_no = '" + l_apl_no + "'"
    query += "   and t1.att_no = '" + l_att_no + "'"
    
    print(query)
    cursor = connection.cursor()
    query_result = cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# TE0202 - END
#####################################################################################

#####################################################################################
# TE0203 - START
#####################################################################################

# 멘토의 프로그램 만족도조사 리스트 ###################################################
class TE0203_list_v1_Serializer(serializers.ModelSerializer):
    # testField = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    unv_nm = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    mp_id = serializers.SerializerMethodField()
    mnte_no = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    sch_cd = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    surv_seq = serializers.SerializerMethodField()
    spc_no = serializers.SerializerMethodField()
    surv_tp = serializers.SerializerMethodField()
    surv_ttl = serializers.SerializerMethodField()
    h_status = serializers.SerializerMethodField()
    p_status = serializers.SerializerMethodField()

    class Meta:
        model = cm_surv_h
        fields = ('pgm_id','surv_seq','ansr_id','apl_no','apl_id','apl_nm','unv_nm','cllg_nm','dept_nm','mp_id','mnte_no','mnte_id','mnte_nm','sch_cd','sch_nm','sch_yr','surv_id','ansr_div','avg_ans_t1','surv_dt','h_status','spc_no','surv_tp','surv_ttl','p_status')

    def get_apl_no(self,obj):
        return obj.apl_no
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_unv_nm(self,obj):
        return obj.unv_nm
    def get_cllg_nm(self,obj):
        return obj.cllg_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_mp_id(self,obj):
        return obj.mp_id
    def get_mnte_no(self,obj):
        return obj.mnte_no
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_sch_cd(self,obj):
        return obj.sch_cd
    def get_sch_nm(self,obj):
        return obj.sch_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_surv_seq(self,obj):
        return obj.surv_seq
    def get_spc_no(self,obj):
        return obj.spc_no
    def get_surv_tp(self,obj):
        return obj.surv_tp
    def get_surv_ttl(self,obj):
        return obj.surv_ttl
    def get_h_status(self,obj):
        return obj.h_status
    def get_p_status(self,obj):
        return obj.p_status

class TE0203_list_v1(generics.ListAPIView):
    queryset = cm_surv_h.objects.all()
    serializer_class = TE0203_list_v1_Serializer
    
    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_term_div = request.GET.get('trn_term', "")
        l_status = request.GET.get('status', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        # /* 만족도 조사 */
        # /* 유저가 멘토일 때 만족도 조사 대상 리스트 */
        # /* 만족도 조사는 멘토, 멘티, 멘티의 교사, 관리자에 따라 select가 다 다릅니다. 따라서 각 케이스에 따른 url을 따로 만들어야합니다. */
        # /* TE0203/list/v1 */
        query = " select t1.id as id /* id */"
        query += "     , t1.pgm_id as pgm_id   /* 만족도 조사 대상(멘토스쿨, 프로그램, 학습외) */"
        query += "     , t1.surv_seq as surv_seq /* 만족도 seq */"
        query += "     , t1.ansr_id as ansr_id  /* 응답자 id */"
        query += "     , t3.apl_no as apl_no         /* 지원 no */"
        query += "     , t3.apl_id as apl_id         /* 지원자(멘토,학생) 학번 */"
        query += "     , t3.apl_nm as apl_nm         /* 지원자(멘토,학생) 명 */"
        query += "     , t3.unv_nm as unv_nm         /* 지원자 대학교 명 */"
        query += "     , t3.cllg_nm as cllg_nm        /* 지원자 대학 명 */"
        query += "     , t3.dept_nm as dept_nm        /* 지원자 학부/학과 명 */"
        query += "     , t4.mp_id as mp_id      /* 멘토링 프로그램id */"
        query += "     , t4.mnte_no as mnte_no    /* 지원 no */"
        query += "     , t4.mnte_id as mnte_id    /* 멘티id */"
        query += "     , t4.mnte_nm as mnte_nm    /* 멘티 명 */"
        query += "     , t4.sch_cd as sch_cd     /* 학교 */"
        query += "     , t4.sch_nm as sch_nm     /* 학교명 */"
        query += "     , t4.sch_yr as sch_yr     /* 학년 */"
        query += "     , t1.surv_id as surv_id   /* 문항세트 id */"
        query += "     , t1.ansr_div as ansr_div  /* 응답자 구분(cm0001) */"
        query += "     , t1.avg_ans_t1 as avg_ans_t1 /* 오지선다형 평균 */"
        query += "     , date_format(t1.surv_dt, '%%Y-%%m-%%d %%H:%%i:%%s') as surv_dt   /* 만족도 조사일 */"
        query += "     , t1.status as h_status    /* 상태(cm0006) */"
        query += "     , t2.spc_no as spc_no    /* 학습외 프로그램no */"
        query += "     , t2.surv_tp as surv_tp   /* 대상 내 유형 */"
        query += "     , t2.surv_ttl as surv_ttl  /* 만족도 조사 제목 */"
        query += "     , t2.status as p_status    /* 상태(cm0008) */"
        query += "  from service20_cm_surv_h t1"
        query += "  left join service20_cm_surv_p t2 on (t2.pgm_id    = t1.pgm_id     "
        query += "                                   and t2.surv_seq  = t1.surv_seq)"
        query += "  left join service20_mp_mtr    t3 on (t3.mp_id     = t1.pgm_id)"
        # query += "                                   and t3.apl_id    = t1.ansr_id )"
        query += "  left join service20_mp_mte    t4 on (t4.mp_id     = t3.mp_id"
        query += "                                   and t4.apl_no    = t3.apl_no )"
        query += "  where t3.mp_id = '" + l_mp_id + "'"
        query += "    and ( (t3.apl_id = '" + l_apl_id + "' and t1.ansr_id = t3.apl_id) "
        query += "        or (t4.tchr_id = '" + l_apl_id + "' and t1.ansr_id = t4.tchr_id) "
        query += "        or (t4.grd_id = '" + l_apl_id + "' and t1.ansr_id = t4.grd_id)"
        query += "        or (t4.mnte_id = '" + l_apl_id + "' and t1.ansr_id = t4.mnte_id) ) "
        # query += "    and t1.ansr_div = '""
        # query += " where t3.yr = '" + l_yr + "'"
        # query += "  and t3.term_div = '" + l_term_div + "'"
        # query += "  and t3.status like Ifnull(Nullif('" + str(l_status) + "', ''), '%%')  "
        # query += "  where t3.mp_id = '" + l_mp_id + "'"
        # query += "    and ( t3.apl_id = '" + l_apl_id + "'"
        # query += "        or t4.tchr_id = '" + l_apl_id + "'"
        # query += "        or t4.grd_id = '" + l_apl_id + "'"
        # query += "        or t4.mnte_id = '" + l_apl_id + "' ) "

        queryset = cm_surv_h.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 유저에 따른 만족도 조사 질문 리스트 ###################################################
class TE0203_detail_Serializer(serializers.ModelSerializer):
    # testField = serializers.SerializerMethodField()
    sort_seq = serializers.SerializerMethodField()
    ques_desc = serializers.SerializerMethodField()
    ques_div = serializers.SerializerMethodField()
    
    class Meta:
        model = cm_surv_a
        fields = ('pgm_id','surv_seq','ansr_id','ques_no','ansr_div','sort_seq','ques_desc','ans_t1','ans_t2','ans_t3','ques_dt','ques_div')

    def get_sort_seq(self,obj):
        return obj.sort_seq
    def get_ques_desc(self,obj):
        return obj.ques_desc
    def get_ques_div(self,obj):
        return obj.ques_div 

class TE0203_detail(generics.ListAPIView):
    queryset = cm_surv_a.objects.all()
    serializer_class = TE0203_detail_Serializer


    def list(self, request):
        l_ansr_id = request.GET.get('ansr_id', "")
        l_pgm_id = request.GET.get('pgm_id', "")
        l_surv_seq = request.GET.get('surv_seq', "")
        l_ansr_div = request.GET.get('ansr_div', "")

        queryset = self.get_queryset()

        # /* 만족도 조사 */
        # /* 유저에 따른 만족도 조사 질문 */
        # /* TE0203/list/detail/ */
        # query = " select t3.id as id /* id */"
        # query += "     , t3.pgm_id as pgm_id  /* 만족도 조사 대상(멘토스쿨, 프로그램, 학습외) */"
        # query += "     , t3.surv_seq as surv_seq/* 만족도 seq */"
        # query += "     , t3.ansr_id as ansr_id /* 응답자 id */"
        # query += "     , t3.ques_no as ques_no /* 만족도 조사 항목 id */"
        # query += "     , t3.ansr_div as ansr_div /* 응답자 구분(cm0001) */"
        # query += "     , t1.sort_seq as sort_seq /* 정렬 순서 */"
        # query += "     , t2.ques_desc as ques_desc/* 질문지    */"
        # query += "     , t3.ans_t1 as ans_t1  /* 선다형 답 */"
        # query += "     , t3.ans_t2 as ans_t2  /* 수필형 답 */"
        # query += "     , t3.ans_t3 as ans_t3  /* 선택 답 */"
        # query += "     , t3.ques_dt as ques_dt /* 설문조사일자 */"
        # query += "     , t2.ques_div as ques_div"
        # query += "  from service20_cm_surv_a t3     /* 만족도 조사 답변 상세 */"
        # query += "  left join service20_cm_surv t2   on (t2.ques_no = t3.ques_no)    /* 만족도 조사 문항 */"
        # query += "  left join service20_cm_surv_q t1 on (t1.ques_no = t3.ques_no"
        # query += "                                   and t1.surv_id = t3.surv_id)    /* 만족도 조사 출제 문항 */"
        # query += " where 1=1"
        # query += "   and t3.ansr_id = '" + l_ansr_id + "'"
        # query += "   and t3.pgm_id = '" + l_pgm_id + "'"
        # query += "   and t3.surv_seq = '" + l_surv_seq + "'"

        query = " select t1.id as id"
        query += "     , t1.pgm_id as pgm_id    /* 만족도 조사 대상(멘토스쿨, 프로그램, 학습외) */"
        query += "     , t1.surv_seq as surv_seq  /* 만족도 seq */"
        query += "     , t1.ansr_id as ansr_id   /* 응답자 id */"
        query += "     , t2.ques_no as ques_no   /* 만족도 조사 항목 id */"
        query += "     , t1.ansr_div as ansr_div  /* 응답자 구분(cm0001) */"
        query += "     , t2.sort_seq as sort_seq  /* 정렬 순서 */"
        query += "     , t3.ques_desc as ques_desc /* 질문지    */"
        query += "     , t4.ans_t1 as ans_t1   /* 선다형 답 */"
        query += "     , t4.ans_t2 as ans_t2   /* 수필형 답 */"
        query += "     , t4.ans_t3 as ans_t3   /* 선택 답 */"
        query += "     , t4.ques_dt ques_dt  /* 설문조사일자 */"
        query += "     , t3.ques_div as ques_div"
        query += "  from service20_cm_surv_h t1     /* 만족도 조사 답변 헤드 */"
        query += "  left join service20_cm_surv_q t2 on (t2.surv_id = t1.surv_id)"
        query += "  left join service20_cm_surv   t3 on (t3.ques_no = t2.ques_no)    /* 만족도 조사 문항 */"
        query += "  left join service20_cm_surv_a t4 on (t1.surv_seq = t4.surv_seq and t2.ques_no = t4.ques_no)"
        query += " where 1=1"
        query += "   and t1.pgm_id    = '" + l_pgm_id + "'     /* 만족도 조사 대상(멘토스쿨, 프로그램, 학습외) */"
        query += "   and t1.surv_seq  = '" + l_surv_seq + "'  /* 만족도 seq */"
        query += "   and t1.ansr_id   = '" + l_ansr_id + "'    /* 응답자 id */"
        # query += "   and t1.ansr_div  = '" + l_ansr_div + "'    /* 응답자 구분 */"
        query += "  order by t2.sort_seq /* 정렬 순서 */"


        queryset = cm_surv_a.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 프로그램 만족도 조사 Insert
@csrf_exempt
def TE0203_Insert(request):
    mp_id = request.POST.get('mp_id', "")
    surv_seq = request.POST.get('surv_seq', "")
    ansr_id = request.POST.get('ansr_id', "")
    ques_no = request.POST.get('ques_no', 0)
    ansr_div = request.POST.get('ansr_div', "")
    surv_id = request.POST.get('surv_id', "")
    avg = request.POST.get('avg', 0)

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    # 저장상태구분 I(제출)/S(임시저장)
    save_status = request.POST.get('save_status', "")

    quesRow = request.POST.get('ques_row', 0)
    row_max = int(quesRow)

    if save_status == "I":
        # 제출
        query = " update service20_cm_surv_h"
        query += " set status = '90'"
        query += "  , surv_dt = now()"
        query += "  , avg_ans_t1 = '" + avg + "'"
        query += "  , upd_id = '" + upd_id + "'"
        query += "  , upd_ip = '" + upd_ip + "'"
        query += "  , upd_dt = now()"
        query += "  , upd_pgm = '" + upd_pgm + "'"
        query += " where pgm_id = '" + mp_id + "'"
        query += "  and surv_seq = '" + surv_seq + "'"
        query += "  and ansr_id = '" + ansr_id + "'"

        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(query)   
    elif save_status == "S":
        # 임시저장
        query = " update service20_cm_surv_h"
        query += " set surv_dt = now()"
        query += "  , avg_ans_t1 = '" + avg + "'"
        query += "  , upd_id = '" + upd_id + "'"
        query += "  , upd_ip = '" + upd_ip + "'"
        query += "  , upd_dt = now()"
        query += "  , upd_pgm = '" + upd_pgm + "'"
        query += " where pgm_id = '" + mp_id + "'"
        query += "  and surv_seq = '" + surv_seq + "'"
        query += "  and ansr_id = '" + ansr_id + "'"

        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(query)   

    # service20_cm_surv_a Insert
    for i in range(0,row_max):
        ques_no = request.POST.get('ques_no'+str(i+1), "0")
        ans_t1 = request.POST.get('ans_t1'+str(i+1), "")
        ans_t2 = request.POST.get('ans_t2'+str(i+1), "")
        ans_t3 = request.POST.get('ans_t3'+str(i+1), "")

        cm_surv_a_flag = cm_surv_a.objects.filter(pgm_id=str(mp_id),surv_seq=str(surv_seq),ansr_id=str(ansr_id),ques_no=str(ques_no)).exists()
        query = ""
        if not cm_surv_a_flag:
            # 미존재
            query += " insert into service20_cm_surv_a ("
            query += "      pgm_id"
            query += "    , surv_seq"
            query += "    , ansr_id"
            query += "    , ques_no"
            query += "    , ansr_div"
            query += "    , ans_t1"
            query += "    , ans_t2"
            query += "    , ans_t3"
            query += "    , ques_dt"
            query += "    , surv_id"
            query += "    , ins_id"
            query += "    , ins_ip"
            query += "    , ins_dt"
            query += "    , ins_pgm"
            query += "    , upd_id"
            query += "    , upd_ip"
            query += "    , upd_dt"
            query += "    , upd_pgm"
            query += ")"
            query += " values ("
            query += "      '" + str(mp_id) + "'"
            query += "    , '" + str(surv_seq) + "'"
            query += "    , '" + str(ansr_id) + "'"
            query += "    , '" + str(ques_no) + "'"
            query += "    , '" + str(ansr_div) + "'"
            query += "    , case when '" + str(ans_t2) + "' = '' and '" + str(ans_t3) + "' = '' then '" + str(ans_t1) +"' else null end "
            query += "    , case when '" + str(ans_t1) + "' = '' and '" + str(ans_t3) + "' = '' then '" + str(ans_t2) +"' else null end "
            query += "    , case when '" + str(ans_t1) + "' = '' and '" + str(ans_t2) + "' = '' then '" + str(ans_t3) +"' else null end "
            query += "    , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 10), '-',''),':',''),' ', '')"
            query += "    , '" + str(surv_id) + "'"
            query += "    , '" + str(ins_id) + "'"
            query += "    , '" + str(ins_ip) + "'"
            query += "    , now()"
            query += "    , '" + str(ins_pgm) + "'"
            query += "    , '" + str(upd_id) + "'"
            query += "    , '" + str(upd_ip) + "'"
            query += "    , now()"
            query += "    , '" + str(upd_pgm) + "'"
            query += " )"

                
        else:
            # 존재
            
            # /*프로그램 만족도 조사_저장*/
            query += " update service20_cm_surv_a t1 "
            query += " set t1.ansr_div = '"+str(ansr_div)+"' "
            query += " , t1.ques_dt = REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 10), '-',''),':',''),' ', '')"
            query += " , t1.surv_id = '"+str(surv_id)+"' "

            query += " , t1.ans_t1 = case when '" + str(ans_t2) + "' = '' and '" + str(ans_t3) + "' = '' then '" + str(ans_t1) +"' else null end "
            query += " , t1.ans_t2 = case when '" + str(ans_t1) + "' = '' and '" + str(ans_t3) + "' = '' then '" + str(ans_t2) +"' else null end "
            query += " , t1.ans_t3 = case when '" + str(ans_t1) + "' = '' and '" + str(ans_t2) + "' = '' then '" + str(ans_t3) +"' else null end "
            

            query += " , t1.upd_ip = '"+str(client_ip)+"' "
            query += " , t1.upd_dt = now() "
            query += " , t1.upd_pgm = '"+str(upd_pgm)+"' "
            query += " where 1=1 "
            query += " and t1.pgm_id    = '"+str(mp_id)+"' "
            query += " and t1.surv_seq = '"+str(surv_seq)+"' "
            query += " and t1.ansr_id = '"+str(ansr_id)+"' "
            query += " and t1.ques_no = '"+str(ques_no)+"' "

            # (따옴표 처리)
            # cm_surv_a.objects.filter(pgm_id=str(mp_id),surv_seq=str(surv_seq),ansr_id=str(ansr_id),ques_no=str(ques_no)).update(ans_t1=str(mtr_revw))


        print("ins_1")
        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(query)  

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# TE0203 - END
#####################################################################################

#####################################################################################
# TE0204 - START
#####################################################################################

#####################################################################################
# TE0204 - START
#####################################################################################

# 프로그램 소감문 작성 리스트 ###################################################
class TE0204_list_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    yr = serializers.SerializerMethodField()
    mnt_term = serializers.SerializerMethodField()
    mp_id = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    mnt_fr_dt = serializers.SerializerMethodField()
    mnt_to_dt = serializers.SerializerMethodField()
    mnt_frto_dt = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    grd_rel = serializers.SerializerMethodField()  
    grd_rel_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    write_dt = serializers.SerializerMethodField()
    min_len_mp_rep_mtr_revw = serializers.SerializerMethodField()
    max_len_mp_rep_mtr_revw = serializers.SerializerMethodField()

    class Meta:
        model = mp_rvw
        fields = '__all__'


    def get_yr(self,obj):
        return obj.yr
    def get_mnt_term(self,obj):        
        return obj.mnt_term
    def get_mp_id(self,obj):        
        return obj.mp_id
    def get_mp_name(self,obj):        
        return obj.mp_name
    def get_mnt_fr_dt(self,obj):        
        return obj.mnt_fr_dt
    def get_mnt_to_dt(self,obj):        
        return obj.mnt_to_dt
    def get_mnt_frto_dt(self,obj):        
        return obj.mnt_frto_dt        
    def get_sch_yr(self,obj):        
        return obj.sch_yr
    def get_grd_rel(self,obj):        
        return obj.grd_rel
    def get_grd_rel_nm(self,obj):        
        return obj.grd_rel_nm
    def get_status_nm(self,obj):        
        return obj.status_nm  
    def get_write_dt(self,obj):        
        return obj.write_dt          
    def get_min_len_mp_rep_mtr_revw(self,obj):        
        return obj.min_len_mp_rep_mtr_revw  
    def get_max_len_mp_rep_mtr_revw(self,obj):        
        return obj.max_len_mp_rep_mtr_revw  

class TE0204_list(generics.ListAPIView):
    queryset = mp_rvw.objects.all()
    serializer_class = TE0204_list_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query  = " select t1.id "
        query += " , t2.yr       /* 연도 */ "
        query += " , t2.mnt_term /* 활동시기 */ "
        query += " , t1.mp_id    /* 멘토링 프로그램id */ "
        query += " , t2.mp_name  /* 멘토링 프로그램 명 */ "
        query += " , substring(t2.mnt_fr_dt, 1, 10) as mnt_fr_dt     /* 활동기간-시작 */ "
        query += " , substring(t2.mnt_to_dt, 1, 10) as mnt_to_dt     /* 활동기간-시작 */ "
        query += " , concat(substring(t2.mnt_fr_dt, 1, 10),' ~ ',substring(t2.mnt_to_dt, 1, 10)) as mnt_frto_dt    /* 활동기간*/ "
        query += " , t1.mnte_id  /* 담당멘티id */ "
        query += " , t1.mnte_nm  /* 담당멘티명 */ "
        query += " , t1.sch_nm   /* 학교명 */ "
        query += " , t3.sch_yr   /* 학년 */ "
        query += " , t1.grd_id   /* 주 보호자 id */"
        query += " , t1.grd_nm   /* 보호자명 */ "
        query += " , t3.grd_rel  /* 보호자 관계(mp0047) */ "
        query += " , c2.std_detl_code_nm AS grd_rel_nm "
        query += " , t1.tchr_id  /* 담당교사id */ "
        query += " , t1.tchr_nm  /* 담당교사명 */ "
        query += " , t1.apl_id   /* 멘토 학번 */ "
        query += " , t1.apl_nm   /* 멘토 이름 */ "
        query += " , t1.status   /* 상태(mp0070) */ "
        query += " , c1.std_detl_code_nm AS status_nm "
        query += " , t1.rvw_dt   /* 작성일 */ "
        query += " , t1.cmp_dt   /* 제출일 */ "
        query += " , case when t1.cmp_dt is not null then substring(t1.cmp_dt, 1, 10) else substring(t1.rvw_dt, 1, 10) end as write_dt"
        query += " , t1.mtr_revw /* 소감문 */ "
        query += " , t1.rvwr_id  /* 소감문 작성자id */ "
        query += " , t1.rvwr_nm  /* 소감문 작성자명 */ "
        query += " , t1.rep_no   /* 보고서 no */ "
        query += " , t1.rep_div  /* 소감문 구분 */ "
        query += " , t1.rvwr_div /* 소감문 작성자 구분 */ "
        query += " , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0008', 'MS0028', '10') min_len_mp_rep_mtr_revw /* 소감문(MTR_REVW) - 프로그램 보고서(MP_REP) */ "   
        query += " , fn_mp_sub_att_val_select_01('" + str(l_mp_id) + "', 'CL0008', 'MS0029', '10') max_len_mp_rep_mtr_revw /* 소감문(MTR_REVW) - 프로그램 보고서(MP_REP) */ "
        query += " from service20_mp_rvw t1 "
        query += " left join service20_mpgm t2 on (t2.mp_id   = t1.mp_id) "
        query += " left join service20_mp_mte t3 on (t3.mp_id   = t1.mp_id "
        query += " and t3.mnte_id  = t1.mnte_id)  "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'mp0070'  /* 상태(mp0070) */ "
        query += " and c1.std_detl_code = t1.status) "
        query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'mp0047'  /* 보호자 관계(mp0047) */"
        query += " and c2.std_detl_code = t3.grd_rel) "
        query += " where 1=1 "
        query += " and t2.yr = '"+l_yr+"'"
        query += " and t2.mnt_term = '"+l_apl_term+"'"
        query += " and t1.mp_id     = '"+l_mp_id+"'"
        query += " and t1.rvwr_id   = '"+l_user_id+"'"


        queryset = mp_rvw.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)          

# 보고서 현황 save
@csrf_exempt
def TE0204_update(request,pk):

    mtr_revw  = request.POST.get('mtr_revw', "")
    upd_id    = request.POST.get('upd_id', "")
    upd_ip    = request.POST.get('upd_ip', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")

    yr        = request.POST.get('yr', "")
    mnt_term  = request.POST.get('mnt_term', "")
    mp_id     = request.POST.get('mp_id', "")
    rvwr_id   = request.POST.get('rvwr_id', "")
    client_ip = request.META['REMOTE_ADDR']


    update_text = ""
    if pk == 1:
        # /*프로그램 최종소감문_저장*/
        update_text  = " update service20_mp_rvw t1 "
        update_text += " set t1.rvw_dt = now() /* 작성일 */ "
        update_text += " , t1.status = '10' /* 상태(20제출, 10작성중) */ "
        update_text += " , t1.upd_id = '"+str(upd_id)+"' "
        update_text += " , t1.upd_ip = '"+str(client_ip)+"' "
        update_text += " , t1.upd_dt = now() "
        update_text += " , t1.upd_pgm = '"+str(upd_pgm)+"' "
        update_text += " where 1=1 "
        update_text += " and t1.mp_id    = '"+str(mp_id)+"' "
        update_text += " and t1.rvwr_id = '"+str(rvwr_id)+"' "

        # 소감문 (따옴표 처리)
        mp_rvw.objects.filter(mp_id=str(mp_id),rvwr_id=str(rvwr_id)).update(mtr_revw=str(mtr_revw))

    elif pk == 2:
        # /*프로그램 최종소감문_제출*/
        update_text  = " update service20_mp_rvw t1 "
        update_text += " set t1.rvw_dt = now() /* 작성일 */ "
        update_text += " , t1.cmp_dt = now() /* 제출일 */ "
        update_text += " , t1.status = '20' /* 상태(20제출, 10작성중) */ "
        update_text += " , t1.upd_id = '"+str(upd_id)+"' "
        update_text += " , t1.upd_ip = '"+str(client_ip)+"' "
        update_text += " , t1.upd_dt = now() "
        update_text += " , t1.upd_pgm = '"+str(upd_pgm)+"' "
        update_text += " where 1=1 "
        update_text += " and t1.mp_id    = '"+str(mp_id)+"' "
        update_text += " and t1.rvwr_id = '"+str(rvwr_id)+"' "

        # 소감문 (따옴표 처리)
        mp_rvw.objects.filter(mp_id=str(mp_id),rvwr_id=str(rvwr_id)).update(mtr_revw=str(mtr_revw))

    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
 
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#####################################################################################
# TE0204 - END
#####################################################################################

#####################################################################################
# TT0105 - START
#####################################################################################

# 계획서 승인 리스트 ###################################################
class TT0105_list_Serializer(serializers.ModelSerializer):
    mntr_id = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    unv_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_plnh
        fields = '__all__'

    def get_mntr_id(self,obj):
        return obj.mntr_id  
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_unv_nm(self,obj):
        return obj.unv_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_sch_nm(self,obj):
        return obj.sch_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_mgr_nm(self,obj):
        return obj.mgr_nm

class TT0105_list(generics.ListAPIView):
    queryset = mp_plnh.objects.all()
    serializer_class = TT0105_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        l_status = request.GET.get('status', "")

        queryset = self.get_queryset()

        # /* 계획서승인 리스트 조회 TT0105/list */
        query = " select t4.id as id"
        query += "     , t4.mp_id as mp_id"
        query += "     , t4.apl_no as apl_no"
        query += "     , t1.mntr_id as mntr_id"
        query += "     , t1.apl_id as apl_id"
        query += "     , t1.apl_nm as apl_nm"
        query += "     , t1.unv_nm as unv_nm"
        query += "     , t1.dept_nm as dept_nm"
        query += "     , t2.mnte_nm as mnte_nm"
        query += "     , t2.sch_nm as sch_nm"
        query += "     , t2.sch_yr as sch_yr"
        query += "     , substring(t4.pln_dt, 1, 16) as pln_dt"
        query += "     , t4.appr_nm as appr_nm"
        query += "     , substring(t4.appr_dt, 1, 16) as appr_dt"
        query += "     , t3.mgr_nm as mgr_nm"
        query += "     , substring(t4.mgr_dt, 1, 16) as mgr_dt"
        query += "     , t4.status as status"
        query += "  from service20_mp_mtr t1"
        query += "  left join service20_mp_mte t2 on (t2.mp_id = t1.mp_id"
        query += "                                  and t2.apl_no = t1.apl_no)"
        query += "  left join service20_mpgm t3 on t3.mp_id = t1.mp_id"
        query += "  left join service20_mp_plnh t4 on (t4.mp_id = t1.mp_id"
        query += "                                  and t4.apl_no = t1.apl_no)"
        query += " where t1.mp_id = '" + l_mp_id + "'"
        query += "   and ( t1.apl_id = '" + l_user_id + "'"
        query += "    or t2.tchr_id = '" + l_user_id + "'"
        query += "    or t2.grd_id = '" + l_user_id + "'"
        query += "    or t4.mgr_id = '" + l_user_id + "' )"
        query += "   and t4.status like Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        query += " order by t1.mntr_id"
        query += "     , t1.apl_nm"
        query += "     , t1.unv_nm"
        query += "     , t1.dept_nm"
        query += "     , t2.mnte_nm"
        query += "     , t2.sch_nm"
        query += "     , t2.sch_yr"

        queryset = mp_plnh.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 계획서 승인 ###################################################
@csrf_exempt
def TT0105_Approval(request):
    l_mp_id = request.POST.get('upd_mp_id', "")
    l_apl_no = request.POST.get('upd_apl_no', "")
    l_user_id = request.POST.get('upd_user_id', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    
    client_ip = request.META['REMOTE_ADDR']

    query = " update service20_mp_plnh"
    query += "   set appr_id = '" + l_user_id + "'"
    query += "     , appr_nm = (select tchr_nm from service20_teacher where tchr_id = '" + l_user_id + "')"
    query += "     , appr_dt = now()"
    query += "     , status = '30'"
    query += "     , upd_id = '" + upd_id + "'"
    query += "     , upd_ip = '" + client_ip + "'"
    query += "     , upd_dt = now()"
    query += "     , upd_pgm = '" + upd_pgm + "'"
    query += " where mp_id = '" + l_mp_id + "'"
    query += "   and apl_no = '" + l_apl_no + "'"

    cursor = connection.cursor()
    query_result = cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 계획서 승인 ###################################################
@csrf_exempt
def TT0105_Back(request):
    l_mp_id = request.POST.get('upd_mp_id', "")
    l_apl_no = request.POST.get('upd_apl_no', "")
    l_user_id = request.POST.get('upd_user_id', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    
    client_ip = request.META['REMOTE_ADDR']

    query = " update service20_mp_plnh"
    query += "   set appr_id = '" + l_user_id + "'"
    query += "     , appr_nm = (select tchr_nm from service20_teacher where tchr_id = '" + l_user_id + "')"
    query += "     , appr_dt = now()"
    query += "     , status = '11' /* 11:교사반려, 12:관리자반려 */"
    query += "     , upd_id = '" + upd_id + "'"
    query += "     , upd_ip = '" + client_ip + "'"
    query += "     , upd_dt = now()"
    query += "     , upd_pgm = '" + upd_pgm + "'"
    query += " where mp_id = '" + l_mp_id + "'"
    query += "   and apl_no = '" + l_apl_no + "'"

    cursor = connection.cursor()
    query_result = cursor.execute(query)

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# TT0105 - END
#####################################################################################

#####################################################################################
# TT0107M - START
#####################################################################################

# 보고서 관리 리스트 ###################################################
class TT0107M_list_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    yr = serializers.SerializerMethodField()
    apl_term = serializers.SerializerMethodField()
    unv_nm = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    rep_div_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    req_dt = serializers.SerializerMethodField()
    appr_dt = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    

    class Meta:
        model = mp_rep
        fields = ('id','mp_id','yr','apl_term','unv_nm','cllg_nm','dept_nm','apl_id','apl_nm','rep_div','rep_div_nm','status','status_nm','rep_ttl','apl_no','rep_no','rep_div','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','rep_ym')

    def get_yr(self,obj):
        return obj.yr
    def get_apl_term(self,obj):        
        return obj.apl_term
    def get_unv_nm(self,obj):        
        return obj.unv_nm
    def get_cllg_nm(self,obj):        
        return obj.cllg_nm
    def get_dept_nm(self,obj):        
        return obj.dept_nm
    def get_apl_id(self,obj):        
        return obj.apl_id
    def get_apl_nm(self,obj):        
        return obj.apl_nm
    def get_rep_div_nm(self,obj):        
        return obj.rep_div_nm
    def get_status_nm(self,obj):        
        return obj.status_nm
    def get_req_dt(self,obj):        
        return obj.req_dt
    def get_appr_dt(self,obj):        
        return obj.appr_dt
    def get_mgr_dt(self,obj):        
        return obj.mgr_dt


class TT0107M_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = TT0107M_list_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        l_rep_div = request.GET.get('rep_div', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        # query = " select distinct t1.id "
        # query += " , t1.mp_id     /* 멘토링 프로그램id */ "
        # query += " , t3.yr"
        # query += " , t3.apl_term"
        # query += " , t2.unv_nm          /* 지원자 대학교 명 */ "
        # query += " , t2.cllg_nm         /* 지원자 대학 명 */ "
        # query += " , t2.dept_nm         /* 지원자 학부/학과 명 */ "
        # query += " , t2.apl_id          /* 지원자(멘토,학생) 학번 */ "
        # query += " , t2.apl_nm          /* 지원자(멘토,학생) 명 */ "
        # query += " , t1.rep_div         /* 보고서 구분(mp0062) */ "
        # query += " , c2.std_detl_code_nm   as rep_div_nm "
        # query += " , t1.status          /* 상태(mp0070) */ "
        # query += " , c1.std_detl_code_nm   as status_nm "
        # query += " , t1.rep_ttl   /* 보고서 제목 : 내용 */ "
        # query += " , t1.apl_no    /* 멘토 지원 no */ "
        # query += " , t1.rep_no    /* 보고서 no */ "
        # query += " , t1.rep_div   /* 보고서 구분(mp0062) */ "
        # query += " , t1.mtr_obj   /* 학습목표 */ "
        # query += " , t1.rep_dt    /* 보고서작성일 */ "
        # query += " , substring(t1.req_dt,  1, 10) req_dt    /* 승인요청일 */ "
        # query += " , t1.mtr_desc  /* 학습내용 */ "
        # query += " , t1.coatching /* 학습외 지도(상담) */ "
        # query += " , t1.spcl_note /* 특이사항 */ "
        # query += " , t1.mtr_revw  /* 소감문 */ "
        # query += " , t1.appr_id   /* 승인자id */ "
        # query += " , t1.appr_nm   /* 승인자명 */ "
        # query += " , substring(t1.appr_dt, 1, 10) appr_dt   /* 보호자 승인일시 */ "
        # query += " , t1.mgr_id    /* 관리자id */ "
        # query += " , substring(t1.mgr_dt,  1, 10) mgr_dt   /* 관리자 승인일시 */ "
        # query += " , t1.rep_ym     "
        # query += " from service20_mp_rep t1     /* 프로그램 보고서 */ "
        # query += " left join service20_mp_mtr t2 on (t2.mp_id   = t1.mp_id "
        # query += " and t2.apl_no = t1.apl_no)       /* 지원 멘토 */ "
        # query += " left join service20_mpgm t3 on (t3.mp_id   = t1.mp_id)  /*지원 멘토*/  "
        # query += "  left join service20_mp_mte t4 on (t4.mp_id     = t2.mp_id"
        # query += "                                   and t4.apl_no = t2.apl_no )    "        
        # query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  /* 상태(mp0070) */ "
        # query += " and c1.std_detl_code = t1.status) "
        # query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  /* 보고서 구분(mp0062) */ "
        # query += " and c2.std_detl_code = t1.rep_div) "
        # query += " where 1=1 "
        # query += " and t3.yr        = '"+l_yr+"'"
        # query += " and t3.apl_term  = '"+l_apl_term+"'"
        # query += " and t1.status    >= 20"
        # query += " and t1.status like Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        # query += " and t1.rep_div   = '"+l_rep_div+"'"
        # query += " and t1.mp_id     = '"+l_mp_id+"'"
        # query += " and ( t4.tchr_id = '"+l_user_id+"'"
        # query += "    or t4.mnte_id = '"+l_user_id+"')"

        query = f"""
                SELECT DISTINCT 
                    t1.id  
                    , t1.mp_id     /* 멘토링 프로그램id */
                    , t1.status    /* 멘토 상태 */
                    , c3.std_detl_code_nm   AS mrt_sts_nm   /* 멘토 상태 */
                    , t4.yr
                    , t4.apl_term 
                    , t1.unv_nm          /* 지원자 대 학교 명 */  
                    , t1.cllg_nm         /* 지원자 대학 명 */  
                    , t1.dept_nm         /* 지원자 학부/학과 명 */  
                    , t1.apl_id          /* 지원자(멘토,학생) 학번 */  
                    , t1.apl_nm          /* 지원자(멘토,학생) 명 */  
                    , t3.rep_div         /* 보고서 구분(mp0062) */  
                    , c2.std_detl_code_nm   AS rep_div_nm  
                    , t3.status          /* 상태(mp0070) */  
                    , CASE WHEN t3.status IS NULL THEN '미작성' ELSE c1.std_detl_code_nm END status_nm  /* 미작성 추가 */
                    , fn_mp_mte_select_01(t1.mp_id, t1.apl_no) mnte_nm /* 매칭 멘티 */
                    , c1.std_detl_code_nm   AS status_nm1
                    , t3.rep_ttl   /* 보고서 제목 : 내용 */  
                    , t3.apl_no    /* 멘토 지원 no */  
                    , t3.rep_no    /* 보고서 no */  
                    , t3.rep_div   /* 보고서 구분(mp0062) */  
                    , t3.mtr_obj   /* 학습목표 */  
                    , t3.rep_dt    /* 보고서작성일 */  
                    , SUBSTRING(t3.req_dt,  1, 10) req_dt    /* 승인요청일 */  
                    , t3.mtr_desc  /* 학습내용 */  
                    , t3.coatching /* 학습외 지도(상담) */  
                    , t3.spcl_note /* 특이사항 */  
                    , t3.mtr_revw  /* 소감문 */  
                    , t3.appr_id   /* 승인자id */  
                    , t3.appr_nm   /* 승인자명 */  
                    , SUBSTRING(t3.appr_dt, 1, 10) appr_dt   /* 보호자 승인일시 */  
                    , CASE WHEN t3.status IS NULL THEN '' WHEN appr_dt IS NULL THEN '승인' ELSE SUBSTRING(t3.appr_dt, 1, 10) END appr_div /* 미작성 시 '', 미승인 시 [승인], 승인 시 승인일시 */
                    , t3.mgr_id    /* 관리자id */  
                    , SUBSTRING(t3.mgr_dt,  1, 10) mgr_dt   /* 관리자 승인일시 */  
                    , t3.rep_ym
                FROM service20_mp_mtr t1
                INNER JOIN (SELECT DISTINCT s1.mp_id, s1.apl_no, s1.sch_nm, s1.tchr_nm
                            FROM service20_mp_mte s1
                            WHERE s1.mp_id     = '{l_mp_id}'
                                AND (s1.tchr_id  = '{l_user_id}'
                                OR s1.mnte_id  = '{l_user_id}')) t2 ON (t2.mp_id  = t1.mp_id
                                                                    AND t2.apl_no = t1.apl_no)
                LEFT JOIN service20_mp_rep t3 ON (t3.mp_id   = t1.mp_id
                                                AND t3.apl_no  = t1.apl_no
                                                /*AND t3.rep_ym  = '201904'*/
                                                /*AND t3.rep_div = 'M'*/)
                INNER JOIN service20_mpgm t4 ON (t4.mp_id   = t1.mp_id)  /*지원 멘토*/
                LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0070'  /* 상태(mp0070) */
                                                AND c1.std_detl_code = t3.status)
                LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code  = 'MP0062'  /* 보고서 구분(mp0062) */  
                                                AND c2.std_detl_code = t3.rep_div)
                LEFT JOIN service20_com_cdd c3 ON (c3.std_grp_code  = 'MP0053'  /* ** 멘토상태 (MP0053) */  
                                                AND c3.std_detl_code = t1.status)
                WHERE 1=1
                AND t4.yr        = '{l_yr}' 
                AND t4.apl_term  = '{l_apl_term}'
                AND t4.mp_id     = '{l_mp_id}'
                AND t3.rep_div   = '{l_rep_div}'
                and t3.status like Ifnull(Nullif('{l_status}', ''), '%%')  
        """
        print(query)
        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)            

# 보고서 현황 save
@csrf_exempt
def TT0107M_update(request,pk):

    mp_id     = request.POST.get('mp_id', "")
    apl_no    = request.POST.get('apl_no', 0)
    rep_no    = request.POST.get('rep_no', 0)
    upd_id    = request.POST.get('upd_id', "")
    upd_ip    = request.POST.get('upd_ip', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")
    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    if pk == 1:
        # /*보고서관리_반려*/
        update_text  = " update service20_mp_rep "
        update_text += " set status    = '11'                 /*status - 반려*/ "
        update_text += " , rep_dt      = null                 /*보고서작성일*/ "
        update_text += " , req_dt      = null                 /*승인요청일*/ "
        update_text += " , upd_id      = '"+str(upd_id)+"'    /*수정자id*/ "
        update_text += " , upd_ip      = '"+str(client_ip)+"' /*수정자ip*/ "
        update_text += " , upd_dt      = now()                /*수정일시*/ "
        update_text += " , upd_pgm     = '"+str(upd_pgm)+"'   /*수정프로그램id*/ "
        update_text += " where mp_id   = '"+mp_id+"' "
        update_text += " and apl_no    = '"+str(apl_no)+"' "
        update_text += " and rep_no    = '"+str(rep_no)+"' "

    elif pk == 2:
        # /*보고서관리_승인*/
        update_text  = " update service20_mp_rep "
        update_text += " set status    = '30'                 /*status - 보호자승인(관리자승인대기)*/ "
        update_text += " , appr_dt     = now()                /*승인일*/ "
        update_text += " , upd_id      = '"+str(upd_id)+"'    /*수정자id*/ "
        update_text += " , upd_ip      = '"+str(client_ip)+"' /*수정자ip*/ "
        update_text += " , upd_dt      = now()                /*수정일시*/ "
        update_text += " , upd_pgm     = '"+str(upd_pgm)+"'   /*수정프로그램id*/ "
        update_text += " where mp_id   = '" +mp_id+"' "
        update_text += " and apl_no    = '"+str(apl_no)+"' "
        update_text += " and rep_no    = '"+str(rep_no)+"' "

    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
 
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#####################################################################################
# TT0107M - END
#####################################################################################

#####################################################################################
# MnteLrnO - START
#####################################################################################

# 멘티의 학습외 신청현황 리스트 ###################################################
class MnteLrnO_list_Serializer(serializers.ModelSerializer):

    mp_name = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    apl_fr_dt = serializers.SerializerMethodField()
    apl_to_dt = serializers.SerializerMethodField()
    mnt_fr_dt = serializers.SerializerMethodField()
    mnt_to_dt = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    apply_yn = serializers.SerializerMethodField()
    apply_status = serializers.SerializerMethodField()
    apply_status_nm = serializers.SerializerMethodField()
    cncl_dt = serializers.SerializerMethodField()
    cncl_rsn = serializers.SerializerMethodField()
    appr_appr = serializers.SerializerMethodField()
    mgr_appr = serializers.SerializerMethodField()
    pick_yn = serializers.SerializerMethodField()
    surv_status = serializers.SerializerMethodField()
    surv_status_nm = serializers.SerializerMethodField()
    att_div = serializers.SerializerMethodField()
    att_div_nm = serializers.SerializerMethodField()

    class Meta:
        model = mp_spc
        fields = '__all__'

    def get_mp_name(self,obj):
        return obj.mp_name       
    def get_apl_id(self,obj):
        return obj.apl_id 
    def get_apl_nm(self,obj):
        return obj.apl_nm 
    def get_apl_fr_dt(self,obj):
        return obj.apl_fr_dt 
    def get_apl_to_dt(self,obj):
        return obj.apl_to_dt 
    def get_mnt_fr_dt(self,obj):
        return obj.mnt_fr_dt 
    def get_mnt_to_dt(self,obj):
        return obj.mnt_to_dt 
    def get_status_nm(self,obj):
        return obj.status_nm 
    def get_apply_yn(self,obj):
        return obj.apply_yn    
    def get_apply_status(self,obj):
        return obj.apply_status       
    def get_apply_status_nm(self,obj):
        return obj.apply_status_nm                  
    def get_cncl_dt(self,obj):
        return obj.cncl_dt 
    def get_cncl_rsn(self,obj):
        return obj.cncl_rsn 
    def get_appr_appr(self,obj):
        return obj.appr_appr     
    def get_mgr_appr(self,obj):
        return obj.mgr_appr    
    def get_pick_yn(self,obj):
        return obj.pick_yn    
    def get_surv_status(self,obj):
        return obj.surv_status 
    def get_surv_status_nm(self,obj):
        return obj.surv_status_nm 
    def get_att_div(self,obj):
        return obj.att_div 
    def get_att_div_nm(self,obj):
        return obj.att_div_nm                                                                                                             

class MnteLrnO_list(generics.ListAPIView):
    queryset = mp_spc.objects.all()
    serializer_class = MnteLrnO_list_Serializer

    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_spc_div = request.GET.get('spc_div', "")
        l_status = request.GET.get('status', "")

        queryset = self.get_queryset()

        query  = "select t1.id "
        query += ", t1.mp_id         /* 멘토링 프로그램id */ "
        query += ", t2.mp_name "
        query += ", t1.spc_no "
        query += ", t1.spc_div       /* 교육구분(mp0064) */ "
        query += ", t1.spc_name      /* 학습외 프로그램 명 */ "
        query += ", t4.apl_id "
        query += ", (select apl_nm from service20_vw_nanum_stdt where apl_id = t4.apl_id) as apl_nm "
        query += ", substring(t1.apl_fr_dt,1,10) as apl_fr_dt    /* 모집기간-시작 */ "
        query += ", substring(t1.apl_to_dt,1,10) as apl_to_dt      /* 모집기간-종료 */ "
        query += ", substring(t1.mnt_fr_dt,1,10) as mnt_fr_dt     /* 활동기간-시작 */ "
        query += ", substring(t1.mnt_to_dt,1,10) as mnt_to_dt     /* 활동기간-종료 */ "
        query += ", (select std_detl_code_nm from service20_com_cdd where std_detl_code = t1.status and std_grp_code = 'mp0084') as status_nm  "
        query += ", case when t1.status = '20' then 'Y' else 'N' end as apply_yn /* 신청*/ "
        query += ", t3.status as apply_status /* 학습외신청상태*/ "
        query += ", (select std_detl_code_nm from service20_com_cdd where std_detl_code = t3.status and std_grp_code = 'mp0085') as apply_status_nm "
        query += ", t3.cncl_dt    /* 지원취소일 */ "
        query += ", t3.cncl_rsn   /* 서류전형취소사유 */     "
        query += ", case when t3.appr_dt is null then '미승인' else '승인' end as appr_appr    /* 보호자승인*/      "
        query += ", case when t3.mgr_dt is null then '미승인' else '승인' end as mgr_appr    /* 관리자승인*/ "
        query += ", case when t3.status = '40' then 'o' when t3.status = '49' then 'x' end as pick_yn /*선발*/ "
        query += ", t5.status as surv_status /*만족도*/ "
        query += ", (select std_detl_code_nm from service20_com_cdd where std_detl_code = t5.status and std_grp_code = 'cm0006') as surv_status_nm "
        query += ", t6.att_div /*출석*/ "
        query += ", (select std_detl_code_nm from service20_com_cdd where std_detl_code = t6.att_div and std_grp_code = 'mp0063') as att_div_nm "
        query += "from service20_mp_spc t1     /* 학습외 프로그램 */ "
        query += "inner join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        query += "inner join service20_mp_spc_mte t3 on (t3.mp_id = t1.mp_id  "
        query += "  and t3.spc_no = t1.spc_no) "
        query += "inner join service20_mp_spc_mtr t4 on (t4.mp_id = t1.mp_id  "
        query += "  and t4.apl_no = t3.apl_no "
        query += "  and t4.spc_no = t3.spc_no) "
        query += "left join service20_cm_surv_h t5 on (t4.mp_id = t1.mp_id  "
        query += " and t5.ansr_id = t3.mnte_id) "
        query += "left join service20_mp_att_mte t6 on (t4.mp_id = t1.mp_id  "
        query += "  and t6.apl_no = t3.apl_no) "
        query += "where 1=1 "
        query += "and t3.mnte_id = '" + l_user_id + "' "
        query += "and t1.yr = '" + l_yr + "' "
        query += "and t1.apl_term = '" + l_apl_term + "' "
        query += "and t1.spc_div like Ifnull(Nullif('" + str(l_spc_div) + "', ''), '%%') "
        query += "and t1.status like Ifnull(Nullif('" + str(l_status) + "', ''), '%%') "
        query += "order by t2.yr DESC, t2.apl_term desc, t1.spc_div, t1.status "

        queryset = mp_spc.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학습외 신청 save
@csrf_exempt
def MnteLrnO_apply(request):

    l_mp_id      = request.POST.get('mp_id', "")
    l_spc_no     = request.POST.get('spc_no', "")
    l_user_id     = request.POST.get('user_id', "")
    l_upd_ip     = request.POST.get('upd_ip', "")
    l_upd_pgm    = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    update_text += "update service20_mp_spc_mte "
    update_text += "   set apl_dt     = now()  /* 신청일 */ "
    update_text += "     , status     = '10'  /* 상태(mp0085) 10:지원 */ "
    update_text += "     , cncl_dt    = null   /* 지원취소일 */ "
    update_text += "     , cncl_rsn   = '00'   /* 서류전형취소사유 */   "    
    update_text += "     , upd_id     = '" + l_user_id + "'  /* 수정자id */ "
    update_text += "     , upd_ip     = '" + l_upd_ip + "'  /* 수정자ip */ "
    update_text += "     , upd_dt     = now()  /* 수정일시 */ "
    update_text += "     , upd_pgm    = '" + l_upd_pgm + "' /* 수정프로그램id */ "
    update_text += " where mp_id   = '" + l_mp_id + "' "
    update_text += "   and spc_no  = '" + l_spc_no + "' "
    update_text += "   and mnte_id = '" + l_user_id + "' "

    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})        

# 학습외 신청취소 save
@csrf_exempt
def MnteLrnO_applyCncl(request):

    l_cncl_rsn   = request.POST.get('cncl_rsn', "")
    l_mp_id      = request.POST.get('mp_id', "")
    l_spc_no     = request.POST.get('spc_no', "")
    l_user_id    = request.POST.get('user_id', "")
    l_upd_ip     = request.POST.get('upd_ip', "")
    l_upd_pgm    = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    update_text += "update service20_mp_spc_mte "
    update_text += "   set status     = '19'  /* 상태(mp0085) 19:지원취소 */ "
    update_text += "     , cncl_dt    = now()   /* 지원취소일 */ "
    update_text += "     , cncl_rsn   = '" + l_cncl_rsn + "'   /* 서류전형취소사유 */   "
    update_text += "     , upd_id     = '" + l_user_id + "'  /* 수정자id */ "
    update_text += "     , upd_ip     = '" + l_upd_ip + "'  /* 수정자ip */ "
    update_text += "     , upd_dt     = now()  /* 수정일시 */ "
    update_text += "     , upd_pgm    = '" + l_upd_pgm + "' /* 수정프로그램id */ "
    update_text += " where mp_id   = '" + l_mp_id + "' "
    update_text += "   and spc_no  = '" + l_spc_no + "' "
    update_text += "   and mnte_id = '" + l_user_id + "' "

    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
#####################################################################################
# MnteLrnO - END
#####################################################################################


@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    
    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id=ms_ida).exists()
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(mp_id=ms_ida)
        rows3 = msch.objects.filter(ms_id=ms_ida)[0]


        for val in rows2:
            key1 = val.att_id

        context = {'message': message,
                        'applyYn' : applyYn,
                        'apl_nm' : rows.apl_nm,
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
                        'grad_div_cd' : rows.grad_div_cd,
                        'grad_div_nm' : rows.grad_div_nm,
                        'cllg_cd' : rows.cllg_cd,
                        'cllg_nm' : rows.cllg_nm,
                        'dept_cd' : rows.dept_cd,
                        'dept_nm' : rows.dept_nm,
                        'mjr_cd' : rows.mjr_cd,
                        'mjr_nm' : rows.mjr_nm,
                        'brth_dt' : rows.brth_dt,
                        'gen_cd' : rows.gen_cd,
                        'gen_nm' : rows.gen_nm,
                        'yr' : rows.yr,
                        'sch_yr' : rows.sch_yr,
                        'term_div' : rows.term_div,
                        'term_nm' : rows.term_nm,
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
                        'tel_no' : rows.tel_no,
                        'tel_no_g' : rows.tel_no_g,
                        'h_addr' : rows.h_addr,
                        'post_no' : rows.post_no,
                        'email_addr' : rows.email_addr,
                        'bank_acct' : rows.bank_acct,
                        'bank_cd' : rows.bank_cd,
                        'bank_nm' : rows.bank_nm,
                        'bank_dpsr' : rows.bank_dpsr,
                        'pr_yr' : rows.pr_yr,
                        'pr_sch_yr' : rows.pr_sch_yr,
                        'pr_term_div' : rows.pr_term_div,
                        'score01' : rows.score01,
                        'score02' : rows.score02,
                        'score03' : rows.score03,
                        'score04' : rows.score04,
                        'score05' : rows.score05,
                        'ms_id' : rows3.ms_id,
                        'ms_name' : rows3.ms_name,
                        }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#멘토링 질문 List######################################################################
@csrf_exempt
def post_mt_quest(request):
    l_ms_id = request.GET.get('ms_id', None)
    r_mp_sub = mp_sub.objects.filter(mp_id=l_ms_id)
    r_mp_sub = r_mp_sub.filter(use_yn='Y')

    response_json = OrderedDict()

    res = []
    for val in r_mp_sub:
        key1 = val.att_id
        key2 = val.att_cdd
        r_com_cdd = com_cdd.objects.filter(std_grp_code=key1,std_detl_code=key2)

    
    context = {'message': 'Ok'}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
####################################################################################



def stdApplyStdView(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'stdApply/submit.html', context)


def Service20_01_View(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'service20/Service20_01.html', context)    


###############################################################      
# 학습외 프로그램 (콤보) Start
###############################################################
class com_combo_spcProgram_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'


class com_combo_spcProgram(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_spcProgram_Serializer

    def list(self, request):
        # yr = request.GET.get('yr', "")
        # apl_term = request.GET.get('apl_term', "")

        queryset = self.get_queryset()
        
        query  = "select '0' id "
        query += "     , '' std_grp_code "
        query += "     , '' std_detl_code "
        query += "     , '전체' std_detl_code_nm "
        query += "union   "
        query += "select t1.id "
        query += "     , t1.std_grp_code "
        query += "     , t1.std_detl_code "
        query += "     , t1.std_detl_code_nm "
        query += "  from service20_com_cdd t1 "
        query += " where t1.std_grp_code = 'mp0064'   "

        print(query)

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)  

###############################################################      
# 학습외 프로그램 (콤보) End
###############################################################

###############################################################      
# 학습외 상태 (콤보) Start
###############################################################
class com_combo_spc_status_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_spc_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_spc_status_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id,std_detl_code,std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001' "
        query += " union  "
        query += " select '','xx','모집완료'  "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 
###############################################################      
# 학습외 상태 (콤보) End
###############################################################


# 프로그램 찾기 (introduce테이블 프로그램)
class com_combo_programIntroduce_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mpgm_introduce
        fields = '__all__'

class com_combo_programIntroduce(generics.ListAPIView):
    queryset = mpgm_introduce.objects.all()
    serializer_class = com_combo_programIntroduce_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query  = "select '0' id"
        query += "     , '' mp_id "
        query += "     , '-------전체-------' subject "
        query += "union "
        query += "select id "
        query += "     , mp_id "
        query += "     , subject "
        query += "  from service20_mpgm_introduce "
        query += " order by subject   "


        queryset = mpgm_introduce.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 회원구분 콤보(멘티, 학부모, 교사만)
class com_combo_member_gubun_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class com_combo_member_gubun(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_member_gubun_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'선택'std_detl_code_nm "
        query += " union  "
        query += " select id, std_detl_code, std_detl_code_nm "
        query += "  from service20_com_cdd "
        query += " where std_grp_code = 'CM0001' "
        query += "   and std_detl_code in ('E', 'G', 'T') "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 멘티와의 관계 콤보
class com_combo_member_rel_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class com_combo_member_rel(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_member_rel_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'선택'std_detl_code_nm "
        query += " union  "
        query += " select id, std_detl_code, std_detl_code_nm "
        query += "  from service20_com_cdd "
        query += " where std_grp_code = 'MP0047' "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 멘티의 학교 리스트 콤보
class com_combo_member_mnte_sch_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class com_combo_member_mnte_sch(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_member_mnte_sch_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query = " select '0' as id, '' as std_detl_code, '선택' as std_detl_code_nm "
        query += " union  "
        query += " select t1.id, t1.std_detl_code, t1.std_detl_code_nm "
        query += "   from (select '0' as id, tchr_id as std_detl_code, sch_nm as std_detl_code_nm "
        query += "           from service20_teacher "
        query += "           group by tchr_id, sch_nm "
        query += "           order by sch_nm) t1 "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 학교 구분 콤보
class com_combo_sch_grd_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class com_combo_sch_grd(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_sch_grd_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'선택'std_detl_code_nm "
        query += " union  "
        query += " select id, std_detl_code, std_detl_code_nm "
        query += "  from service20_com_cdd "
        query += " where std_grp_code = 'MP0006' "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 만족도조사 상태 콤보
class com_combo_surv_status_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class com_combo_surv_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_surv_status_Serializer

    def list(self, request):
               
        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id, std_detl_code, std_detl_code_nm "
        query += "  from service20_com_cdd "
        query += " where std_grp_code = 'CM0006' "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

class mpmgListSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','img_src','testField','apl_fr_dt','apl_to_dt','mp_intro')

    def get_testField(self, obj):
        return 'test'     


class mpmgListView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpmgListSerializer

    def list(self, request):
        queryset = self.get_queryset()

        query = "select * from service20_mpgm where status = '20' and now() between apl_fr_dt and apl_to_dt and use_div = 'Y' order by apl_to_dt desc,apl_fr_dt desc"


        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class main_list_mento_count_Serializer(serializers.ModelSerializer):

    cnt = serializers.SerializerMethodField()
    class Meta:
        model = mentor
        fields = ('mntr_id','cnt')

    def get_cnt(self, obj):
        return obj.cnt     


class main_list_mento_count(generics.ListAPIView):
    queryset = mentor.objects.all()
    serializer_class = main_list_mento_count_Serializer

    def list(self, request):
        queryset = self.get_queryset()

        v_count = mentor.objects.count()
        

        context = {'count': v_count,
                    }
    
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

        # query = "select count(*) as cnt from service20_mentor"
        # queryset = mentor.objects.raw(query)

        # serializer_class = self.get_serializer_class()
        # serializer = serializer_class(queryset, many=True)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # return Response(serializer.data)        

# 회원가입 중복체크
class member_overlap_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = '__all__'

class member_overlap(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = member_overlap_Serializer

    def list(self, request):
        member_id = request.GET.get('member_id', "")
        member_nm = request.GET.get('member_nm', "")
        member_birth = request.GET.get('member_birth', "")
        member_gubun = request.GET.get('member_gubun', "")
        message = "Ok" 

        # 멘티
        if member_gubun == "E":
            mnte_flag = mentee.objects.filter(mnte_nm=member_nm, brth_dt=member_birth).exists()

            if not mnte_flag:
                message = "true"
            else:
                message = "false"
        # 교사
        elif member_gubun == "T":
            teacher_flag = teacher.objects.filter(tchr_id=member_id).exists()

            if not teacher_flag:
                message = "true"
            else:
                message = "false"
        # 학부모
        elif member_gubun == "G":
            guardian_flag = guardian.objects.filter(grdn_nm=member_nm, brth_dt=member_birth).exists()

            if not guardian_flag:
                message = "true"
            else:
                message = "false"

        context = {'message': message,} 
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 회원가입 학부모 검색
class member_popup_guard_Serializer(serializers.ModelSerializer):

    class Meta:
        model = guardian
        fields = '__all__'

class member_popup_guard(generics.ListAPIView):
    queryset = guardian.objects.all()
    serializer_class = member_popup_guard_Serializer

    def list(self, request):
        grdn_nm = request.GET.get('grdn_nm', "")
        brth_dt = request.GET.get('brth_dt', "")

        queryset = self.get_queryset()

        query = f"""
                SELECT grdn_id AS grdn_id
                    , grdn_nm AS grdn_nm
                    , brth_dt AS brth_dt
                    , replace(mob_no, '-', '') AS mob_no
                    , replace(tel_no, '-', '') AS tel_no
                    , h_addr AS h_addr
                FROM service20_guardian
                WHERE grdn_nm = '{grdn_nm}'
                AND brth_dt = '{brth_dt}';
        """

        print(query)
        queryset = guardian.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 회원가입 insert
@csrf_exempt
def member_insert(request):
    cursor = connection.cursor()

    member_gubun = request.POST.get('member_gubun', "")
    member_id = request.POST.get('member_id', "")
    member_nm = request.POST.get('member_nm', " ")
    member_birth = request.POST.get('member_birth', "")
    member_nm_e = request.POST.get('member_nm_e', "")
    member_pwd = request.POST.get('member_pwd', "")
    member_gen = request.POST.get('member_gen', "")
    member_mob = request.POST.get('member_mob', "")
    member_tel = request.POST.get("member_tel","")
    member_email = request.POST.get('member_email', "")   
    member_post = request.POST.get("member_post","")                         
    member_addr = request.POST.get('member_addr', "")
    member_city = request.POST.get('member_city', "")
    member_gu = request.POST.get('member_gu', "")
    member_grd_nm = request.POST.get('member_grd_nm', "")
    member_grd_tel = request.POST.get('member_grd_tel', "")                      
    member_rel = request.POST.get('member_rel', "")
    member_sch_grd = request.POST.get('member_sch_grd', "")
    member_sch = request.POST.get('member_sch', "")
    member_sch_nm = request.POST.get('member_sch_nm', "")
    member_sch_yr = request.POST.get('member_sch_yr', "")
    member_post_sch = request.POST.get('member_sch_post', "")
    member_addr_sch = request.POST.get('member_sch_addr', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    client_ip = request.META['REMOTE_ADDR']

    login_id = ""

    print("member_gubun===" + member_gubun)
    # 멘티
    if member_gubun == "E":
        # 멘티ID 부여
        mentee_id_query = f"""select CONCAT('T',substr(DATE_FORMAT(now(), '%Y'),3,2),(select ifnull(lpad(max(right(mnte_id,4)) + 1,4,0),'0001')   from service20_mentee where substr(mnte_id,2,2)  = substr(DATE_FORMAT(now(), '%Y'),3,2))) as id from dual"""
        print(mentee_id_query)
        cursor.execute(mentee_id_query)
        results_01 = namedtuplefetchall(cursor) 
        mentee_id= results_01[0].id

        teacher_row = teacher.objects.filter(tchr_id=member_sch)[0]
        tchr_nm = teacher_row.tchr_nm
        tchr_mob_no = teacher_row.mob_no
        # tchr_city = teacher_row.area_city
        # tchr_gu = teacher_row.area_gu
        tchr_s_addr = teacher_row.s_addr
        tchr_email = teacher_row.email_addr

        # 성별 치환 (1:M, 2:F)
        if member_gen == "1":
            member_gen = "M"
        else:
            member_gen = "F"

        l_insert_query = f"""
                            insert
                            into   service20_mentee
                                (
                                        mnte_id,
                                        mnte_nm,
                                        mnte_nm_e,
                                        brth_dt,
                                        sch_grd,
                                        sch_cd,
                                        sch_nm,
                                        gen,
                                        yr,
                                        term_div,
                                        sch_yr,
                                        mob_no,
                                        pwd,
                                        grd_id,
                                        tchr_id,
                                        tchr_nm,
                                        tchr_tel,
                                        prnt_nat_cd,
                                        prnt_nat_nm,
                                        area_city,
                                        area_gu,
                                        h_addr,
                                        s_addr,
                                        email_addr,
                                        mp_id,
                                        apl_no,
                                        mp_dt,
                                        cnt_mp_a,
                                        cnt_mp_p,
                                        cnt_mp_c,
                                        cnt_mp_g,
                                        ins_id,
                                        ins_ip,
                                        ins_dt,
                                        ins_pgm,
                                        upd_id,
                                        upd_ip,
                                        upd_dt,
                                        upd_pgm
                                )
                                values
                                (
                                        '{mentee_id}',
                                        '{member_nm}',
                                        '{member_nm_e}',
                                        '{member_birth}',
                                        '{member_sch_grd}',
                                        ' ',
                                        '{member_sch_nm}',
                                        '{member_gen}',
                                        '',
                                        '',
                                        '{member_sch_yr}',
                                        '{member_mob}',
                                        '{member_pwd}',
                                        ' ',
                                        '{member_sch}',
                                        '{tchr_nm}',
                                        '{tchr_mob_no}',
                                        ' ',
                                        ' ',
                                        '{member_city}',
                                        '{member_gu}',
                                        '{member_addr}',
                                        '{tchr_s_addr}',
                                        '{tchr_email}',
                                        ' ',
                                        0,
                                        ' ',
                                        '0',
                                        '0',
                                        '0',
                                        '0',
                                        '{mentee_id}',
                                        '{client_ip}',
                                        now(),
                                        '{ins_pgm}',
                                        '{mentee_id}',
                                        '{client_ip}',
                                        now(),
                                        '{ins_pgm}'
                                )
        """
        print(l_insert_query)
        cursor.execute(l_insert_query)

        login_id = mentee_id
    # 교사
    elif member_gubun == "T":
        l_insert_query = f"""
                            insert
                                into
                                    service20_teacher (
                                    tchr_id
                                    , tchr_nm
                                    , tchr_nm_e
                                    , sch_grd
                                    , sch_cd
                                    , sch_nm
                                    , mob_no
                                    , tel_no
                                    , area_city
                                    , area_gu
                                    , h_addr
                                    , h_post_no
                                    , s_addr
                                    , s_post_no
                                    , email_addr
                                    , ins_id
                                    , ins_ip
                                    , ins_dt
                                    , ins_pgm
                                    , upd_id
                                    , upd_ip
                                    , upd_dt
                                    , upd_pgm
                                    , pwd)
                                values(
                                '{member_id}'
                                , '{member_nm}'
                                , '{member_nm_e}'
                                , '{member_sch_grd}'
                                , ''
                                , '{member_sch}'
                                , '{member_mob}'
                                , '{member_tel}'
                                , '{member_city}'
                                , '{member_gu}'
                                , '{member_addr}'
                                , '{member_post}'
                                , '{member_addr_sch}'
                                , '{member_post_sch}'
                                , '{member_email}'
                                , '{member_id}'
                                , '{client_ip}'
                                , now()
                                , '{ins_pgm}'
                                , '{member_id}'
                                , '{client_ip}'
                                , now()
                                , '{ins_pgm}'
                                , '{member_pwd}')
        """
        print(l_insert_query)
        cursor.execute(l_insert_query)

        login_id = member_id
    # 학부모
    elif member_gubun == "G":
        # 학부모ID 부여
        grdn_id_query = f"""select CONCAT('R',substr(DATE_FORMAT(now(), '%Y'),3,2),(select ifnull(lpad(max(right(grdn_id,4)) + 1,4,0),'0001') from service20_guardian where substr(grdn_id,2,2)  = substr(DATE_FORMAT(now(), '%Y'),3,2))) as id from dual"""
        print(grdn_id_query)
        cursor.execute(grdn_id_query)
        results_01 = namedtuplefetchall(cursor) 
        grdn_id= results_01[0].id

        l_insert_query = f"""
                            insert
                                into
                                    service20_guardian (
                                    grdn_id
                                    , grdn_nm
                                    , grdn_nm_e
                                    , rel_tp
                                    , brth_dt
                                    , mob_no
                                    , tel_no
                                    , moth_nat_cd
                                    , moth_nat_nm
                                    , tch_id
                                    , h_addr
                                    , h_post_no
                                    , email_addr
                                    , ins_id
                                    , ins_ip
                                    , ins_dt
                                    , ins_pgm
                                    , upd_id
                                    , upd_ip
                                    , upd_dt
                                    , upd_pgm
                                    , pwd)
                                values(
                                '{grdn_id}'
                                , '{member_nm}'
                                , '{member_nm_e}'
                                , '{member_rel}'
                                , '{member_birth}'
                                , '{member_mob}'
                                , '{member_tel}'
                                , ' '
                                , ' '
                                , '{member_sch}'
                                , '{member_addr}'
                                , '{member_post}'
                                , '{member_email}'
                                , '{grdn_id}'
                                , '{client_ip}'
                                , now()
                                , '{ins_pgm}'
                                , '{grdn_id}'
                                , '{client_ip}'
                                , now()
                                , '{ins_pgm}'
                                , '{member_pwd}')
        """
        print(l_insert_query)
        cursor.execute(l_insert_query)

        login_id = grdn_id

    context = {'login_id': login_id,'login_pwd': member_pwd} 
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#파일업로드 멘토스쿨
@csrf_exempt
def com_upload_ms(request):

    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/ms_apl/'
    UPLOAD_DIR = '/NANUM/www/img/ms_apl/'
    UPLOAD_DIR_JOB = '/NANUM/www/img/ms_job/'    
    # UPLOAD_DIR = '/home/'
    if request.method == 'POST':
        l_user_id = request.POST.get("user_id")
        l_ms_id = request.POST.get("ms_id")

        l_file = request.POST.get("file")
        l_job_file = request.POST.get("job_file")
        boolean_file = 'N'
        boolean_job_file = 'N'
        if l_file == None:
            boolean_file = 'Y'
        if l_job_file == None:
            boolean_job_file = 'Y'

        if boolean_file == 'Y':
            file = request.FILES['file']
            filename = file._name
            n_filename = str(l_user_id) + '_' + str(l_ms_id) + '' + os.path.splitext(filename)[1]
            print(n_filename)
            print (UPLOAD_DIR)
            
            fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')

            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            cursor = connection.cursor()
            fullFile = str(UPLOAD_DIR) + str(n_filename)
            fullFile = "/img/ms_apl/"+ str(n_filename)
            insert_sql = "update service20_ms_apl set  id_pic = '" + str(fullFile) + "' where ms_id = '"+ str(l_ms_id) + "' and apl_id = '" +  str(l_user_id) +"' "
            print(insert_sql)
            cursor.execute(insert_sql)

        if boolean_job_file == 'Y':
            # job
            job_file = request.FILES['job_file']
            job_filename = job_file._name
            n_job_filename = str(l_user_id) + '_' + str(l_ms_id) + '' + os.path.splitext(job_filename)[1]

            # job
            fp = open('%s/%s' % (UPLOAD_DIR_JOB, n_job_filename) , 'wb')

            for chunk in job_file.chunks():
                fp.write(chunk)
            fp.close()
            # job

            cursor = connection.cursor()
            job_fullFile = "/img/ms_job/"+ str(n_job_filename)
            insert_sql = "update service20_ms_apl set  file_job_fav = '" + str(job_fullFile) + "' where ms_id = '"+ str(l_ms_id) + "' and apl_id = '" +  str(l_user_id) +"' "
            print(insert_sql)
            cursor.execute(insert_sql)

        return HttpResponse('File Uploaded')

    return HttpResponse('Failed to Upload File')

#파일업로드 테스트
@csrf_exempt
def com_upload(request):

    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/mp_mtr/'
    UPLOAD_DIR = '/NANUM/www/img/mp_mtr/'
    UPLOAD_DIR_JOB = '/NANUM/www/img/mp_job/'    

    if request.method == 'POST':

        l_user_id = request.POST.get("user_id")
        l_mp_id = request.POST.get("mp_id")

        l_file = request.POST.get("file")
        # l_job_file = request.POST.get("job_file")
        boolean_file = 'N'
        boolean_job_file = 'N'
        if l_file == None:
            boolean_file = 'Y'
        # if l_job_file == None:
        #     boolean_job_file = 'Y'
        
        if boolean_file == 'Y':
            file = request.FILES['file']
            filename = file._name
            n_filename = str(l_user_id) + '_' + str(l_mp_id) + '' + os.path.splitext(filename)[1]

            fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')

            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            cursor = connection.cursor()
            fullFile = str(UPLOAD_DIR) + str(n_filename)
            fullFile = "/img/mp_mtr/"+ str(n_filename)
            insert_sql = "update service20_mp_mtr set id_pic = '" + str(fullFile) + "' where mp_id = '"+ str(l_mp_id) + "' and apl_id = '" +  str(l_user_id) +"' "
            print(insert_sql)
            cursor.execute(insert_sql)

        # if boolean_job_file == 'Y':
        #     # job
        #     job_file = request.FILES['job_file']
        #     job_filename = job_file._name
        #     n_job_filename = str(l_user_id) + '_' + str(l_mp_id) + '' + os.path.splitext(job_filename)[1]

        #     # job
        #     fp = open('%s/%s' % (UPLOAD_DIR_JOB, n_job_filename) , 'wb')

        #     for chunk in job_file.chunks():
        #         fp.write(chunk)
        #     fp.close()
        #     # job

        #     cursor = connection.cursor()
        #     job_fullFile = "/img/mp_job/"+ str(n_job_filename)
        #     insert_sql = "update service20_mp_mtr set  file_job_fav = '" + str(job_fullFile) + "' where mp_id = '"+ str(l_mp_id) + "' and apl_id = '" +  str(l_user_id) +"' "
        #     print(insert_sql)
        #     cursor.execute(insert_sql)    
        

        
        
        return HttpResponse('File Uploaded')

    return HttpResponse('Failed to Upload File')


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
