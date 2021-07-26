import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal, QBasicTimer
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame, QMainWindow, QMessageBox


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setStyleSheet("")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhHiddenText)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 700, 460))
        self.background.setText("")
        self.background.setTextFormat(QtCore.Qt.PlainText)
        self.background.setPixmap(QtGui.QPixmap("Background.jpg"))

        self.board = QtWidgets.QLabel(self.centralwidget)
        self.board.setGeometry(QtCore.QRect(0, 460, 700, 140))
        self.board.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 255, 123), stop:1 rgba(255, 255, 255, 255));")
        self.board.setText("")
        self.board.setPixmap(QtGui.QPixmap("board.png"))
        self.board.setObjectName("board")

        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)

        self.text_level = QtWidgets.QLabel(self.centralwidget)
        self.text_level.setGeometry(QtCore.QRect(90, 465, 150, 40))
        self.text_level.setFont(font)
        self.text_level.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_level.setObjectName("text_level")

        self.text_score = QtWidgets.QLabel(self.centralwidget)
        self.text_score.setGeometry(QtCore.QRect(90, 515, 170, 40))
        self.text_score.setFont(font)
        self.text_score.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_score.setObjectName("text_score")

        self.text_lives = QtWidgets.QLabel(self.centralwidget)
        self.text_lives.setGeometry(QtCore.QRect(480, 465, 150, 40))
        self.text_lives.setFont(font)
        self.text_lives.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_lives.setObjectName("text_lives")

        self.text_speed = QtWidgets.QLabel(self.centralwidget)
        self.text_speed.setGeometry(QtCore.QRect(480, 515, 19 0, 40))
        self.text_speed.setFont(font)
        self.text_speed.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_speed.setObjectName("text_speed")

        self.play_zone = Play_zone(self.centralwidget)
        self.play_zone.setGeometry(QtCore.QRect(0, 0, 700, 460))
        self.play_zone.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.play_zone.setFrameShadow(QtWidgets.QFrame.Raised)
        self.play_zone.setObjectName("play_zone")
        self.play_zone.msg_score[str].connect(self.text_score.setText)
        self.play_zone.msg_acceleration[str].connect(self.text_speed.setText)
        self.play_zone.msg_lives[str].connect(self.text_lives.setText)
        self.play_zone.msg_level[str].connect(self.text_level.setText)
        self.play_zone.start()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        self.menuRules = QtWidgets.QMenu(self.menubar)
        self.menuRules.setObjectName("menuRules")

        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuRules.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))
        self.text_level.setText(_translate("MainWindow", "Level: " + str(self.play_zone.level)))
        self.text_score.setText(_translate("MainWindow", "Score: " + str(self.play_zone.score)))
        self.text_lives.setText(_translate("MainWindow", "Lives: " + str(self.play_zone.lives)))
        self.text_speed.setText(_translate("MainWindow", "Speed: x" + str(-(self.play_zone.acceleration - 20) / 10)))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuRules.setTitle(_translate("MainWindow", "Rules"))


class Food():
    acceleration = 0
    score = 1
    grow = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        constructors = [self.default_score, self.default_score, self.default_score, self.default_score,
                        self.default_score, self.bonus_score, self.decrease_score, self.fast_score, self.fast_score,
                        self.slow_score]
        constructors[random.randint(0, 9)]()

    def default_score(self):
        self.color = QColor(0xEFD334)

    def bonus_score(self):
        self.color = QColor(0xED4830)
        self.score = 3

    def decrease_score(self):
        self.color = QColor(0x8C1778)
        self.grow = -1

    def fast_score(self):
        self.color = QColor(0x32127A)
        self.acceleration = -1

    def slow_score(self):
        self.color = QColor(0x00C5CD)
        self.acceleration = 1


class Play_zone(QFrame):
    number_blocks_x = 40
    number_blocks_y = 26

    msg_score = pyqtSignal(str)
    msg_acceleration = pyqtSignal(str)
    msg_lives = pyqtSignal(str)
    msg_level = pyqtSignal(str)

    def __init__(self, parent):
        super(Play_zone, self).__init__(parent)
        self.set_standard_position()
        self.max_len = 4
        self.timer = QBasicTimer()
        self.default_speed = 120
        self.score = 0
        self.food = []
        self.grow_snake = False
        self.speed_changed = False
        self.score_changed = False
        self.decrease_snake = False
        self.lives = 3
        self.level = 1
        self.levels = dict()
        self.make_levels()
        self.drop_food()
        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.timer.start(self.default_speed * self.acceleration // 10, self)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Down:
            if self.direction != "up":
                self.direction = "down"
        elif key == Qt.Key_Up:
            if self.direction != "down":
                self.direction = "up"

        elif key == Qt.Key_Left:
            if self.direction != "right":
                self.direction = "left"

        elif key == Qt.Key_Right:
            if self.direction != "left":
                self.direction = "right"

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        top_board = rect.bottom() - Play_zone.number_blocks_y * self.rect_height()

        for coordinates in self.levels[self.level]:
            self.draw_rect(painter, rect.left() + coordinates[0] * self.rect_width(),
                           top_board + coordinates[1] * self.rect_height(), QColor(0x2F4F4F))
        for coordinates in self.food:
            self.draw_rect(painter, rect.left() + coordinates.x * self.rect_width(),
                           top_board + coordinates.y * self.rect_height(), coordinates.color)
            break
        for coordinates in self.snake:
            self.draw_rect(painter, rect.left() + coordinates[0] * self.rect_width(),
                           top_board + coordinates[1] * self.rect_height())

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.is_food_collision()
            self.is_death()
            self.change_level()
            self.update()

    def set_standard_position(self):
        self.direction = "down"
        self.acceleration = 10
        self.msg_acceleration.emit("Speed: x" + str(-(self.acceleration - 20) / 10))
        self.snake = [[5, 10], [5, 11]]
        self.head_x = self.snake[0][0]
        self.head_y = self.snake[0][1]

    def draw_rect(self, painter, x, y, color=QColor(0x1C542D)):
        painter.fillRect(x + 1, y + 1, self.rect_width() - 2,
                         self.rect_height() - 2, color)

    def rect_width(self):
        return self.contentsRect().width() / Play_zone.number_blocks_x

    def rect_height(self):
        return self.contentsRect().height() / Play_zone.number_blocks_y

    def make_levels(self):
        first_level = []
        self.levels[1] = first_level
        second_level = []
        for i in range(0, Play_zone.number_blocks_x):
            second_level.append([i, 0])
            second_level.append([i, Play_zone.number_blocks_y - 1])
        for i in range(0, Play_zone.number_blocks_y):
            second_level.append([0, i])
            second_level.append([Play_zone.number_blocks_x - 1, i])
        self.levels[2] = second_level
        third_level = []
        for i in range(0, Play_zone.number_blocks_x, 6):
            start_wall = random.randint(5, Play_zone.number_blocks_y)
            end_wall = random.randint(5, Play_zone.number_blocks_y)
            if start_wall > end_wall:
                start_wall, end_wall = end_wall, start_wall
            for j in range(start_wall, end_wall):
                third_level.append([i, j])
        self.levels[3] = third_level
        fourth_level = []
        for i in range(0, Play_zone.number_blocks_x, 6):
            for j in range(0, Play_zone.number_blocks_y, 6):
                fourth_level.append([i, j])
        self.levels[4] = fourth_level

    def move_snake(self):
        if self.direction == "left":
            self.head_x, self.head_y = self.head_x - 1, self.head_y
            if self.head_x < 0:
                self.head_x = Play_zone.number_blocks_x - 1

        if self.direction == "right":
            self.head_x, self.head_y = self.head_x + 1, self.head_y
            if self.head_x == Play_zone.number_blocks_x:
                self.head_x = 0

        if self.direction == "down":
            self.head_x, self.head_y = self.head_x, self.head_y + 1
            if self.head_y == Play_zone.number_blocks_y:
                self.head_y = 0

        if self.direction == "up":
            self.head_x, self.head_y = self.head_x, self.head_y - 1
            if self.head_y < 0:
                self.head_y = Play_zone.number_blocks_y

        head = [self.head_x, self.head_y]
        self.snake.insert(0, head)

        if not self.score_changed:
            self.snake.pop()

        else:
            self.msg_score.emit("Score: " + str(self.score))
            self.score_changed = False
            if self.speed_changed:
                self.msg_acceleration.emit("Speed: x" + str(-(self.acceleration - 20) / 10))
                self.timer.stop()
                self.start()
                self.speed_changed = False
            if self.grow_snake:
                self.grow_snake = False
            else:
                self.snake.pop()
                if len(self.snake) > 2:
                    self.snake.pop()
                self.decrease_snake = False

    def change_level(self):
        if len(self.snake) >= self.max_len:
            self.timer.stop()
            if len(self.levels) > self.level:
                self.set_standard_position()
                self.level += 1
                self.msg_level.emit("Level: " + str(self.level))
                self.start()
            else:
                self.update()
                self.end_game("You won")

    def is_death(self):
        death = False
        for coordinates in self.levels[self.level]:
            if coordinates == self.snake[0]:
                death = True
                break
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                death = True
                break
        if death:
            self.timer.stop()
            self.lives -= 1
            self.msg_lives.emit("Lives: " + str(self.lives))
            if self.lives > 0:
                self.set_standard_position()
                self.start()
            else:
                self.update()
                self.end_game("You lose")

    def is_food_collision(self):
        max_speed = 15
        for coordinates in self.food:
            if coordinates.x == self.snake[0][0] and coordinates.y == self.snake[0][1]:
                self.food.remove(coordinates)
                self.score += coordinates.score
                self.score_changed = True
                if (self.acceleration >= 0.2 and coordinates.acceleration < 0) or \
                        (self.acceleration <= max_speed and coordinates.acceleration > 0):
                    self.speed_changed = True
                    self.acceleration += coordinates.acceleration
                if coordinates.grow != - 1:
                    self.grow_snake = True
                else:
                    self.decrease_snake = True
                self.drop_food()

    def drop_food(self):
        x = random.randint(3, 38)
        y = random.randint(3, 24)

        for coordinates in self.levels[self.level]:
            if coordinates == [x, y]:
                self.drop_food()

        for coordinates in self.snake:
            if coordinates == [x, y]:
                self.drop_food()
        self.food.append(Food(x, y))

    def end_game(self, message):
        end = QMessageBox()
        end.setWindowTitle("game over")
        end.setText(message + "\nAnother one?")
        end.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        end.buttonClicked.connect(self.button_handler)
        end.exec_()

    def button_handler(self, button):
        if button.text() == "&Yes":
            self.restart()

    def restart(self):
        self.set_standard_position()
        self.score = 0
        self.food = []
        self.lives = 3
        self.level = 1
        self.drop_food()
        self.msg_acceleration.emit("Speed: x" + str(-(self.acceleration - 20) / 10))
        self.msg_lives.emit("Lives: " + str(self.lives))
        self.msg_score.emit("Score: " + str(self.score))
        self.msg_level.emit("Level: " + str(self.level))
        self.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
