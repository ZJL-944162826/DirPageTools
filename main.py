from utils import dir_util

if __name__ == "__main__":
    # 根目录路径
    root_path = r"D:\user\Documents\WeChat Files\qq944162826\FileStorage\File"
    # 用来存放所有的目录路径
    file_list = []
    dir_util.foreach_dir(root_path, None, file_list)
    print(file_list)
    # gui.start_window()
