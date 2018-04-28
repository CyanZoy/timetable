# utf-8
from django.shortcuts import (
    render, HttpResponse
)
from scheduler.models import *
import os
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from scheduler.constants import *
from utils.request_url import divice_request_path
from utils.date_format import date_handler, DateFormat
from scheduler.view.main import ChangeList, Pagina
import json
from django.db.models import Q
from scheduler.constants import *


class kkh(forms.Form):
    a = forms.CharField()


@staff_member_required
def index(request):
    path_split = divice_request_path(request, defaut_div='/')
    p = {}
    for _ in path_split:
        if _:
            p[_] = URL_TO_NAME[_]
    contenxt = {'dashboard': 'active-menu', 'path': p.items()}
    return render(request, 'htmls/index.html', contenxt)


@staff_member_required
def table(request):
    user_agent = request.META['HTTP_USER_AGENT']
    extra_context = {}
    if len([k for k in ['iPhone', 'Android'] if k not in user_agent]) == len(['iPhone', 'Android']):
        extra_context['sitemap_ul'] = 'in'
        extra_context['sitemap'] = 'active-menu'

    # 判断教师u=1，学生u=2，教室u=3
    u = request.GET.get('u')
    # 获取传入页数
    page = request.GET.get('page')
    sousuo = request.GET.get('s')
    if not sousuo:
        sousuo = ''
    display_length = request.GET.get('display_length')

    display_length = 10 if not display_length else int(display_length) if int(display_length) <= 100 else 100

    page = int(page) if page else 1
    # path_split = divice_request_path(request, defaut_div='/')
    # p = {'index': '首页'}
    # for _ in path_split:
    #     if len(_):
    #         p[_] = URL_TO_NAME[_]

    pag = None
    if sousuo:
        if u == '1':
            pag = Pagina(Js, page, display_length, (Q(KCZWMC__contains=sousuo) | Q(JSZGH__contains=sousuo)), KCZWMC__isnull=False)
        if u == '2':
            pag = Pagina(Xs, page, display_length, (Q(KCB__contains=sousuo) | Q(XH__contains=sousuo)), KCB__isnull=False)

    if not sousuo:
        if u == '1':
                pag = Pagina(Js, page, display_length, KCZWMC__isnull=False)
        elif u == '2':
                pag = Pagina(Xs, page, display_length, KCB__isnull=False)
        else:
                pag = Pagina(Js, page, display_length, KCZWMC__isnull=False)

    left_page = sorted(pag.left_page)
    right_page = sorted(pag.right_page)

    contenxt = {
        'u': u,
        # 'path': p.items(),
        'contacts': pag,
        'current_page': page,
        'left_page': left_page,
        'mid_page': sorted(pag.mid_page),
        'right_page': right_page,
        'sousuo': sousuo,
        'length': display_length,
        'select': [10, 25, 50, 100],
    }

    contenxt.update(extra_context)
    return render(request, 'htmls/table.html', contenxt)


@staff_member_required
@permission_required('scheduler.is_teacher', login_url='/login/')
def specific(request):
    user_agent = request.META['HTTP_USER_AGENT']
    extra_context = {}
    if len([k for k in ['iPhone', 'Android'] if k not in user_agent]) == len(['iPhone', 'Android']):
        extra_context['search'] = 'active-menu'
    path_split = divice_request_path(request, defaut_div='/')
    p = {'index': '首页'}
    for _ in path_split:
        if len(_):
            p[_] = URL_TO_NAME[_]

    if not request.is_ajax():
        contenxt = {
            'path': p.items(),
        }
        contenxt.update(extra_context)
        return render(request, 'htmls/specific.html', contenxt)
    else:
        from collections import defaultdict
        import time
        start_time = time.time()
        week = request.GET.get('week')
        # 编号
        num = request.GET.get('num')
        if not num:
            return HttpResponse('false')
        lis = defaultdict(list)
        current_week = Rq.objects.get(NYR=DateFormat().current_time_n_y_r()).DJZ
        lis['current_week'] = current_week
        if not week:
            week = [w for w in range(current_week, current_week+3) if w <= ChangeList.get_field_count(Rq, 'DJZ').DJZ]
        else:
            week = [int(w) for w in week.split(',')]
        lis['week_info'] = week

        # import numpy as np
        # sign = np.zeros(shape=(12, 8), dtype=bool)
        # 当前学年
        year_mon = DateFormat().current_time_to_academic_year()

        result = Js.objects.filter(Q(QSZ__lte=min(week)) | Q(JSZ__gte=max(week)), JSZGH=str(num), KCZWMC__isnull=False,
                                   ).order_by('XQJ', 'SJD').values('QSZ', 'JSZ', 'SJD', 'XQJ', 'SKCD', 'DSZ', 'JSMC',
                                                                   'KCZWMC')
        # 以下查询新添课程包括补课，调课，换教师，过滤条件为学年，教师工号或姓名，周次
        extract = Tt.objects.filter(Q(XQSZ__gte=min(week)) | Q(XJSZ__lte=max(week)), XJSZGH=str(num),
                                    XKKH__contains=year_mon,).values()

        # 以下查询休课课程，休课课程包括调课，换教师，停课，过滤条件为学年，教师工号或姓名，周次
        extract_s = Tt.objects.filter(Q(YQSZ__gte=min(week)) | Q(YJSZ__lte=max(week)), YJSZGH=str(num),
                                      XKKH__contains=year_mon,).values()
        # print(extract_s)
        for i in result:
            for w in week:
                if w in range(i['QSZ'], i['JSZ'] + 1):
                    lis[w].append(i)

        # 存放选课名称大小50
        from collections import deque
        temporary_class = {}

        # 以下处理课程调换，节假日
        for w in week:
            if extract:
                for _ in extract:
                    if _['BDLB'] in ['调课', '补课', '换教师'] and w in range(int(_['XQSZ']), int(_['XJSZ'])+1):
                        # 如果有新时间点则采用新时间点否则采用原时间点
                        ysjd = _['XSJD'] if _['XSJD'] else _['YSJD'] if _['YSJD'] else 0
                        # 判断新增课程是否与已有课程冲突
                        # and not sign[int(ysjd), int(_['XXQJ'])]
                        if ysjd:
                            xkkh = _['XKKH'].split('-')[3]
                            if xkkh not in temporary_class:
                                a = Js.objects.filter(XKKH__contains=xkkh,
                                                                          KCZWMC__isnull=False).values('KCZWMC').distinct()
                                if a:
                                    temporary_class[xkkh] = a[0]['KCZWMC']
                            new_class = {'SJD': int(ysjd), 'XQJ': _['XXQJ'],

                                         'SKCD': int(_['XSKCD']) if _['XSKCD'] else int(_['YSKCD']),
                                         'DSZ': '', 'JSMC': '待完善', 'KCZWMC': temporary_class[xkkh],
                                         'class_code': CLASS_CODE[_['BDLB']]}
                            lis[w].append(new_class)

            if extract_s:
                for j in extract_s:
                    if j['BDLB'] in ['调课', '停课', '换教师'] and w in range(int(j['YQSZ']), int(j['YJSZ'])+1):
                        stop_class = {'SJD': j['YSJD'], 'XQJ': j['YXQJ'], 'SKCD': 0, 'class_code': 'V002'}
                        lis[w].append(stop_class)

            # 处理节假日
            rq = Rq.objects.filter(DJZ=w, JJMC__isnull=False)
            if rq:
                for j in rq:
                    lis[w].append({'SJD': 1, 'XQJ': j.XQJ, 'SKCD': 13, 'DSZ': '单', 'JSMC': j.JJMC + '',
                                   'KCZWMC': j.JJMC})

        print('处理完成用时', time.time()-start_time)

        # b = json.dumps(lis, default=date_handler, ensure_ascii=False)
        # print(b)
        return HttpResponse(json.dumps(lis, default=date_handler, ensure_ascii=False))


@permission_required('scheduler.is_teacher', login_url='/login/')
def Te(request):
    print(request.user.username)
    print(request.user.user_permissions.all())
    print(request.user.has_perm('scheduler.is_teacher'))
    # js = Js.objects.all()
    # paginator = Paginator(js, 5)
    # page = 3
    # contacts = paginator.get_page(page)
    # print(contacts)
    return HttpResponse("123")


def Te2(request):
    return HttpResponse('456')

