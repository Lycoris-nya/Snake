import random
import sys
import json
from collections import deque

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
        self.setup_ui_menu(MainWindow)

    def setup_ui_main_widgets(self, MainWindow):
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
        self.text_speed.setGeometry(QtCore.QRect(480, 515, 190, 40))
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
        self.play_zone.msg_exit.connect(self.back_to_menu)
        self.play_zone.start()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def back_to_menu(self):
        self.centralwidget.hide()
        self.setup_ui_menu(self.mv)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))
        self.text_level.setText(_translate("MainWindow", "Level: " + str(self.play_zone.level)))
        self.text_score.setText(_translate("MainWindow", "Score: " + str(self.play_zone.score)))
        self.text_lives.setText(_translate("MainWindow", "Lives: " + str(self.play_zone.lives)))
        self.text_speed.setText(_translate("MainWindow", "Speed: x" + str(-(self.play_zone.acceleration - 20) / 10)))

    def setup_ui_menu(self, MainWindow):
        self.mv = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)

        self.menu_widget = QtWidgets.QWidget(MainWindow)
        self.menu_widget.setObjectName("menu_widget")

        self.menu_background = QtWidgets.QLabel(self.menu_widget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.menu_background.setText("")
        self.menu_background.setPixmap(QtGui.QPixmap("2693280.jpg"))
        self.menu_background.setObjectName("menu_background")

        self.text_start = QtWidgets.QPushButton(self.menu_widget)
        self.text_start.setGeometry(QtCore.QRect(100, 80, 500, 100))

        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)

        self.text_start.setFont(font)
        self.text_start.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.text_start.setObjectName("start")
        self.text_start.clicked.connect(self.start)

        self.text_info = QtWidgets.QPushButton(self.menu_widget)
        self.text_info.setGeometry(QtCore.QRect(100, 220, 500, 100))
        self.text_info.setFont(font)
        self.text_info.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.text_info.setObjectName("info")

        self.text_exit = QtWidgets.QPushButton(self.menu_widget)
        self.text_exit.setGeometry(QtCore.QRect(100, 360, 500, 100))
        self.text_exit.setFont(font)
        self.text_exit.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.text_exit.setObjectName("exit")
        self.text_exit.clicked.connect(self.exit)

        MainWindow.setCentralWidget(self.menu_widget)

        self.retranslate_menu_Ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_menu_Ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.text_start.setText(_translate("MainWindow", "Start"))
        self.text_info.setText(_translate("MainWindow", "Info"))
        self.text_exit.setText(_translate("MainWindow", "Exit"))

    def start(self):
        self.menu_widget.hide()
        self.setup_ui_main_widgets(self.mv)

    def exit(self):
        self.mv.close()


# class Portal():
#
#     color_1 = 0xf5ffff
#     color_2 = 0xc3cef7
#     color_3 = 0xe3bbf2
#
#     def __init__(self, x, y, color):
#         self.x = x
#         self.y = y
#         if color == 1:
#             self.color = self.color_1
#         elif color == 2:
#             self.color = self.color_2
#         else:
#             self.color = self.color_3


class Food:
    acceleration = 0
    score = 1
    grow = 1
    default_colour = 0xEFD334
    bonus_colour = 0xED4830
    decrease_colour = 0x8C1778
    fast_colour = 0x32127A
    slow_colour = 0x00C5CD

    def __init__(self, x, y):
        self.x = x
        self.y = y
        constructors = [self.default_score, self.default_score, self.default_score, self.default_score,
                        self.default_score, self.bonus_score, self.decrease_score, self.fast_score, self.fast_score,
                        self.slow_score]
        constructors[random.randint(0, 9)]()

    def default_score(self):
        self.color = QColor(self.default_colour)

    def bonus_score(self):
        self.color = QColor(self.bonus_colour)
        self.score = 3

    def decrease_score(self):
        self.color = QColor(self.decrease_colour)
        self.grow = -1

    def fast_score(self):
        self.color = QColor(self.fast_colour)
        self.acceleration = -1

    def slow_score(self):
        self.color = QColor(self.slow_colour)
        self.acceleration = 1


class Play_zone(QFrame):
    number_blocks_x = 40
    number_blocks_y = 26
    max_level = 4
    start_speed = 10
    start_direction = "down"
    last_direction = "down"
    snake_colour = 0x1C542D
    wall_colour = 0x2F4F4F
    portal_color = 0xe3bbf2

    msg_score = pyqtSignal(str)
    msg_acceleration = pyqtSignal(str)
    msg_lives = pyqtSignal(str)
    msg_level = pyqtSignal(str)
    msg_exit = pyqtSignal()

    def __init__(self, parent):
        super(Play_zone, self).__init__(parent)
        with open("save.txt", "r") as q:
            line = q.read()
        if len(line) > 0:
            save_box = QMessageBox()
            save_box.setWindowTitle("save")
            save_box.setText("Do you want to continue the game?")
            save_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            save_box.buttonClicked.connect(self.button_handler_start)
            save_box.exec_()
        else:
            self.new_run()
        self.max_len = 4
        self.directions = deque()
        self.timer = QBasicTimer()
        self.default_speed = 120
        self.food = []
        self.grow_snake = False
        self.speed_changed = False
        self.score_changed = False
        self.decrease_snake = False
        self.drop_food()
        self.setFocusPolicy(Qt.StrongFocus)

    def button_handler_start(self, button):
        if button.text() == "&Yes":
            with open("save.txt", "r") as q:
                line = q.read()
                data = json.loads(line)
                self.levels = data["levels"]
                self.score = data["snake"]["score"]
                self.lives = data["snake"]["lives"]
                self.level = data["snake"]["level"]
                self.direction = data["snake"]["direction"]
                self.acceleration = data["snake"]["acceleration"]
                self.portals = data["portals"]
                self.snake = data["snake"]["body"]
                self.head_x = self.snake[0][0]
                self.head_y = self.snake[0][1]
        else:
            self.new_run()

    def new_run(self):
        self.set_standard_position()
        self.score = 0
        self.lives = 3
        self.level = 1
        self.levels = dict()
        self.portals = dict()
        self.make_levels()
        self.make_portal()

    def saved_run(self):
        pass

    def start(self):
        self.timer.start(self.default_speed * self.acceleration // 10, self)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Q:
            self.save()

        if key == Qt.Key_W:
            self.timer.stop()
            self.msg_exit.emit()

        if key == Qt.Key_Down:
            self.directions.append("down")
        elif key == Qt.Key_Up:
            self.directions.append("up")

        elif key == Qt.Key_Left:
            self.directions.append("left")

        elif key == Qt.Key_Right:
            self.directions.append("right")

    def change_direction(self):
        if len(self.directions) > 0:
            new_direction = self.directions.popleft()
            if new_direction == "down":
                if self.direction != "up":
                    self.direction = "down"

            elif new_direction == "up":
                if self.direction != "down":
                    self.direction = "up"

            elif new_direction == "left":
                if self.direction != "right":
                    self.direction = "left"

            elif new_direction == "right":
                if self.direction != "left":
                    self.direction = "right"

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        top_board = rect.bottom() - Play_zone.number_blocks_y * self.rect_height()

        for portal in self.portals[str(self.level)]:
            self.draw_rect(painter, rect.left() + portal[0] * self.rect_width(),
                           top_board + portal[1] * self.rect_height(), QColor(self.portal_color))

        for wall in self.levels[str(self.level)]:
            self.draw_rect(painter, rect.left() + wall[0] * self.rect_width(),
                           top_board + wall[1] * self.rect_height(), QColor(self.wall_colour))

        for food in self.food:
            self.draw_rect(painter, rect.left() + food.x * self.rect_width(),
                           top_board + food.y * self.rect_height(), food.color)
            break
        for snake in self.snake:
            self.draw_rect(painter, rect.left() + snake[0] * self.rect_width(),
                           top_board + snake[1] * self.rect_height(), QColor(self.snake_colour))

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.is_food_collision()
            self.is_death()
            self.change_level()
            self.update()

    def set_standard_position(self):
        self.directions = deque()
        self.direction = self.start_direction
        self.last_direction = self.start_direction
        self.acceleration = self.start_speed
        self.msg_acceleration.emit("Speed: x" + self.generate_speed_text())
        self.snake = [[5, 10], [5, 11]]
        self.head_x = self.snake[0][0]
        self.head_y = self.snake[0][1]

    def draw_rect(self, painter, x, y, color):
        painter.fillRect(x + 1, y + 1, self.rect_width() - 2,
                         self.rect_height() - 2, color)

    def rect_width(self):
        return self.contentsRect().width() / Play_zone.number_blocks_x

    def rect_height(self):
        return self.contentsRect().height() / Play_zone.number_blocks_y

    def make_levels(self):
        first_level = []
        self.levels["1"] = first_level
        second_level = []
        for i in range(0, Play_zone.number_blocks_x):
            second_level.append([i, 0])
            second_level.append([i, Play_zone.number_blocks_y - 1])
        for i in range(0, Play_zone.number_blocks_y):
            second_level.append([0, i])
            second_level.append([Play_zone.number_blocks_x - 1, i])
        self.levels["2"] = second_level
        third_level = []
        for i in range(0, Play_zone.number_blocks_x, 6):
            start_wall = random.randint(5, Play_zone.number_blocks_y)
            end_wall = random.randint(5, Play_zone.number_blocks_y)
            if start_wall > end_wall:
                start_wall, end_wall = end_wall, start_wall
            for j in range(start_wall, end_wall):
                third_level.append([i, j])
        self.levels["3"] = third_level
        fourth_level = []
        for i in range(0, Play_zone.number_blocks_x, 6):
            for j in range(0, Play_zone.number_blocks_y, 6):
                fourth_level.append([i, j])
        self.levels["4"] = fourth_level

    def move_snake(self):
        self.change_direction()
        if self.is_portal():
            if self.snake[0] == self.portals[str(self.level)][0]:
                self.head_x, self.head_y = self.portals[str(self.level)][1][0], self.portals[str(self.level)][1][1]
            else:
                self.head_x, self.head_y = self.portals[str(self.level)][0][0], self.portals[str(self.level)][0][1]
        else:
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
                self.msg_acceleration.emit("Speed: x" + self.generate_speed_text())
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

    def generate_speed_text(self):
        return str((20 - self.acceleration) / 10)

    def change_level(self):
        if len(self.snake) >= self.max_len and self.level < self.max_level:
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
        for coordinates in self.levels[str(self.level)]:
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

    def is_portal(self):
        if (self.snake[0] == self.portals[str(self.level)][0] and self.snake[1] != self.portals[str(self.level)][1]) \
                or (self.snake[0] == self.portals[str(self.level)][1] and self.snake[1] != self.portals[str(self.level)][0]):
            return True
        return False

    def is_food_collision(self):
        max_speed = 15
        for food in self.food:
            if food.x == self.snake[0][0] and food.y == self.snake[0][1]:
                self.food.remove(food)
                self.score += food.score
                self.score_changed = True
                if (self.acceleration >= 0.2 and food.acceleration < 0) or \
                        (self.acceleration <= max_speed and food.acceleration > 0):
                    self.speed_changed = True
                    self.acceleration += food.acceleration
                if food.grow != - 1:
                    self.grow_snake = True
                else:
                    self.decrease_snake = True
                self.drop_food()

    def drop_food(self):
        x = random.randint(3, 38)
        y = random.randint(3, 24)

        for coordinates in self.levels[str(self.level)]:
            if coordinates == [x, y]:
                self.drop_food()
                return

        for coordinates in self.snake:
            if coordinates == [x, y]:
                self.drop_food()
                return
        self.food.append(Food(x, y))

    def end_game(self, message):
        end = QMessageBox()
        end.setWindowTitle("game over")
        end.setText(message + "\nAnother one?")
        end.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        end.buttonClicked.connect(self.button_handler_end_game)
        end.exec_()

    def button_handler_end_game(self, button):
        if button.text() == "&Yes":
            self.restart()
        else:
            self.msg_exit.emit()

    def restart(self):
        self.set_standard_position()
        self.score = 0
        self.food = []
        self.lives = 3
        self.level = 1
        self.drop_food()
        self.msg_acceleration.emit("Speed: x" + self.generate_speed_text())
        self.msg_lives.emit("Lives: " + str(self.lives))
        self.msg_score.emit("Score: " + str(self.score))
        self.msg_level.emit("Level: " + str(self.level))
        self.start()

    def save(self):
        self.timer.stop()
        save_box = QMessageBox()
        save_box.setWindowTitle("save")
        save_box.setText("Do you want to save the game?")
        save_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        save_box.buttonClicked.connect(self.button_handler_save)
        save_box.exec_()

    def button_handler_save(self, button):
        if button.text() == "&Yes":
            f = json.dumps({"snake": {"direction": self.direction, "acceleration": self.acceleration,
                                      "body": self.snake, "head_x": self.snake[0][0], "head_y": self.snake[0][1],
                                      "score": self.score, "lives": self.lives, "level": self.level},
                            "levels": self.levels,
                            "portals": self.portals})
            with open("save.txt", "w") as q:
                q.write(f)
                self.start()
        else:
            self.start()

    def make_portal(self):
        x_enter = random.randint(12, 38)
        y_enter = random.randint(12, 24)
        x_exit = random.randint(12, 38)
        y_exit = random.randint(12, 24)
        while x_enter == x_exit and y_enter == y_exit:
            x_exit = random.randint(12, 38)
            y_exit = random.randint(12, 24)
        self.portals["1"] = [[x_enter, y_enter], [x_exit, y_exit]]
        self.portals["2"] = [[self.number_blocks_x // 2, 5], [self.number_blocks_x // 2, self.number_blocks_y - 5]]
        self.portals["3"] = [[6 * random.randint(2, 4) + 3, self.number_blocks_y // 2],
                             [6 * random.randint(2, 4) + 5, self.number_blocks_y // 2]]
        self.portals["4"] = [[7, 7], [21, 21]]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
