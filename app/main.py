# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLineEdit
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from GeneticAlgorithm import GeneticAlgorithm
from Chromosome import Chromosome

class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.load_ui()

    def findButtonClick(self):
        wantedResult = int(self.ui.wantedLine.text())
        population = int(self.ui.populationLine.text())
        parentLen = 6
        mutationRate = 0.1

        alg = GeneticAlgorithm(wantedResult, population, parentLen, mutationRate)
        alg.generatePopulation()

        result: Chromosome
        generation = 0
        while True:
            generation += 1
            print("Generation: ", generation)
            alg.calculateObjectiveValues()
            alg.calculateFitnessValues()

            alg.doRouleteWheel()

            alg.doCrossOverAndMutate()
            result = alg.checkIfFinished()
            if result is not None:
                break

        print("%d + %d + %d = %d" %(result.a, result.b, result.c, wantedResult))

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
