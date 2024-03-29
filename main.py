import random
import sys
import json
from collections import deque
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal, QBasicTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame, QMainWindow, QMessageBox


class Ui_MainWindow(QMainWindow):
    WIDTH = 700
    HEIGHT = 600
    TEXT_PANEL_HEIGHT = 140
    BACKGROUND_HEIGHT = 460
    BOARD = "board.png"
    BACKGROUND = "Background.jpg"

    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.WIDTH, self.HEIGHT)
        MainWindow.setStyleSheet("")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.setup_ui_menu(MainWindow)

    def setup_ui_main_widgets(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, self.WIDTH, self.BACKGROUND_HEIGHT))
        self.background.setText("")
        self.background.setTextFormat(QtCore.Qt.PlainText)
        self.background.setPixmap(QtGui.QPixmap(self.BACKGROUND))

        self.board = QtWidgets.QLabel(self.centralwidget)
        self.board.setGeometry(QtCore.QRect(0, self.BACKGROUND_HEIGHT, self.WIDTH, self.TEXT_PANEL_HEIGHT))
        self.board.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 255, 123), stop:1 rgba(255, 255, 255, 255));")
        self.board.setText("")
        self.board.setPixmap(QtGui.QPixmap(self.BOARD))
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
        self.play_zone.setGeometry(QtCore.QRect(0, 0, self.WIDTH, self.BACKGROUND_HEIGHT))
        self.play_zone.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.play_zone.setFrameShadow(QtWidgets.QFrame.Raised)
        self.play_zone.setObjectName("play_zone")
        self.play_zone.msg_score[str].connect(self.text_score.setText)
        self.play_zone.msg_acceleration[str].connect(self.text_speed.setText)
        self.play_zone.msg_lives[str].connect(self.text_lives.setText)
        self.play_zone.msg_level[str].connect(self.text_level.setText)
        self.play_zone.msg_exit.connect(self.back_to_menu_from_play_zone)
        self.play_zone.start()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_play_zone_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def back_to_menu_from_play_zone(self):
        self.centralwidget.hide()
        self.setup_ui_menu(self.main_window)

    def retranslate_play_zone_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))
        self.text_level.setText(_translate("MainWindow", "Level: " + str(self.play_zone.level)))
        self.text_score.setText(_translate("MainWindow", "Score: " + str(self.play_zone.score)))
        self.text_lives.setText(_translate("MainWindow", "Lives: " + str(self.play_zone.lives)))
        self.text_speed.setText(_translate("MainWindow", "Speed: x" + str(-(self.play_zone.acceleration - 20) / 10)))

    def setup_ui_menu(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.WIDTH, self.HEIGHT)

        self.menu_widget = QtWidgets.QWidget(MainWindow)
        self.menu_widget.setObjectName("menu_widget")

        self.menu_background = QtWidgets.QLabel(self.menu_widget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, self.WIDTH, self.HEIGHT))
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
        self.text_start.clicked.connect(self.from_menu_to_play_zone)

        self.text_info = QtWidgets.QPushButton(self.menu_widget)
        self.text_info.setGeometry(QtCore.QRect(100, 220, 500, 100))
        self.text_info.setFont(font)
        self.text_info.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(227, 239, 227, 181), stop:1 rgba(255, 255, 255, 255));")
        self.text_info.setObjectName("info")
        self.text_info.clicked.connect(self.from_menu_to_info)

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

    def from_menu_to_play_zone(self):
        self.menu_widget.hide()
        self.setup_ui_main_widgets(self.main_window)

    def from_menu_to_info(self):
        self.menu_widget.hide()
        self.setup_info_Ui(self.main_window)

    def from_info_to_menu(self):
        self.info_centralwidget.hide()
        self.setup_ui_menu(self.main_window)

    def exit(self):
        self.main_window.close()

    def setup_info_Ui(self, MainWindow):
        self.info_centralwidget = QtWidgets.QWidget(MainWindow)
        self.info_centralwidget.setObjectName("info_centralwidget")
        self.info_background = QtWidgets.QLabel(self.info_centralwidget)
        self.info_background.setGeometry(QtCore.QRect(0, 0, self.WIDTH, self.HEIGHT))
        self.info_background.setText("")
        self.info_background.setPixmap(QtGui.QPixmap("info.jpg"))
        self.info_background.setObjectName("info_background")

        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(14)

        self.pushButton = QtWidgets.QPushButton(self.info_centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 500, 150, 70))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0.488636, x2:1, y2:0.494318, stop:0 rgba(219, 217, 168, 255), stop:1 rgba(255, 255, 255, 255));")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.from_info_to_menu)

        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)

        self.info_text = QtWidgets.QLabel(self.info_centralwidget)
        self.info_text.setGeometry(QtCore.QRect(80, 30, 570, 180))
        self.info_text.setFont(font)
        self.info_text.setObjectName("info_text")

        font.setPointSize(11)

        self.wall_color = QtWidgets.QLabel(self.info_centralwidget)
        self.wall_color.setGeometry(QtCore.QRect(80, 210, 520, 40))
        self.wall_color.setFont(font)
        self.wall_color.setStyleSheet("background-color: rgb(47, 79, 79);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "")
        self.wall_color.setObjectName("wall_color")

        self.decrease_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.decrease_colour.setGeometry(QtCore.QRect(80, 330, 520, 40))
        self.decrease_colour.setFont(font)
        self.decrease_colour.setStyleSheet("background-color: rgb(140, 23, 120);\n"
                                           "color: rgb(255, 255, 255);")
        self.decrease_colour.setObjectName("decrease_colour")

        self.default_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.default_colour.setGeometry(QtCore.QRect(80, 290, 520, 40))
        self.default_colour.setFont(font)
        self.default_colour.setStyleSheet("background-color: rgb(239, 211, 52);")
        self.default_colour.setObjectName("default_colour")

        self.portal_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.portal_colour.setGeometry(QtCore.QRect(80, 250, 520, 40))
        self.portal_colour.setFont(font)
        self.portal_colour.setStyleSheet("background-color: rgb(227, 187, 242);")
        self.portal_colour.setObjectName("portal_colour")

        self.bonus_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.bonus_colour.setGeometry(QtCore.QRect(80, 450, 520, 40))
        self.bonus_colour.setFont(font)
        self.bonus_colour.setStyleSheet("background-color: rgb(237, 72, 48);")
        self.bonus_colour.setObjectName("bonus_colour")

        self.fast_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.fast_colour.setGeometry(QtCore.QRect(80, 410, 520, 40))
        self.fast_colour.setFont(font)
        self.fast_colour.setStyleSheet("background-color: rgb(50, 18, 122);\n"
                                       "color: rgb(255, 255, 255);")
        self.fast_colour.setObjectName("fast_colour")

        self.slow_colour = QtWidgets.QLabel(self.info_centralwidget)
        self.slow_colour.setGeometry(QtCore.QRect(80, 370, 520, 40))
        self.slow_colour.setFont(font)
        self.slow_colour.setStyleSheet("background-color: rgb(0, 197, 205);")
        self.slow_colour.setObjectName("slow_colour")

        MainWindow.setCentralWidget(self.info_centralwidget)

        self.retranslate_info_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_info_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Back"))
        self.info_text.setText(_translate("MainWindow",
                                          "<html><head/><body><p>Управление змейкой происходит с помощью стрелок</p><p>Q - сохранить игру</p><p>W - выйти из игры </p><p>После запуска игры щелкните мышкой по игровому полю</p><p>Обозначения:</p><p><br/></p></body></html>"))
        self.wall_color.setText(_translate("MainWindow", "- преграда"))

        self.decrease_colour.setText(_translate("MainWindow", "- еда уменьшающая змейку"))
        self.default_colour.setText(_translate("MainWindow", "- стандартная еда"))
        self.portal_colour.setText(_translate("MainWindow", "- портал"))
        self.bonus_colour.setText(_translate("MainWindow", "- еда с бонусными очками"))
        self.fast_colour.setText(_translate("MainWindow", "- еда увеличивающая скорость"))
        self.slow_colour.setText(_translate("MainWindow", "- еда уменьшающая скорость"))


class food:
    DEFAULT_COLOUR = 0xEFD334
    BONUS_COLOUR = 0xED4830
    DECREASE_COLOUR = 0x8C1778
    FAST_COLOUR = 0x32127A
    SLOW_COLOUR = 0x00C5CD

    acceleration = 0
    score = 1
    grow = 1

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        fillers = [self.default_score, self.default_score, self.default_score, self.default_score,
                   self.default_score, self.bonus_score, self.decrease_score, self.fast_score, self.fast_score,
                   self.slow_score]
        self.type = random.choice(fillers)()

    def default_score(self):
        self.color = QColor(self.DEFAULT_COLOUR)
        return 0

    def bonus_score(self):
        self.color = QColor(self.BONUS_COLOUR)
        self.score = 3
        return 1

    def decrease_score(self):
        self.color = QColor(self.DEFAULT_COLOUR)
        self.grow = -1
        return 2

    def fast_score(self):
        self.color = QColor(self.FAST_COLOUR)
        self.acceleration = -1
        return 3

    def slow_score(self):
        self.color = QColor(self.SLOW_COLOUR)
        self.acceleration = 1
        return 4

    def fill_by_type(self, food_type, x, y):
        fillers = [self.default_score, self.bonus_score, self.decrease_score, self.fast_score, self.slow_score]
        self.type = fillers[food_type]()
        self.x = x
        self.y = y


class Play_zone(QFrame):
    NUMBER_BLOCKS_X = 40
    NUMBER_BLOCKS_Y = 26

    SNAKE_COLOUR = 0x1C542D
    WALL_COLOUR = 0x2F4F4F
    PORTAL_COLOUR = 0xe3bbf2

    START_POSITION = [[5, 11], [5, 10]]
    MAX_LEVEL = 4
    MAX_LEN = 4

    default_speed = 120
    start_speed = 10
    start_direction = "down"
    live_count = 3

    msg_score = pyqtSignal(str)
    msg_acceleration = pyqtSignal(str)
    msg_lives = pyqtSignal(str)
    msg_level = pyqtSignal(str)
    msg_exit = pyqtSignal()

    def __init__(self, parent):
        super(Play_zone, self).__init__(parent)
        if os.path.exists("save.txt"):
            with open("save.txt", "r") as save:
                line = save.read()
            if len(line) > 0:
                save_box = QMessageBox()
                save_box.setWindowTitle("save")
                save_box.setText("Do you want to continue the game?")
                save_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                save_box.buttonClicked.connect(self.button_handler_start)
                save_box.exec_()
        else:
            self.new_run()

        self.directions = deque()
        self.timer = QBasicTimer()
        self.grow_snake = False
        self.speed_changed = False
        self.score_changed = False
        self.decrease_snake = False
        self.setFocusPolicy(Qt.StrongFocus)

    @staticmethod
    def new_direction(current_direction, directions):
        if len(directions) > 0:
            new_direction = directions.popleft()
            if new_direction == "down":
                if current_direction != "up":
                    return "down"

            elif new_direction == "up":
                if current_direction != "down":
                    return "up"

            elif new_direction == "left":
                if current_direction != "right":
                    return "left"

            elif new_direction == "right":
                if current_direction != "left":
                    return "right"
        return current_direction

    @staticmethod
    def make_levels():
        levels = {"1": []}
        second_level = []
        for i in range(0, Play_zone.NUMBER_BLOCKS_X):
            second_level.append([i, 0])
            second_level.append([i, Play_zone.NUMBER_BLOCKS_Y - 1])
        for i in range(0, Play_zone.NUMBER_BLOCKS_Y):
            second_level.append([0, i])
            second_level.append([Play_zone.NUMBER_BLOCKS_X - 1, i])
        levels["2"] = second_level
        third_level = []
        for i in range(0, Play_zone.NUMBER_BLOCKS_X, 6):
            start_wall = random.randint(5, Play_zone.NUMBER_BLOCKS_Y)
            end_wall = random.randint(5, Play_zone.NUMBER_BLOCKS_Y)
            if start_wall > end_wall:
                start_wall, end_wall = end_wall, start_wall
            for j in range(start_wall, end_wall):
                third_level.append([i, j])
        levels["3"] = third_level
        fourth_level = []
        for i in range(0, Play_zone.NUMBER_BLOCKS_X, 6):
            for j in range(0, Play_zone.NUMBER_BLOCKS_Y, 6):
                fourth_level.append([i, j])
        levels["4"] = fourth_level
        return levels

    @staticmethod
    def load_levels(data):
        levels = Play_zone.make_levels()
        levels['3'] = data['levels']['3']
        return levels

    @staticmethod
    def make_step(direction, head_x, head_y):
        if direction == "left":
            head_x, head_y = head_x - 1, head_y
            if head_x < 0:
                head_x = Play_zone.NUMBER_BLOCKS_X - 1

        if direction == "right":
            head_x, head_y = head_x + 1, head_y
            if head_x == Play_zone.NUMBER_BLOCKS_X:
                head_x = 0

        if direction == "down":
            head_x, head_y = head_x, head_y + 1
            if head_y == Play_zone.NUMBER_BLOCKS_Y:
                head_y = 0

        if direction == "up":
            head_x, head_y = head_x, head_y - 1
            if head_y < 0:
                head_y = Play_zone.NUMBER_BLOCKS_Y

        return [head_x, head_y]

    @staticmethod
    def check_death(head, level, snake):
        for coordinates in level:
            if coordinates == head:
                return True
        for snake_point in snake[1:]:
            if snake_point == head:
                return True
        return False

    def button_handler_start(self, button):

        if button.text() == "&Yes":
            with open("save.txt", "r") as save:
                try:
                    line = save.read()
                    data = json.loads(line)

                    self.score = data["snake"]["score"]
                    self.lives = data["snake"]["lives"]
                    self.level = data["snake"]["level"]
                    self.direction = data["snake"]["direction"]
                    self.acceleration = data["snake"]["acceleration"]
                    self.snake = data["snake"]["body"]
                    self.portals = data["portals"]
                    self.levels = Play_zone.load_levels(data)
                    self.food = []
                    for food_data in data["food"]:
                        food_ = food()
                        food_.fill_by_type(food_data["type"], food_data["pos_x"], food_data["pos_y"])
                        self.food.append(food_)

                except:
                    save_box = QMessageBox()
                    save_box.setWindowTitle("ERROR")
                    save_box.setText("SORRY, your save data is corrupted. You will start from beginning")
                    save_box.setStandardButtons(QMessageBox.Ok)
                    save_box.exec_()
                    self.new_run()

        else:
            self.new_run()

    def new_run(self):
        
        self.direction = self.start_direction
        self.set_standard_position()
        self.score = 0
        self.lives = self.live_count
        self.level = 1
        self.levels = self.make_levels()
        self.portals = dict()
        self.make_portal()
        self.food = []
        self.drop_food()

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

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        top_board = rect.bottom() - Play_zone.NUMBER_BLOCKS_Y * self.rect_height()

        for portal in self.portals[str(self.level)]:
            self.draw_rect(painter, rect.left() + portal[0] * self.rect_width(),
                           top_board + portal[1] * self.rect_height(), QColor(self.PORTAL_COLOUR))

        for wall in self.levels[str(self.level)]:
            self.draw_rect(painter, rect.left() + wall[0] * self.rect_width(),
                           top_board + wall[1] * self.rect_height(), QColor(self.WALL_COLOUR))

        for food in self.food:
            self.draw_rect(painter, rect.left() + food.x * self.rect_width(),
                           top_board + food.y * self.rect_height(), food.color)
            break
        for snake in self.snake:
            self.draw_rect(painter, rect.left() + snake[0] * self.rect_width(),
                           top_board + snake[1] * self.rect_height(), QColor(self.SNAKE_COLOUR))

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
        self.acceleration = self.start_speed
        self.msg_acceleration.emit("Speed: x" + self.generate_speed_text())
        self.snake = self.START_POSITION.copy()
        self.snake[0][0] = self.snake[0][0]
        self.snake[0][1] = self.snake[0][1]

    def draw_rect(self, painter, x, y, color):
        painter.fillRect(x + 1, y + 1, self.rect_width() - 2,
                         self.rect_height() - 2, color)

    def rect_width(self):
        return self.contentsRect().width() / Play_zone.NUMBER_BLOCKS_X

    def rect_height(self):
        return self.contentsRect().height() / Play_zone.NUMBER_BLOCKS_Y

    def move_snake(self):
        self.direction = self.new_direction(self.direction, self.directions)

        if self.is_portal():
            if self.snake[0] == self.portals[str(self.level)][0]:
                snake_x, snake_y = self.portals[str(self.level)][1][0], self.portals[str(self.level)][1][1]
            else:
                snake_x, snake_y = self.portals[str(self.level)][0][0], self.portals[str(self.level)][0][1]
            head = [snake_x, snake_y]
        else:

            head = self.make_step(self.direction, self.snake[0][0], self.snake[0][1])

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
                if len(self.snake) > 2:
                    self.snake.pop()
                self.decrease_snake = False

    def generate_speed_text(self):
        return str((20 - self.acceleration) / 10)

    def change_level(self):
        if len(self.snake) >= self.MAX_LEN and self.level < self.MAX_LEVEL:
            self.timer.stop()
            self.set_standard_position()
            self.level += 1
            self.msg_level.emit("Level: " + str(self.level))
            self.start()
            self.drop_food()

    def is_death(self):
        death = self.check_death(self.snake[0], self.levels[str(self.level)], self.snake)
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
        portal = self.portals[str(self.level)]
        return (self.snake[0] == portal[0] and self.snake[1] != portal[1]) or \
               (self.snake[0] == portal[1] and self.snake[1] != portal[0])

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
        if len(self.food) >= 1:
            self.food = []
        x = random.randint(3, self.NUMBER_BLOCKS_X - 2)
        y = random.randint(3, self.NUMBER_BLOCKS_Y - 2)

        for portal in self.portals[str(self.level)]:
            if portal == [x, y]:
                self.drop_food()
                return

        for level in self.levels[str(self.level)]:
            if level == [x, y]:
                self.drop_food()
                return

        for snake in self.snake:
            if snake == [x, y]:
                self.drop_food()
                return
        self.food.append(food(x, y))

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
            f = json.dumps(
                {
                    "snake": {
                        "direction": self.direction, "acceleration": self.acceleration,
                        "body": self.snake, "head_x": self.snake[0][0], "head_y": self.snake[0][1],
                        "score": self.score, "lives": self.lives, "level": self.level,
                    },
                    "levels": {"3": self.levels['3']},
                    "portals": self.portals,
                    "food": [
                        {"pos_x": self.food[i].x, "pos_y": self.food[i].y, "type": self.food[i].type}
                        for i in range(len(self.food))
                    ]
                }
            )
            with open("save.txt", "w") as save:
                save.write(f)
            self.start()
        else:
            self.start()

    def make_portal(self):
        self.portals = {}
        x_enter = random.randint(12, self.NUMBER_BLOCKS_X - 2)
        y_enter = random.randint(12, self.NUMBER_BLOCKS_Y - 2)
        x_exit = random.randint(12, self.NUMBER_BLOCKS_X - 2)
        y_exit = random.randint(12, self.NUMBER_BLOCKS_Y - 2)
        while x_enter == x_exit and y_enter == y_exit:
            x_exit = random.randint(12, self.NUMBER_BLOCKS_X - 2)
            y_exit = random.randint(12, self.NUMBER_BLOCKS_Y - 2)
        self.portals["1"] = [[x_enter, y_enter], [x_exit, y_exit]]
        self.portals["2"] = [[self.NUMBER_BLOCKS_X // 2, 5], [self.NUMBER_BLOCKS_X // 2, self.NUMBER_BLOCKS_Y - 5]]
        self.portals["3"] = [[6 * random.randint(2, 4) + 3, self.NUMBER_BLOCKS_Y // 2],
                             [6 * random.randint(2, 4) + 5, self.NUMBER_BLOCKS_Y // 2]]
        self.portals["4"] = [[7, 7], [21, 21]]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
