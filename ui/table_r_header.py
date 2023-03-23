import sys

from PyQt5.QtWidgets import QApplication, QWidget,  QVBoxLayout,  QTableWidget, QCheckBox, QHeaderView, QStyle, QStyleOptionButton, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QRect
import table_r


class TableRHeader(QHeaderView):
    """自定义表头类"""

    # 自定义 复选框全选信号
    select_all_clicked = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 0
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(TableRHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(TableRHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2.)

        if logicalIndex == 0:
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
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(TableRHeader, self).mousePressEvent(event)

    # # 自定义信号 select_all_clicked 的槽方法
    # def change_state(self, isOn):
    #     # 如果行表头复选框为勾选状态
    #     if isOn:
    #         # 将所有的复选框都设为勾选状态
    #         for i in table_r.ALL_HEADER_COMBOBOX:
    #             i.setCheckState(Qt.Checked)
    #     else:
    #         for i in table_r.ALL_HEADER_COMBOBOX:
    #             i.setCheckState(Qt.Unchecked)
