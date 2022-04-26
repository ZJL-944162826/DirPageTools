import sys

from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QCheckBox, QHeaderView, QStyle, \
    QStyleOptionButton, QTableWidgetItem, QGridLayout, QPushButton, QStyledItemDelegate
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from do.obj_info import ObjInfo
from common import enum
from uuid import UUID
import uuid
import copy

# 用来装行表头所有复选框 全局变量
from ui.page_item import PageItem

ALL_HEADER_COMBOBOX = {}

"""窗口类"""


class TableR(QTableWidget):

    ONE_EDIT = True
    # 表头字段，全局变量
    HEADER_FIELD = ['',
                    '题名',
                    '页次',
                    '',
                    # 'row_id',
                    # 'checkbox_id',
                    # 'parent_row_id'
                    ]

    ALL_PAGE = 1

    def __init__(self, *__args):
        super().__init__(*__args)
        # 设置表格头
        self.set_table_header()
        # 设置表格
        self.set_table_widget()
        self.init_ui()
        self.itemChanged.connect(self.monitor_edit)

    # 监听编辑事件
    def monitor_edit(self):
        if self.ONE_EDIT:
            row = self.currentIndex().row()
            column = self.currentIndex().column()
            # 编辑页次
            if column == 2:
                self.edit_page(row)

    def init_ui(self):
        ALL_HEADER_COMBOBOX.clear()
        self.ALL_PAGE = 0

    # 设置行表头字段
    def set_table_header(self):
        # 设置列数
        self.setColumnCount(len(self.HEADER_FIELD))
        header = CheckBoxHeader()  # 实例化自定义表头
        self.setHorizontalHeader(header)  # 设置表头
        self.setHorizontalHeaderLabels(self.HEADER_FIELD)  # 设置行表头字段
        # 表头自适应
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        # self.right_tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnWidth(0, 10)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 40)
        self.setWordWrap(True)
        header.SELECT_ALL_CLICKED.connect(header.change_state)  # 行表头复选框单击信号与槽

    # 设置表格
    def set_table_widget(self):
        # 表格控件
        # 交替行颜色
        self.setAlternatingRowColors(True)

    def append_row(self, row: int, data: ObjInfo, role: int, parent_id=None):
        row_id = str(uuid.uuid4())
        checkbox_id = str(uuid.uuid4())
        self.insertRow(row)
        # 设置选择框
        checkbox = QCheckBox()
        self.setCellWidget(row, 0, checkbox)
        ALL_HEADER_COMBOBOX[checkbox_id] = checkbox
        # 设置题名与文件目录信息
        data_item = QTableWidgetItem(data.obj_name)
        self.setItem(row, 1, data_item)
        data_item.setData(role, data)
        data_item.setData(enum.ROW_ID_ROLE, row_id)
        data_item.setData(enum.CHECK_BOX_ROLE, checkbox_id)
        if parent_id is not None:
            data_item.setData(enum.PARENT_ITEM_ID_ROLE, parent_id)
        # 设置页码
        page_item = PageItem()
        page_item.setFlags(page_item.flags() & ~Qt.ItemIsEditable)
        self.setItem(row, 2, page_item)
        # 设置目录展开收缩按钮
        if data.obj_type is '0':
            open_btn = QPushButton("展开")
            self.setCellWidget(row, 3, open_btn)
            open_btn.clicked.connect(self.open_dir)
        # 测试
        # self.setItem(row, 4, QTableWidgetItem(data_item.data(enum.ROW_ID_ROLE)))
        # self.setItem(row, 5, QTableWidgetItem(data_item.data(enum.CHECK_BOX_ROLE)))
        # self.setItem(row, 6, QTableWidgetItem(data_item.data(enum.PARENT_ITEM_ID_ROLE)))
        self.reload_page()
        return row_id

    def remove_row(self, row: int):
        # 数据item
        data_item = self.item(row, 1)
        # 将复选框排除ALL_HEADER_COMBOBOX
        checkbox_id = data_item.data(enum.CHECK_BOX_ROLE)
        if checkbox_id in ALL_HEADER_COMBOBOX.keys():
            del ALL_HEADER_COMBOBOX[checkbox_id]
        self.removeRow(row)
        self.reload_page()

    def open_dir(self):
        row = self.currentIndex().row()
        # 复选框item
        checkbox = self.cellWidget(row, 0)
        checkbox.setEnabled(False)
        checkbox.setCheckState(Qt.Unchecked)
        # 数据item
        data_item = self.item(row, 1)
        # 当文件夹被打开后输出时自动忽略
        data_item.setData(enum.IGNORE_ROLE, True)
        data_item.setForeground(QBrush(QColor('#cccccc')))
        # 页码item
        page_item = self.item(row, 2)
        page_item.setForeground(QBrush(QColor('#cccccc')))
        # 将复选框排除ALL_HEADER_COMBOBOX
        checkbox_id = data_item.data(enum.CHECK_BOX_ROLE)
        del ALL_HEADER_COMBOBOX[checkbox_id]
        # 得到父id
        row_id = data_item.data(enum.ROW_ID_ROLE)
        parent_dir = data_item.data(enum.DIR_TREE_ROLE)
        start_page = data_item.data(enum.OBJ_START_PAGE_ROLE)
        if len(parent_dir.dir_list):
            self.foreach_add_obj(parent_dir.dir_list, enum.DIR_TREE_ROLE, start_page, row, row_id)
        if len(parent_dir.file_list):
            self.foreach_add_obj(parent_dir.file_list, enum.FILE_TREE_ROLE, start_page, row, row_id)
        # 设置目录展开收缩按钮
        if parent_dir.obj_type is '0':
            open_btn = QPushButton("关闭")
            self.setCellWidget(self.currentIndex().row(), 3, open_btn)
            open_btn.clicked.connect(self.close_dir)
        self.reload_page()

    def foreach_add_obj(self, obj_list: [ObjInfo], role: int, start_page: int, row: int, parent_id):
        for line, child_obj in enumerate(obj_list):
            new_line = row + line + 1
            self.append_row(new_line, child_obj, role, parent_id)

    def close_dir(self, row=None):
        if row is None or row is False:
            row = self.currentIndex().row()
        # 复选框item
        checkbox = self.cellWidget(row, 0)
        checkbox.setEnabled(True)
        # 数据item
        data_item = self.item(row, 1)
        # 当文件夹被关闭后输出时自动添加
        data_item.setData(enum.IGNORE_ROLE, False)
        data_item.setForeground(QBrush(QColor('#000000')))
        checkbox_id = data_item.data(enum.CHECK_BOX_ROLE)
        ALL_HEADER_COMBOBOX[checkbox_id] = checkbox
        # 得到rowId
        row_id = data_item.data(enum.ROW_ID_ROLE)
        # 页码item
        page_item = self.item(row, 2)
        page_item.setForeground(QBrush(QColor('#000000')))
        # 删除子节点
        rows = self.find_need_del_row(row_id)
        desc_rows = sorted(rows, reverse=True)
        for i in desc_rows:
            self.remove_row(i)
        data = data_item.data(enum.DIR_TREE_ROLE)
        if data.obj_type is '0':
            open_btn = QPushButton("展开")
            self.setCellWidget(self.currentIndex().row(), 3, open_btn)
            open_btn.clicked.connect(self.open_dir)

    def find_need_del_row(self, parent_id):
        rows = []
        i = self.rowCount()
        while i > 0:
            i -= 1
            data_item_temp = self.item(i, 1)
            parent_id_tag = data_item_temp.data(enum.PARENT_ITEM_ID_ROLE)
            row_id = data_item_temp.data(enum.ROW_ID_ROLE)
            if parent_id == parent_id_tag:
                rows.append(i)
                if data_item_temp.data(enum.IGNORE_ROLE):
                    rows += self.find_need_del_row(row_id)
        return rows

    def new(self):
        obj = ObjInfo(uuid.uuid4().int, 1, '新建题名', '', 1, "", None, [], [])
        tag = True
        for i in range(self.rowCount()):
            if i <= 0:
                continue
            else:
                checkbox = self.cellWidget(i, 0)
                if checkbox.checkState() == Qt.Checked:
                    self.append_row(i + 1, obj, enum.FILE_TREE_ROLE)
                    tag = False
                    break
        if tag:
            self.append_row(self.rowCount(), obj, enum.FILE_TREE_ROLE)

    def top(self):
        for i in range(self.rowCount()):
            if i <= 0:
                continue
            else:
                checkbox = self.cellWidget(i, 0)
                if checkbox.checkState() == Qt.Checked:
                    self.switch_row(i, i - 1)

    def down(self):
        i = self.rowCount()
        while i > 0:
            i -= 1
            if i >= self.rowCount() - 1:
                continue
            else:
                checkbox = self.cellWidget(i, 0)
                if checkbox.checkState() == Qt.Checked:
                    self.switch_row(i, i + 1)

    def remove(self):
        i = self.rowCount()
        while i > 0:
            i -= 1
            if i > self.rowCount() - 1:
                continue
            else:
                checkbox = self.cellWidget(i, 0)
                if checkbox.checkState() == Qt.Checked:
                    self.remove_row(i)

    def switch_row(self, row_1: int, row_2: int):
        checkbox_1 = self.cellWidget(row_1, 0)
        checkbox_2 = self.cellWidget(row_2, 0)
        data_item_1 = self.takeItem(row_1, 1)
        data_item_2 = self.takeItem(row_2, 1)
        page_item_1 = self.takeItem(row_1, 2)
        page_item_2 = self.takeItem(row_2, 2)
        btn_1 = self.cellWidget(row_1, 3)
        btn_2 = self.cellWidget(row_2, 3)
        # 选择框交换
        if checkbox_1.checkState() == Qt.Checked and checkbox_2.checkState() == Qt.Unchecked:
            checkbox_1.setCheckState(Qt.Unchecked)
            checkbox_2.setCheckState(Qt.Checked)
        elif checkbox_1.checkState() == Qt.Unchecked and checkbox_2.checkState() == Qt.Checked:
            checkbox_1.setCheckState(Qt.Checked)
            checkbox_2.setCheckState(Qt.Unchecked)
        # 内容交换
        self.setItem(row_1, 1, data_item_2)
        self.setItem(row_1, 2, page_item_2)
        self.setItem(row_2, 1, data_item_1)
        self.setItem(row_2, 2, page_item_1)
        # 对应checkboxId交换
        checkbox_id_1 = data_item_1.data(enum.CHECK_BOX_ROLE)
        checkbox_id_2 = data_item_2.data(enum.CHECK_BOX_ROLE)
        ALL_HEADER_COMBOBOX[checkbox_id_1] = checkbox_2
        ALL_HEADER_COMBOBOX[checkbox_id_2] = checkbox_1
        # data_item_1.setData(enum.CHECK_BOX_ROLE, checkbox_id_2)
        # data_item_2.setData(enum.CHECK_BOX_ROLE, checkbox_id_1)
        # 按钮交换
        row_1_is_dir = data_item_1.data(enum.DIR_TREE_ROLE) is not None
        row_2_is_dir = data_item_2.data(enum.DIR_TREE_ROLE) is not None
        if row_1_is_dir is True and row_2_is_dir is False:
            btn_text = btn_1.text()
            btn_item = QPushButton(btn_text)
            self.removeCellWidget(row_1, 3)
            self.setCellWidget(row_2, 3, btn_item)
            if btn_text == "展开":
                btn_item.clicked.connect(self.open_dir)
                checkbox_1.setEnabled(True)
                checkbox_2.setEnabled(True)
            else:
                btn_item.clicked.connect(self.close_dir)
                checkbox_1.setEnabled(True)
                checkbox_2.setEnabled(False)
        elif row_1_is_dir is False and row_2_is_dir is True:
            btn_text = btn_2.text()
            btn_item = QPushButton(btn_text)
            self.setCellWidget(row_1, 3, btn_item)
            self.removeCellWidget(row_2, 3)
            if btn_text == "展开":
                btn_item.clicked.connect(self.open_dir)
                checkbox_1.setEnabled(True)
                checkbox_2.setEnabled(True)
            else:
                btn_item.clicked.connect(self.close_dir)
                checkbox_1.setEnabled(False)
                checkbox_2.setEnabled(True)
        elif row_1_is_dir is True and row_2_is_dir is True:
            btn_text_1 = btn_1.text()
            btn_text_2 = btn_2.text()
            new_btn_1 = QPushButton(btn_text_1)
            new_btn_2 = QPushButton(btn_text_2)
            self.removeCellWidget(row_1, 3)
            self.removeCellWidget(row_2, 3)
            self.setCellWidget(row_1, 3, new_btn_2)
            self.setCellWidget(row_2, 3, new_btn_1)
            if btn_text_1 == "展开":
                new_btn_1.clicked.connect(self.open_dir)
                checkbox_2.setEnabled(True)
            else:
                new_btn_1.clicked.connect(self.close_dir)
                checkbox_2.setEnabled(False)
            if btn_text_2 == "展开":
                new_btn_2.clicked.connect(self.open_dir)
                checkbox_1.setEnabled(True)
            else:
                new_btn_2.clicked.connect(self.close_dir)
                checkbox_1.setEnabled(False)
        self.reload_page()

    def reload_page(self):
        all_page = 0
        for row in range(self.rowCount()):
            # 数据item
            data_item = self.item(row, 1)
            row_is_dir = data_item.data(enum.DIR_TREE_ROLE) is not None
            if row_is_dir:
                dir_is_open = data_item.data(enum.IGNORE_ROLE) is True
                if dir_is_open:
                    self.setItem(row, 2, PageItem())
                    continue
                data = data_item.data(enum.DIR_TREE_ROLE)
            else:
                data = data_item.data(enum.FILE_TREE_ROLE)
            if data.obj_page == 1:
                all_page += 1
                start_end_page = str(all_page)
            elif data.obj_page > 1:
                start_page = all_page + 1
                all_page += data.obj_page
                end_page = all_page
                # 方案1：显示开始页-结束页
                # start_end_page = str(start_page) + '-' + str(end_page)
                # 方案2：只显示开始页
                start_end_page = str(start_page)
            else:
                start_end_page = str(all_page)
            self.setItem(row, 2, PageItem(start_end_page))

    def edit_page(self, row: int):
        self.ONE_EDIT = False
        now_page = self.item(row, 2)
        now_page_txt = now_page.text()
        next_page_txt = 0
        if row is not 0:
            next_page_txt = self.item(row + 1, 2).text()
            if next_page_txt.__contains__('-'):
                next_page_txt = next_page_txt.split('-')[0]
        # next_page_txt = None
        # if row is not self.rowCount() - 1:
        #     next_page_txt = self.item(row + 1, 2).text()
        if now_page_txt.__contains__('-'):
            median = int(now_page_txt.split('-')[0]) - int(next_page_txt) + 1
        else:
            median = int(now_page_txt) - int(next_page_txt) + 2
        for all_row in range(self.rowCount()):
            if all_row <= row:
                continue
            new_page = self.item(all_row, 2)
            new_page_txt = new_page.text()
            if new_page_txt.__contains__('-'):
                new_page_txt_array = new_page_txt.split('-')
                new_page_txt = str(int(new_page_txt_array[0]) + median) + '-' + str(int(new_page_txt_array[1]) + median)
            else:
                new_page_txt = str(int(new_page_txt) + median)
            self.setItem(all_row, 2, PageItem(new_page_txt))
        self.ONE_EDIT = True


class CheckBoxHeader(QHeaderView):
    """自定义表头类"""

    # 自定义 复选框全选信号
    SELECT_ALL_CLICKED = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 0
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logical_index):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logical_index)
        painter.restore()
        self._y_offset = int((rect.height() - self._width) / 2.)
        if logical_index == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 SELECT_ALL_CLICKED()
                self.SELECT_ALL_CLICKED.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 自定义信号 SELECT_ALL_CLICKED 的槽方法
    def change_state(self):
        # 如果行表头复选框为勾选状态
        if self.isOn:
            # 将所有的复选框都设为勾选状态
            for i in ALL_HEADER_COMBOBOX.values():
                i.setCheckState(Qt.Checked)
        else:
            for i in ALL_HEADER_COMBOBOX.values():
                i.setCheckState(Qt.Unchecked)

