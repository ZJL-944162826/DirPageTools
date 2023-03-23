import sys

from PyQt5.QtWidgets import QApplication

from ui.gui import MainWin

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        ex = MainWin(app)
        sys.exit(app.exec_())
    except Exception as e:
        print(e)





