from django.shortcuts import render
from rest_framework import generics, serializers
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.http import HttpResponse,Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *
from service20.models import *
from django.db import connection
# Create your views here.

class Service10AuthListSerializer(serializers.ModelSerializer):

    class Meta:
        model = vm_nanum_stdt
        fields = ('apl_id', 'apl_nm','apl_nm_e','univ_cd','univ_nm')



class Service10AuthListView(generics.ListAPIView):
    queryset = vm_nanum_stdt.objects.all()
    serializer_class = Service10AuthListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

@csrf_exempt
def post_login(request):
	ida = request.POST.get('user_id', None)
	passa = request.POST.get('user_pw', None)
	chk_info = request.POST.get('chk_info', None)

	#created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)

	created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
	#rows = vm_nanum_stdt.objects.filter(apl_id=ida)
	#rows2 = vm_nanum_stdt.objects.get("apl_nm")
	
	client_ip = request.META['REMOTE_ADDR']

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
	query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
	query += " where user_id = '"+str(ida)+"'"
	cursor = connection.cursor()
	query_result = cursor.execute(query)  
	results = namedtuplefetchall(cursor)  
	if query_result == 0:
		v_login_gubun = ''
		v_user_div = ''
	else:
		v_login_gubun_code = str(results[0].user_div)
		v_login_gubun = str(results[0].std_detl_code_nm)
		v_user_div =  str(results[0].user_div)

	if v_user_div == "M" or v_user_div == "S":
		created_flag = "ok"
	elif v_user_div == "G":
		# 학부모
		created_flag = "ok"
	elif v_user_div == "T":
		# 교사
		created_flag = "ok"
	elif v_user_div == "E":
		# 멘티
		created_flag = "ok"

	if not created_flag:
		message = "Fail"
		context = {'message': message}

		########################################################################
		# 타대학생 로그인처리 - 시작
		########################################################################

		# 로그인처리 - 시작                
		query = "select t1.id,t1.std_id        /* 타대생 id(학교코드+학번) */ ";
		query += "     , t1.std_nm        /* 타대생 명 */ ";
		query += "     , t1.std_nm_e      /* 타대생 영문명 */ ";
		query += "     , t1.ms_id         /* 멘토스쿨id */ ";
		query += "     , t1.apl_no        /* 지원 no */ ";
		query += "     , t1.apl_id        /* 지원자id(학번) */ ";
		query += "     , t1.reg_dt        /* 등록일 */ ";
		query += "     , t1.unv_cd        /* 타대생 대학교 코드(mp0044) */ ";
		query += "     , t1.unv_nm        /* 타대생 대학교 명 */ ";
		query += "     , t1.cllg_cd       /* 타대생 대학 코드 */ ";
		query += "     , t1.cllg_nm       /* 타대생 대학 명 */ ";
		query += "     , t1.dept_cd       /* 타대생 학부/학과 코드 */ ";
		query += "     , t1.dept_nm       /* 타대생 학부/학과 명 */ ";
		query += "     , t1.brth_dt       /* 생년월일 */ ";
		query += "     , t1.gen           /* 성별 */ ";
		query += "     , t1.yr            /* 학년도 */ ";
		query += "     , t1.term_div      /* 학기 */ ";
		query += "     , t1.sch_yr        /* 학년 */ ";
		query += "     , t1.exp_dt        /* 자격 박탈일 */ ";
		query += "     , t1.exp_rsn       /* 박탈 사유 */ ";
		query += "     , t1.mob_no        /* 휴대전화 */ ";
		query += "     , t1.tel_no        /* 집전화 */ ";
		query += "     , t1.tel_no_g      /* 보호자 연락처 */ ";
		query += "     , t1.h_addr        /* 집주소 */ ";
		query += "     , t1.post_no       /* 우편번호 */ ";
		query += "     , t1.email_addr    /* 이메일 주소 */ ";
		query += "     , t1.bank_acct     /* 은행 계좌 번호 */ ";
		query += "     , t1.bank_cd       /* 은행 코드 */ ";
		query += "     , t1.bank_nm       /* 은행 명 */ ";
		query += "     , t1.bank_dpsr     /* 예금주 */ ";
		query += "     , t1.cnt_mp_a      /* 멘토링 지원 경력 */ ";
		query += "     , t1.cnt_mp_p      /* 멘토링 수행 경력 */ ";
		query += "     , t1.cnt_mp_c      /* 멘토링 완료 경력 */ ";
		query += "     , t1.cnt_mp_g      /* 멘토링 중도포기 경력 */ ";
		query += "     , t1.inv_agr_div   /* 개인정보 동의 여부 */ ";
		query += "     , t1.inv_agr_dt    /* 개인정보 동의 일시 */ ";
		query += "     , t1.dept_chr_id   /* 학과장 id */ ";
		query += "     , t1.dept_chr_nm   /* 학과장 명 */ ";
		query += "     , t1.ast_id        /* 조교 id */ ";
		query += "     , t1.ast_nm        /* 조교 명 */ ";
		query += "     , t1.dept_appr_div /* 학과 승인 여부 */ ";
		query += "     , t1.dept_appr_dt  /* 학과 승인 날짜 */ ";
		query += "     , t1.dept_retn_rsn /* 학과 반려 사유 */ ";
		query += "     , t1.ins_id        /* 입력자id */ ";
		query += "     , t1.ins_ip        /* 입력자ip */ ";
		query += "     , t1.ins_dt        /* 입력일시 */ ";
		query += "     , t1.ins_pgm       /* 입력프로그램id */ ";
		query += "     , t1.upd_id        /* 수정자id */ ";
		query += "     , t1.upd_ip        /* 수정자ip */ ";
		query += "     , t1.upd_dt        /* 수정일시 */ ";
		query += "     , t1.upd_pgm       /* 수정프로그램id */ ";
		query += "     , t1.mjr_cd        /* 전공코드 */ ";
		query += "     , t1.mjr_nm        /* 전공명 */ ";
		query += "     , t1.pwd           /* 비밀번호 */ ";    
		query += " from service20_oth_std t1     /* 부산대학교 학생 정보 */ "              
		query += " where t1.std_id='"+ida+"'" 
		V_OTH_GUBUN = 'F'
		print(query)
		queryset2 = oth_std.objects.raw(query)
		for var2 in queryset2:
			print(var2.std_id)
			# vl_cscore1 = var2.fin_scr
			V_OTH_GUBUN = 'T'
			message = "Ok"
			context = {'message': message,
			'apl_id' : str(var2.std_id),
			'apl_nm' : str(var2.std_nm),
			'univ_cd' : str(var2.unv_cd),
			'univ_nm' : str(var2.unv_nm),
			'brth_dt' : str(var2.brth_dt),
			'gen_cd' : str(var2.gen),
			'gen_nm' : str(var2.gen),
			'login_gubun_code' : 'OTH',
			'login_gubun' : '타대학생'
			}

		########################################################################
		# 타대학생 로그인처리 - 종료
		########################################################################
	else:
		message = "Ok"
		# rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
		if v_user_div == "M" or v_user_div == "S":
			# 멘토/학생
			rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
			v_apl_id = rows.apl_id
			v_apl_nm = rows.apl_nm.replace('\'','')
		elif v_user_div == "G":
			# 학부모
			created_flag2 = guardian.objects.filter(grdn_id=ida,pwd=passa).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
				# select * from service20_guardian;
				rows = guardian.objects.filter(grdn_id=ida,pwd=passa)[0]
				v_apl_id = rows.grdn_id
				v_apl_nm = rows.grdn_nm.replace('\'','')
		elif v_user_div == "T":
			# 교사
			created_flag2 = teacher.objects.filter(tchr_id=ida,pwd=passa).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
				# select * from service20_teacher;	
				rows = teacher.objects.filter(tchr_id=ida,pwd=passa)[0]
				v_apl_id = rows.tchr_id
				v_apl_nm = rows.tchr_nm.replace('\'','')
		elif v_user_div == "E":
			# 멘티
			created_flag2 = mentee.objects.filter(mnte_id=ida).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
				# select * from service20_manager;
				rows = mentee.objects.filter(mnte_id=ida)[0]
				v_apl_id = rows.mnte_id
				v_apl_nm = rows.mnte_nm.replace('\'','')		

		client_ip = request.META['REMOTE_ADDR']
		query = " insert into service20_com_evt     /* 이벤트로그 */ ";
		query += "      ( evt_gb     /* 이벤트구분 */ ";
		query += "     , evt_userid /* 이벤트사용자id */ ";
		query += "     , evt_ip     /* 이벤트발생 ip */ ";
		query += "     , evt_dat    /* 이벤트일시 */ ";
		query += "     , evt_desc   /* 이벤트 내용 */ ";
		query += "     , ins_id     /* 입력자id */ ";
		query += "     , ins_ip     /* 입력자ip */ ";
		query += "     , ins_dt     /* 입력일시 */ ";
		query += "     , ins_pgm    /* 입력프로그램id */ ";
		query += ") ";
		query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ ";
		query += "     , '"+ida+"' AS evt_userid /* 이벤트사용자id */ ";
		query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
		query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
		query += "     , CONCAT('','로그인') evt_desc   /* 이벤트 내용 */ ";
		query += "     , '"+ida+"' AS ins_id     /* 입력자id */ ";
		query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
		query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
		query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
		cursor_log = connection.cursor()
		query_result = cursor_log.execute(query)  

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
			v_user_div =  str(results[0].user_div)

		if v_user_div == "M" or v_user_div == "S":
			# 멘토/학생
			context = {'message': message,
					'apl_nm' : v_apl_nm,
					'apl_id' : v_apl_id,
					'univ_cd' : rows.univ_cd,
					'univ_nm' : rows.univ_nm,
					'grad_div_cd' : rows.grad_div_cd,
					'grad_div_nm' : rows.grad_div_nm,
					'cllg_cd' : rows.cllg_cd,
					'cllg_nm' : rows.cllg_nm,
					'dept_cd' : rows.dept_cd,
					'dept_nm' : rows.dept_nm.replace('\'',''),
					'mjr_cd' : rows.mjr_cd,
					'mjr_nm' : rows.mjr_nm,
					'brth_dt' : rows.brth_dt,
					'gen_cd' : rows.gen_cd,
					'gen_nm' : rows.gen_nm,
					'yr' : rows.yr,
					'sch_yr' : rows.sch_yr,
					'term_div' : rows.term_div,
					'term_nm' : rows.term_nm,
					'stdt_div' : rows.stdt_div,
					'stdt_nm' : rows.stdt_nm,
					'mob_nm' : rows.mob_nm,
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
					'score04_tp' : rows.score04_tp,
					'score05' : rows.score05,
					'mntr_id' : v_mntr_id,
                    'login_gubun_code' : v_login_gubun_code,
                    'login_gubun' : v_login_gubun
					}
		elif v_user_div == "G":
			# 학부모
			created_flag2 = guardian.objects.filter(grdn_id=ida,pwd=passa).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
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
			created_flag2 = teacher.objects.filter(tchr_id=ida,pwd=passa).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
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
			created_flag2 = mentee.objects.filter(mnte_id=ida,pwd=passa).exists()
			if not created_flag2:
				message = "Fail"
				context = {'message': message}
			else:
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

			########################################################################
			# 타대학생 로그인처리 - 시작
			########################################################################

			# 로그인처리 - 시작                
			query = "select t1.std_id        /* 타대생 id(학교코드+학번) */ ";
			query += "     , t1.std_nm        /* 타대생 명 */ ";
			query += "     , t1.std_nm_e      /* 타대생 영문명 */ ";
			query += "     , t1.ms_id         /* 멘토스쿨id */ ";
			query += "     , t1.apl_no        /* 지원 no */ ";
			query += "     , t1.apl_id        /* 지원자id(학번) */ ";
			query += "     , t1.reg_dt        /* 등록일 */ ";
			query += "     , t1.unv_cd        /* 타대생 대학교 코드(mp0044) */ ";
			query += "     , t1.unv_nm        /* 타대생 대학교 명 */ ";
			query += "     , t1.cllg_cd       /* 타대생 대학 코드 */ ";
			query += "     , t1.cllg_nm       /* 타대생 대학 명 */ ";
			query += "     , t1.dept_cd       /* 타대생 학부/학과 코드 */ ";
			query += "     , t1.dept_nm       /* 타대생 학부/학과 명 */ ";
			query += "     , t1.brth_dt       /* 생년월일 */ ";
			query += "     , t1.gen           /* 성별 */ ";
			query += "     , t1.yr            /* 학년도 */ ";
			query += "     , t1.term_div      /* 학기 */ ";
			query += "     , t1.sch_yr        /* 학년 */ ";
			query += "     , t1.exp_dt        /* 자격 박탈일 */ ";
			query += "     , t1.exp_rsn       /* 박탈 사유 */ ";
			query += "     , t1.mob_no        /* 휴대전화 */ ";
			query += "     , t1.tel_no        /* 집전화 */ ";
			query += "     , t1.tel_no_g      /* 보호자 연락처 */ ";
			query += "     , t1.h_addr        /* 집주소 */ ";
			query += "     , t1.post_no       /* 우편번호 */ ";
			query += "     , t1.email_addr    /* 이메일 주소 */ ";
			query += "     , t1.bank_acct     /* 은행 계좌 번호 */ ";
			query += "     , t1.bank_cd       /* 은행 코드 */ ";
			query += "     , t1.bank_nm       /* 은행 명 */ ";
			query += "     , t1.bank_dpsr     /* 예금주 */ ";
			query += "     , t1.cnt_mp_a      /* 멘토링 지원 경력 */ ";
			query += "     , t1.cnt_mp_p      /* 멘토링 수행 경력 */ ";
			query += "     , t1.cnt_mp_c      /* 멘토링 완료 경력 */ ";
			query += "     , t1.cnt_mp_g      /* 멘토링 중도포기 경력 */ ";
			query += "     , t1.inv_agr_div   /* 개인정보 동의 여부 */ ";
			query += "     , t1.inv_agr_dt    /* 개인정보 동의 일시 */ ";
			query += "     , t1.dept_chr_id   /* 학과장 id */ ";
			query += "     , t1.dept_chr_nm   /* 학과장 명 */ ";
			query += "     , t1.ast_id        /* 조교 id */ ";
			query += "     , t1.ast_nm        /* 조교 명 */ ";
			query += "     , t1.dept_appr_div /* 학과 승인 여부 */ ";
			query += "     , t1.dept_appr_dt  /* 학과 승인 날짜 */ ";
			query += "     , t1.dept_retn_rsn /* 학과 반려 사유 */ ";
			query += "     , t1.ins_id        /* 입력자id */ ";
			query += "     , t1.ins_ip        /* 입력자ip */ ";
			query += "     , t1.ins_dt        /* 입력일시 */ ";
			query += "     , t1.ins_pgm       /* 입력프로그램id */ ";
			query += "     , t1.upd_id        /* 수정자id */ ";
			query += "     , t1.upd_ip        /* 수정자ip */ ";
			query += "     , t1.upd_dt        /* 수정일시 */ ";
			query += "     , t1.upd_pgm       /* 수정프로그램id */ ";
			query += "     , t1.mjr_cd        /* 전공코드 */ ";
			query += "     , t1.mjr_nm        /* 전공명 */ ";
			query += "     , t1.pwd           /* 비밀번호 */ ";    
			query += " from service20_oth_std t1     /* 부산대학교 학생 정보 */ "              
			query += " where t1.std_id='"+ida+"'" 
			V_OTH_GUBUN = 'F'
			print(query)
			queryset2 = oth_std.objects.raw(query)
			for var2 in queryset2:
				print(var2.std_id)
				# vl_cscore1 = var2.fin_scr
				V_OTH_GUBUN = 'T'
				message = "Ok"
				context = {'message': message,
				'apl_id' : str(var2.std_id),
				'apl_nm' : str(var2.std_nm),
				'univ_cd' : str(var2.unv_cd),
				'univ_nm' : str(var2.unv_nm),
				'brth_dt' : str(var2.brth_dt),
				'gen_cd' : str(var2.gen),
				'gen_nm' : str(var2.gen),
				'login_gubun_code' : 'OTH',
				'login_gubun' : '타대학생'
				}

			########################################################################
			# 타대학생 로그인처리 - 종료
			########################################################################
		# context = {'message': message,
		# 			'apl_nm' : v_apl_nm,
		# 			'apl_id' : v_apl_id,
		# 			'univ_cd' : rows.univ_cd,
		# 			'univ_nm' : rows.univ_nm,
		# 			'grad_div_cd' : rows.grad_div_cd,
		# 			'grad_div_nm' : rows.grad_div_nm,
		# 			'cllg_cd' : rows.cllg_cd,
		# 			'cllg_nm' : rows.cllg_nm,
		# 			'dept_cd' : rows.dept_cd,
		# 			'dept_nm' : rows.dept_nm.replace('\'',''),
		# 			'mjr_cd' : rows.mjr_cd,
		# 			'mjr_nm' : rows.mjr_nm,
		# 			'brth_dt' : rows.brth_dt,
		# 			'gen_cd' : rows.gen_cd,
		# 			'gen_nm' : rows.gen_nm,
		# 			'yr' : rows.yr,
		# 			'sch_yr' : rows.sch_yr,
		# 			'term_div' : rows.term_div,
		# 			'term_nm' : rows.term_nm,
		# 			'stdt_div' : rows.stdt_div,
		# 			'stdt_nm' : rows.stdt_nm,
		# 			'mob_nm' : rows.mob_nm,
		# 			'tel_no' : rows.tel_no,
		# 			'tel_no_g' : rows.tel_no_g,
		# 			'h_addr' : rows.h_addr,
		# 			'post_no' : rows.post_no,
		# 			'email_addr' : rows.email_addr,
		# 			'bank_acct' : rows.bank_acct,
		# 			'bank_cd' : rows.bank_cd,
		# 			'bank_nm' : rows.bank_nm,
		# 			'bank_dpsr' : rows.bank_dpsr,
		# 			'pr_yr' : rows.pr_yr,
		# 			'pr_sch_yr' : rows.pr_sch_yr,
		# 			'pr_term_div' : rows.pr_term_div,
		# 			'score01' : rows.score01,
		# 			'score02' : rows.score02,
		# 			'score03' : rows.score03,
		# 			'score04' : rows.score04,
		# 			'score04_tp' : rows.score04_tp,
		# 			'score05' : rows.score05,
		# 			'mntr_id' : v_mntr_id,
  #                   'login_gubun_code' : v_login_gubun_code,
  #                   'login_gubun' : v_login_gubun
		# 			}
	
		print(context)
	#return HttpResponse(json.dumps(context), content_type="application/json")
	return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



def authView(request):
    context = None
    return render(request, 'service10/Service10Auth.html', context)
