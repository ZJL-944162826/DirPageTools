import os
from utils import file_util
from do.dir_info import DirInfo

DIR_ID_TEMP = 0


def foreach_dir(root_path, old_dir_info: DirInfo = None, file_list: [] = None, root=True):
    # 获取该目录下所有的文件名称和目录名称
    if root is True:
        old_dir_info = get_root_dir_info(root_path)
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            new_dir_info = get_dir_info(old_dir_info, dir_file_path)
            # 递归获取所有文件和目录的路径
            foreach_dir(dir_file_path, new_dir_info, file_list, False)
        else:
            file_info = file_util.get_file_info(old_dir_info, dir_file_path)
            if file_info is not None:
                old_dir_info.file_list.append(file_info)
                old_dir_info.dir_page += file_info.file_page
                if file_list is not None:
                    file_list.append(file_info)
    return old_dir_info


def get_root_dir_info(path):
    global DIR_ID_TEMP
    DIR_ID_TEMP += 1
    dir_url, dir_name = os.path.split(path)
    root_dir_info = DirInfo(
        DIR_ID_TEMP,
        dir_name,
        dir_url,
        [],
        [],
        None,
        0
    )
    return root_dir_info


def get_dir_info(old_dir_info: DirInfo, path):
    global DIR_ID_TEMP
    DIR_ID_TEMP += 1
    dir_url, dir_name = os.path.split(path)
    if old_dir_info is not None:
        parent_dir_id = old_dir_info.parent_dir_id
    else:
        parent_dir_id = None
    new_dir_info = DirInfo(
        DIR_ID_TEMP,
        dir_name,
        dir_url,
        [],
        [],
        parent_dir_id,
        0,
    )
    if old_dir_info is not None:
        old_dir_info.dir_list.append(new_dir_info)
    return new_dir_info
