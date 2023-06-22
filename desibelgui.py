import sys
from PyQt5 import QtGui,QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

class gui(QMainWindow):
    def __init__(self):
        super(gui, self).__init__()
        self.initUI()

    def dataReady(self):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.End)
        #cursor.insertText(str(self.process.readAll()))
        cursor.insertText(self.process.readAll().data().decode())
        self.output.ensureCursorVisible()

    def callProgram(self):
        # run the process
        # `start` takes the exec and a list of arguments
        self.process.start('python',['-u','desibelolcer.py'])

    def initUI(self):
        # Layout are better for placing widgets
        layout =  QHBoxLayout()
        self.runButton =  QPushButton('Baslat')
        self.runButton.clicked.connect(self.callProgram)

        self.output =  QTextEdit()
        self.setGeometry(100, 60, 1000, 800)
        layout.addWidget(self.output)
        layout.addWidget(self.runButton)

        centralWidget =  QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.dataReady)

        # Just to prevent accidentally running multiple times
        # Disable the button when process starts, and enable it when it finishes
        self.process.started.connect(lambda: self.runButton.setEnabled(False))
        self.process.finished.connect(lambda: self.runButton.setEnabled(True))


#Function Main Start
def main():
    app =QApplication(sys.argv)
    ui=gui()
    ui.show()
    sys.exit(app.exec_())
#Function Main END

if __name__ == '__main__':
    main() 