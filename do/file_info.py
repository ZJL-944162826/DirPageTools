class FileInfo:
    # 文件id
    file_id = ""

    # 文件名
    file_name = ""

    # 文件所在地址
    file_path = ""

    # 文件大小
    file_size = 0

    # 文件类型
    file_type = ""

    # 文件页码
    file_page = 0

    # 所属目录ID
    parent_dir_id = ""

    def __init__(self, file_id, file_name, file_path, file_size, file_type, file_page, parent_dir_id):
        self.file_id = file_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.file_page = file_page
        self.parent_dir_id = parent_dir_id



