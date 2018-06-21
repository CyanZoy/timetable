from django.shortcuts import HttpResponse
from api import ierror
from api.models import Appid
import time
from api.util.main import *
import json
from scheduler.view import main
from api.view.open import *


def api(request):
    # try:
        appid = request.GET.get('appid')
        userid = request.GET.get('userid')
        sign = request.GET.get('sign')
        doorid = request.GET.get('doorid')
        timestamp = request.GET.get('timestamp')
        print("GET:", appid, userid, doorid, timestamp, sign)
        if not appid:
            return HttpResponse(ierror.LACK_APPID)
        elif not sign:
            return HttpResponse(ierror.LACK_SIGN)
        elif not userid:
            return HttpResponse(ierror.LACK_USERID)
        elif not doorid:
            return HttpResponse(ierror.LACK_DOORID)
        elif not timestamp:
            return HttpResponse(ierror.LACK_TIMESTAMP)

        if int(time.time()) - int(timestamp) > 30:
            return HttpResponse(ierror.OVERDUE_TIME)

        # 根据appid获取appsecret
        client = Appid.objects.get(appid=appid)
        print('client=', client)
        if not client:
            return HttpResponse(ierror.WORNG_APPID)
        else:
            sortlist = [client.appsecret, timestamp, doorid, userid, appid]
            flag = equal_sign(sortlist, sign)
            if flag:
                a = can_open(num=userid, t=1, doorid=doorid)
                print(a)
                return HttpResponse('True')
            else:
                return HttpResponse(ierror.VERIFICATION_NOT_PASS)
    # except Exception as e:
    #     print(e)
    #     return HttpResponse(ierror.VERIFICATION_NOT_PASS)

