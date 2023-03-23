import json


class ObjInfo:
    # id
    obj_id = ""

    # 类型 0：目录 其他：文件
    obj_type = ""

    # 名称
    obj_name = ""

    # 地址
    obj_path = ""

    # 页码
    obj_page = 0

    # 所属目录ID
    parent_obj_id = ""

    # 父级
    parent_obj = None

    # 子目录
    dir_list = []

    # 子文件
    file_list = []

    def __init__(self, obj_id, obj_type, obj_name, obj_path, obj_page, parent_obj_id, parent_obj, dir_list, file_list):
        self.obj_id = obj_id
        self.obj_type = obj_type
        self.obj_name = obj_name
        self.obj_path = obj_path
        self.obj_page = obj_page
        self.parent_obj_id = parent_obj_id
        # self.parent_obj = parent_obj
        self.dir_list = dir_list
        self.file_list = file_list


class ObjInfoDecode(json.JSONDecoder):

    def decode(self, s, **kwargs):
        dic = super().decode(s)
        return self.dic_2_obj(dic)

    def dic_2_obj(self, dic):
        obj_info = ObjInfo(dic['obj_id'], dic['obj_type'], dic['obj_name'], dic['obj_path'], dic['obj_page'],
                           dic['parent_obj_id'], None, [], [])
        if dic['dir_list'] is not None and dic['dir_list'].__len__() > 0:
            dir_list = []
            for dir_child in dic['dir_list']:
                dir_list.append(self.dic_2_obj(dir_child))
            obj_info.dir_list = dir_list
        if dic['file_list'] is not None and dic['file_list'].__len__() > 0:
            file_list = []
            for file_child in dic['file_list']:
                file_list.append(self.dic_2_obj(file_child))
            obj_info.file_list = file_list
        return obj_info
