# This Python file uses the following encoding: utf-8
import sys
import os

from decimal import Decimal
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QWidget, QLineEdit
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from GeneticAlgorithm import GeneticAlgorithm
from Chromosome import Chromosome

class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.load_ui()
        self.setWindowTitle("SOFCO - project number 2")

    def findButtonClick(self):
        wantedResult = int(self.ui.wantedLine.text())

        if wantedResult > 765:
            wantedResult = 765
            self.ui.wantedLine.setText("765")
        if wantedResult < 0:
            self.ui.wantedLine.setText("0")
            wantedResult = 0

        population = int(self.ui.populationLine.text())
        parentLen = population
        mutationRate = float(self.ui.mutationLine.text())
        self.ui.logField.setText("")

        alg = GeneticAlgorithm(wantedResult, population, parentLen, mutationRate)
        alg.generatePopulation()
        alg.calculateObjectiveValues()
        alg.calculateFitnessValues()

        result: Chromosome
        generation = 0
        while True:
            generation += 1
            #print("Generation: ", generation)
            alg.doRouleteWheel()

            alg.doCrossOverAndMutate()
            alg.calculateObjectiveValues()
            alg.calculateFitnessValues()

            log = self.ui.logField.toPlainText()
            log += ("Generation: %d \n" %(generation))
            log += alg.getChromosomesString()
            self.ui.logField.setText(log + "\n")

            result = alg.checkIfFinished()
            if result is not None:
                break

        self.ui.resultLabel.setText("Result: %d + %d + %d = %d" %(result.a, result.b, result.c, wantedResult))

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui: QWidget = loader.load(ui_file, self)
        ui_file.close()

        self.ui.findButton.clicked.connect(self.findButtonClick)

        self.onlyIntWanted = QtGui.QIntValidator()
        self.onlyIntPopulation = QtGui.QIntValidator()
        self.onlyIntWanted.setRange(0, 765)
        self.ui.wantedLine.setValidator(self.onlyIntWanted)
        self.ui.populationLine.setValidator(self.onlyIntPopulation)



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = MainWin()
    widget.show()
    sys.exit(app.exec_())
