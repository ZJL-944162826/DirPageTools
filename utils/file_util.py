import os
from do.file_info import FileInfo
from do.dir_info import DirInfo
from common.type_list import TYPE_LIST
import struct

FILE_ID_TEMP = 0
IMAGE_TYPE = [".gif", ".png", ".jpg"]


def get_file_info(dir_info: DirInfo, path):
    print("-- file: " + path)
    suffix = os.path.splitext(path)[1]
    print("-- file-suffix: " + suffix)
    if suffix in IMAGE_TYPE:
        file_info = read_image(dir_info, path)
    else:
        file_info = None
    return file_info


def read_image(dir_info: DirInfo, path):
    global FILE_ID_TEMP
    FILE_ID_TEMP += 1
    info = os.stat(path)
    dir_url, file_name = os.path.split(path)
    image_info = FileInfo(
        FILE_ID_TEMP,
        file_name,
        dir_url,
        info.st_size,
        get_file_type(path),
        1,
        dir_info.dir_id
    )
    return image_info


# 字节码转16进制字符串
def get_bytes_2_hex(byte):
    num = len(byte)
    hex_str = u""
    for i in range(num):
        t = u"%x" % byte[i]
        if len(t) % 2:
            hex_str += u"0"
        hex_str += t
    return hex_str.upper()


# 获取文件类型
def get_file_type(file_name):
    # 必需二制字读取
    bin_file = open(file_name, 'rb')
    f_type = 'unknown'
    for h_code in TYPE_LIST.keys():
        # 需要读多少字节
        num_of_bytes = int(len(h_code) / 2)
        # 每次读取都要回到文件头，不然会一直往后读取
        bin_file.seek(0)
        # 一个 "B"表示一个字节
        h_bytes = struct.unpack_from("B" * num_of_bytes, bin_file.read(num_of_bytes))
        f_h_code = get_bytes_2_hex(h_bytes)
        if f_h_code == h_code:
            f_type = TYPE_LIST[h_code]
            break
    bin_file.close()
    return f_type
