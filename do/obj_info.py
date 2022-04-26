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
        self.parent_obj = parent_obj
        self.dir_list = dir_list
        self.file_list = file_list




