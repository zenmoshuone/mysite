from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.utils import timezone
import datetime
from django.db.models import Sum

# 总阅读数 与 当天阅读数
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):  # 获取cookie,看浏览器是否存在cookie，不存在阅读次数加一
        # 总阅读数 +1  #get_or_create,如果为空，则从新创建一个，返回一个元祖
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 +1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

# 获取前7天的阅读次数
def get_seven_days_read_data(content_type):
    today = timezone.now().date()  #获取今天的数据
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(
            read_num_sum=Sum('read_num'))  # aggregate聚合  Sum求和 得到所有的阅读次数{'read_num_sum':?}键值对
        read_nums.append(result['read_num_sum'] or 0)  # 如果前面那个为False就取0
    return dates, read_nums

def get_today_hot_data(content_type):#获取今天的热门数据，获取前7条
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]

def get_yesterday_hot_data(content_type): #获取昨天的热门数据，获取前7条
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]