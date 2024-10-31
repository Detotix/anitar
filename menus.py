from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QIcon
import sys
import windowsettings
import os
import json

#TODO create some comments for everything

def presettings(darkmode=False):
    app = QApplication.instance()

    new_window = QMainWindow()
    new_window.setWindowIcon(QIcon('app.ico'))
    new_window.setWindowTitle("settings")
    new_window.setGeometry(300, 200, 300, 200)
    new_window.setFixedSize(new_window.size())
    windowsettings.darkmode(new_window, darkmode)
    windowsettings.nofullscreen(new_window)

    new_window.show()

    loop = QEventLoop()
    new_window.destroyed.connect(loop.quit)
    loop.exec_()
def settings(ev="", root="", qtv=False, darkmode=False):
    global close
    end=False
    close = False
    b = open("settings.json", "r")
    add = json.loads(b.read())["addition"]
    b.close()

    # Check if a QApplication instance already exists
    if not qtv:
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    new_window = QMainWindow()
    new_window.setWindowIcon(QIcon('app.ico'))
    new_window.setWindowTitle("settings")
    new_window.setGeometry(300, 200, 300, 200 if not qtv else 250)
    new_window.setFixedSize(new_window.size())
    windowsettings.darkmode(new_window,darkmode)
    windowsettings.nofullscreen(new_window)

    number_label = QLabel("Loudness Increment:")
    number_entry = QLineEdit()
    selection_label = QLabel("select char:")
    options = os.listdir("chars/")
    selected_option = QComboBox()
    selected_option.addItems(options)
    selected_option.setCurrentIndex(0)

    def close_p():
        global close
        close = True
        end=True
        sys.exit()
        new_window.hide()

    def close_root():
        end=True
        new_window.hide()

    def save_data():
        global close
        loudness_increment = number_entry.text()
        selected_character = selected_option.currentText()
        if not loudness_increment:
            loudness_increment = str(add)
        save = {"select": selected_character, "addition": int(loudness_increment)}
        save=json.loads(open("settings.json", "r").read()) | save
        with open("settings.json", "w") as a:
            a.write(json.dumps(save, indent=4, sort_keys=True))
        new_window.close()

    save_button = QPushButton("Save")
    save_button.clicked.connect(save_data)
    layout = QVBoxLayout()
    layout.addWidget(number_label)
    layout.addWidget(number_entry)
    layout.addWidget(selection_label)
    layout.addWidget(selected_option)
    layout.addWidget(save_button)
    if qtv:
        closee = QPushButton("close programm")
        closee.clicked.connect(close_p)
        layout.addWidget(closee)
    central_widget = QWidget()
    central_widget.setLayout(layout)
    new_window.setCentralWidget(central_widget)
    new_window.show()
    if not qtv:
        # Start the application's event loop if no QApplication instance was running
        app.exec_()
    else:
        # Use a QEventLoop to wait for the window to be closed
        loop = QEventLoop()
        new_window.destroyed.connect(loop.quit)
        loop.exec_()
    return close
def charerror(knownerrors,darkmode=False):
    app = QApplication.instance()

    new_window = QMainWindow()
    new_window.setWindowIcon(QIcon('app.ico'))
    new_window.setWindowTitle("Char error menu - pre (unfinished)")
    new_window.setGeometry(0, 0, 700, 400)
    new_window.setFixedSize(new_window.size())
    windowsettings.darkmode(new_window, darkmode)
    windowsettings.nofullscreen(new_window)
    for i, error in enumerate(knownerrors):
        identifyer = QLabel("{0}".format(error["type"]), new_window)
        identifyer.move(30,i*21)
        errormessage = QLabel("---  {0}".format(error["message"]), new_window)
        errormessage.move(60,i*21)
        errormessage.setMinimumSize(600, 5)
        etype=error["type"].replace("warn", "#FFDE59").replace("error", "#EE4345").replace("info", "#98F5F9")
        identifyer.setStyleSheet(f"color: {etype};")
        errormessage.setStyleSheet(f"color: {etype};")

    new_window.show()

    loop = QEventLoop()
    new_window.destroyed.connect(loop.quit)
    loop.exec_()