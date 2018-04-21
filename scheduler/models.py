
from django.db import models


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
    KCB = models.CharField('课程表',max_length=200)
    XKCS = models.CharField(max_length=50)
    XSF = models.CharField('选上否',max_length=1)
    GUID = models.CharField(max_length=50, primary_key=True)
    # JSMC = models.CharField('教室名称', max_length=40)
    KCZWMC = models.CharField('课程中文名', max_length=460)
    KCYWMC = models.CharField('课程英文名', max_length=460)

    def __str__(self):
        return self.XH

    def kcm(self):
        x=self.KCB
        b=self.KCB.index('<br>')
        z=x[:b]
        return z

    def jsmh(self):
        x=self.KCB

        xlist=x.split('<br>')

        return xlist[3]








    class Meta:
        verbose_name = '学生课表'
        verbose_name_plural =verbose_name
        db_table = 'DSJ_JW_KB_XSKCB'
        app_label = 'scheduler'