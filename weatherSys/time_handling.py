from datetime import datetime
import time


# datetime转成字符串，
# strftime函数就是接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定
def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%d-%H-%M-%S")  # 字符串需要不需要"-"，自己定


# 字符串转成datetime
# strptime函数就是根据指定的格式把一个时间字符串解析为时间元组
def string_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H-%M-%S")  # 注意string的格式要和后面对应


# 把字符串转成时间戳形式
# mktime函数接收struct_time对象或者完整的九位元组元素作为参数，返回用秒数来表示时间的浮点数。
def string_to_timestamp(strTime):
    return time.mktime(string_to_datetime(strTime).timetuple())


# 把时间戳转成字符串形式
# strftime函数就是接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定
def timestamp_to_string(stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))


# 把datetime类型转外时间戳形式
# mktime函数接收struct_time对象或者完整的九位元组元素作为参数，返回用秒数来表示时间的浮点数。
def datetime_to_timestamp(dateTim):
    return time.mktime(dateTim.timetuple())

