import sys
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Cybry')
        self.resize(400, 300)

        self.helpS = 'Cybry is a simple game inspired by a traditional chinese drinking game.\n\
At the start of the game, every player has the same number of dices.\n\
Players take turns to make a choice of taking away one of these four\n\
kinds of dices: red(includes 1 and 4), blue(includes 2, 3, 5, 6),\n\
big(4, 5, 6) and small(1, 2, 3). All players need to take away the dices\n\
which have been anounced. Once someone has lost all his dices, the game ends.'

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.initSplashView()
        self.initGameView()

        self.setAction()
        self.setMenu()

        self.main = QStackedWidget()
        self.main.addWidget(self.splash)
        self.main.addWidget(self.game)
        self.main.setCurrentWidget(self.splash)
        self.setCentralWidget(self.main)
        center(self)

    def setAction(self):
        self.newGameAct = QAction('&New', self, triggered=self.newGame)
        self.quit = QAction('&Quit', self, triggered=self.quit)
        self.helpAct = QAction('&Help', self, triggered=self.help)

    def setMenu(self):
        self.gameMenu = QMenu('&Game', self)
        self.gameMenu.addAction(self.newGameAct)
        self.gameMenu.addAction(self.quit)

        self.helpMenu = QMenu('&Help', self)
        self.helpMenu.addAction(self.helpAct)

        self.menuBar().addMenu(self.gameMenu)
        self.menuBar().addMenu(self.helpMenu)

    def newGame(self):
        self.newGameW = QWidget()
        self.newGameW.setWindowTitle('New Game')
        layout = QVBoxLayout()
        self.playerNum = 5
        self.diceNumMax = 6
        self.order = 1

        playerL = QLabel()
        playerL.setText('How Many Players?')
        self.playerSP = QSpinBox()
        self.playerSP.setRange(2, 9)
        self.playerSP.setValue(self.playerNum)

        diceNumL = QLabel()
        diceNumL.setText('How Many Dices?')
        self.diceNumSP = QSpinBox()
        self.diceNumSP.setRange(5, 15)
        self.diceNumSP.setValue(self.diceNumMax)

        orderL = QLabel()
        orderL.setText('You Start From?')
        self.orderSP = QSpinBox()
        self.orderSP.setRange(1, self.playerNum)
        self.orderSP.setValue(self.order)

        self.randomPlayer = QPushButton('Random Players')
        self.randomOrder = QPushButton('Random Order')
        newGameB = QPushButton('OK')

        self.playerSP.valueChanged.connect(self.valueChanged)
        self.diceNumSP.valueChanged.connect(self.valueChanged)
        self.orderSP.valueChanged.connect(self.valueChanged)
        self.randomPlayer.clicked.connect(self.randomPlay)
        self.randomOrder.clicked.connect(self.randomPlay)
        newGameB.clicked.connect(lambda: self.buttonClicked('newGame'))

        layout.addWidget(playerL)
        layout.addWidget(self.playerSP)
        layout.addWidget(diceNumL)
        layout.addWidget(self.diceNumSP)
        layout.addWidget(orderL)
        layout.addWidget(self.orderSP)
        layout.addWidget(self.randomPlayer)
        layout.addWidget(self.randomOrder)
        layout.addWidget(newGameB)

        self.newGameW.setLayout(layout)
        self.newGameW.show()
        center(self.newGameW)

    def valueChanged(self):
        sp = self.sender()
        if sp == self.playerSP:
            self.playerNum = sp.value()
            self.orderSP.setRange(1, self.playerNum)
        if sp == self.diceNumSP:
            self.diceNumMax = sp.value()
        if sp == self.orderSP:
            self.order = sp.value()

    def randomPlay(self):
        clickedB = self.sender()
        if clickedB == self.randomPlayer:
            self.playerNum = random.randint(2, 9)
            self.playerSP.setValue(self.playerNum)
        elif clickedB == self.randomOrder:
            self.order = random.randint(1, self.playerNum)
            self.orderSP.setValue(self.order)

    def initSplashView(self):
        self.splash = QWidget()
        splashMsg = QLabel("Welcome to CYBRY !")
        splashMsg.setAlignment(Qt.AlignCenter)
        helpL = QLabel(self.helpS)
        helpL.setAlignment(Qt.AlignCenter)

        newGameB = QPushButton("Start A New Game")
        newGameB.clicked.connect(self.newGame)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(newGameB)
        layout.addStretch()

        splashLayout = QVBoxLayout()
        splashLayout.addWidget(splashMsg)
        splashLayout.addWidget(helpL)
        splashLayout.addLayout(layout)
        self.splash.setLayout(splashLayout)

    def initGameView(self):
        self.game = QWidget()
        self.gameLayout = QVBoxLayout()
        self.game.setLayout(self.gameLayout)

        self.choiceL = QLabel()
        self.diceLayout = QVBoxLayout()
        self.choiceLayout = QVBoxLayout()
        self.initChoice()
        self.gameLayout.addWidget(self.choiceL)
        self.gameLayout.addLayout(self.diceLayout)
        self.gameLayout.addLayout(self.choiceLayout)

    def initChoice(self):
        layout = QFormLayout()

        self.red = QRadioButton('Take away red ones')
        self.blue = QRadioButton('Take away blue ones')
        self.big = QRadioButton('Take away ones larger than 3')
        self.small = QRadioButton('Take away ones smaller than 4')

        self.group = QButtonGroup()
        self.group.addButton(self.red)
        self.group.addButton(self.blue)
        self.group.addButton(self.big)
        self.group.addButton(self.small)

        self.endTurnB = QPushButton('Next')
        self.endTurnB.clicked.connect(self.endTurn)

        layout.addRow(self.red, self.blue)
        layout.addRow(self.big, self.small)
        self.choiceLayout.addLayout(layout)
        self.choiceLayout.addStretch()
        self.choiceLayout.addWidget(self.endTurnB)

    def startGame(self):

        self.dice = {}
        self.diceNum = {}
        self.round = 1
        self.yourTurn = False
        self.reRoll = False
        self.gameOver = False

        self.main.setCurrentWidget(self.game)

        self.whosTurn()
        if self.yourTurn is True:
            self.choiceEnabled('y')
        else:
            self.choiceEnabled('n')

        for i in range(1, self.playerNum + 1):
            self.diceNum[i] = self.diceNumMax

        self.rollDice()

    def rollDice(self):
        self.diceNumL = {}

        self.status.showMessage('ROUND ' + str(self.round))

        self.whosTurn()
        if self.yourTurn is True:
            self.choiceL.setText('It\'s Your Turn.')
        else:
            self.choiceL.setText('It\'s Player ' + str(self.turn) + '\'s Turn.')

        clearLayout(self, self.diceLayout)
        i = 1
        while i < self.playerNum + 1:
            self.diceNumL[i] = QLabel()
            self.dice[i] = {}
            self.diceLabelInit()
            for j in range(1, self.diceNum[i] + 1):
                self.dice[i][j] = random.randint(1, 6)
                if i == self.order or i == self.round:
                    self.diceNumL[i].setText(self.diceNumL[i].text() + " " + str(self.dice[i][j]))
                else:
                    self.diceNumL[i].setText(self.diceNumL[i].text() + " ?")
            self.diceLayout.addWidget(self.diceNumL[i])
            i = i + 1

    def makeChoice(self):
        # player side
        if self.yourTurn is True:
            self.choiceEnabled('y')
            if self.red.isChecked():
                self.choiceToDice('red')
            elif self.blue.isChecked():
                self.choiceToDice('blue')
            elif self.big.isChecked():
                self.choiceToDice('big')
            elif self.small.isChecked():
                self.choiceToDice('small')
            else:
                QMessageBox.warning(self, "Warning", "Please make your choice !", QMessageBox.Cancel)
        # AI side
        else:
            red = 0
            blue = 0
            big = 0
            small = 0
            for j in range(1, self.diceNum[self.turn] + 1):
                if self.dice[self.turn][j] == 1 or 3:
                    red = red + 1
                elif self.dice[self.turn][j] == 2 or 4 or 5 or 6:
                    blue = blue + 1
                elif self.dice[self.turn][j] == 4 or 5 or 6:
                    big = big + 1
                elif self.dice[self.turn][j] == 1 or 2 or 3:
                    small = small + 1
            aiDice = {'red': red, 'blue': blue, 'big': big, 'small': small}
            aiChoice = min(aiDice, key=aiDice.get)
            self.choiceToDice(aiChoice)

    def takeEffect(self):
        clearLayout(self, self.diceLayout)
        self.diceLabelInit()
        for i in range(1, self.playerNum + 1):
            for j in range(1, self.diceNum[i] + 1):
                if self.dice[i][j] in self.takeAway:
                    del self.dice[i][j]
                    self.diceNum[i] = self.diceNum[i] - 1
                    if self.diceNum[i] == 0:
                        self.gameOver = True
                        self.setButtonText()
                else:
                    if i == self.order or i == self.round:
                        self.diceNumL[i].setText(self.diceNumL[i].text() + " " + str(self.dice[i][j]))
                    else:
                        self.diceNumL[i].setText(self.diceNumL[i].text() + " ?")
            self.diceLayout.addWidget(self.diceNumL[i])

        self.reRoll = True
        self.choiceEnabled('n')

    def endTurn(self):
        self.setButtonText()
        if self.gameOver:
            self.status.clearMessage()
            self.main.setCurrentWidget(self.splash)
            self.endTurnB.setText('Next')
        if not self.gameOver:
            if self.reRoll is True:
                self.round = self.round + 1
                self.rollDice()
                self.reRoll = False
            else:
                self.makeChoice()

    def choiceToDice(self, arg):
        if arg == 'red':
            self.takeAway = [1, 3]
        elif arg == 'blue':
            self.takeAway = [2, 4, 5, 6]
        elif arg == 'big':
            self.takeAway = [4, 5, 6]
        elif arg == 'small':
            self.takeAway = [1, 2, 3]

        if self.yourTurn is True:
            self.choiceL.setText('You took away ' + arg + ' ones.')
        else:
            self.choiceL.setText('Player ' + str(self.turn) + ' took away ' + arg + ' ones.')

        self.group.setExclusive(False)
        vars(self)[arg].setChecked(False)
        self.group.setExclusive(True)

        self.takeEffect()

    def diceLabelInit(self):
        for i in range(1, self.playerNum + 1):
            self.diceNumL[i] = QLabel()
            if i != self.order:
                self.diceNumL[i].setText("player " + str(i) + " 's dices :")
            else:
                self.diceNumL[i].setText('YOUR dices :')

    def whosTurn(self):
        self.turn = self.round % self.playerNum
        if self.turn == 0:
            self.turn = self.playerNum
        if self.turn == self.order:
            self.yourTurn = True
        else:
            self.yourTurn = False

    def setButtonText(self):
        if self.gameOver:
            self.endTurnB.setText('Game Over')
        else:
            if self.reRoll:
                self.endTurnB.setText('Roll Dice')
            else:
                self.endTurnB.setText('Next')

    def choiceEnabled(self, arg):
        if arg == 'y':
            self.red.setEnabled(True)
            self.blue.setEnabled(True)
            self.big.setEnabled(True)
            self.small.setEnabled(True)
        elif arg == 'n':
            self.red.setDisabled(True)
            self.blue.setDisabled(True)
            self.big.setDisabled(True)
            self.small.setDisabled(True)

    def buttonClicked(self, arg):
        if arg == 'newGame':
            self.newGameW.close()
            self.startGame()
        elif arg == 'quitHelp':
            self.helpW.close()

    def quit(self):
        sys.exit()

    def help(self):
        self.helpW = QWidget()
        helpL = QLabel(self.helpS)
        helpL.setAlignment(AlignLeft)

        okB = QPushButton('Ok')
        okB.clicked.connect(lambda: self.buttonClicked('quitHelp'))
        _layout = QHBoxLayout()
        _layout.addStretch()
        _layout.addWidget(okB)
        _layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(helpL)
        layout.addLayout(_layout)

        self.helpW.setLayout(layout)

        self.helpW.show()
        center(helpW)


def center(self):
    screen = QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


def clearLayout(self, layout):
    for i in reversed(list(range(layout.count()))):
        layout.itemAt(i).widget().setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cybry = MainWindow()
    cybry.show()
    sys.exit(app.exec_())
