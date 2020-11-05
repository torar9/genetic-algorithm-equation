# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.load_ui()

    def findButtonClick(self):
        population = int(self.ui.populationLine.text())
        wanted = int(self.ui.wantedLine.text())
        print("pop: ", population)
        print("want: ", wanted)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui: QWidget = loader.load(ui_file, self)
        ui_file.close()

        self.ui.findButton.clicked.connect(self.findButtonClick)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = MainWin()
    widget.show()
    sys.exit(app.exec_())
