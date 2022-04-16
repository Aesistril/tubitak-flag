# TODO: Write some comments

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from configparser import ConfigParser
class os: 
    from os.path import dirname
    from os import listdir
class platform: from platform import system

try:
    f = open(os.dirname(__file__)+"/chksrc")
    if f.read() == "Xt6xb5qnzU4N2aiOIQFzznThuRSznSXvkF20y2Gk30vCA5RcR9IUf6gpfXLvT9yoJIX5PN":
        srcrun = True
except:
    srcrun = False

userOS = platform.system()

# Get the file paths for each os
dirs = ConfigParser()
if srcrun == True: dirs.read(os.dirname(__file__)+"/config/dirs/src.conf")
elif userOS == "Windows": dirs.read("C:/ProgramFiles/tubitak-flag/windows.conf")
elif userOS == "Linux": dirs.read("/etc/tubitak-flag/dirs/unix.conf")
elif userOS == "Unix": dirs.read("/etc/tubitak-flag/dirs/unix.conf")
# There will be macOS support soon (APPIMAGEs maybe?)

lang = "Turkish.conf" # There will be a dropdown menu to select this

# Language select menu
class select_lang(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/select_lang.ui', self)

# Select game widget (The main menu)
class select_game(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/select_game.ui', self)

# A window to put widgets on
class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        # Place the select_lang widget on the main window
        self.select_lang = select_lang()
        self.setCentralWidget(self.select_lang)
        self.setFixedSize(520, 200)
        # Add languages to language selection menu
        for l in os.listdir(dirs["resources"]["lang"].replace("-filepath-", os.dirname(__file__))):
            self.select_lang.comboBox.addItem(l.replace(".conf", ""))
        self.select_lang.lang_ok.clicked.connect(self.changeLang)
        
    # Change language
    def changeLang(self):
        self.lang = ConfigParser()
        # Read the comboBox and read the config file of language user has selected
        test = dirs["resources"]["lang"] + "/" + self.select_lang.comboBox.currentText() + ".conf"
        self.lang.read(dirs["resources"]["lang"].replace("-filepath-", os.dirname(__file__)) + "/" + self.select_lang.comboBox.currentText() + ".conf")
        self.draw_select_game()

    def draw_select_game(self):
        # Draw the main menu
        self.select_game = select_game()
        self.setCentralWidget(self.select_game)
        self.select_game.sel_game_label.setText(self.lang["sel_game"]["sel_game_label"])
        self.select_game.region_game.setText(self.lang["sel_game"]["region_game"])
        self.select_game.country_game.setText(self.lang["sel_game"]["country_game"])
        self.setFixedSize(639, 450)

# Start the application
if __name__ == '__main__':
    class sys: from sys import argv, exit
    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())