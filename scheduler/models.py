from django.db import models
from utils.date_format import DateFormat


class tes(models.Model):
    isbn = models.CharField(max_length=255, null=True)
    book_name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'book'


class Dsj(models.Model):
    # DSJ_TS_DZJG
    TM = models.CharField('题名', max_length=400)
    ZRZ = models.CharField('责任者', max_length=400)
    ISBN = models.CharField('ISBN号', max_length=160, null=True)
    CBS = models.CharField('出版社', max_length=400, null=True)
    CBRQ = models.CharField('出版日期', max_length=40, null=True)
    JGRQ = models.CharField('荐购日期', max_length=10)
    DGZT = models.CharField('订购状态', max_length=1, null=True, help_text='订购状态 0未处理 1已订购 2不订购 3退订')
    HFZT = models.CharField('回复状态', max_length=1, null=True, help_text='回复状态 0未回复 1已回复')
    DCZT = models.CharField('典藏状态', max_length=1, null=True)
    CLSM = models.CharField('处理说明', max_length=4000, null=True)
    SFRZH = models.CharField('身份认证号(同证件号,学号/教工号)', max_length=20)
    JGID = models.CharField('荐购记录ID', max_length=90, primary_key=True)
    UPD = models.DateField('记录日期', null=True)

    class Meta:
        verbose_name = '预订图书'
        verbose_name_plural = '图书'
        db_table = 'DSJ_TS_DZJG'
        app_label = 'scheduler'


class Js(models.Model):
    """教学场地/教师课程表"""
    XN = models.CharField('学年', max_length=18)
    XQ = models.CharField('学期', max_length=40)
    JSBH = models.CharField('教室编号', max_length=10)
    XQJ = models.CharField('星期几', max_length=40)
    SJD = models.IntegerField('时间点', help_text='1表示第1节课开始,3表示第三节开始')
    DSZ = models.CharField('单双周', max_length=6)
    QSZ = models.IntegerField('起始周')
    JSZ = models.IntegerField('结束周')
    SKCD = models.IntegerField('上课长度', help_text='2表示2节,3表示3节')
    XKKH = models.CharField('选课课号', max_length=100)
    JSZGH = models.CharField('教师职工号', max_length=20)
    BZ = models.CharField('备注', max_length=400)
    PK = models.CharField('课表来源', max_length=4)
    GUID = models.CharField(max_length=50, primary_key=True)
    JSMC = models.CharField('教室名称', max_length=40)
    UPD = models.DateField('更新时间', max_length=7)
    KCZWMC = models.CharField('课程中文名', max_length=460)
    KCYWMC = models.CharField('课程英文名', max_length=460)

    def __str__(self):
        return self.JSZGH

    class Meta:
        verbose_name = '教学场地/教师表'
        verbose_name_plural = '教学场地/教师表'
        db_table = 'DSJ_JW_KB_JXCD_JS'
        app_label = 'scheduler'
        permissions = (
            ("is_teacher", "教师权限"),
        )


class Xs(models.Model):
    XN = models.CharField('学年', max_length=18)
    XQ = models.CharField('学期', max_length=40)
    # JSBH = models.CharField('教室编号', max_length=10)
    XH = models.CharField('学号', max_length=20)
    XKKH = models.CharField('选课课号', max_length=100)
    XQJ = models.CharField('星期几', max_length=40)
    DJJ = models.IntegerField('第几节')
    SKCD = models.IntegerField('上课长度', help_text='2表示2节,3表示3节')
    DSZ = models.CharField('单双周', max_length=6)
    QSZ = models.IntegerField('起始周')
    JSZ = models.IntegerField('结束周')
    KCB = models.CharField('课程表', max_length=200, null=True)
    XKCS = models.CharField(max_length=50, null=True)
    XSF = models.CharField('选上否', max_length=1, null=True)
    GUID = models.CharField(max_length=50, primary_key=True)
    KCZWMC = models.CharField('课程中文名', max_length=460, null=True)
    KCYWMC = models.CharField('课程英文名', max_length=460, null=True)

    def __str__(self):
        return self.XH

    def kcm(self):
        if self.KCB:
            return self.KCB.split('<br>')[0]
        else:
            return None

    def jsmh(self):
        if self.KCB:
            return self.KCB.split('<br>')[3]
        else:
            return None

    class Meta:
        verbose_name = '学生课表'
        verbose_name_plural = verbose_name
        db_table = 'DSJ_JW_KB_XSKCB'
        app_label = 'scheduler'


class Rq(models.Model):
    """节假日表"""
    jq = [('0', '端午节'), ('1', '清明节'), ('2', '劳动节')]

    XN = models.CharField(max_length=10, verbose_name='学年', null=False, default=DateFormat().current_time_to_academic_xn())
    XQ = models.CharField(max_length=2, verbose_name='学期', null=False, default=DateFormat().current_time_to_academic_xq())
    N = models.IntegerField(verbose_name='年', null=False)
    Y = models.IntegerField(verbose_name='月', null=False)
    R = models.IntegerField(verbose_name='日', null=False)
    DJZ = models.IntegerField(verbose_name='第几周', null=False)
    XQJ = models.IntegerField(verbose_name='星期几', null=False)
    NYR = models.CharField(max_length=12, primary_key=True, verbose_name='年月日', null=False)
    SFDYC = models.CharField(max_length=1, verbose_name='是否第一次', null=True)
    ZC = models.IntegerField(verbose_name='', null=True)
    ZC1 = models.IntegerField(verbose_name='', null=True)
    DJZ1 = models.IntegerField(verbose_name='', null=True)
    JJMC = models.CharField(max_length=20, verbose_name='节假日名称', null=True)

    class Meta:
        verbose_name = '日期周次及节假日对应表'
        verbose_name_plural = verbose_name
        app_label = 'scheduler'
        db_table = 'DSJ_JW_KB_RQKSZB'


class Tt(models.Model):
    """调停课表"""
    BDLB = models.CharField(max_length=16, verbose_name='099变动类别')
    BDBH = models.CharField(max_length=30, verbose_name='099变动编号', primary_key=True)
    XKKH = models.CharField(max_length=40, verbose_name='099选课课号')
    YJSZGH = models.CharField(max_length=10, verbose_name='099原教师职工号')
    YQSZ = models.IntegerField(verbose_name='099原起始周')
    YJSZ = models.IntegerField(verbose_name='099原结束周')
    YXQJ = models.CharField(max_length=2, verbose_name='099原星期几')
    YSJD = models.CharField(max_length=2, verbose_name='099原时间段')
    YDSZ = models.CharField(max_length=4, verbose_name='099原单双周')
    YSKCD = models.CharField(max_length=2, verbose_name='099原上课长度')
    YJSBH = models.CharField(max_length=10, verbose_name='099原教室编号')
    XJSZGH = models.CharField(max_length=10, verbose_name='099现教师职工号')
    XQSZ = models.IntegerField(verbose_name='099现起始周')
    XJSZ = models.IntegerField(verbose_name='099现结束周')
    XXQJ = models.CharField(max_length=2, verbose_name='099现星期几')
    XSJD = models.CharField(max_length=2, verbose_name='099现时间段')
    XDSZ = models.CharField(max_length=4, verbose_name='099现单双周')
    XSKCD = models.CharField(max_length=2, verbose_name='099现上课长度')
    XJSBH = models.CharField(max_length=10, verbose_name='099现教室编号')
    JSSFYXBD = models.CharField(max_length=4, verbose_name='099允许变教室')
    JSLB = models.CharField(max_length=50, verbose_name='099教室类别')
    ZWS = models.CharField(max_length=4, verbose_name='099座位数')
    XQYQ = models.CharField(max_length=4, verbose_name='099校区要求')
    BDYY = models.CharField(max_length=160, verbose_name='099变动原因')
    SQSJ = models.CharField(max_length=20, verbose_name='099申请时间')
    SQR = models.CharField(max_length=20, verbose_name='099申请人')
    SHBJ = models.CharField(max_length=2, verbose_name='099审核标记')
    SHSJ = models.CharField(max_length=20, verbose_name='099审核时间')
    SHR = models.CharField(max_length=20, verbose_name='099审核人')
    JCJG = models.CharField(max_length=100, verbose_name='')
    QBQZZ = models.CharField(max_length=4, verbose_name='099标志')
    YYLB = models.CharField(max_length=80, verbose_name='')
    SFJLZHXS = models.CharField(max_length=2, verbose_name='099是否记录调停课总学时')
    XYSHBJ = models.CharField(max_length=8, verbose_name='099学院审核标记 ')
    XYSHSJ = models.CharField(max_length=20, verbose_name='099学院审核时间 ')
    XYSHR = models.CharField(max_length=20, verbose_name='099学院审核人 ')
    KC = models.CharField(max_length=4, verbose_name='')

    class Meta:
        verbose_name = '调停课信息表'
        verbose_name_plural = verbose_name
        app_label = 'scheduler'
        db_table = 'DSJ_JW_KB_TTKXXB'

    def __str__(self):
        return self.YJSZGH+','+self.XJSZGH+','+self.JSLB


class JsAccount(models.Model):
    ACCOUNT = models.CharField(max_length=255, primary_key=True)
    NAME = models.CharField(max_length=255)
    EMPLOYEETYPE = models.CharField(max_length=255)
    SEX = models.CharField(max_length=255)
    DEPARTMENT = models.CharField(max_length=255)
    COLLEGENAME = models.CharField(max_length=255)
    PRONAME = models.CharField(max_length=255)
    GRADENAME = models.CharField(max_length=255)
    CLASSNAME = models.CharField(max_length=255)
    DQZT = models.CharField(max_length=255)
    SYNCTIME = models.DateField()

    class Meta:
        verbose_name = '人员信息表'
        verbose_name_plural = verbose_name
        app_label = 'scheduler'
        db_table = 'USERINFO'


class GlobalKctj(models.Model):
    """此表为全校性调课，例如节假日统一调课"""
    Month = [(str(i), str(i)) for i in range(1, 13)]
    Day = [(str(i), str(i)) for i in range(1, 32)]
    Sjd_odd = [(str(i), str(i)) for i in range(1, 16, 2)]
    # Sjd_odd.append(('0', '请选择'))
    Sjd_even = [(str(i), str(i)) for i in range(2, 16, 2)]
    # Sjd_even.append(('0', '请选择'))

    ID = models.IntegerField(primary_key=True)
    XN = models.CharField(max_length=50, verbose_name='学年', default=DateFormat().current_time_to_academic_year())
    YDATE = models.DateField(verbose_name='原日期')
    XDATE = models.DateField(verbose_name='新日期')
    EXCEPTS = models.CharField(max_length=5, verbose_name='除去的课程起始点(请选择)',
                               choices=sorted(Sjd_odd, key=lambda k: int(k[0])), default='')
    EXCEPTE = models.CharField(max_length=5, verbose_name='除去的课程结束点(请选择)',
                               choices=sorted(Sjd_even, key=lambda k: int(k[0])), default='')
    EXCEPTTYPE = models.CharField(max_length=50, verbose_name='除去课程的类型')

    class Meta:
        verbose_name = '全局调课'
        verbose_name_plural = verbose_name
        app_label = 'scheduler'
        db_table = 'GLOBAL_SWITCH'
