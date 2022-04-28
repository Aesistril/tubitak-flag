#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSvg
from configparser import ConfigParser
class random: from random import randint, choice
class os: 
    from os.path import dirname, splitext
    from os import listdir, environ
class platform: from platform import system
from playsound import playsound
from threading import Thread

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

# Language selection menu
class select_lang(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/select_lang.ui', self)
class question_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/question.ui', self)

class choice_widget(QtWidgets.QWidget):
    def __init__(self, parent=None, text="choice"):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/choice.ui', self)
        self.choice_name.setText(text)

class country_game_config(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/country_game_config.ui', self)

class end_game(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        uic.loadUi(dirs["resources"]["qt6-ui"].replace("-filepath-", os.dirname(__file__))+'/end_game.ui', self)

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
        self.lang.read(dirs["resources"]["lang"].replace("-filepath-", os.dirname(__file__)) + "/" + self.select_lang.comboBox.currentText() + ".conf", encoding="utf-8")
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
        self.select_game.country_game.setText(self.lang["sel_game"]["country_game"])
        self.select_game.region_game.setText(self.lang["sel_game"]["region_game"])
        self.select_game.country_game.clicked.connect(self.draw_country_game_config)
        self.select_game.region_game.clicked.connect(self.draw_region_game_config)
        self.setCentralWidget(self.select_game)
        self.setFixedSize(640, 450)

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
        try: del self.region_game, self.question_widget
        except: pass
        self.question_widget = question_widget()
        self.question_widget.tf.setText(self.lang["question"]["tf_format"].replace("-correct-", str(0)).replace("-false-", str(0)))
        self.setCentralWidget(self.question_widget)
        self.choice_count = self.region_game_config.choice_count_spin.value()
        self.setFixedSize(640, 40+320+(60*self.choice_count))
        self.correct_ans, self.false_ans, self.solved_q_count = 0, 0, 0
        self.region_game_qc = self.region_game_config.q_count_spin.value()
        self.draw_question(self.question_widget, self.choice_count, self.region_game_qc, self.lang["region_list"]["list"].split(","), mode="region")

    def draw_country_game_config(self):
        # Delete the old self.country_game_config if possible
        try: del self.country_game_config
        except: pass
        self.country_game_config = country_game_config()
        self.country_game_config.choice_count_label.setText(self.lang["country_game_config"]["choice_count_label"])
        self.country_game_config.q_count_label.setText(self.lang["country_game_config"]["q_count_label"])
        self.country_game_config.title.setText(self.lang["country_game_config"]["title"])
        self.country_game_config.start.setText(self.lang["country_game_config"]["start"])
        self.country_game_config.return_main.setText(self.lang["country_game_config"]["return_main"])
        self.setCentralWidget(self.country_game_config)
        self.country_game_config.return_main.clicked.connect(self.draw_select_game)
        self.country_game_config.start.clicked.connect(self.run_country_game)
    
    def run_country_game(self):
        try: del self.country_game, self.question_widget
        except: pass
        self.question_widget = question_widget()
        self.question_widget.tf.setText(self.lang["question"]["tf_format"].replace("-correct-", str(0)).replace("-false-", str(0)))
        self.setCentralWidget(self.question_widget)
        self.choice_count = self.country_game_config.choice_count_spin.value()
        self.setFixedSize(640, 60+320+(60*self.choice_count))
        self.correct_ans, self.false_ans, self.solved_q_count = 0, 0, 0
        self.country_game_qc = self.country_game_config.q_count_spin.value()
        self.draw_question(self.question_widget, self.choice_count, self.country_game_qc, self.lang["country_list"]["list"].split(","), mode="country")

    def draw_question(self, gameObj, choice, q_count, choice_list, mode): # Generate a new question and display it
        self.correct = random.randint(1, choice) # Decide the correct answer
        self.correct_ans_name = random.choice(self.lang["country_list"]["list"].split(",")).lower()
        # Display a random flag
        self.flag = QtGui.QPixmap()
        # debug_flag_test = ""
        # self.flag.load(debug_flag_test)
        self.flag.load(dirs["resources"]["flags"].replace("-filepath-", os.dirname(__file__))+"/"+self.correct_ans_name+".png")
        self.flag = self.flag.scaledToWidth(640)
        gameObj.flag_pic.setPixmap(self.flag)
        gameObj.flag_pic.setAlignment(QtCore.Qt.AlignCenter)
        # Delete old buttons if possible
        try:
            for i in range(1, choice+1):
                locals()[str(i)+"cho"].setParent(None)
                del locals()[str(i)+"cho"]
        except: pass
        if mode == "country":
        # Draw and connect the choice buttons
            choosed_countries = [] # Prevent duplicate answers
            choosed_countries.append(self.correct_ans_name)
            y = 380
            for i in range(1, choice+1):
                if i == self.correct:
                    locals()[str(i)+"cho"] = choice_widget(parent=gameObj, text=self.lang["country_names"][self.correct_ans_name])
                    locals()[str(i)+"cho"].move(0, y)
                    locals()[str(i)+"cho"].choice_name.clicked.connect(lambda: self.correct_func(q_count, gameObj, mode))
                else:
                    while True:
                        rand_country = random.choice(choice_list).lower()
                        if rand_country not in choosed_countries:
                            choosed_countries.append(rand_country)
                            break
                    locals()[str(i)+"cho"] = choice_widget(parent=gameObj, text=self.lang["country_names"][rand_country])
                    locals()[str(i)+"cho"].move(0, y)
                    locals()[str(i)+"cho"].choice_name.clicked.connect(lambda: self.false_func(q_count, gameObj, mode))
                y += 60
        elif mode == "region":
            y = 380
            choosed_regions = [] # Don't choose the same region twice
            # Pick another country if first one does not exist
            while True:
                try:
                    correct_region = self.lang["regions"][self.correct_ans_name] # Find the correct answer
                except:
                    self.correct_ans_name = random.choice(self.lang["country_list"]["list"].split(",")).lower() # Choose another country
                else: 
                    break
            choosed_regions.append(correct_region)
            for i in range(1, choice+1):
                if i == self.correct:
                    locals()[str(i)+"cho"] = choice_widget(parent=gameObj, text=correct_region)
                    locals()[str(i)+"cho"].move(0, y)
                    locals()[str(i)+"cho"].choice_name.clicked.connect(lambda: self.correct_func(q_count, gameObj, mode))
                else:
                    while True:
                        rand_region = random.choice(choice_list)
                        if rand_region not in choosed_regions:
                            choosed_regions.append(rand_region)
                            break
                    locals()[str(i)+"cho"] = choice_widget(parent=gameObj, text=rand_region)
                    locals()[str(i)+"cho"].move(0, y)
                    locals()[str(i)+"cho"].choice_name.clicked.connect(lambda: self.false_func(q_count, gameObj, mode))
                y += 60
    
    def correct_func(self, q_count, gameObj, mode):
        sound_thread = Thread(target=lambda: playsound(sound=dirs["resources"]["sounds"].replace("-filepath-", os.dirname(__file__))+"/correct.wav"))
        sound_thread.start()
        self.correct_ans += 1
        self.solved_q_count += 1
        self.setCentralWidget(None)
        del gameObj
        gameObj = question_widget()
        self.setCentralWidget(gameObj)
        gameObj.tf.setText(self.lang["question"]["tf_format"].replace("-correct-", str(self.correct_ans)).replace("-false-", str(self.false_ans)))
        if mode == "country":
            self.draw_question(gameObj, self.choice_count, q_count, self.lang["country_list"]["list"].split(","), mode)
        elif mode == "region":
            self.draw_question(gameObj, self.choice_count, self.region_game_qc, self.lang["region_list"]["list"].split(","), mode)
        if self.solved_q_count == q_count:
            self.draw_end_game()
    
    def false_func(self, q_count, gameObj, mode):
        sound_thread = Thread(target=lambda: playsound(sound=dirs["resources"]["sounds"].replace("-filepath-", os.dirname(__file__))+"/wrong.wav"))
        sound_thread.start()
        self.false_ans += 1
        self.solved_q_count += 1
        self.setCentralWidget(None)
        del gameObj
        gameObj = question_widget()
        self.setCentralWidget(gameObj)
        gameObj.tf.setText(self.lang["question"]["tf_format"].replace("-correct-", str(self.correct_ans)).replace("-false-", str(self.false_ans)))
        if mode == "country":
            self.draw_question(gameObj, self.choice_count, q_count, self.lang["country_list"]["list"].split(","), mode)
        elif mode == "region":
            self.draw_question(gameObj, self.choice_count, self.region_game_qc, self.lang["region_list"]["list"].split(","), mode)
        if self.solved_q_count == q_count:
            self.draw_end_game()
    
    def draw_end_game(self):
        end_game_widget = end_game()
        if self.correct_ans >= self.false_ans:
            Thread(target=lambda: playsound(sound=dirs["resources"]["sounds"].replace("-filepath-", os.dirname(__file__))+"/clap.wav")).start()
            end_game_widget.title.setText(self.lang["end_game"]["title_win"])
        elif self.correct_ans < self.false_ans:
            Thread(target=lambda: playsound(sound=dirs["resources"]["sounds"].replace("-filepath-", os.dirname(__file__))+"/fail.wav")).start()
            end_game_widget.title.setText(self.lang["end_game"]["title_fail"])
        end_game_widget.result.setText(self.lang["end_game"]["result_format"].replace("-correct-", str(self.correct_ans)).replace("-false-", str(self.false_ans)))
        end_game_widget.home.setText(self.lang["end_game"]["return"])
        end_game_widget.home.clicked.connect(self.draw_select_game)
        self.setCentralWidget(end_game_widget)
            

# Start the application
if __name__ == '__main__':
    class sys: from sys import argv, exit
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    app = QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())
