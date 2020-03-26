import sys
import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtWidgets import *

sys.setrecursionlimit(10000)


class Block(QPushButton):
    def __init__(self, block_id):
        super().__init__()
        self.id = block_id
        self.position = (0, 0)
        self.num_mine_around = 0
        self.mine_flag = False

        self.mine_score = 0  # for the fanatic

    def get_id(self):
        return self.id

    def set_position(self, position):
        self.position = position
        return

    def get_position(self):
        return self.position

    def set_num_mine_around(self, num_mine_around):
        self.num_mine_around = num_mine_around
        return

    def get_num_mine_around(self):
        return self.num_mine_around

    def set_mine_flag(self, mine_flag):
        self.mine_flag = mine_flag
        return

    def get_mine_flag(self):
        return self.mine_flag

    def get_mine_score(self):
        return self.mine_score

    def set_mine_score(self, mine_score):
        self.mine_score = mine_score
        return


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.board_size = 20
        self.mine_num = 80
        self.block_ids = [i for i in range(0, self.board_size ** 2)]
        self.mine_ids = random.sample(range(0, self.board_size ** 2), self.mine_num)
        self.safe_ids = list(set(self.block_ids).difference(set(self.mine_ids)))

        self.toggled_blocks = []  # for fanatic
        self.valuable_blocks = []  # for fanatic

        self.initiate()

    def initiate(self):
        # 1. generate the grid layout
        grid = QGridLayout()
        # 1.1. set grid layout settings
        grid.setSpacing(2)
        grid.setContentsMargins(0, 0, 0, 0)
        # 2. generate the chessboard
        for i in self.block_ids:
            # 2.1. generate block entities
            setattr(self, "block" + str(i), Block(i))
            # 2.2. set block settings
            block_entry = getattr(self, "block" + str(i))
            block_entry.set_position(self.get_position(i))
            block_entry.set_num_mine_around(self.detect_mine_around(block_entry.get_position()))
            if i in self.mine_ids:
                block_entry.set_mine_flag(True)

            block_entry.setCheckable(True)
            block_entry.setFixedSize(self.board_size * 2 - 1, self.board_size * 2 - 1)
            block_entry.setStyleSheet("background-color: grey")
            block_entry.toggled.connect(self.toggle_event)
            grid.addWidget(block_entry, i // self.board_size, i % self.board_size)
        # 3. set main window
        self.setLayout(grid)
        self.setGeometry(0, 0, self.board_size ** 2 * 2, self.board_size ** 2 * 2)
        self.setFixedSize(self.board_size ** 2 * 2, self.board_size ** 2 * 2)
        self.setWindowTitle("Mine Sweeper")
        self.show()

    def get_position(self, block_id):
        x = block_id // self.board_size
        y = block_id % self.board_size
        return (x, y)

    def toggle_check_block(self, block_id):
        if getattr(self, "block" + str(block_id)).isChecked():
            return
        else:
            getattr(self, "block" + str(block_id)).toggle()

    def detect_mine_around(self, position):
        num_mine_around = 0
        x, y = position[0], position[1]

        # up
        if x - 1 >= 0 and (x - 1) * self.board_size + y in self.mine_ids:
            num_mine_around += 1
        # up-left corner
        if x - 1 >= 0 and y - 1 >= 0 and (x - 1) * self.board_size + y - 1 in self.mine_ids:
            num_mine_around += 1
        # up-right corner
        if x - 1 >= 0 and y + 1 <= self.board_size - 1 and (x - 1) * self.board_size + y + 1 in self.mine_ids:
            num_mine_around += 1
        # down
        if x + 1 <= self.board_size - 1 and (x + 1) * self.board_size + y in self.mine_ids:
            num_mine_around += 1
        # down-left corner
        if x + 1 <= self.board_size - 1 and y - 1 >= 0 and (x + 1) * self.board_size + y - 1 in self.mine_ids:
            num_mine_around += 1
        # down-right corner
        if x + 1 <= self.board_size - 1 and y + 1 <= self.board_size - 1 and (
                x + 1) * self.board_size + y + 1 in self.mine_ids:
            num_mine_around += 1
        # left
        if y - 1 >= 0 and x * self.board_size + y - 1 in self.mine_ids:
            num_mine_around += 1
        # right
        if y + 1 <= self.board_size and x * self.board_size + y + 1 in self.mine_ids:
            num_mine_around += 1
        return num_mine_around

    def expand(self, block_id):
        block_entry = getattr(self, "block" + str(block_id))
        if block_entry.get_num_mine_around() == 0:
            position = block_entry.get_position()
            x, y = position[0], position[1]

            if x == 0 and y == 0:
                return
            elif x == 0 and y == self.board_size - 1:
                return
            elif x == self.board_size - 1 and y == 0:
                return
            elif x == self.board_size - 1 and y == self.board_size - 1:
                return
            elif x == 0:
                # right
                self.toggle_check_block(block_id + 1)
                # left
                self.toggle_check_block(block_id - 1)
                # right-down
                self.toggle_check_block(block_id + 1 + self.board_size)
                # left-down
                self.toggle_check_block(block_id - 1 + self.board_size)
                # down
                self.toggle_check_block(block_id + self.board_size)
                return
            elif x == self.board_size - 1:
                # right
                self.toggle_check_block(block_id + 1)
                # left
                self.toggle_check_block(block_id - 1)
                # right-up
                self.toggle_check_block(block_id + 1 - self.board_size)
                # left-up
                self.toggle_check_block(block_id - 1 - self.board_size)
                # up
                self.toggle_check_block(block_id - self.board_size)
                return
            elif y == 0:
                # right
                self.toggle_check_block(block_id + 1)
                # right-down
                self.toggle_check_block(block_id + 1 + self.board_size)
                # right-up
                self.toggle_check_block(block_id + 1 - self.board_size)
                # up
                self.toggle_check_block(block_id - self.board_size)
                # down
                self.toggle_check_block(block_id + self.board_size)
                return
            elif y == self.board_size - 1:
                # left
                self.toggle_check_block(block_id - 1)
                # left-down
                self.toggle_check_block(block_id - 1 + self.board_size)
                # left-up
                self.toggle_check_block(block_id - 1 - self.board_size)
                # up
                self.toggle_check_block(block_id - self.board_size)
                # down
                self.toggle_check_block(block_id + self.board_size)
                return
            else:
                # right
                self.toggle_check_block(block_id + 1)
                # left
                self.toggle_check_block(block_id - 1)
                # right-down
                self.toggle_check_block(block_id + 1 + self.board_size)
                # left-down
                self.toggle_check_block(block_id - 1 + self.board_size)
                # right-up
                self.toggle_check_block(block_id + 1 - self.board_size)
                # left-up
                self.toggle_check_block(block_id - 1 - self.board_size)
                # up
                self.toggle_check_block(block_id - self.board_size)
                # down
                self.toggle_check_block(block_id + self.board_size)
                return

    def toggle_event(self):
        self.sender().setEnabled(False)
        if self.sender().mine_flag:
            self.sender().setStyleSheet("background-color: red")
            QMessageBox.information(self, "Game Over!", "It's a mine!")
            # self.statusBar().showMessage("it's a mine!")
        else:
            num_mine_around = self.sender().get_num_mine_around()
            if num_mine_around == 0:
                self.expand(self.sender().get_id())
                self.sender().setText(' ')
            else:
                self.valuable_blocks.append(self.sender().id)  # for fanatic

                self.sender().setText(str(num_mine_around))

            self.safe_ids.remove(self.sender().id)
            if not self.safe_ids:
                QMessageBox.information(self, "Game Over!", "You win!")
            # else:
            #     print(self.safe_ids)

        self.toggled_blocks.append(self.sender().id)  # for fanatic

    def get_block_around(self,block_id):
        pass


    def fanatic_sweeper(self):
        pass
        # only use the information: 1) indexes of toggled blocks 2) toggled blocks 3) total mine number
        # mines: mines
        # toggled blocks: blocks been toggled
        # remain_blocks: differences of all and toggled blocks
        # valuable blocks: blocks that has been toggled and indexed with a number
        mines = []
        remain_blocks=[]
        while len(mines) < self.mine_num:
            if not self.valuable_blocks:
                random_start = random.randint(0, self.board_size ** 2 - 1)
                self.toggle_check_block(random_start)
                print(self.toggled_blocks)
                print(self.valuable_blocks)
                remain_blocks=list(set(self.block_ids).difference(set(self.toggled_blocks)))
            else:
                for i in self.valuable_blocks:
                    entry=getattr(self, "block" + str(i))
                    num_mine_around=entry.num_mine_around



            break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.fanatic_sweeper()

    sys.exit(app.exec_())
