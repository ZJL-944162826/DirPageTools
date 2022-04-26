from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QListView, QTreeView, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QMouseEvent
from PyQt5.QtCore import Qt, QRect
from collections import deque
import sys


class QComboTreeBox(QComboBox):
    class MyTreeView(QTreeView):
        def __init__(self, parent: QWidget = None, vars=None):
            super().__init__(parent)
            self.vars = vars
            self.setExpandsOnDoubleClick(False)
            self.setHeaderHidden(True)

        def mousePressEvent(self, event):
            self.vars["lock"] = False
            currIndex = self.currentIndex()
            index = currIndex.sibling(currIndex.row(), 0).data()  # 获取同一行不同列的数据
            self.vars["currIndex"] = currIndex

            '''自己创建点击节点Node三角折叠/展开功能'''
            rect = self.visualRect(currIndex)
            expandOrCollape = QRect(rect.left() - 20, rect.top(), 20, rect.height())
            if expandOrCollape.contains(event.pos()):
                self.vars["expandOrCollape"] = True
                if self.isExpanded(currIndex):
                    self.setExpanded(currIndex, False)
                else:
                    self.setExpanded(currIndex, True)
            else:
                self.vars["expandOrCollape"] = False
            '''自己创建点击节点Node三角折叠/展开功能'''

            # super().mousePressEvent(event)   # super()会出现节点打不开的情况，所以才自己创建点击节点Node三角折叠/展开功能

        def mouseDoubleClickEvent(self, event):
            self.vars["lock"] = False
            super().mouseDoubleClickEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vars = dict()
        self.vars["lock"] = True
        self.vars["lineEdit"] = QLineEdit(self)
        self.vars["lineEdit"].setReadOnly(True)
        self.vars["listView"] = self.MyTreeView(self, self.vars)
        self.vars["listViewModel"] = QStandardItemModel(self)
        self.setModel(self.vars["listViewModel"])
        self.setView(self.vars["listView"])
        self.setLineEdit(self.vars["lineEdit"])
        # self.MyTreeView(self, self.vars).setExpandsOnDoubleClick(False)
        self.view_settings()
        self.activated.connect(self.__show_selected)
        # self.add_item("(全选)")
        # self.add_item("其他")
        data = [(1, 0, 'A'), (2, 0, 'B'), (3, 0, 'C'), (4, 0, 'D'), (5, 0, 'E'), (6, 0, 'F'), (7, 0, 'G'), (8, 0, 'H'),
                (9, 1, 'J'), (10, 1, 'K'), (11, 1, 'L'), (
                    12, 1, 'Q'), (14, 2, 'E'), (15, 2, 'R'), (13, 2, 'W')]
        self.importData(data)

    # QtreeView展示视图的一些设置
    def view_settings(self):
        self.view().setMinimumWidth(500)
        self.view().setMinimumHeight(300)
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    # 往QtreeView中添加数据
    def importData(self, data, root=None):
        self.vars["listViewModel"].setRowCount(0)
        if root is None:
            root = QStandardItem()
            self.vars["listViewModel"].appendRow(root)
            root.setText("全选")
            root.setCheckable(True)
            root.setCheckState(Qt.Checked)
        seen = {}  # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value[1] == 0:
                parent = root
            else:
                pid = value[1]
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value[0]
            child = QStandardItem()
            child.setText(value[2])
            child.setCheckable(True)
            child.setCheckState(Qt.Checked)
            parent.appendRow([
                child,
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    # # 根据文本添加子项
    # def add_item(self, text: "str"):
    #     self.topitem = QStandardItem()
    #     self.topitem.setText(text)
    #     self.topitem.setCheckable(True)
    #     self.topitem.setCheckState(Qt.Checked)
    #     self.vars["listViewModel"].appendRow(self.topitem)
    #
    # # 根据文本添加子项
    # def add_subitem(self, text: "str"):
    #     item = QStandardItem()
    #     item.setText(text)
    #     item.setCheckable(True)
    #     item.setCheckState(Qt.Checked)
    #     self.topitem.appendRow(item)

    def __show_selected(self, index):
        this = self.vars["currIndex"]
        model = self.vars["listViewModel"]
        current_standardItem = model.itemFromIndex(this)
        item = self.vars["listViewModel"].item(index)
        # print(item.hasChildren(),item.rowCount(),item.child(item.rowCount()-1).text())
        # print(this.data(), this.parent().data(), this.model().item(index), this.row())
        # print(this.model().itemFromIndex(this),model.itemFromIndex(this))
        # print(self.MyTreeView(self, self.vars).selectionModel())
        if self.vars["expandOrCollape"]:
            pass
            # print("Mouse_Clicked_On_ExpandOrCollape")
        else:
            current_standardItem.setCheckState(
                Qt.Unchecked if current_standardItem.checkState() == Qt.Checked else Qt.Checked)
            self.QcomboTreebox_child_node(current_standardItem)

        self.vars["lock"] = True

    # 递归寻找所有子节点，并改变其复选框状态
    def QcomboTreebox_child_node(self, item):
        if item.hasChildren() == True:
            total_child_count = item.rowCount()
            for i in range(total_child_count):
                child_item = item.child(i)
                child_item.setCheckState(Qt.Checked if item.checkState() == Qt.Checked else Qt.Unchecked)
                self.QcomboTreebox_child_node(child_item)

    # 递归寻找所有父节点,并展开
    def QcomboTreebox_parent_node(self, item):
        if item.parent() != None:
            pitem = item.parent()
            pitem.setExpanded(True)
            self.QcomboTreebox_parent_node(pitem)

    # def handleChanged(self, item, column):
    #     count = item.childCount()
    #     if item.checkState(column) == Qt.Checked:
    #         for index in range(count):
    #             item.child(index).setCheckState(0, Qt.Checked)
    #     if item.checkState(column) == Qt.Unchecked:
    #         for index in range(count):
    #             item.child(index).setCheckState(0, Qt.Unchecked)

    def hidePopup(self):
        if self.vars["lock"]:
            super().hidePopup()


def run():
    app = QApplication(sys.argv)
    win = QComboTreeBox()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()