def byteLengthToHumanReadable(bytes: int):
    """将字节长度转化为人类可读的形式，返回一个元组`(数量，单位)`"""
    if bytes >= 1024 * 1024 * 1024:
        number = round(bytes / 1024 / 1024 / 1024, 2)
        unit = "GB"
    elif bytes >= 1024 * 1024:
        number = round(bytes / 1024 / 1024, 2)
        unit = "MB"
    elif bytes >= 1024:
        number = round(bytes / 1024, 2)
        unit = "KB"
    else:
        number = bytes
        unit = "B"
    return number, unit
