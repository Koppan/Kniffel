import sys
from qtpy import QtWidgets
from kniffel_gui.mainwindow import Ui_MainWindow
from random import choice
from PyQt5 import QtGui, QtCore

app = QtWidgets.QApplication(sys.argv)

FIRST_ROLL = 1
dice_count = 5
THROWS = ['_', '_', '_', '_', '_']
PLAYER = 1

PLAYERS = []


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.knifwin = Ui_MainWindow()
        self.knifwin.setupUi(self)
        self.setWindowTitle('KNIFFELLLLLLLLL!!!')

        self.knifwin.roll_btn.clicked.connect(self.roll)
        self.knifwin.new_throw.clicked.connect(self.reset_dices)
        self.knifwin.first_roll.clicked.connect(self.btn1_press)
        self.knifwin.second_roll.clicked.connect(self.btn2_press)
        self.knifwin.third_roll.clicked.connect(self.btn3_press)
        self.knifwin.fourth_roll.clicked.connect(self.btn4_press)
        self.knifwin.fifth_roll.clicked.connect(self.btn5_press)

        self.knifwin.calc_top.released.connect(self.calc_top)
        self.knifwin.calc_bottom.released.connect(self.calc_bottom)
        self.knifwin.calc_total.released.connect(self.calc_total)

        self.knifwin.tableWidget.currentCellChanged.connect(self.calc_total)
        # self.knifwin.tableWidget.cellClicked.connect(self.calc_total)

        self.knifwin.np_button.released.connect(self.next_player)

        global PLAYER, PLAYERS
        player_count = int(input('How many players?'))
        PLAYER = player_count
        for i in range(int(player_count)):
            PLAYERS.append(i)
        # print(PLAYERS, len(PLAYERS))

        self.knifwin.tableWidget.setColumnCount(player_count + 1)
        # PLAYERS = PLAYERS[2:]
        # print(PLAYERS)

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)

        brush2 = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush2.setStyle(QtCore.Qt.Dense5Pattern)

        brush3 = QtGui.QBrush(QtGui.QColor(51, 51, 51, 255))
        brush3.setStyle(QtCore.Qt.Dense4Pattern)

        for item in PLAYERS:
            for i in range(len(PLAYERS)):
                self.knifwin.tableWidget.setHorizontalHeaderItem(item + 1,
                                                                 QtWidgets.QTableWidgetItem(f'Spieler {item + 1}'))

        for item in PLAYERS:
            for i in range(19):
                self.knifwin.tableWidget.setItem(i, item + 1, QtWidgets.QTableWidgetItem())

        for item in PLAYERS:
            for i in range(9, 16):
                self.knifwin.tableWidget.setItem(i, item + 1, QtWidgets.QTableWidgetItem('0'))

        for item in PLAYERS:
            for row in range(0, 6):
                self.knifwin.tableWidget.setItem(row, item + 1, QtWidgets.QTableWidgetItem('0'))
                self.knifwin.tableWidget.item(6, item + 1).setBackground(brush)
                self.knifwin.tableWidget.item(7, item + 1).setText('Plus 35 Pkt.')

                self.knifwin.tableWidget.item(8, item + 1).setBackground(brush2)
                self.knifwin.tableWidget.item(16, item + 1).setBackground(brush)
                self.knifwin.tableWidget.item(17, item + 1).setBackground(brush3)
                self.knifwin.tableWidget.item(18, item + 1).setBackground(brush2)

    def roll(self):
        # throw_string = ''
        font = QtGui.QFont()
        font.setPointSize(30)

        if not self.knifwin.first_roll.isDefault():
            self.knifwin.first_roll.setText(str(self.roll_dice(0)))
            self.knifwin.first_roll.setFont(font)
        if not self.knifwin.second_roll.isDefault():
            self.knifwin.second_roll.setText(str(self.roll_dice(1)))
            self.knifwin.second_roll.setFont(font)
        if not self.knifwin.third_roll.isDefault():
            self.knifwin.third_roll.setText(str(self.roll_dice(2)))
            self.knifwin.third_roll.setFont(font)
        if not self.knifwin.fourth_roll.isDefault():
            self.knifwin.fourth_roll.setText(str(self.roll_dice(3)))
            self.knifwin.fourth_roll.setFont(font)
        if not self.knifwin.fifth_roll.isDefault():
            self.knifwin.fifth_roll.setText(str(self.roll_dice(4)))
            self.knifwin.fifth_roll.setFont(font)
        self.calc_top()
        self.calc_bottom()

    #  for throw in THROWS:
    #    throw_string += str(throw)
    # print(throw_string)

    def reset_dices(self):
        self.knifwin.first_roll.setDefault(False)
        self.knifwin.second_roll.setDefault(False)
        self.knifwin.third_roll.setDefault(False)
        self.knifwin.fourth_roll.setDefault(False)
        self.knifwin.fifth_roll.setDefault(False)
        self.roll()

    def roll_dice(self, dice):
        roll_nums = [1, 2, 3, 4, 5, 6]
        dice1_roll = choice(roll_nums)
        THROWS[dice] = dice1_roll
        return dice1_roll

    def btn1_press(self):
        global dice_count
        if not self.knifwin.first_roll.isDefault():
            self.knifwin.first_roll.setDefault(True)
            dice_count -= 1
        else:
            self.knifwin.first_roll.setDefault(False)
            dice_count += 1
        # print(dice_count)

    def btn2_press(self):
        global dice_count
        if not self.knifwin.second_roll.isDefault():
            self.knifwin.second_roll.setDefault(True)
            dice_count -= 1
        else:
            self.knifwin.second_roll.setDefault(False)
            dice_count += 1
        # print(dice_count)

    def btn3_press(self):
        global dice_count
        if not self.knifwin.third_roll.isDefault():
            self.knifwin.third_roll.setDefault(True)
            dice_count -= 1
        else:
            self.knifwin.third_roll.setDefault(False)
            dice_count += 1
        # print(dice_count)

    def btn4_press(self):
        global dice_count
        if not self.knifwin.fourth_roll.isDefault():
            self.knifwin.fourth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.knifwin.fourth_roll.setDefault(False)
            dice_count += 1
        # print(dice_count)

    def btn5_press(self):
        global dice_count
        if not self.knifwin.fifth_roll.isDefault():
            self.knifwin.fifth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.knifwin.fifth_roll.setDefault(False)
            dice_count += 1
        # print(dice_count)

    def calc_top(self):
        row_content_top = list()
        for i in range(6):
            r = self.knifwin.tableWidget.item(i, PLAYER).text()
            row_content_top.append(r)
        # print(row_content_top)

        row_counter = 0
        for item in row_content_top:
            row_counter += int(item)
        # print(row_counter)

        self.knifwin.tableWidget.setItem(6, PLAYER, QtWidgets.QTableWidgetItem(str(row_counter)))

        total = self.calc_bonus()
        if row_counter >= 63:
            self.knifwin.tableWidget.setItem(17, PLAYER, QtWidgets.QTableWidgetItem(str(total)))
        else:
            self.knifwin.tableWidget.setItem(17, PLAYER, QtWidgets.QTableWidgetItem(str(row_counter)))
        # self.knifwin.tableWidget.item(6, 1).setBackground(QtGui.QColor(125, 125, 125, 120))

        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.Dense4Pattern)
        self.knifwin.tableWidget.item(17, PLAYER).setBackground(brush)

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)
        self.knifwin.tableWidget.item(6, PLAYER).setBackground(brush)

        self.calc_bonus()

    def calc_bonus(self):
        total_top_noBonus = int(self.knifwin.tableWidget.item(6, PLAYER).text())
        total_top = 0
        if total_top_noBonus >= 63:
            total_top = total_top_noBonus + 35
            self.knifwin.tableWidget.setItem(8, PLAYER, QtWidgets.QTableWidgetItem(str(total_top)))

            brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
            brush.setStyle(QtCore.Qt.Dense5Pattern)
            self.knifwin.tableWidget.item(8, PLAYER).setBackground(brush)
        # print(total_top)
        return total_top

    def calc_bottom(self):
        row_content_bottom = list()
        for i in range(9, 16):
            r = self.knifwin.tableWidget.item(i, PLAYER).text()
            row_content_bottom.append(r)
        # print(row_content_bottom)

        row_counter = 0
        for item in row_content_bottom:
            row_counter += int(item)
        # print(row_counter)

        self.knifwin.tableWidget.setItem(16, PLAYER, QtWidgets.QTableWidgetItem(str(row_counter)))

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)
        self.knifwin.tableWidget.item(16, PLAYER).setBackground(brush)

    def calc_total(self):
        self.calc_top()
        self.calc_bottom()
        top = int(self.knifwin.tableWidget.item(17, PLAYER).text())
        bottom = int(self.knifwin.tableWidget.item(16, PLAYER).text())
        total = top + bottom
        # print(total)

        self.knifwin.tableWidget.setItem(18, PLAYER, QtWidgets.QTableWidgetItem(str(total)))

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense5Pattern)
        self.knifwin.tableWidget.item(18, PLAYER).setBackground(brush)

    def next_player(self):

        self.reset_dices()

        global PLAYER

        if PLAYER >= len(PLAYERS):
            PLAYER = 1
        else:
            PLAYER += 1
        # print(f'current player playing is player: {PLAYER}!')

        brush = QtGui.QBrush(QtGui.QColor(52, 235, 161))
        default_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        if PLAYER == 1:
            self.knifwin.tableWidget.horizontalHeaderItem(len(PLAYERS)).setBackground(default_brush)
            self.knifwin.tableWidget.horizontalHeaderItem(1).setBackground(brush)
        else:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER - 1).setBackground(default_brush)
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush)


wn = MainWindow()
wn.show()
sys.exit(app.exec_())
