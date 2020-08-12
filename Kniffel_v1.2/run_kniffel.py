import sys
from qtpy import QtWidgets
from kniffel_gui.mainwindow import Ui_MainWindow
from random import choice
from PyQt5 import QtGui, QtCore
import os
from time import sleep

app = QtWidgets.QApplication(sys.argv)

FIRST_ROLL = 1
dice_count = 5
THROWS = ['_', '_', '_', '_', '_']
throws = 0
PLAYER = 1

PLAYERS = []

file_dice_1 = 'kniffel_gui/1.png'
dice_1_pressed = 'kniffel_gui/1_pressed.png'
dice_1 = os.path.join(os.path.abspath(os.getcwd()), file_dice_1)

file_dice_2 = 'kniffel_gui/2.png'
dice_2_pressed = 'kniffel_gui/2_pressed.png'
dice_2 = os.path.join(os.path.abspath(os.getcwd()), file_dice_2)

file_dice_3 = 'kniffel_gui/3.png'
dice_3_pressed = 'kniffel_gui/3_pressed.png'
dice_3 = os.path.join(os.path.abspath(os.getcwd()), file_dice_3)

file_dice_4 = 'kniffel_gui/4.png'
dice_4_pressed = 'kniffel_gui/4_pressed.png'
dice_4 = os.path.join(os.path.abspath(os.getcwd()), file_dice_4)

file_dice_5 = 'kniffel_gui/5.png'
dice_5_pressed = 'kniffel_gui/5_pressed.png'
dice_5 = os.path.join(os.path.abspath(os.getcwd()), file_dice_5)

file_dice_6 = 'kniffel_gui/6.png'
dice_6_pressed = 'kniffel_gui/6_pressed.png'
dice_6 = os.path.join(os.path.abspath(os.getcwd()), file_dice_6)

dices = {'1': dice_1, '2': dice_2, '3': dice_3, '4': dice_4, '5': dice_5, '6': dice_6}

pressed_dices = {'1': dice_1_pressed, '2': dice_2_pressed, '3': dice_3_pressed, '4': dice_4_pressed,
                 '5': dice_5_pressed, '6': dice_6_pressed}

dice1_value = 0
dice2_value = 0
dice3_value = 0
dice4_value = 0
dice5_value = 0


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.knifwin = Ui_MainWindow()
        self.knifwin.setupUi(self)
        self.setWindowTitle('KNIFFELLLLLLLLL!!!')

        self.first_dice = self.knifwin.first_roll
        self.sec_dice = self.knifwin.second_roll
        self.third_dice = self.knifwin.third_roll
        self.fourth_dice = self.knifwin.fourth_roll
        self.fifth_dice = self.knifwin.fifth_roll

        self.knifwin.roll_btn.clicked.connect(self.roll)
        self.first_dice.clicked.connect(self.btn1_press)
        self.sec_dice.clicked.connect(self.btn2_press)
        self.third_dice.clicked.connect(self.btn3_press)
        self.fourth_dice.clicked.connect(self.btn4_press)
        self.fifth_dice.clicked.connect(self.btn5_press)

        # self.knifwin.calc_top.released.connect(self.calc_top)
        # self.knifwin.calc_bottom.released.connect(self.calc_bottom)
        # self.knifwin.calc_total.released.connect(self.calc_total)

        self.knifwin.tableWidget.currentCellChanged.connect(self.calc_total)

        self.knifwin.np_button.released.connect(self.next_player)

        self.first_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_1))
        self.sec_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_2))
        self.third_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_3))
        self.fourth_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_4))
        self.fifth_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_5))

        global PLAYER, PLAYERS
        running = True
        while running:
            player_count = input('How many players?')
            try:
                player_count = int(player_count)
                running = False
            except:
                print('please input a number (in digits)')
                continue
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

    def style(self, btn, file):
        btn.setStyleSheet("QPushButton{{border-image: url({0});}}".format(file))

    def roll(self):
        global throws, dice1_value, dice2_value, dice3_value, dice4_value, dice5_value
        if throws <= 2:
            throws += 1
            # throw_string = ''
            font = QtGui.QFont()
            font.setPointSize(30)

            self.animate_click()

            if not self.knifwin.first_roll.isDefault():
                rolled = str(self.roll_dice(0))
                # self.first_dice.setText(str(rolled))
                self.style(self.first_dice, dices[rolled])
                dice1_value = rolled
            if not self.knifwin.second_roll.isDefault():
                rolled = str(self.roll_dice(0))
                # self.sec_dice.setText(str(rolled))
                self.style(self.sec_dice, dices[rolled])
                dice2_value = rolled
            if not self.knifwin.third_roll.isDefault():
                rolled = str(self.roll_dice(0))
                # self.third_dice.setText(str(rolled))
                self.style(self.third_dice, dices[rolled])
                dice3_value = rolled
            if not self.knifwin.fourth_roll.isDefault():
                rolled = str(self.roll_dice(0))
                # self.fourth_dice.setText(str(rolled))
                self.style(self.fourth_dice, dices[rolled])
                dice4_value = rolled
            if not self.knifwin.fifth_roll.isDefault():
                rolled = str(self.roll_dice(0))
                # self.fifth_dice.setText(str(rolled))
                self.style(self.fifth_dice, dices[rolled])
                dice5_value = rolled
            self.calc_top()
            self.calc_bottom()
        else:
            self.knifwin.first_roll.setEnabled(False)
            self.knifwin.second_roll.setEnabled(False)
            self.knifwin.third_roll.setEnabled(False)
            self.knifwin.fourth_roll.setEnabled(False)
            self.knifwin.fifth_roll.setEnabled(False)
            print('Only 3 throws possible!!')

    def animate_click(self):
        global PLAYER, throws

        brush_1 = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush_2 = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush_3 = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        if throws == 1:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_1)
        elif throws == 2:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_2)
        elif throws == 3:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_3)

    def reset_dices(self):

        font = QtGui.QFont()
        font.setPointSize(8)

        first_dice = self.knifwin.first_roll
        sec_dice = self.knifwin.second_roll
        third_dice = self.knifwin.third_roll
        fourth_dice = self.knifwin.fourth_roll
        fifth_dice = self.knifwin.fifth_roll

        self.knifwin.first_roll.setDefault(False)
        self.knifwin.second_roll.setDefault(False)
        self.knifwin.third_roll.setDefault(False)
        self.knifwin.fourth_roll.setDefault(False)
        self.knifwin.fifth_roll.setDefault(False)

        self.knifwin.first_roll.setEnabled(True)
        self.knifwin.second_roll.setEnabled(True)
        self.knifwin.third_roll.setEnabled(True)
        self.knifwin.fourth_roll.setEnabled(True)
        self.knifwin.fifth_roll.setEnabled(True)

        first_dice.setFont(font)
        sec_dice.setFont(font)
        third_dice.setFont(font)
        fourth_dice.setFont(font)
        fifth_dice.setFont(font)

        self.style(first_dice, dice_1)
        self.style(sec_dice, dice_2)
        self.style(third_dice, dice_3)
        self.style(fourth_dice, dice_4)
        self.style(fifth_dice, dice_5)

        # self.roll()

    def roll_dice(self, dice):
        roll_nums = [1, 2, 3, 4, 5, 6]
        dice_roll = choice(roll_nums)
        THROWS[dice] = dice_roll
        return dice_roll

    def btn1_press(self):
        global dice_count
        if not self.knifwin.first_roll.isDefault():
            self.style(self.first_dice, pressed_dices[dice1_value])
            self.knifwin.first_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style(self.first_dice, dices[dice1_value])
            self.knifwin.first_roll.setDefault(False)
            self.first_dice.setText('')
            dice_count += 1

    def btn2_press(self):
        global dice_count
        if not self.knifwin.second_roll.isDefault():
            self.style(self.sec_dice, pressed_dices[dice2_value])
            self.knifwin.second_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style(self.sec_dice, dices[dice2_value])
            self.knifwin.second_roll.setDefault(False)
            self.sec_dice.setText('')
            dice_count += 1

    def btn3_press(self):
        global dice_count
        if not self.knifwin.third_roll.isDefault():
            self.style(self.third_dice, pressed_dices[dice3_value])
            self.knifwin.third_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style(self.third_dice, dices[dice3_value])
            self.knifwin.third_roll.setDefault(False)
            self.third_dice.setText('')
            dice_count += 1

    def btn4_press(self):
        global dice_count
        if not self.knifwin.fourth_roll.isDefault():
            self.style(self.fourth_dice, pressed_dices[dice4_value])
            self.knifwin.fourth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style(self.fourth_dice, dices[dice4_value])
            self.knifwin.fourth_roll.setDefault(False)
            self.fourth_dice.setText('')
            dice_count += 1

    def btn5_press(self):
        global dice_count
        if not self.knifwin.fifth_roll.isDefault():
            self.style(self.fifth_dice, pressed_dices[dice5_value])
            self.knifwin.fifth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style(self.fifth_dice, dices[dice5_value])
            self.knifwin.fifth_roll.setDefault(False)
            self.fifth_dice.setText('')
            dice_count += 1


    def calc_top(self):
        row_content_top = list()
        for i in range(6):
            r = self.knifwin.tableWidget.item(i, PLAYER).text()
            try:
                r = int(r)
            except:
                r = 0
                self.knifwin.tableWidget.item(i, PLAYER).setText('0')
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
            try:
                r = int(r)
            except:
                r = 0
                self.knifwin.tableWidget.item(i, PLAYER).setText('0')
            row_content_bottom.append(r)
        #print(row_content_bottom)

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

        global PLAYER, throws

        throws = 0

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
