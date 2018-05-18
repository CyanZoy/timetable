from django.shortcuts import HttpResponse
from api import ierror
from api.models import Appid
import time
from api.util import main
import json


def api(request):
    try:
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
            flag = main.equal_sign(sortlist, sign)
            if flag:
                print('验证通过')
                return HttpResponse('True')
            else:
                return HttpResponse(ierror.VERIFICATION_NOT_PASS)
    except Exception as e:
        print(e)
        return HttpResponse(ierror.VERIFICATION_NOT_PASS)

