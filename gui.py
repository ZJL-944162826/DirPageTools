import sys
from utils import dir_util
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QGridLayout, QLineEdit, QTreeView, \
    QTableView, QCommandLinkButton, QPushButton, QFileSystemModel, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPalette


class MainWin(QWidget):
    WINDOW_TITLE = '文件目录管理工具'
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    TREE_HEADER = ['目录\\文件名']
    TABLE_HEADER = ['值']
    TABLE_DIR_NAME = ['目录名', '目录路径']
    TABLE_FILE_NAME = ['文件名', '文件路径', '文件大小', '文件类型', '文件页码']

    DIR_TREE_ROLE = 101
    FILE_TREE_ROLE = 102

    def __init__(self):
        super().__init__()
        self.in_lab = QLabel('输入目录：')
        self.in_edit = QLineEdit()
        self.in_btn = QPushButton('选择文件')
        self.icon_map = {}

        self.left_lab = QLabel('目录列表')
        self.dir_tree = QTreeView()
        self.tree_model = QStandardItemModel()

        self.right_lab = QLabel('目录\\文件信息')
        # self.dir_tab = QTableView()
        self.main_tree = QTreeView()
        # self.tab_model = QStandardItemModel()
        self.main_model = QStandardItemModel()

        self.out_lab = QLabel('输出目录：')
        self.out_edit = QLineEdit()
        self.out_btn = QPushButton('选择目录')
        self.init_ui()

    def init_ui(self):
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # 固定大小
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # 禁用最大最小
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        # 居中
        self.center()
        self.setWindowTitle(self.WINDOW_TITLE)
        # 内容
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addLayout(self.init_in_model(), 1, 0)
        grid.addLayout(self.init_dir_model(), 2, 0)
        grid.addLayout(self.init_out_model(), 3, 0)

        self.setLayout(grid)
        self.show()

    def init_in_model(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.in_lab, 1, 0)
        grid.addWidget(self.in_edit, 1, 1)
        grid.addWidget(self.in_btn, 1, 3)

        self.in_btn.clicked.connect(self.update_dir_model)
        return grid

    def init_dir_model(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.left_lab, 1, 0)
        grid.addWidget(self.dir_tree, 2, 0)
        self.tree_model.setHorizontalHeaderLabels(self.TREE_HEADER)
        self.dir_tree.setModel(self.tree_model)
        # self.dir_tree.clicked.connect(self.item_clicked) 废除
        # 废除
        # grid.addWidget(self.right_lab, 1, 1)
        # grid.addWidget(self.dir_tab, 2, 1)
        # self.tab_model.setHorizontalHeaderLabels(self.TABLE_HEADER)
        # self.dir_tab.setModel(self.tab_model)
        # self.dir_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.dir_tab.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.dir_tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

        grid.addWidget(self.right_lab, 1, 1)
        grid.addWidget(self.main_tree, 2, 1)
        return grid

    def update_dir_model(self):
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(self.TREE_HEADER)
        # 根目录路径
        root_path = r"D:\user\Documents\WeChat Files\qq944162826\FileStorage\File"
        self.in_edit.setText(root_path)
        # 用来存放所有的目录路径
        file_list = []
        dir_list = [dir_util.foreach_dir(root_path, None, file_list)]
        self.foreach_dir(dir_list)

    def foreach_dir(self, dir_list, parent_item=None):
        for dir_info in dir_list:
            now_item = self.add_item(dir_info.dir_name, dir_info, self.DIR_TREE_ROLE, parent_item)
            if dir_info.dir_list is not None:
                self.foreach_dir(dir_info.dir_list, now_item)
            if dir_info.file_list is not None:
                for child_file in dir_info.file_list:
                    if child_file is not None:
                        child_item = self.add_item(child_file.file_name, child_file, self.FILE_TREE_ROLE, now_item)

    def add_item(self, obj_name, obj_data=None, role=None, parent_item=None):
        item = QStandardItem()
        item.setText(obj_name)
        item.setData(obj_data, role)
        item.setEditable(False)
        if parent_item is None:
            self.tree_model.appendRow(item)
        else:
            parent_item.appendRow([item])
        # 图标
        dir_icon = QIcon()
        if role == self.DIR_TREE_ROLE:
            dir_icon.addFile(r"static\icon\folder.ico")
        elif role == self.FILE_TREE_ROLE:
            dir_icon.addFile(r"static\icon\pictures.ico")
        item.setIcon(dir_icon)
        return item

    def item_clicked(self, item):
        dir_info = self.tree_model.itemData(item).get(self.DIR_TREE_ROLE)
        file_info = self.tree_model.itemData(item).get(self.FILE_TREE_ROLE)
        if dir_info is not None:
            print('目录')
            self.tab_model.clear()
            self.tab_model.setHorizontalHeaderLabels(self.TABLE_HEADER)
            self.tab_model.setVerticalHeaderLabels(self.TABLE_DIR_NAME)
            dir_name_item = QStandardItem(dir_info.dir_name)
            dir_name_item.setEditable(False)
            dir_path_item = QStandardItem(dir_info.dir_path)
            dir_path_item.setEditable(False)
            self.tab_model.setItem(0, dir_name_item)
            self.tab_model.setItem(1, dir_path_item)
        else:
            print('文件')
            self.tab_model.clear()
            self.tab_model.setHorizontalHeaderLabels(self.TABLE_HEADER)
            self.tab_model.setVerticalHeaderLabels(self.TABLE_FILE_NAME)
            file_name_item = QStandardItem(file_info.file_name)
            file_name_item.setEditable(False)
            file_path_item = QStandardItem(file_info.file_path)
            file_path_item.setEditable(False)
            file_size_item = QStandardItem(file_info.file_size)
            file_size_item.setEditable(False)
            file_type_item = QStandardItem(file_info.file_type)
            file_type_item.setEditable(False)
            file_page_item = QStandardItem(file_info.file_page)
            self.tab_model.setItem(0, file_name_item)
            self.tab_model.setItem(1, file_path_item)
            self.tab_model.setItem(2, file_size_item)
            self.tab_model.setItem(3, file_type_item)
            self.tab_model.setItem(4, file_page_item)

    def edit_file_page(self):
        print(1111)

    def init_out_model(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.out_lab, 1, 0)
        grid.addWidget(self.out_edit, 1, 1)
        grid.addWidget(self.out_btn, 1, 3)
        return grid

    def init_btn_model(self):
        grid = QGridLayout()
        grid.setSpacing(10)

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())
