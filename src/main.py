# TODO: Write some comments

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from configparser import ConfigParser
class os: from os.path import dirname
class platform: from platform import system

lang = "Turkish.conf"
dirs = ConfigParser()

try:
    f = open(os.dirname(__file__)+"/chksrc")
    if f.read() == "Xt6xb5qnzU4N2aiOIQFzznThuRSznSXvkF20y2Gk30vCA5RcR9IUf6gpfXLvT9yoJIX5PN":
        srcrun = True
except:
    srcrun = False

userOS = platform.system()

# TODO: Complete this
if srcrun == True: dirs.read(os.dirname(__file__)+"/config/dirs/src.conf")
elif userOS == "Windows": dirs.read("C:/ProgramFiles/tubitak-flag")
elif userOS == "Linux": dirs.read("/etc/tubitak-flag/dirs/unix.conf")


class select_game(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi('./src/qt6-ui/select_game.ui', self)

class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.select_game = select_game()
        self.setCentralWidget(self.select_game)
        self.setFixedSize(639, 450)
        self.select_game.region_game.setText("Kıta bulma")

if __name__ == '__main__':
    class sys: from sys import argv, exit
    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())