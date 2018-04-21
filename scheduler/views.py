# utf-8
from django.shortcuts import (
    render, HttpResponse
)
from scheduler.models import *
import os
from django.template.response import TemplateResponse
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from scheduler.constants import *
from utils.request_url import divice_request_path
from utils.date_format import date_handler
from scheduler.view.main import ChangeList, Pagina
import json


class kkh(forms.Form):
    a = forms.CharField()


# @staff_member_required
def index(request):
    path_split = divice_request_path(request, defaut_div='/')
    p = {}
    for _ in path_split:
        if _:
            p[_] = URL_TO_NAME[_]
    contenxt = {'dashboard': 'active-menu', 'path': p.items()}
    return render(request, 'htmls/index.html', contenxt)


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
        sousuo=''
    example_length=request.GET.get('dataTables-example_length')

    if not example_length:
        example_length=15
    example_length=int(example_length)

    if not page:
        page = 1
    page = int(page)

    path_split = divice_request_path(request, defaut_div='/')
    p = {'index': '首页'}
    for _ in path_split:
        if len(_):
            p[_] = URL_TO_NAME[_]

    pag = None
    if sousuo:
        if u == '1':
            from django.db.models import Q
            pag = Pagina(Js, page, example_length, (Q(KCZWMC__contains=sousuo) | Q(JSZGH__contains=sousuo)),KCZWMC__isnull=False)
        if u=='2':
            from django.db.models import Q
            pag = Pagina(Xs, page, example_length, (Q(KCB__contains=sousuo) | Q(XH__contains=sousuo)), KCB__isnull=False)

    if not sousuo:
        if u == '1':
                pag = Pagina(Js, page, example_length, KCZWMC__isnull=False)
        elif u == '2':
                pag = Pagina(Xs, page, example_length, KCB__isnull=False)
        else:
                pag = Pagina(Js, page, example_length, KCZWMC__isnull=False)

    left_page = sorted(pag.left_page)
    right_page = sorted(pag.right_page)

    contenxt = {
        'u': u,
        'path': p.items(),
        'contacts': pag,
        'left_page': left_page,
        'current_page': page,
        'mid_page': sorted(pag.mid_page),
        'right_page': right_page,
        'sousuo':sousuo,
        'example_length':example_length

    }

    contenxt.update(extra_context)
    return render(request, 'htmls/table.html', contenxt)


@staff_member_required
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
        week = request.GET.get('week')
        num = request.GET.get('num')
        print(num)
        week = week.split(',')
        lis = defaultdict(list)
        lis['week_info'] = week
        if not week:
            week = '1'
        for w in week:
            chan = ChangeList(Js, 1000, JSZGH=str(num), KCZWMC__isnull=False, QSZ__lte=w, JSZ__gte=w)
            result = chan.get_result_by_range('XQJ', 'SJD')
            lis['week'] = w
            for i in result:
                # i['DSZ'] = i['DSZ'].replace('单', '1').replace('双', '2')
                lis[w].append(i)

        # b = json.dumps(lis, default=date_handler, ensure_ascii=False)
        # print(b)
        return HttpResponse(json.dumps(lis, default=date_handler, ensure_ascii=False))


from django.contrib.auth.decorators import permission_required


@permission_required('auth.add_user', login_url='/login/')
def Te(request):
    print(request.user.username)
    print(request.user.user_permissions.all())
    print(request.user.has_perm('auth.add_user'))
    # js = Js.objects.all()
    # paginator = Paginator(js, 5)
    # page = 3
    # contacts = paginator.get_page(page)
    # print(contacts)
    return HttpResponse("123")


def Te2(request):
    return HttpResponse('456')
