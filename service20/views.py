from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *
from service20.models import *
from polls.models import Choice, Question
from django.db.models import Max


from collections  import OrderedDict
import json
# api/moim 으로 get하면 이 listview로 연결

class Service20ListSerializer(serializers.ModelSerializer):



    status = serializers.SerializerMethodField()
    class Meta:
        model = msch
        fields = ('ms_id', 'ms_name','yr','yr_seq','sup_org','img_src','ins_dt','ins_id','apl_term','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt','tot_apl','cnt_apl','status')


    def get_status(self,obj):
        now = datetime.datetime.today()
        if obj.apl_fr_dt == None:
            return '개설중'
        elif now < obj.apl_fr_dt:
            return '개설중'
        elif obj.apl_fr_dt <= now < obj.apl_to_dt:
            return '모집중'
        elif now > obj.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'
    get_status.short_description = '상태'        

class Service20ListView(generics.ListAPIView):



    queryset = msch.objects.all()
    serializer_class = Service20ListSerializer

    def list(self, request):
        l_yr = request.GET.get('yr', None)
        l_trn_term = request.GET.get('trn_term', None)

        print(l_yr)
        print(l_trn_term)

        queryset = self.get_queryset()
        if l_yr != '':
            print(l_yr)
            queryset = queryset.filter(yr=l_yr)

        if l_trn_term != '':
            print(l_trn_term)
            queryset = queryset.filter(trn_term=l_trn_term)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


def stdApplyStdView(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'stdApply/submit.html', context)


def Service20_01_View(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'service20/Service20_01.html', context)    



@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id_id=ms_ida).exists()
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vm_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vm_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(ms_id=ms_ida)
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
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
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
                    'ms_id' : rows3.ms_id,
                    'ms_name' : rows3.ms_name,
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


class post_user_info_Quest_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','use_indc')


class post_user_info_Quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = post_user_info_Quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None)           
        l_exist = ms_sub.objects.filter(ms_id_id=key1).exists()
        
        queryset = self.get_queryset()
        if not l_exist:
            queryset = queryset.filter(std_grp_code='')
        else:
            l_key1 = ms_sub.objects.filter(ms_id_id=key1)[0].att_cdh
            l_key_query = ms_sub.objects.filter(ms_id_id=key1).values_list('att_cdd_id', flat=True) 
            #ms_sub 테이블에서 질문내역 조회
            
            if not l_key_query:
                queryset = queryset.filter(std_grp_code=l_key1, std_detl_code__in=l_key_query)
            else:
                queryset = queryset.filter(std_grp_code=l_key1)
            #조회한 질문내역 기준으로 공통코드 조회

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 질문유형 가져오기
class post_user_info_persion_Quest_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','use_indc')


# 멘토링 프로그램 질문유형 가져오기
class post_user_info_persion_Quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = post_user_info_persion_Quest_Serializer
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None)           
        l_exist = mp_sub.objects.filter(ms_id=key1).exists()
        
        queryset = self.get_queryset()
        if not l_exist:
            queryset = queryset.filter(std_grp_code='')
        else:
            l_key1 = mp_sub.objects.filter(ms_id=key1)[0].att_cdh
            l_key_query = mp_sub.objects.filter(ms_id=key1).values_list('att_cdd', flat=True) 
            #mp_sub 테이블에서 질문내역 조회
            
            if not l_key_query:
                queryset = queryset.filter(std_grp_code=l_key1, std_detl_code__in=l_key_query)
            else:
                queryset = queryset.filter(std_grp_code=l_key1)
            #조회한 질문내역 기준으로 공통코드 조회

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


@csrf_exempt
def post_user_info_persion(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id_id=ms_ida).exists()
    #mp_mtr
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vm_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vm_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(ms_id=ms_ida)
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
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
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
                    'ms_id' : rows3.ms_id,
                    'ms_name' : rows3.ms_name,
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def post_msApply(request):
    ida = request.POST.get('memberNo', None)
    programId = request.POST.get('programID', None)
    que1 = request.POST.get('que1', None)
    que2 = request.POST.get('que2', None)
    que3 = request.POST.get('que3', None)
    que4 = request.POST.get('que4', None)
    que5 = request.POST.get('que5', None)

    ms_ida = request.POST.get('ms_id', None)
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id_id = programId
    ms_apl_max = ms_apl.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
    #ms_apl_max = ms_apl.objects.all().last()
    #ms_apl_max = ms_apl_max + 1
    apl_no = ms_apl_max
    apl_id = ida
    apl_no = ms_apl_max['vlMax']
    apl_no = apl_no + 1;
    
    print("11")
    model_instance = ms_apl(
        ms_id_id=ms_id_id, 
        apl_no=apl_no, 
        apl_id=apl_id,
        apl_nm=rows.apl_nm,
        unv_cd=rows.univ_cd,
        unv_nm=rows.univ_nm,
        cllg_cd=rows.cllg_cd,
        cllg_nm=rows.cllg_nm,
        dept_cd=rows.dept_cd,
        dept_nm=rows.dept_nm,
        brth_dt=rows.brth_dt,
        gen=rows.gen_cd,
        yr=rows.yr,
        term_div=rows.term_div,
        sch_yr=rows.sch_yr,
        mob_no=rows.mob_nm,
        tel_no=rows.tel_no,
        tel_no_g=rows.tel_no_g,
        h_addr=rows.h_addr
        )
    model_instance.save()
    
    for i in range(0,5):
        if i==0:
            anst2 = que1
        if i==1:
            anst2 = que2
        if i==2:
            anst2 = que3
        if i==3:
            anst2 = que4
        if i==4:
            anst2 = que5

        print("33")

        model_instance2 = ms_ans(
            ms_id=ms_id_id, 
            test_div='10', 
            apl_no=apl_no,
            ques_no=i+1,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            sort_seq =i+1,
            ans_t2=anst2
            )
        model_instance2.save()
        print("44cc")
    context = {'message': 'Ok'}

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})





class mpmgListSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','img_src','testField')

    def get_testField(self, obj):
        return 'test'     


class mpmgListView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpmgListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)





class mpmgListPersonSerializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','img_src','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt','cnt_trn','status')

    def get_applyFlag(self, obj):
        return 'Y'     
    def get_applyStatus(self, obj):
        return '미지원'  

    def get_status(self,obj):
        now = datetime.datetime.today()
        if obj.apl_fr_dt == None:
            return '개설중'
        elif now < obj.apl_fr_dt:
            return '개설중'
        elif obj.apl_fr_dt <= now < obj.apl_to_dt:
            return '모집중'
        elif now > obj.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'
    get_status.short_description = '상태'     



class mpmgListPersionView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpmgListPersonSerializer

    def list(self, request):
        l_yr = request.GET.get('yr', None)
        l_apl_term = request.GET.get('apl_term', None)

        queryset = self.get_queryset()

        if l_yr != '':
            print(l_yr)
            queryset = queryset.filter(yr=l_yr)

        if l_apl_term != '':
            print(l_apl_term)
            queryset = queryset.filter(apl_term=l_apl_term)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)



#멘토스쿨 콤보박스
class comboMpmgListSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','ms_name')


class comboMpmgListView(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = comboMpmgListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#멘토스쿨 콤보박스Detail
class comboMpmgListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','ms_name')


class comboMpmgListViewDetail(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = comboMpmgListDetailSerializer

    def list(self, request):
        l_ms_id = request.GET.get('ms_id', None)
        print(l_ms_id)
        queryset = self.get_queryset()
        queryset = queryset.filter(ms_id=l_ms_id)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id_id=ms_ida).exists()
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vm_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vm_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(ms_id=ms_ida)
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
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
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
                    'ms_id' : rows3.ms_id,
                    'ms_name' : rows3.ms_name,
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})




#멘토링 질문 List######################################################################
@csrf_exempt
def post_mt_quest(request):
    l_ms_id = request.GET.get('ms_id', None)
    r_mp_sub = mp_sub.objects.filter(ms_id=l_ms_id)
    r_mp_sub = r_mp_sub.filter(use_yn='Y')

    response_json = OrderedDict()

    res = []
    for val in r_mp_sub:
        print("1234")
        key1 = val.att_id
        key2 = val.att_cdd
        r_com_cdd = com_cdd.objects.filter(std_grp_code=key1,std_detl_code=key2)

    print("a")
    print(json.dumps(res))

    context = {'message': 'Ok'}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
####################################################################################


