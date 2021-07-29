from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)

        self.menu_widget = QtWidgets.QWidget(MainWindow)
        self.menu_widget.setObjectName("menu_widget")

        self.menu_background = QtWidgets.QLabel(self.menu_widget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.menu_background.setText("")
        self.menu_background.setPixmap(QtGui.QPixmap("2693280.jpg"))
        self.menu_background.setObjectName("menu_background")

        self.start = QtWidgets.QPushButton(self.menu_widget)
        self.start.setGeometry(QtCore.QRect(100, 80, 500, 100))

        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)

        self.start.setFont(font)
        self.start.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.start.setObjectName("start")

        self.info = QtWidgets.QPushButton(self.menu_widget)
        self.info.setGeometry(QtCore.QRect(100, 220, 500, 100))
        self.info.setFont(font)
        self.info.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.info.setObjectName("info")

        self.exit = QtWidgets.QPushButton(self.menu_widget)
        self.exit.setGeometry(QtCore.QRect(100, 360, 500, 100))
        self.exit.setFont(font)
        self.exit.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.exit.setObjectName("exit")

        MainWindow.setCentralWidget(self.menu_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start.setText(_translate("MainWindow", "Start"))
        self.info.setText(_translate("MainWindow", "Info"))
        self.exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
