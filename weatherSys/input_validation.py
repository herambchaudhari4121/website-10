


def longitude_latitude_validation(longitude, latitude):
    message = '设备添加成功'
    try:
        if float(latitude) > 90 or float(longitude) > 180:
            message = '请输入合法经纬度数值！'
            return False, message
    except:
        message = '经纬度为数字！'
        return False, message
    return True, message
