import sys
from qtpy import QtWidgets
from kniffel_gui.mainwindow import Ui_MainWindow
from setup_gui.setup_window import Ui_Setup_Window  # Importing
from random import choice
from PyQt5 import QtGui, QtCore

FIRST_ROLL = 1
dice_count = 5  # Setting global variables
THROWS = ['_', '_', '_', '_', '_']
throws = 0
PLAYER = 1

PLAYERS = []

TURNS = 0

started = False
running = True

brush_1 = None
brush_2 = None
brush_3 = None

#  # --- Setup Variables --- #  #
PLAYERNAMES = None  # Variables, available from the Setup menu

#  # --- Pictures --- # #
dice_1 = 'kniffel_gui/1.png'
dice_1_pressed = 'kniffel_gui/1_pressed.png'

dice_2 = 'kniffel_gui/2.png'
dice_2_pressed = 'kniffel_gui/2_pressed.png'  # retrieving dice picture files

dice_3 = 'kniffel_gui/3.png'
dice_3_pressed = 'kniffel_gui/3_pressed.png'

dice_4 = 'kniffel_gui/4.png'
dice_4_pressed = 'kniffel_gui/4_pressed.png'

dice_5 = 'kniffel_gui/5.png'
dice_5_pressed = 'kniffel_gui/5_pressed.png'

dice_6 = 'kniffel_gui/6.png'
dice_6_pressed = 'kniffel_gui/6_pressed.png'

dices = {'1': dice_1, '2': dice_2, '3': dice_3, '4': dice_4, '5': dice_5,
         '6': dice_6}  # assigning a value to each dice picture

pressed_dices = {'1': dice_1_pressed, '2': dice_2_pressed, '3': dice_3_pressed, '4': dice_4_pressed,
                 '5': dice_5_pressed, '6': dice_6_pressed}  # assigning a value to each pressed dice picture

dice1_value = 0
dice2_value = 0  # setting the dice values
dice3_value = 0
dice4_value = 0
dice5_value = 0


class MainWindow(QtWidgets.QMainWindow):  # Kniffelwindow
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.knifwin = Ui_MainWindow()
        self.knifwin.setupUi(self)  # Setup of the Kniffel window
        self.setWindowTitle('KNIFFELLLLLLLLL!!!')

        self.first_dice = self.knifwin.first_roll
        self.sec_dice = self.knifwin.second_roll
        self.third_dice = self.knifwin.third_roll  # Shortening names
        self.fourth_dice = self.knifwin.fourth_roll
        self.fifth_dice = self.knifwin.fifth_roll

        self.knifwin.roll_btn.clicked.connect(self.roll)
        self.first_dice.clicked.connect(self.btn1_press)
        self.sec_dice.clicked.connect(self.btn2_press)  # connecting dices to their functions when pressed
        self.third_dice.clicked.connect(self.btn3_press)
        self.fourth_dice.clicked.connect(self.btn4_press)
        self.fifth_dice.clicked.connect(self.btn5_press)

        self.knifwin.tableWidget.currentCellChanged.connect(self.calc_total)
        self.knifwin.tableWidget.cellClicked.connect(self.entry_throw_top_part)  # connecting cells to functions
        # self.knifwin.tableWidget.cellClicked.connect(self.get_clicked_cell_index)

        self.knifwin.np_button.released.connect(self.next_player)  # connecting the next player button

        self.first_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_1))
        self.sec_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_2))
        self.third_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_3))  # formatting the dices
        self.fourth_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_4))
        self.fifth_dice.setStyleSheet("QPushButton{{border-image: url({0});}}".format(dice_5))

        self.setup()  # setup() ln: 108

        global started  # Set the start Player to the first Player
        if started:
            self.next_player()
            started = False

    def setup(self):
        global PLAYER, PLAYERS, PLAYERNAMES
        # running = True
        # while running:
        # player_count = input('How many players?')
        # try:
        #   player_count = int(player_count)
        #  running = False
        # except:
        #   print('please input a number (in digits)')
        #  continue
        # PLAYER = player_count
        for i in range(int(PLAYER)):  # determine Players
            PLAYERS.append(i)

        self.knifwin.tableWidget.setColumnCount(PLAYER + 1)  # setting columns = Players

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)

        brush2 = QtGui.QBrush(QtGui.QColor(125, 125, 125))  # some nice brushes for the cells
        brush2.setStyle(QtCore.Qt.Dense5Pattern)

        brush3 = QtGui.QBrush(QtGui.QColor(51, 51, 51, 255))
        brush3.setStyle(QtCore.Qt.Dense4Pattern)

        for item in PLAYERS:  # putting player name (determined in Setup window) in headers
            for i in range(len(PLAYERS)):
                self.knifwin.tableWidget.setHorizontalHeaderItem(item + 1,
                                                                 QtWidgets.QTableWidgetItem(f'{PLAYERNAMES[item]}'))

        for item in PLAYERS:
            for i in range(19):  # filling all the blank cells with QTableWidgetItems
                self.knifwin.tableWidget.setItem(i, item + 1, QtWidgets.QTableWidgetItem())

        for item in PLAYERS:
            for i in range(9, 16):  # filling bottom part cells with '0'
                self.knifwin.tableWidget.setItem(i, item + 1, QtWidgets.QTableWidgetItem('0'))

        for item in PLAYERS:
            for row in range(0, 6):  # creating top part Kniffelblatt
                self.knifwin.tableWidget.setItem(row, item + 1, QtWidgets.QTableWidgetItem('0'))
                self.knifwin.tableWidget.item(6, item + 1).setBackground(brush)
                self.knifwin.tableWidget.item(7, item + 1).setText('Plus 35 Pkt.')

                self.knifwin.tableWidget.item(8, item + 1).setBackground(brush2)
                self.knifwin.tableWidget.item(16, item + 1).setBackground(brush)
                self.knifwin.tableWidget.item(17, item + 1).setBackground(brush3)
                self.knifwin.tableWidget.item(18, item + 1).setBackground(brush2)

    def style_file(self, btn, file):  # set the appearance of a button to a certain picture
        btn.setStyleSheet("QPushButton{{border-image: url({0});}}".format(file))

    def roll(self):
        global throws, dice1_value, dice2_value, dice3_value, dice4_value, dice5_value, THROWS
        if throws <= 2:  # prevent player of rolling more than 3 times
            throws += 1

            self.animate_click()  # changing the background color of the current player to show, he rolled

            if not self.knifwin.first_roll.isDefault():  # if button isn't selected: roll the die and set
                rolled = str(self.roll_dice(0))  # the appearance to corresponding file as well as setting the
                self.style_file(self.first_dice, dices[rolled])  # dice's value corresponding to the rolled number
                dice1_value = rolled
            if not self.knifwin.second_roll.isDefault():
                rolled = str(self.roll_dice(1))
                self.style_file(self.sec_dice, dices[rolled])
                dice2_value = rolled
            if not self.knifwin.third_roll.isDefault():
                rolled = str(self.roll_dice(2))
                self.style_file(self.third_dice, dices[rolled])
                dice3_value = rolled
            if not self.knifwin.fourth_roll.isDefault():
                rolled = str(self.roll_dice(3))
                self.style_file(self.fourth_dice, dices[rolled])
                dice4_value = rolled
            if not self.knifwin.fifth_roll.isDefault():
                rolled = str(self.roll_dice(4))
                self.style_file(self.fifth_dice, dices[rolled])
                dice5_value = rolled
            self.calc_top()  # calculate the top part
            self.calc_bottom()  # calculate the bottom part (of Kniffelblatt)
        else:
            self.knifwin.first_roll.setEnabled(False)  # if rolled 3 times: disable buttons and tell the Player
            self.knifwin.second_roll.setEnabled(False)
            self.knifwin.third_roll.setEnabled(False)
            self.knifwin.fourth_roll.setEnabled(False)
            self.knifwin.fifth_roll.setEnabled(False)
            print('Only 3 throws possible!!')
        self.enable_dices()  # enable dies again to be able to roll again

    def entry_throw_top_part(self):  # get the sum of selected dies and writes it into the clicked cell
        index_x, index_y = self.get_clicked_cell_index()  # automatically calls next_player() and calculates
        if index_y < 6 and index_x == PLAYER:  # the whole Kniffelblatt
            throw_value = 0
            clicked1, clicked2, clicked3, clicked4, clicked5 = self.checked_btn_clicked()
            if clicked1:
                throw_value += int(dice1_value)
            if clicked2:
                throw_value += int(dice2_value)
            if clicked3:
                throw_value += int(dice3_value)
            if clicked4:
                throw_value += int(dice4_value)
            if clicked5:
                throw_value += int(dice5_value)

            self.knifwin.tableWidget.setItem(index_y, index_x, QtWidgets.QTableWidgetItem(str(throw_value)))
            self.calc_total()
            self.next_player()

    def get_clicked_cell_index(self):
        col = self.knifwin.tableWidget.currentColumn()
        row = self.knifwin.tableWidget.currentRow()
        index = col, row
        return index  # returns index (x,y) of a clicked cell

    def checked_btn_clicked(self):
        dice1 = None
        dice2 = None
        dice3 = None
        dice4 = None
        dice5 = None
        if self.first_dice.isDefault():
            dice1 = True
        if self.sec_dice.isDefault():
            dice2 = True
        if self.third_dice.isDefault():
            dice3 = True
        if self.fourth_dice.isDefault():
            dice4 = True
        if self.fifth_dice.isDefault():
            dice5 = True

        return dice1, dice2, dice3, dice4, dice5  # checks which of the buttons are clicked

    def animate_click(self):
        global PLAYER, throws, brush_1, brush_2, brush_3  # see above

        if throws == 1:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_1)
        elif throws == 2:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_2)
        elif throws == 3:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush_3)

    def reset_dices(self):

        self.enable_dices()  # enable dices

        self.first_dice.setDefault(False)
        self.sec_dice.setDefault(False)
        self.third_dice.setDefault(False)
        self.fourth_dice.setDefault(False)
        self.fifth_dice.setDefault(False)

        self.style_file(self.first_dice, dice_1)
        self.style_file(self.sec_dice, dice_2)  # setting them visually to 1,2,3,4,5
        self.style_file(self.third_dice, dice_3)
        self.style_file(self.fourth_dice, dice_4)
        self.style_file(self.fifth_dice, dice_5)

    def disable_dices(self):
        self.first_dice.setEnabled(False)
        self.sec_dice.setEnabled(False)
        self.third_dice.setEnabled(False)  # disable all dices
        self.fourth_dice.setEnabled(False)
        self.fifth_dice.setEnabled(False)

    def enable_dices(self):  # enabling them
        self.first_dice.setEnabled(True)
        self.sec_dice.setEnabled(True)
        self.third_dice.setEnabled(True)
        self.fourth_dice.setEnabled(True)
        self.fifth_dice.setEnabled(True)

    def roll_dice(self, dice):  # roll a random number between 1-6 with a certain dice
        global THROWS
        roll_nums = [1, 2, 3, 4, 5, 6]
        dice_roll = choice(roll_nums)
        THROWS[dice] = dice_roll  # for console: print(THROWS) to see throw in console (no longer necessary)
        return dice_roll

    def btn1_press(self):  # change button visually when pressed
        global dice_count
        if not self.knifwin.first_roll.isDefault():
            self.style_file(self.first_dice, pressed_dices[dice1_value])
            self.knifwin.first_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style_file(self.first_dice, dices[dice1_value])
            self.knifwin.first_roll.setDefault(False)
            dice_count += 1

    def btn2_press(self):
        global dice_count
        if not self.knifwin.second_roll.isDefault():
            self.style_file(self.sec_dice, pressed_dices[dice2_value])
            self.knifwin.second_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style_file(self.sec_dice, dices[dice2_value])
            self.knifwin.second_roll.setDefault(False)
            dice_count += 1

    def btn3_press(self):
        global dice_count
        if not self.knifwin.third_roll.isDefault():
            self.style_file(self.third_dice, pressed_dices[dice3_value])
            self.knifwin.third_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style_file(self.third_dice, dices[dice3_value])
            self.knifwin.third_roll.setDefault(False)
            dice_count += 1

    def btn4_press(self):
        global dice_count
        if not self.knifwin.fourth_roll.isDefault():
            self.style_file(self.fourth_dice, pressed_dices[dice4_value])
            self.knifwin.fourth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style_file(self.fourth_dice, dices[dice4_value])
            self.knifwin.fourth_roll.setDefault(False)
            dice_count += 1

    def btn5_press(self):
        global dice_count
        if not self.knifwin.fifth_roll.isDefault():
            self.style_file(self.fifth_dice, pressed_dices[dice5_value])
            self.knifwin.fifth_roll.setDefault(True)
            dice_count -= 1
        else:
            self.style_file(self.fifth_dice, dices[dice5_value])
            self.knifwin.fifth_roll.setDefault(False)
            dice_count += 1

    def calc_top(self):  # calculate the top part of the Kniffelblatt
        row_content_top = list()
        for i in range(6):  # top part goes from line 1-6
            r = self.knifwin.tableWidget.item(i, PLAYER).text()  # retrieving the data in the column
            try:
                r = int(r)
            except:
                r = 0
                self.knifwin.tableWidget.item(i, PLAYER).setText('0')
            row_content_top.append(r)  # appending the value to row_content_top
        # print(row_content_top)

        row_counter = 0
        for item in row_content_top:  # adding all the values together
            row_counter += int(item)
        # print(row_counter)

        self.knifwin.tableWidget.setItem(6, PLAYER,
                                         QtWidgets.QTableWidgetItem(str(row_counter)))  # writing points in table

        total = self.calc_bonus()  # calculate whether bonus conditions have been reached
        if row_counter >= 63:  # if so: write total in table
            self.knifwin.tableWidget.setItem(17, PLAYER, QtWidgets.QTableWidgetItem(str(total)))
        else:  # if not write total without bonus in table
            self.knifwin.tableWidget.setItem(17, PLAYER, QtWidgets.QTableWidgetItem(str(row_counter)))

        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.Dense4Pattern)  # after writing the score in the cell, we have to set the bg again
        self.knifwin.tableWidget.item(17, PLAYER).setBackground(brush)

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)
        self.knifwin.tableWidget.item(6, PLAYER).setBackground(brush)

    def calc_bonus(self):  # calculating the bonus
        total_top_noBonus = int(self.knifwin.tableWidget.item(6, PLAYER).text())
        total_top = 0
        if total_top_noBonus >= 63:
            total_top = total_top_noBonus + 35
            self.knifwin.tableWidget.setItem(8, PLAYER, QtWidgets.QTableWidgetItem(str(total_top)))

            brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
            brush.setStyle(QtCore.Qt.Dense5Pattern)
            self.knifwin.tableWidget.item(8, PLAYER).setBackground(brush)
        return total_top

    def calc_bottom(self):  # calculating the bottom part of the table
        row_content_bottom = list()
        for i in range(9, 16):  # bottom part goes from row 9-16
            r = self.knifwin.tableWidget.item(i, PLAYER).text()  # retrieving the score
            try:
                r = int(r)
            except:
                r = 0
                self.knifwin.tableWidget.item(i, PLAYER).setText('0')
            row_content_bottom.append(r)
        # print(row_content_bottom)

        row_counter = 0
        for item in row_content_bottom:  # calculating the total score of the bottom part
            row_counter += int(item)
        # print(row_counter)

        self.knifwin.tableWidget.setItem(16, PLAYER,
                                         QtWidgets.QTableWidgetItem(str(row_counter)))  # writing score in cell

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense4Pattern)  # resetting the background
        self.knifwin.tableWidget.item(16, PLAYER).setBackground(brush)

    def calc_total(self):  # calculating top an bottom part and ading them together
        self.calc_top()
        self.calc_bottom()
        top = int(self.knifwin.tableWidget.item(17, PLAYER).text())
        bottom = int(self.knifwin.tableWidget.item(16, PLAYER).text())
        total = top + bottom

        self.knifwin.tableWidget.setItem(18, PLAYER, QtWidgets.QTableWidgetItem(str(total)))  # write total in cell

        brush = QtGui.QBrush(QtGui.QColor(125, 125, 125))
        brush.setStyle(QtCore.Qt.Dense5Pattern)  # setting bg again
        self.knifwin.tableWidget.item(18, PLAYER).setBackground(brush)

    def next_player(self):  # setting current playing player to the next

        self.reset_dices()
        self.disable_dices()

        global PLAYER, throws, TURNS

        TURNS += 1  # due to the fact that Kniffel is played in 13 turns for each player, we have to count those to
        # determine the end

        if TURNS > 13 * len(PLAYERS):  # possible turns: 13 for each player
            self.finish()

        if PLAYER >= len(PLAYERS):
            PLAYER = 1  # the 'next-player-loop'
        else:
            PLAYER += 1

        brush = QtGui.QBrush(QtGui.QColor(52, 235, 161))
        default_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        if PLAYER == 1:  # visualising the current player by highlighting their column or at least the header
            self.knifwin.tableWidget.horizontalHeaderItem(len(PLAYERS)).setBackground(default_brush)
            self.knifwin.tableWidget.horizontalHeaderItem(1).setBackground(brush)
        else:
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER - 1).setBackground(default_brush)
            self.knifwin.tableWidget.horizontalHeaderItem(PLAYER).setBackground(brush)

    def get_greatest(self, list_):  # return greatest value of a list
        nlist = []
        for i in list_:  # converting string list into integer list
            nlist.append(int(i))

        greatest = nlist[0]
        for i in nlist:
            if i > greatest:
                greatest = nlist[nlist.index(i)]  # determine the greatest score

        return greatest, nlist.index(greatest)  # points, player

    def finish(self):  # "End-Screen"
        print('''--- Spiel zu Ende!! ---
Die Punkte sind wiefolgt verteilt:
        ''')
        tot_points = []

        for i in PLAYERS:
            total = self.knifwin.tableWidget.item(18, i + 1).text()  # retrieving total points from each player
            print(f'Player {i + 1}: ' + PLAYERNAMES[i] + ' mit ' + str(total) + ' Punkten')  # printing those
            tot_points.append(total)

        points, player = self.get_greatest(tot_points)  # calculating the winner
        # print(points, player)
        print(f'\nGewonnen hat Spieler: {player + 1} mit {points} Punkten')  # printing the winner

        self.disable_dices()
        self.knifwin.roll_btn.setEnabled(False)  # disabling all buttons/dies
        self.knifwin.np_button.setEnabled(False)


class Setup_Window(QtWidgets.QMainWindow):  # Setup window
    def __init__(self, parent=None):
        global PLAYER, started

        super(Setup_Window, self).__init__(parent)

        self.su_wn = Ui_Setup_Window()
        self.su_wn.setupUi(self)
        self.setWindowTitle('Setup Kniffel!!!')  # setup the Setup

        self.su_wn.pushButton.clicked.connect(self.on_to_kniffel_click)
        self.su_wn.pushButton.clicked.connect(self.set_color)  # connecting buttons

        self.su_wn.fcolor.currentIndexChanged.connect(self.set_color)
        self.su_wn.scolor.currentIndexChanged.connect(
            self.set_color)  # connecting drop down Menus to change highlighting
        self.su_wn.tcolor.currentIndexChanged.connect(self.set_color)  # of throws (animate_click())

        started = True  # Initialized the game as started

    def set_color(self):  # setting the colors used in animate_click() corresponding to the player's selection
        global brush_1, brush_2, brush_3

        colors = {'Red': (255, 0, 0),
                  'Green': (0, 255, 0),
                  'Blue': (0, 0, 255),
                  'Purple': (185, 66, 245),
                  'Brown': (77, 38, 0),
                  'Black': (0, 0, 0),
                  'Yellow': (236, 242, 56)
                  }

        sel1 = self.su_wn.fcolor.currentText()
        sel2 = self.su_wn.scolor.currentText()
        sel3 = self.su_wn.tcolor.currentText()

        bad_word = 'select color'
        if not sel1 == bad_word and sel2 != bad_word and sel3 != bad_word:
            col1_1, col1_2, col1_3 = colors[sel1]
            col2_1, col2_2, col2_3 = colors[sel2]
            col3_1, col3_2, col3_3 = colors[sel3]
            brush_1 = QtGui.QBrush(QtGui.QColor(col1_1, col1_2, col1_3))
            brush_2 = QtGui.QBrush(QtGui.QColor(col2_1, col2_2, col2_3))
            brush_3 = QtGui.QBrush(QtGui.QColor(col3_1, col3_2, col3_3))
        else:
            brush_1 = QtGui.QBrush(QtGui.QColor(255, 0, 0))  # if nothing or not 3 colors have been selected:
            brush_2 = QtGui.QBrush(QtGui.QColor(0, 255, 0))  # it sets the standard colors (red,green,blue)
            brush_3 = QtGui.QBrush(QtGui.QColor(0, 0, 255))

    def on_to_kniffel_click(self):
        global PLAYER, PLAYERNAMES

        PLAYERNAMES = self.su_wn.names.text().split(',')
        PLAYER = len(PLAYERNAMES)  # setting amount of Players according to Players the player put in
        wn = MainWindow(self)  # set the window to the Kniffelwindow
        wn.show()  # show the window


def main():
    app = QtWidgets.QApplication(sys.argv)  # creating an QWidgets application
    wn = Setup_Window()  # setting the window
    wn.show()  # showing the window
    sys.exit(app.exec_())  # exit loop


if __name__ == '__main__':  # if this file is run: call main()
    main()
