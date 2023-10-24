from django.db import models
import uuid, datetime

# 用户类
from django.db.models.signals import post_save
from django.dispatch import receiver

class Student(models.Model):
    STATUS_CHOICE = (
        (0, "待审核"),
        (1, "已通过"),
        (-1, "被驳回"),
        (2, "未准备")
    )
    # 账号信息
    uuid = models.UUIDField("UUID", default=uuid.uuid4, primary_key=True)
    # oUCRZ49Jty8WKNmvh3xlfuFHbL3M, 28位的唯一id
    openid = models.CharField("微信id", max_length=28, unique=True, default=None, null=True, blank=True)
    id_card = models.CharField("身份证号", max_length=18, null=True)
    student_number = models.CharField("学号", max_length=12, unique=True)
    name = models.CharField("姓名", max_length=50)
    have_info = models.BooleanField("是否有信息", default=False)
    have_report_info = models.BooleanField("是否有报道信息", default=False)
    check_in = models.BooleanField("报道情况", default=False)
    check_in_time = models.DateTimeField("报道时间", default=datetime.datetime.now)
    status = models.IntegerField("审核状态", default=2, choices=STATUS_CHOICE)
    send_info = models.TextField("发送数据", default='')

    def __str__(self):
        return f'{self.uuid}'

# 图片类
class Image(models.Model):
    UPLOAD_TO = 'static/new/'
    DEFAULT = 'static/none.jpg'
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    hs = models.ImageField("核酸检测结果", upload_to=UPLOAD_TO+'hs', default=DEFAULT, blank=True)
    health_code = models.ImageField("健康码", upload_to=UPLOAD_TO+'health_code', default=DEFAULT, blank=True)
    tour_code = models.ImageField("行程码", upload_to=UPLOAD_TO+'tour_code', default=DEFAULT, blank=True)
    photo = models.ImageField("本人照片", upload_to=UPLOAD_TO + 'photo', default=DEFAULT, blank=True)
    number = models.IntegerField("已经上传的照片数量", default=0)

@receiver(post_save, sender=Student)
def create_image(sender, instance=None, created=False, **kwargs):
    if created and instance:
        Image.objects.create(student=instance)

# 报道信息类
class ReportInfo(models.Model):
    # 报道相关
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    estimated_arrival_time = models.DateField("预计报道时间")
    whether_delay_report = models.BooleanField("是否推迟报道", default=False)
    delay_report_reason = models.TextField("延迟报道的原因", blank=True, null=True)
    transportation = models.CharField("交通工具", max_length=10)
    car_no = models.CharField("车次", max_length=100, null=True, blank=True)

    def to_dic(self):
        dic = {
            'estimated_arrival_time': self.estimated_arrival_time,
            'whether_delay_report': self.whether_delay_report,
            'delay_report_reason': self.delay_report_reason,
            'transportation': self.transportation,
            'car_no': self.car_no
        }
        return dic


# 信息类
class Info(models.Model):
    # 性别的选项
    SEX_CHOICE = (
        ("男", "男"),
        ("女", "女")
    )
    # 民族的选项
    ETHNIC_CHOICE = (
        ("汉族","汉族"),
        ("蒙古族","蒙古族"),
        ("回族","回族"),
        ("藏族","藏族"),
        ("维吾尔族","维吾尔族"),
        ("苗族","苗族"),
        ("彝族","彝族"),
        ("壮族","壮族"),
        ("布依族","布依族"),
        ("朝鲜族","朝鲜族"),
        ("满族","满族"),
        ("侗族","侗族"),
        ("瑶族","瑶族"),
        ("白族","白族"),
        ("土家族","土家族"),
        ("哈尼族","哈尼族"),
        ("哈萨克族","哈萨克族"),
        ("傣族","傣族"),
        ("黎族","黎族"),
        ("傈僳族","傈僳族"),
        ("佤族","佤族"),
        ("畲族","畲族"),
        ("高山族","高山族"),
        ("拉祜族","拉祜族"),
        ("水族","水族"),
        ("东乡族","东乡族"),
        ("纳西族","纳西族"),
        ("景颇族","景颇族"),
        ("柯尔克孜族","柯尔克孜族"),
        ("土族","土族"),
        ("达斡尔族","达斡尔族"),
        ("仫佬族","仫佬族"),
        ("羌族","羌族"),
        ("布朗族","布朗族"),
        ("撒拉族","撒拉族"),
        ("毛南族","毛南族"),
        ("仡佬族","仡佬族"),
        ("锡伯族","锡伯族"),
        ("阿昌族","阿昌族"),
        ("普米族","普米族"),
        ("塔吉克族","塔吉克族"),
        ("怒族","怒族"),
        ("乌孜别克族","乌孜别克族"),
        ("俄罗斯族","俄罗斯族"),
        ("鄂温克族","鄂温克族"),
        ("德昂族","德昂族"),
        ("保安族","保安族"),
        ("裕固族","裕固族"),
        ("京族","京族"),
        ("塔塔尔族","塔塔尔族"),
        ("独龙族","独龙族"),
        ("鄂伦春族","鄂伦春族"),
        ("赫哲族","赫哲族"),
        ("门巴族","门巴族"),
        ("珞巴族","珞巴族"),
        ("基诺族","基诺族"),
        ("其他","其他"),
        ("外国血统","外国血统"),
    )
    # 政治面貌的选项
    ZZMM_CHOICE = (
        ("共青团员","共青团员"),
        ("群众","群众"),
    )

    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    id_card = models.CharField("身份证号", max_length=18)
    # 个人信息
    name = models.CharField("姓名", max_length=50)
    sex = models.CharField("性别", max_length=1, choices=SEX_CHOICE)
    ethnic = models.CharField("民族", max_length=10, choices=ETHNIC_CHOICE)
    the_religion = models.BooleanField("是否有宗教信仰", default=False)
    religion = models.CharField("宗教信仰", max_length=100, null=True, blank=True)
    '''
    生源地是指考生的来源地。
    对于以不同户籍多次参加过高考的考生来说，以最后一次参加高考时的户籍所在地为生源地。
    生源地以教育局的系统信息为准。从2016年起，以户籍所在地为生源地
    '''
    origin = models.CharField("生源地", max_length=100)
    postcode = models.CharField("邮政编码", max_length=6)
    phone_number = models.CharField("电话", max_length=11)
    political_landscape = models.CharField("政治面貌", max_length=6, choices=ZZMM_CHOICE)
    father_name = models.CharField("父亲姓名", max_length=50, null=True, blank=True)
    mother_name = models.CharField("母亲姓名", max_length=50, null=True, blank=True)
    father_phone = models.CharField("父亲电话", max_length=11, null=True, blank=True)
    mother_phone = models.CharField("母亲电话", max_length=11, null=True, blank=True)
    detailed_address = models.CharField("详细地址", max_length=100)
    '''
    “籍贯，本人出生时祖父的居住地，登记填至县级行政区划。不能确定祖父居住地的，随父亲籍贯；
    不能确定父亲籍贯的，登记本人的出生地。父亲是外国人或《出生医学证明》未记载父亲信息的，随母亲籍贯。
    弃婴等籍贯不详的，登记收养人籍贯或收养机构所在地的县级行政区划。
    经批准加入中华人民共和国国籍的外国人，登记入籍前所在国家的名称。”
    '''
    native_place = models.CharField("籍贯", max_length=100)
    household_address = models.CharField("户籍地址", max_length=100)
    qq = models.CharField("QQ号码", max_length=12)
    wechat = models.CharField("微信号", max_length=28, null=True, blank=True)

    # 大学信息
    student_number = models.CharField('学号', max_length=12)
    dormitory_id = models.CharField("宿舍id", max_length=20, blank=True, null=True)
    student_class = models.CharField("班级", max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.id_card}_{self.name}'
