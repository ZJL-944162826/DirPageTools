from doctest import Example

from PyQt5.QtWidgets import QTableWidgetItem


class PageItem(QTableWidgetItem):

    def __init__(self, *__args):
        super().__init__(*__args)

    def monitor_edit(self):
        check_state = self.checkState()
        print(check_state)
