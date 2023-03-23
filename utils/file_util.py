import os
import pdfplumber
import pythoncom
import win32com
import win32com.client
import xlrd
import zipfile
import shutil
import pptx

from xml.dom.minidom import parse
from openpyxl import load_workbook
from do.obj_info import ObjInfo
from common import enum

FILE_ID_TEMP = 0
IMAGE_TYPE = [".gif", ".png", ".jpg",
              ".GIF", ".PNG", ".JPG"]
DOC_TYPE = [".doc", ".docx",
            ".DOC", ".DOCX"]
PDF_TYPE = [".pdf",
            ".PDF"]
XLS_TYPE = [".xls",
            ".XLS"]
XLSX_TYPE = [".xlsx",
             ".XLSX"]
OFD_TYPE = [".ofd",
            ".OFD"]
PPT_TYPE = [".ppt", ".pptx",
            ".PPT", "PPTX"]


def get_file_info(dir_info: ObjInfo, path):
    # print("-- file: " + path)
    suffix = os.path.splitext(path)[1]
    # print("-- file-suffix: " + suffix)
    dir_url, file_name = os.path.split(path)
    if suffix in IMAGE_TYPE:
        file_info = read_image(dir_info, path)
    elif suffix in DOC_TYPE:
        file_info = read_doc(dir_info, path)
    elif suffix in PDF_TYPE:
        file_info = read_pdf(dir_info, path)
    elif suffix in XLS_TYPE:
        file_info = read_xls(dir_info, path)
    elif suffix in XLSX_TYPE:
        file_info = read_xlsx(dir_info, path)
    elif suffix in OFD_TYPE:
        file_info = read_ofd(dir_info, path, dir_url)
    elif suffix in PPT_TYPE:
        file_info = read_ppt(dir_info, path)
    else:
        file_info = read_unknown_file(dir_info, path)
    global FILE_ID_TEMP
    FILE_ID_TEMP += 1
    # file_name = file_name.split('.')[0]
    file_info.obj_id = "file" + str(FILE_ID_TEMP)
    file_info.obj_name = file_name.split('.', 1)[0]
    file_info.obj_path = dir_url
    return file_info


def read_image(dir_info: ObjInfo, path):
    os.stat(path)
    image_info = ObjInfo(
        "",
        enum.IMG_TYPE,
        "",
        "",
        1,
        dir_info.obj_id,
        dir_info,
        [],
        []
    )
    return image_info


def read_doc(dir_info: ObjInfo, path):
    try:
        pythoncom.CoInitialize()
        # 调用word程序，不在前台显示
        w = win32com.client.Dispatch("Word.Application")
        w.Visible = 0
        w.DisplayAlerts = 0
        # 打开一个word文档
        doc = w.Documents.Open(path)
        # 获取总页数
        w.ActiveDocument.Repaginate()
        page = w.ActiveDocument.ComputeStatistics(2)
        # 保存并关闭
        doc.Close()
        onj_info = ObjInfo(
            "",
            enum.DOC_TYPE,
            "",
            "",
            page,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_pdf(dir_info: ObjInfo, path):
    try:
        pdf = pdfplumber.open(path)
        page = len(pdf.pages)
        pdf.close()
        onj_info = ObjInfo(
            "",
            enum.PDF_TYPE,
            "",
            "",
            page,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_xls(dir_info: ObjInfo, path):
    try:
        wb = xlrd.open_workbook(path)
        page = len(wb.sheets())
        onj_info = ObjInfo(
            "",
            enum.XLS_TYPE,
            "",
            "",
            page,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_xlsx(dir_info: ObjInfo, path):
    try:
        wb = load_workbook(path)
        page = len(wb.get_sheet_names())
        wb.close()
        onj_info = ObjInfo(
            "",
            enum.XLS_TYPE,
            "",
            "",
            page,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_ofd(dir_info: ObjInfo, path, dir_url):
    try:
        file_path = unzip_file(path, dir_url + "\\~temp")
        io = f"{file_path}\\OFD.xml"
        element = parse(io).documentElement
        nodes = element.getElementsByTagName('ofd:DocRoot')
        pages = 1
        for i in range(len(nodes)):
            sun_node = nodes[i].childNodes
            for j in range(len(sun_node)):
                node_io = f"{file_path}\\" + sun_node[j].data
                node_element = parse(node_io).documentElement
                page_nodes = node_element.getElementsByTagName('ofd:Page')
                pages = len(page_nodes)
        shutil.rmtree(file_path)
        onj_info = ObjInfo(
            "",
            enum.OFD_TYPE,
            "",
            "",
            pages,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_ppt(dir_info: ObjInfo, path):
    try:
        presentation = pptx.Presentation(path)
        page = len(presentation.slides)
        onj_info = ObjInfo(
            "",
            enum.PPT_TYPE,
            "",
            "",
            page,
            dir_info.obj_id,
            dir_info,
            [],
            []
        )
        return onj_info
    except Exception as e:
        print("引发异常：", repr(e))
        return read_unknown_file(dir_info, path)


def read_unknown_file(dir_info: ObjInfo, path):
    os.stat(path)
    onj_info = ObjInfo(
        "",
        enum.UNDEFINED_TYPE,
        "",
        "",
        1,
        dir_info.obj_id,
        dir_info,
        [],
        []
    )
    return onj_info


def unzip_file(zip_path, unzip_path=None):
    """
    :param zip_path: ofd格式文件路径
    :param unzip_path: 解压后的文件存放目录
    :return: unzip_path
    """
    if not unzip_path:
        unzip_path = zip_path.split('.')[0]
    with zipfile.ZipFile(zip_path, 'r') as f:
        for file in f.namelist():
            f.extract(file, path=unzip_path)
    return unzip_path
