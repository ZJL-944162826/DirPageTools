import sys
from ui.gui import MainWin
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin(app)
    sys.exit(app.exec_())
