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
class region_game_config(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/region_game_config.ui', self)

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
        self.lang.read(dirs["resources"]["lang"].replace("-filepath-", os.dirname(__file__)) + "/" + self.select_lang.comboBox.currentText() + ".conf")
        del self.select_lang
        self.setWindowTitle(self.lang["misc"]["window_title"]) # Change the window title
        self.draw_select_game()

    def draw_select_game(self):
        # Delete the old self.select_game if possible
        try: del self.select_game
        except: pass
        # Draw the main menu
        self.select_game = select_game()
        self.select_game.sel_game_label.setText(self.lang["sel_game"]["sel_game_label"])
        self.select_game.region_game.setText(self.lang["sel_game"]["region_game"])
        self.select_game.country_game.setText(self.lang["sel_game"]["country_game"])
        self.select_game.region_game.clicked.connect(self.draw_region_game_config)
        self.select_game.country_game.clicked.connect(self.draw_country_game)
        self.setCentralWidget(self.select_game)
        self.setFixedSize(640, 450)
    
    def draw_country_game(self):
        pass

    def draw_region_game_config(self):
        # Delete the old self.region_game_config if possible
        try: del self.region_game_config
        except: pass
        self.region_game_config = region_game_config()
        self.region_game_config.choice_count_label.setText(self.lang["region_game_config"]["choice_count_label"])
        self.region_game_config.q_count_label.setText(self.lang["region_game_config"]["q_count_label"])
        self.region_game_config.title.setText(self.lang["region_game_config"]["title"])
        self.region_game_config.start.setText(self.lang["region_game_config"]["start"])
        self.region_game_config.return_main.setText(self.lang["region_game_config"]["return_main"])
        self.setCentralWidget(self.region_game_config)

        self.region_game_config.return_main.clicked.connect(self.draw_select_game)
        self.region_game_config.start.clicked.connect(self.run_region_game)
    
    def run_region_game(self):
        pass

# Start the application
if __name__ == '__main__':
    class sys: from sys import argv, exit
    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())