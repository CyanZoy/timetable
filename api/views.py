from django.shortcuts import render

# api


def api(request):
    appid = request.GET.get('appid')
    # 根据appid获取appsecret

