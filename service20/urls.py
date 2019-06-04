from django.urls import path
from service20.views import *
from service20.views2 import *
from . import views
from . import views2

app_name = 'service20'

urlpatterns = [
    
     #path('', views.stdApplyIns, name='stdApplyIns'),

     #멘토링 질문리스트 (미사용)
    # path('post_mt_quest/', post_mt_quest, name='post_mt_Quest'),   

    path('stdApplyStdView/', stdApplyStdView, name='detail'),
    path('Service20_01/', Service20_01_View, name='detail'),
    path('mpmgListView/', mpmgListView.as_view(), name='mpmgListView'),

    ########################################################################################
    # 공통(com)
    #
    ########################################################################################    
    #자료실
    path('com/datacenter/', com_datacenter.as_view(), name='com_datacenter'), 
    #자료실 디테일
    path('com/datacenter/detail/', com_datacenter_detail.as_view(), name='com_datacenter_detail'), 
    #공지사항
    path('com/notice/', com_notice.as_view(), name='com_notice'), 
    #공지사항 디테일
    path('com/notice/detail/', com_notice_detail.as_view(), name='com_notice_detail'), 
    path('com/mentoHistory/list/', com_mentoHistory_list.as_view(), name='com_mentoHistory_list'), 
    path('com/mentoHistory/', com_mentoHistory.as_view(), name='com_mentoHistory'), 
    #파일업로드(멘토스쿨용)
    path('com/upload/ms/', com_upload_ms, name='com_upload_ms'), 
    #파일업로드
    path('com/upload/', com_upload, name='com_upload'), 
    #리턴URLTest
    path('login/login/', login_login, name='login_login'), 
    path('login/login/admin/', login_login_admin, name='login_login_admin'), 
    #리턴URLTest
    path('login/returnsso/', login_returnsso, name='login_returnsso'), 
    #리턴URLTest
    path('login/session/', login_session, name='login_session'), 
    # 년도 콤보박스
    path('com/combo/yr/', com_combo_yr.as_view(), name='com_combo_yr'),
    # 학기 콤보박스
    path('com/combo/termdiv/', com_combo_termdiv.as_view(), name='com_combo_termdiv'),
    # 모집상태 콤보박스
    path('com/combo/ms/status/', com_combo_ms_status.as_view(), name='com_combo_ms_status'),
    # 모집상태 콤보박스
    path('com/combo/mp/status/', com_combo_mp_status.as_view(), name='com_combo_mp_status'),
    # 월단위 콤보박스
    path('com/combo/month/', com_combo_month.as_view(), name='com_combo_month'),
    # 취소사유 콤보박스
    path('com/combo/cnclRsn/', com_combo_cnclRsn.as_view(), name='com_combo_cnclRsn'),
    # 학습외 멘티 취소사유 콤보박스
    path('com/combo/mnteCnclRsn/', com_combo_mnteCnclRsn.as_view(), name='com_combo_mnteCnclRsn'),   
    path('com/combo/repdiv/', com_combo_repdiv.as_view(), name='com_combo_repdiv'), 
    path('com/combo/com_cdd/', com_combo_com_cdd.as_view(), name='com_combo_com_cdd'), 
    # 보호자승인 콤보박스
    path('com/combo/appr/', com_combo_appr.as_view(), name='com_combo_appr'),
    # 관리자승인 콤보박스
    path('com/combo/mgr/', com_combo_mgr.as_view(), name='com_combo_mgr'),
    # 계획서, 보고서 상태 콤보박스
    path('com/combo/pln/status/', com_combo_pln_status.as_view(), name='com_combo_pln_status'),
    # 멘토의 학번으로 해당되는 멘티찾기
    path('com/list/my_mentee/', com_list_my_mentee.as_view(), name='com_list_my_mentee'),
    # 프로그램 찾기
    path('com/combo/program/', com_combo_program.as_view(), name='com_combo_program'),
    # 프로그램의 상태에 따른 프로그램 콤보박스
    path('com/combo/program2/', com_combo_program2.as_view(), name='com_combo_program2'), 
    # 멘토,멘티 의 상태가 활동 중인 프로그램 콤보박스
    path('com/combo/program3/', com_combo_program3.as_view(), name='com_combo_program3'), 

    # 어학점수
    path('com/user/fe/', com_user_fe.as_view(), name='com_user_fe'),
    # 봉사점수
    path('com/user/sa/', com_user_sa.as_view(), name='com_user_sa'),
    # 사용자정보
    path('com/user/', com_user.as_view(), name='com_user'),

    # 교육구분 콤보박스
    path('com/combo/edu/', com_combo_edu.as_view(), name='com_combo_edu'),
    # 출석구분 콤보박스
    path('com/combo/att/div/', com_combo_att_div.as_view(), name='com_combo_att_div'),
    # 출석상태 콤보박스
    path('com/combo/att/status/', com_combo_att_status.as_view(), name='com_combo_att_status'),
    # 학습외 프로그램 리스트(콤보)
    path('com/combo/spcProgram/', com_combo_spcProgram.as_view(), name='com_combo_spcProgram'),
    # 학습외 모집상태 콤보박스
    path('com/combo/spc/status/', com_combo_spc_status.as_view(), name='com_combo_spc_status'),
    # 프로그램 찾기 (introduce테이블 프로그램)
    path('com/combo/programIntroduce/', com_combo_programIntroduce.as_view(), name='com_combo_programIntroduce'),
    # 회원구분 콤보(멘티, 학부모, 교사만)
    path('com/combo/member_gubun/', com_combo_member_gubun.as_view(), name='com_combo_member_gubun'), 
    # 멘티와의 관계 콤보
    path('com/combo/member_rel/', com_combo_member_rel.as_view(), name='com_combo_member_rel'), 
    # 멘티의 학교 리스트 콤보
    path('com/combo/member_mnte_sch/', com_combo_member_mnte_sch.as_view(), name='com_combo_member_mnte_sch'), 
    # 학교 구분 콤보
    path('com/combo/sch_grd/', com_combo_sch_grd.as_view(), name='com_combo_sch_grd'), 
    # 만족도조사 상태 콤보
    path('com/combo/surv/status/', com_combo_surv_status.as_view(), name='com_combo_sch_grd'), 
    ########################################################################################
    # 공통(com)
    #
    ########################################################################################    

    ########################################################################################
    # MainPage
    #
    ########################################################################################
    # 현재 모집중인 멘토링 프로그램
    path('main/list/1/', mpmgListView.as_view(), name='mpmgListView'),
    # 현재 등록된 멘토건수
    path('main/list/mento_count/', main_list_mento_count.as_view(), name='main_list_mento_count'),
    ########################################################################################
    # MainPage
    #
    ########################################################################################

    ########################################################################################
    # membership(회원가입)
    #
    ########################################################################################
    # 회원가입 중복체크
    path('member/overlap/', member_overlap.as_view(), name='member_overlap'),
    # 회원가입 학부모 검색
    path('member/popup/guard/', member_popup_guard.as_view(), name='member_popup_guard'),
    # 회원가입 insert
    path('member/insert/', member_insert, name='member_insert'),
    ########################################################################################
    # membership(회원가입)
    #
    ########################################################################################

    ########################################################################################
    # myPage
    #
    ########################################################################################
    # 멘토 마이페이지
    path('myapge/mentoList/', mentoMypage_list.as_view(), name='mentoMypage_list'),
    # 멘티 마이페이지
    path('myapge/menteList/', menteMypage_list.as_view(), name='menteMypage_list'),    
    # 교사 마이페이지
    path('myapge/tchrList/', tchrMypage_list.as_view(), name='tchrMypage_list'), 
    # 학부모 마이페이지
    path('myapge/grdList/', grdMypage_list.as_view(), name='grdMypage_list'),    
    # 기타사용자 마이페이지
    path('myapge/ectUserList/', ectUserListMypage_list.as_view(), name='ectUserListMypage_list'),       
    # 마이페이지 프로그램리스트
    path('myapge/programList/', programMypage_list.as_view(), name='programMypage_list'),    
    # 멘토 프로그램별 멘티 리스트
    path('myapge/mentoMenteList/', mentoMenteMypage_list.as_view(), name='mentoMenteMypage_list'),
    # 교사,학부모 프로그램별 멘티 리스트
    path('myapge/pgmMenteList/', pgmMenteMypage_list.as_view(), name='pgmMenteMypage_list'),   
    # 멘토스쿨
    path('myapge/mschList/', mschListMypage_list.as_view(), name='mschListMypage_list'), 
    # 멘토 활동 내역
    path('myapge/mentoActiveList/', mentoActiveListMypage_list.as_view(), name='mentoActiveListMypage_list'),  
    # 멘티 활동 내역
    path('myapge/menteActiveList/', menteActiveListMypage_list.as_view(), name='menteActiveListMypage_list'),        
    # 멘토 출석부
    path('myapge/mentoAttdList/', mentoAttdListMypage_list.as_view(), name='mentoAttdListMypage_list'), 
    # 멘토 출석부(상세)
    path('myapge/mentoAttdDetailList/', mentoAttdDetailListMypage_list.as_view(), name='mentoAttdDetailListMypage_list'),     
    # 인증서
    path('myapge/report/certificateList/', certificateListMypage_list.as_view(), name='certificateListMypage_list'),
    # 패스워드 변경
    path('mypage/update/', mypage_update, name='mypage_update'),       
    ########################################################################################
    # myPage
    #
    ########################################################################################
    

    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################
    path('MS0101M/list/chk/1/', MS0101M_list_chk_1.as_view(), name='MS0101M_list_chk_1'),
    path('MS0101M/list/chk/2/', MS0101M_list_chk_2.as_view(), name='MS0101M_list_chk_2'),
    path('MS0101M/list/chk/3/', MS0101M_list_chk_3.as_view(), name='MS0101M_list_chk_3'),
    path('MS0101M/list/chk/4/', MS0101M_list_chk_4.as_view(), name='MS0101M_list_chk_4'),
    path('MS0101M/list/chk/5/', MS0101M_list_chk_5.as_view(), name='MS0101M_list_chk_5'),
    path('MS0101M/list/chk/7/', MS0101M_list_chk_7.as_view(), name='MS0101M_list_chk_7'),
    path('MS0101M/list/chk/8/', MS0101M_list_chk_8.as_view(), name='MS0101M_list_chk_8'),
    # 멘토스쿨 리스트 조회
    path('MS0101M/list/', MS0101M_list.as_view(), name='MS0101M_list'),
    # 멘토스쿨 질문유형 가져오기
    path('MS0101M/quest/', MS0101M_quest.as_view(), name='MS0101M_quest'), 
    # 멘토스쿨 신청
    path('MS0101M/save/', MS0101M_save, name='MS0101M_save'), 
    # 성적,봉사,어학 가져오기
    path('MS0101M/detail/', MS0101M_detail, name='MS0101M_detail'),
    # 멘토스쿨(관리자) - 기본정보
    path('MS0101M/admin/list/', MS0101M_adm_list.as_view(), name='MS0101M_adm_list'),
    # 멘토링 프로그램(관리자) - 어학점수
    path('MS0101M/admin/list/fe/', MS0101M_adm_list_fe.as_view(), name='MS0101M_adm_list_fe'),
    # 멘토링 프로그램(관리자) - 봉사점수
    path('MS0101M/admin/list/sa/', MS0101M_adm_list_sa.as_view(), name='MS0101M_adm_list_sa'),
    # 멘토스쿨(관리자) - 질문
    path('MS0101M/admin/quest/', MS0101M_adm_quest.as_view(), name='MS0101M_adm_quest'),
    # 멘토스쿨(관리자) 수락
    path('MS0101M/admin/acpt_save/', MS0101M_adm_acpt_save, name='MS0101M_adm_acpt_save'), 
    # 멘토스쿨(관리자) 수락취소
    path('MS0101M/admin/acpt_cancle/', MS0101M_adm_acpt_cancle, name='MS0101M_adm_acpt_cancle'), 
    # 멘토스쿨(관리자) update
    path('MS0101M/admin/update/', MS0101M_adm_update, name='MS0101M_adm_update'), 
    # 멘토스쿨(관리자) cancle
    path('MS0101M/admin/cancle/', MS0101M_adm_cancle, name='MS0101M_adm_cancle'), 
    # 멘토링 프로그램(레포트) - 기본정보
    path('MS0101M/report/list/', MS0101M_report_list.as_view(), name='MS0101M_report_list'),
    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################

    ########################################################################################
    # 멘토링 프로그램(MP0101M - START )
    #
    ########################################################################################
    # 멘토링 프로그램 리스트 조회
    path('MP0101M/list/chk/1/', MP0101M_list_chk_1.as_view(), name='MP0101M_list_chk_1'),
    path('MP0101M/list/chk/2/', MP0101M_list_chk_2.as_view(), name='MP0101M_list_chk_2'),
    path('MP0101M/list/chk/3/', MP0101M_list_chk_3.as_view(), name='MP0101M_list_chk_3'),
    path('MP0101M/list/chk/4/', MP0101M_list_chk_4.as_view(), name='MP0101M_list_chk_4'),
    path('MP0101M/list/chk/5/', MP0101M_list_chk_5.as_view(), name='MP0101M_list_chk_5'),
    path('MP0101M/list/chk/6/', MP0101M_list_chk_6.as_view(), name='MP0101M_list_chk_6'),
    path('MP0101M/list/chk/7/', MP0101M_list_chk_7.as_view(), name='MP0101M_list_chk_7'),
    path('MP0101M/list/chk/8/', MP0101M_list_chk_8.as_view(), name='MP0101M_list_chk_8'),
    path('MP0101M/list/chk/9/', MP0101M_list_chk_9.as_view(), name='MP0101M_list_chk_9'),
    # 멘토링 프로그램 리스트 조회
    path('MP0101M/list/', MP0101M_list.as_view(), name='MP0101M_list'),
    # 멘토링 프로그램 신청내역(홈페이지)
    path('MP0101M/list/all/hompage/', MP0101M_list_all_hompage.as_view(), name='MP0101M_list_all_hompage'),
    # 멘토링 프로그램 신청내역(앱)
    path('MP0101M/list/all/', MP0101M_list_all.as_view(), name='MP0101M_list_all'),
    # 멘토링 프로그램 신청내역
    path('MP0101M/list/all/mypage/', MP0101M_list_all_mypage.as_view(), name='MP0101M_list_all_mypage'),
    # 멘토링 프로그램 질문유형 가져오기
    path('MP0101M/quest/', MP0101M_quest.as_view(), name='MP0101M_quest'), 
    # 멘토링 프로그램 신청
    path('MP0101M/save/', MP0101M_save, name='MP0101M_save'), 
    # 성적,봉사,어학 가져오기
    path('MP0101M/detail/', MP0101M_detail, name='MP0101M_detail'),
    # 멘토링 프로그램(관리자) - 기본정보
    path('MP0101M/admin/list/', MP0101M_adm_list.as_view(), name='MP0101M_adm_list'),
    # 멘토링 프로그램(관리자) - 어학점수
    path('MP0101M/admin/list/fe/', MP0101M_adm_list_fe.as_view(), name='MP0101M_adm_list_fe'),
    # 멘토링 프로그램(관리자) - 봉사점수
    path('MP0101M/admin/list/sa/', MP0101M_adm_list_sa.as_view(), name='MP0101M_adm_list_sa'),
    # 멘토링 프로그램(관리자) - 질문
    path('MP0101M/admin/quest/', MP0101M_adm_quest.as_view(), name='MP0101M_adm_quest'),
    # 멘토링 프로그램(관리자) 수락
    path('MP0101M/admin/acpt_save/', MP0101M_adm_acpt_save, name='MP0101M_adm_acpt_save'), 
    # 멘토링 프로그램(관리자) 수락취소
    path('MP0101M/admin/acpt_cancle/', MP0101M_adm_acpt_cancle, name='MP0101M_adm_acpt_cancle'), 
    # 멘토링 프로그램(관리자) update
    path('MP0101M/admin/update/', MP0101M_adm_update, name='MP0101M_adm_update'), 
    # 멘토링 프로그램(관리자) cancle
    path('MP0101M/admin/cancle/', MP0101M_adm_cancle, name='MP0101M_adm_cancle'), 
    # 멘토링 프로그램(레포트) - 기본정보
    path('MP0101M/report/list/', MP0101M_report_list.as_view(), name='MP0101M_report_list'),

    # 멘토링 프로그램 - 해외봉사활동 프로그램 (카운트)
    path('MP0101M/service/cnt/', MP0101M_service_cnt.as_view(), name='MP0101M_service_cnt'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (희망도시 콤보)
    path('MP0101M/service/combo/city/', MP0101M_service_combo_city.as_view(), name='MP0101M_service_combo_city'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (분야 콤보)
    path('MP0101M/service/combo/field/', MP0101M_service_combo_field.as_view(), name='MP0101M_service_combo_field'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (첨부파일 카운트)
    path('MP0101M/service/upload/cnt/', MP0101M_service_upload_cnt.as_view(), name='MP0101M_service_upload_cnt'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기)
    path('MP0101M/service/apl_no/', MP0101M_service_apl_no.as_view(), name='MP0101M_service_apl_no'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (insert)
    path('MP0101M/service/insert/', MP0101M_service_insert, name='MP0101M_service_insert'), 
    # 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(insert)
    path('MP0101M/service/upload/', MP0101M_upload, name='MP0101M_upload'),
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (데이터)
    path('MP0101M/admin/service/chc/', MP0101M_admin_service_chc.as_view(), name='MP0101M_admin_service_chc'),    
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (첨부데이터)
    path('MP0101M/admin/service/atc/', MP0101M_admin_service_atc.as_view(), name='MP0101M_admin_service_atc'), 
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (update)
    path('MP0101M/service/update/', MP0101M_service_update, name='MP0101M_service_update'), 
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 파일 업로드(update)
    path('MP0101M/service/upload/update/', MP0101M_upload_update, name='MP0101M_upload_update'),
    # 멘토링 프로그램(레포트) - 해외봉사활동 프로그램 (데이터)
    path('MP0101M/service/report/chc/', MP0101M_service_report_chc.as_view(), name='MP0101M_service_report_chc'),
    # 멘토링 프로그램 - mp_sub 코드 (sub_code)
    path('MP0101M/service/sub/', MP0101M_service_sub.as_view(), name='MP0101M_service_sub'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (콤보)
    path('MP0101M/service/combo/', MP0101M_service_combo.as_view(), name='MP0101M_service_combo'),

    # 멘토링 프로그램 리스트에서 팀 단위 status 가져오기
    path('MP0101M/list/team/status/', MP0101M_team_status.as_view(), name='MP0101M_team_status'), 
    # 멘토링 프로그램 팀단위 로그인id 가져오기
    path('MP0101M/team/logininfo/', MP0101M_team_logininfo.as_view(), name='MP0101M_team_logininfo'), 
    # 멘토링 프로그램 팀단위 질문유형 가져오기
    path('MP0101M/team/quest/', MP0101M_team_quest.as_view(), name='MP0101M_team_quest'), 
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (카운트)
    path('MP0101M/service/team/cnt/', MP0101M_service_team_cnt.as_view(), name='MP0101M_service_team_cnt'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (희망도시 콤보)
    path('MP0101M/service/team/combo/city/', MP0101M_service_team_combo_city.as_view(), name='MP0101M_service_team_combo_city'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (분야 콤보)
    path('MP0101M/service/team/combo/field/', MP0101M_service_team_combo_field.as_view(), name='MP0101M_service_team_combo_field'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (첨부파일 카운트)
    path('MP0101M/service/team/upload/cnt/', MP0101M_service_team_upload_cnt.as_view(), name='MP0101M_service_team_upload_cnt'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (apl_no 가져오기)
    path('MP0101M/service/team/apl_no/', MP0101M_service_team_apl_no.as_view(), name='MP0101M_service_team_apl_no'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (insert)
    path('MP0101M/service/team/insert/', MP0101M_service_team_insert, name='MP0101M_service_team_insert'), 
    # 멘토링 프로그램 - 해외봉사활동 프로그램 파일 업로드(insert)
    path('MP0101M/service/team/upload/', MP0101M_team_upload, name='MP0101M_team_upload'),
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (데이터)
    path('MP0101M/admin/service/team/chc/', MP0101M_admin_service_team_chc.as_view(), name='MP0101M_admin_service_team_chc'),    
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (첨부데이터)
    path('MP0101M/admin/service/team/atc/', MP0101M_admin_service_team_atc.as_view(), name='MP0101M_admin_service_team_atc'), 
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 (update)
    path('MP0101M/service/team/update/', MP0101M_service_team_update, name='MP0101M_service_team_update'), 
    # 멘토링 프로그램(관리자) - 해외봉사활동 프로그램 파일 업로드(update)
    path('MP0101M/service/team/upload/update/', MP0101M_team_upload_update, name='MP0101M_team_upload_update'),
    # 멘토링 프로그램(레포트) - 해외봉사활동 프로그램 (데이터)
    path('MP0101M/service/team/report/chc/', MP0101M_service_team_report_chc.as_view(), name='MP0101M_service_team_report_chc'),
    # 멘토링 프로그램 - mp_sub 코드 (sub_code)
    path('MP0101M/service/team/sub/', MP0101M_service_team_sub.as_view(), name='MP0101M_service_team_sub'),
    # 멘토링 프로그램 - 해외봉사활동 프로그램 (콤보)
    path('MP0101M/service/team/combo/', MP0101M_service_team_combo.as_view(), name='MP0101M_service_team_combo'),
    # 멘토링 프로그램(관리자) - 질문
    path('MP0101M/admin/team/quest/', MP0101M_adm_team_quest.as_view(), name='MP0101M_adm_team_quest'),
    # 멘토링 프로그램(관리자) - 업로드가능한 첨부파일
    path('MP0101M/service/file/chk/', MP0101M_service_team_upload_file_chk.as_view(), name='MP0101M_service_team_upload_file_chk'),
    # 멘토링 프로그램(팀원팝업) - 조회
    path('popupTeam/list/', popupTeam_list.as_view(), name='popupTeam_list'),
    # 멘토링 프로그램(팀원팝업) - delete
    path('popupTeam/delete/', popupTeam_delete, name='popupTeam_delete'),
    # 멘토링 프로그램(팀원팝업) - insert
    path('popupTeam/insert/', popupTeam_insert, name='popupTeam_insert'),
    ########################################################################################
    # 멘토링 프로그램(MP0101M - END )
    #
    ########################################################################################
    
    ########################################################################################
    # 학습외신청(멘토) 리스트(MP0102M - START )
    #
    ########################################################################################
    # 학습외신청(멘토) 리스트
    path('MP0102M/mento/list/', MP0102M_list.as_view(), name='MP0102M_list'), 
    # 학습외신청(멘티) 리스트
    path('MP0102M/mentee/list/', MP0102M_mentee_list.as_view(), name='MP0102M_mentee_list'), 
    # 학습외신청(멘토) 학습외 신청 및 취소
    path('MP0102M/mento/update/', MP0102M_mento_update, name='MP0102M_mento_update'),
    # 학습외신청(멘티) 학습외 신청 및 취소
    path('MP0102M/mentee/update/', MP0102M_mentee_update, name='MP0102M_mentee_update'),
    # 학습외신청(멘토) 보호자 승인 양식 detail set
    path('MP0102M/mento/report/', MP0102M_mento_report.as_view(), name='MP0102M_mento_report'),   
    # 학습외신청(멘토) 취소사유 콤보
    path('MP0102M/mento/combo/cncl/', MP0102M_mento_cncl.as_view(), name='MP0102M_mento_cncl'),   
    ########################################################################################
    # 학습외신청(멘토) 리스트(MP0102M - END )
    #
    ########################################################################################

    ########################################################################################
    # 프로그램 수행계획서(MP0103M - START )
    #
    ########################################################################################
    # 프로그램 수행계획서 콤보
    path('MP0103M/v1/', MP0103M_v1.as_view(), name='MP0103M_v1'),
    # 프로그램 수행계획서 리스트
    path('MP0103M/list/', MP0103M_list.as_view(), name='MP0103M_list'),
    # 프로그램 수행계획서 상세
    path('MP0103M/detail/', MP0103M_Detail.as_view(), name='MP0103M_Detail'),
    # 프로그램 수행계획서 작성 폼 데이터
    path('MP0103M/detail/v2/', MP0103M_Detail_v2.as_view(), name='MP0103M_Detail_v2'),
    # 프로그램 수행계획서 -> 최초 작성 시 주차 수를 셋팅
    path('MP0103M/list/v1/', MP0103M_list_v1.as_view(), name='MP0103M_list_v1'),
    # 프로그램 수행계획서 Insert
    path('MP0103M/insert/', MP0103M_Insert, name='MP0103M_Insert'),
    # 프로그램 수행계획서 Update
    path('MP0103M/update/', MP0103M_Update, name='MP0103M_Update'),
    # 프로그램 수행계획서 승인요청
    path('MP0103M/approval/', MP0103M_Approval, name='MP0103M_Approval'),
    ########################################################################################
    # 프로그램 수행계획서(MP0103M - END )
    #
    ########################################################################################

    ########################################################################################
    # 출석관리 리스트(MP0104M - START )
    #
    ########################################################################################
    # 출석관리 리스트
    path('MP0104M/list/', MP0104M_list.as_view(), name='MP0104M_list'),
    # 출석관리 상세
    path('MP0104M/detail/', MP0104M_Detail.as_view(), name='MP0104M_Detail'),
    ########################################################################################
    # 출석관리 리스트(MP0104M - END )
    #
    ########################################################################################

    ########################################################################################
    # 출석 변경 소명(MP01041M - START )
    #
    ########################################################################################
    # 멘토 리스트
    path('MP01041M/mtr/', MP01041M_mtr.as_view(), name='MP01041M_mtr'),
    # 멘티 리스트 소명
    path('MP01041M/mte/req/', MP01041M_mte_req.as_view(), name='MP01041M_mte_req'),
    # 멘티 리스트 콤보 추가
    path('MP01041M/combo/mte/att/', MP01041M_combo_mte_att.as_view(), name='MP01041M_combo_mte_att'),
    # 멘티 리스트 추가 상세
    path('MP01041M/mte/att/', MP01041M_mte_att.as_view(), name='MP01041M_mte_att'),
    # 멘토에 따른 멘티 리스트
    path('MP01041M/mtr/mte/', MP01041M_mtr_mte.as_view(), name='MP01041M_mtr_mte'),
    # 프로그램 리스트 콤보 추가
    path('MP01041M/combo/mpgm/att/', MP01041M_combo_mpgm_att.as_view(), name='MP01041M_combo_mpgm_att'),
    # 출석 상세
    path('MP01041M/att/', MP01041M_att.as_view(), name='MP01041M_att'),
    # 출석 추가
    path('MP01041M/insert/', MP01041M_Insert, name='MP01041M_Insert'),
    # 출석 소명
    path('MP01041M/req/', MP01041M_req, name='MP01041M_req'),
    # 출석 수정
    path('MP01041M/upd/', MP01041M_upd, name='MP01041M_upd'),
    # insert 후 max att_no, req_no 가져오기
    path('MP01041M/att/max/', MP01041M_att_max.as_view(), name='MP01041M_att_max'),
    # 출석(소명) 파일 업로드
    path('MP01041M/upload/', MP01041M_upload, name='MP01041M_upload'),
    # 출석(수정) 파일 업로드
    path('MP01041M/upload/upd/', MP01041M_upload_upd, name='MP01041M_upload_upd'),
    # 학습외 출석 여부
    path('MP01041M/att/cnt/', MP01041M_att_cnt.as_view(), name='MP01041M_att_cnt'),
    # 학습외 보고서 추가
    path('MP01041M/att/insert/', MP01041M_att_insert, name='MP01041M_att_insert'),
    ########################################################################################
    # 출석 변경 소명(MP01041M - END )
    #
    ########################################################################################
    
    ########################################################################################
    # 보고서 현황(MP0105M - START )
    #
    ########################################################################################
    # 보고서 현황 리스트
    path('MP0105M/list/', MP0105M_list.as_view(), name='MP0105M_list'),   
    # 보고서 현황 상세
    path('MP0105M/detail/', MP0105M_detail.as_view(), name='MP0105M_detail'),   
    # 보고서 현황 상세
    path('MP0105M/detail/2/', MP0105M_detail_2.as_view(), name='MP0105M_detail_2'),   
    # 보고서 현황 콤보1
    path('MP0105M/combo/1/', MP0105M_combo_1.as_view(), name='MP0105M_combo_1'),   
    # 보고서 현황 save
    path('MP0105M/update/<int:pk>/', MP0105M_update, name='MP0105M_update'),
    # 보고서 멘토 정보 조회
    path('MP0105M/listMento/', MP0105M_listMento.as_view(), name='MP0105M_listMento'),   
    # 보고서 생성 버튼 조회 
    path('MP0105M/listBtn/', MP0105M_listBtn.as_view(), name='MP0105M_listBtn'),      
    # 보고서 생성
    path('MP0105M/rprtCrea/', MP0105M_insert, name='MP0105M_insert'),   
    # 보고서 Min, Max
    path('MP0105M/detail/min_max/', MP0105M_detail_min_max.as_view(), name='MP0105M_detail_min_max'),         
    ########################################################################################
    # 보고서 현황(MP0105M - END )
    #
    ########################################################################################

    ########################################################################################
    # 월별 활동비 (MP0106M - START )
    #
    ########################################################################################
    # 월별 활동비 리스트
    path('MP0106M/list/', MP0106M_list.as_view(), name='MP0106M_list'),   
    ########################################################################################
    # 월별 활동비 (MP0106M - END )
    #
    ########################################################################################

    ########################################################################################
    # 활동중단 사유서 (MP0107 - START )
    #
    ########################################################################################
    # 활동중단 사유서 리스트
    path('MP0107/list/', MP0107_list.as_view(), name='MP0107_list'),   
    # 활동중단 사유서 save
    path('MP0107/update/<int:pk>/', MP0107_update, name='MP0107_update'),    
    ########################################################################################
    # 활동중단 사유서 (MP0107 - END )
    #
    ########################################################################################

    ########################################################################################
    # 미완료 소명서 (MP0108 - START )
    #
    ########################################################################################
    # 미완료 소명서 리스트
    path('MP0108/list/', MP0108_list.as_view(), name='MP0108_list'),   
    # 미완료 소명서 save
    path('MP0108/update/<int:pk>/', MP0108_update, name='MP0108_update'),    
    ########################################################################################
    # 미완료 소명서 (MP0108 - END )
    #
    ######################################################################################## 

################################################################################################################################################################################
# 멘티
# 
################################################################################################################################################################################    


    ########################################################################################
    # 멘티의 프로그램 신청현황(TE0201 - START )
    #
    ########################################################################################
    # # 멘티의 프로그램 신청현황 리스트
    path('TE0201/list/', TE0201_list.as_view(), name='TE0201_list'),   
    # # 멘티의 프로그램 신청현황 상세
    path('TE0201/detail/', TE0201_detail.as_view(), name='TE0201_detail'),   
    ########################################################################################
    # 멘티의 프로그램 신청현황(TE0201 - END )
    #
    ########################################################################################

    ########################################################################################
    # 멘티출석확인(TE0202 - START )
    #
    ########################################################################################
    # # 멘티출석확인 멘티 리스트
    path('TE0202/list/', TE0202_list.as_view(), name='TE0202_list'),   
    # # 멘티출석확인 멘티에 따른 월별 멘토 리스트
    path('TE0202/detail/', TE0202_detail.as_view(), name='TE0202_detail'),   
    # # 멘티출석확인 멘토 출석 승인
    path('TE0202/approval/', TE0202_Approval, name='TE0202_Approval'),   
    ########################################################################################
    # 멘티출석확인(TE0202 - END )
    #
    ########################################################################################

    ########################################################################################
    # 만족도 조사(TE0203 - START )
    #
    ########################################################################################
    # # 프로그램 만족도 조사 리스트
    path('TE0203/list/v1/', TE0203_list_v1.as_view(), name='TE0203_list_v1'),   
    # # 유저에 따른 만족도 조사 질문
    path('TE0203/detail/', TE0203_detail.as_view(), name='TE0203_detail'),   
    ########################################################################################
    # # 프로그램 만족도 조사 제출
    path('TE0203/detail/insert/', TE0203_Insert, name='TE0203_Insert'),   
    ########################################################################################

    ########################################################################################
    # 프로그램 소감문 작성(TE0204 - START )
    #
    ########################################################################################
    # # 프로그램 소감문 리스트 
    path('TE0204/list/', TE0204_list.as_view(), name='TE0204_list'), 
    # #프로그램 소감문 save
    path('TE0204/update/<int:pk>/', TE0204_update, name='TE0204_update'),        
    ########################################################################################
    # 프로그램 소감문 작성(TE0204 - END )
    #
    ########################################################################################

    ########################################################################################
    # 계획서 승인(TT0105 - START )
    #
    ########################################################################################
    # # 계획서 승인 리스트
    path('TT0105/list/', TT0105_list.as_view(), name='TT0105_list'),    
    # # 계획서 승인
    path('TT0105/approval/', TT0105_Approval, name='TT0105_Approval'),    
    # # 계획서 반려
    path('TT0105/back/', TT0105_Back, name='TT0105_Back'),   
    ########################################################################################
    # 계획서 승인(TT0105 - END )
    #
    ########################################################################################

    ########################################################################################
    # 보고서 관리(TT0107M - START )
    #
    ########################################################################################
    # # 보고서 관리 리스트
    path('TT0107M/list/', TT0107M_list.as_view(), name='TT0107M_list'),    
    # # 보고서 현황 save
    path('TT0107M/update/<int:pk>/', TT0107M_update, name='TT0107M_update'),    
    ########################################################################################
    # 보고서 관리(TT0107M - END )
    #
    ########################################################################################

    ########################################################################################
    # 멘티의 학습외 신청(MnteLrnO - START )
    #
    ########################################################################################
    # # 멘티의 학습외 신청현황 리스트
    path('MnteLrnO/list/', MnteLrnO_list.as_view(), name='MnteLrnO_list'),     
    # # 학습외 신청
    path('MnteLrnO/apply/', MnteLrnO_apply, name='MnteLrnO_apply'),    
    # # 학습외 신청취소
    path('MnteLrnO/applyCncl/', MnteLrnO_applyCncl, name='MnteLrnO_applyCncl'),                
    ########################################################################################
    # 멘티의 학습외 신청(MnteLrnO - END )
    #
    ########################################################################################

################################################################################################################################################################################
# 멘티
# 
################################################################################################################################################################################    

    
    ########################################################################################
    # view2 부분 (시작)
    #
    ########################################################################################
    #멘토스쿨 콤보박스
    path('msComboListView/', msComboListView.as_view(), name='msComboListView'),
    #멘토스쿨 콤보박스 Detail
    path('msComboListViewDetail/', msComboListViewDetail.as_view(), name='comboMpmgListViewDetail'),
       #환산
    path('msFn1/', msFn1, name='msFn1'),
    #사정
    path('msFn2/', msFn2, name='msFn2'),
    #엑셀
    path('msFn3/', msFn3, name='msFn3'),    
    #면접
    path('msFn4/', msFn4, name='msFn4'),
    #합격자업로드
    path('msFn6/', msFn6, name='msFn6'),
    #합격자업로드_전송
    path('msFn6_Submit/', msFn6_Submit, name='msFn6_Submit'),
    #합격자업로드_전송
    path('msFn6_Submit2/', msFn6_Submit2, name='msFn6_Submit2'),

    #합격자업로드
    path('msFn7/', msFn7, name='msFn7'),
    #최종합격자업로드_전송
    path('msFn7_Submit/', msFn7_Submit, name='msFn7_Submit'),
    #최종합격자업로드_전송
    path('msFn7_Submit2/', msFn7_Submit2, name='msFn7_Submit2'),

    #멘토스쿨 팝업1
    path('msPop1/', msPop1, name='msPop1'),    
    #멘토스쿨 핍압1_조회1
    path('msPop1_Det1/', msPop1_Det1.as_view(), name='msPop1_Det1'), 
    #멘토스쿨 핍압1_조회2
    path('msPop1_Det2/', mpPop1_Det2, name='msPop1_Det2'), 

    #멘토스쿨 핍압1_조회3_채점자 교수 조회
    path('msPop1_Det3/', msPop1_Det3.as_view(), name='msPop1_Det3'), 
    #멘토스쿨 핍압1_조회4_채점문항 
    path('msPop1_Det4/', msPop1_Det4.as_view(), name='msPop1_Det4'), 
    #멘토스쿨 핍압1_조회5_답변
    path('msPop1_Det5/', msPop1_Det5.as_view(), name='msPop1_Det5'), 
    #멘토스쿨 핍압1_조회5_답변_저장
    path('msPop1_Det5_Save/', msPop1_Det5_Save, name='msPop1_Det5_Save'), 
    #멘토스쿨 리포트 조회
    path('msFn8/', msFn8, name='msFn8'), 
	



    #멘토스쿨 환산표
    #path('msFn1/', msFn1, name='msFn1'),

    #멘토링 콤보박스
    path('mpComboListView/', mpComboListView.as_view(), name='mpComboListView'),
    #멘토링 콤보박스 Detail
    path('mpComboListViewDetail/', mpComboListViewDetail.as_view(), name='mpComboListViewDetail'),
    #환산
    path('mpFn1/', mpFn1, name='mpFn1'),
    #사정
    path('mpFn2/', mpFn2, name='mpFn2'),
    #엑셀
    path('mpFn3/', mpFn3, name='mpFn3'),    
    #면접
    path('mpFn4/', mpFn4, name='mpFn4'),
    #합격자업로드
    path('mpFn6/', mpFn6, name='mpFn6'), 
    #합격자업로드_전송
    path('mpFn6_Submit/', mpFn6_Submit, name='mpFn6_Submit'),
    #합격자업로드_전송
    path('mpFn6_Submit2/', mpFn6_Submit2, name='mpFn6_Submit2'),

	#

    #합격자업로드
    path('mpFn7/', mpFn7, name='mpFn7'),


    #멘토링 리포트 조회 페이지 이동
    path('mpFn8/', mpFn8, name='mpFn8'), 

    #멘토링 리포트 조회 페이지 이동
    path('mpFn8_2/', mpFn8_2, name='mpFn8_2'), 

    #멘토링 리포트 조회 상세 리스트
    path('mpFn8_Det1/', mpFn8_Det1.as_view(), name='mpFn8_Det1'), 

    #멘토링 리포트 조회 상세 리스트(서류채점자)
    path('mpFn8_Det2/', mpFn8_Det2.as_view(), name='mpFn8_Det2'), 

    #MP_MTR 학번으로 보기 (조교)
    path('mpFn8_Det3/', mpFn8_Det3.as_view(), name='mpFn8_Det3'), 

    #멘토링 리포트 조교
    path('mpFn8_assist/', mpFn8_assist, name='mpFn8_assist'), 
    #학과장 승인
    path('mpFn8_assist_confirm/', mpFn8_assist_confirm, name='mpFn8_assist_confirm'), 

    #학과장 일괄승인
    path('mpFn8_assist_confirm_all/', mpFn8_assist_confirm_all, name='mpFn8_assist_confirm_all'), 

    #학과장 반려
    path('mpFn8_assist_cancle/', mpFn8_assist_cancle, name='mpFn8_assist_cancle'), 


    #면접 관리자 코멘트
    path('mpFn8_gabu/', mpFn8_gabu, name='mpFn8_gabu'), 

    #면접 가부
    path('mpFn8_gabu2/', mpFn8_gabu2, name='mpFn8_gabu2'), 
    
    

    
    
    #지원서 점수 업로드
    path('mpFn9/', mpFn9, name='mpFn9'),

    #지원서 점수 업로드
    path('mpFn9_Submit/', mpFn9_Submit, name='mpFn9_Submit'),

    #가산점 점수 업로드
    path('mpFn10/', mpFn10, name='mpFn10'),

    #지원서 점수 업로드
    path('mpFn10_Submit/', mpFn10_Submit, name='mpFn10_Submit'),


    #최종합격자업로드_전송
    #path('msFn7_Submit/', msFn7_Submit, name='msFn7_Submit'),
    #최종합격자업로드_전송
    #path('msFn7_Submit2/', msFn7_Submit2, name='msFn7_Submit2'),

    #멘토링 팝업1
    path('mpPop1/', mpPop1, name='mpPop1'),    
    #멘토랑핍압1_조회1
    path('mpPop1_Det1/', mpPop1_Det1.as_view(), name='mpPop1_Det1'), 
    #멘토랑핍압1_조회2   
    path('mpPop1_Det2/', mpPop1_Det2, name='mpPop1_Det2'), 
    #멘토랑 핍압1_조회3_채점자 교수 조회
    path('mpPop1_Det3/', mpPop1_Det3.as_view(), name='mpPop1_Det3'), 
    #멘토랑 핍압1_조회4_채점문항 
    path('mpPop1_Det4/', mpPop1_Det4.as_view(), name='mpPop1_Det4'), 
    #멘토랑 핍압1_조회5_답변
    path('mpPop1_Det5/', mpPop1_Det5.as_view(), name='mpPop1_Det5'), 
    #멘토랑 핍압1_조회5_답변_저장 
    path('mpPop1_Det5_Save/', mpPop1_Det5_Save, name='mpPop1_Det5_Save'), 
 

    #SMS 팝업
    path('sms/', sms, name='sms'), 
    path('sms_result/', sms_result, name='sms_result'), 



    #학교 시스템으로 sms을 send 해준다
    path('sms_send/', sms_send, name='sms_send'), 


    #조교, 학과장한테 SMS를 보낸다.
    path('sms_send_assist/', sms_send_assist, name='sms_send_assist'), 


	#리턴URLTest
    path('returnsso/', returnsso, name='returnsso'), 



	#개인정보리턴
    path('agree_cont1/', agree_cont1.as_view(), name='agree_cont1'), 



	#멘토스쿨공통코드학년가져오기
    path('ms_com_cd1/', ms_com_cd1.as_view(), name='ms_com_cd1'), 

	#멘토스쿨공통코드학년저장하기
    path('ms_com_save1/', ms_com_save1, name='ms_com_save1'), 

	#멘토스쿨공통코드학점평균저장하기
    path('ms_com_save2/', ms_com_save2, name='ms_com_save2'),     


    #멘토링프로그램공통코드학년가져오기
    path('mp_com_cd1/', mp_com_cd1.as_view(), name='mp_com_cd1'), 

	#멘토링프로그램공통코드학년저장하기
    path('mp_com_save1/', mp_com_save1, name='mp_com_save1'),





	#관리자로그인
    path('admint/', ms_com_cd1.as_view(), name='ms_com_cd1'), 


 
	#파일업로드
    path('upload/', upload, name='upload'), 

	#공지사항
    path('bbs1/', bbs1.as_view(), name='bbs1'), 


	#공통코드 이름 가져오기
    path('comcode/', comcode.as_view(), name='comcode'), 

	###모바일
	#멘토링 프로그램 List

    ########################################################################################
    # view2 부분 (종료)
    #
    ########################################################################################



    ########################################################################################
    # 강주원 (시작)
    #
    ########################################################################################

    # 강주원 작업 시작

    # 교사용 멘토링 프로그램 리스트
    path('MP0101M/teacher/list/', TeacherMP0101MList.as_view(), name='MP0101M_list_teacher'),
    # 부모용 멘토링 프로그램 리스트
    path('MP0101M/guardian/list/', GuardianMP0101MList.as_view(), name='MP0101M_list_guardian'),
    # 멘토링 프로그램 상세 조회
    path('MP0101M/mpgms/detail/', MPAttView.as_view(), name='MP0101M_detail'),

    # 질문문항 세트 수정
    path('MP0101M/questions/', MoveQuestionView.as_view(), name='MoveQuestion'),
    path('users/login/', UserLoginView.as_view(), name='UserLogin'),
    
    # 난수 API
    path('RANDOM/number/', RandomViewSet.as_view(), name='Random'),
    #강주원 작업 종료







]
