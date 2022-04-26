class DirInfo:
    # 目录ID
    dir_id = ""

    # 目录名
    dir_name = ""

    # 目录路径
    dir_path = ""

    # 子目录
    dir_list = []

    # 子文件
    file_list = []

    # 所属目录ID
    parent_dir_id = ""

    # 文件夹页码数量
    dir_page = 0

    def __init__(self, dir_id, dir_name, dir_path, dir_list: [], file_list: [], parent_dir_id, dir_page):
        self.dir_id = dir_id
        self.dir_name = dir_name
        self.dir_path = dir_path
        self.dir_list = dir_list
        self.file_list = file_list
        self.parent_dir_id = parent_dir_id
        self.dir_page = dir_page



