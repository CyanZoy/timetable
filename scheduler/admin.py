from django.contrib import admin
from scheduler.models import *
from django.utils.html import format_html
from django.core.paginator import Paginator
from scheduler.constants import *

admin.site.site_header = "课表管理"
admin.site.index_title = "站点管理"
admin.site.site_title = '管理'


@admin.register(Dsj)
class DsjAdmin(admin.ModelAdmin):
    list_display = ('TM', 'ZRZ', 'ISBN', 'CBS', 'CBRQ', 'JGRQ', 'dgzt', 'hfzt', 'DCZT', 'CLSM', 'SFRZH', 'JGID', 'UPD')
    search_fields = ('ISBN',)
    # list_filter = ('TM', )
    list_per_page = 10
    readonly_fields = ('TM', )
    # view_on_site = True

    def hfzt(self, obj):
        if obj.HFZT == '0':
            return format_html("<span style='color:red'>未回复</span>")
        return format_html("<span style='color:blue'>已回复</span>")
    hfzt.short_description = '回复状态'

    def dgzt(self, obj):
        return format_html("<span style='color:{0}'>{1}</span>".format(DSJ_TS_DZJG_DGZT_COLOR[obj.DGZT],
                                                                       DSJ_TS_DZJG_DGZT[obj.DGZT]))
    dgzt.short_description = '订购状态'


@admin.register(Js)
class JsAdmin(admin.ModelAdmin):
    list_display = ('XN', 'XQ', 'JSBH', 'XQJ', 'SJD', 'DSZ', 'QSZ', 'JSZ', 'SKCD',
                    'XKKH', 'JSZGH', 'BZ', 'JSMC', 'UPD', 'KCZWMC', 'KCYWMC')
    exclude = ('GUID',)

