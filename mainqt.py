import threading
import sys
import json
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
from PyQt5.QtCore import QTimer, Qt
import windowsettings
import events
import menus
import loudness
import platform
import traceback
t1 = threading.Thread(target=loudness.getloudness)
t1.daemon = True
t1.start()
try:
    open("settings.json").close()
except:
    with open("settings.json", "w") as createsettings:
        createsettings.write('{\n"addition": 120,\n"select": "none"\n}')
def keyp(event):
    global close
    global window
    if event.key() == Qt.Key_Escape:
        close=menus.settings("","", qtv=True, darkmode=darkmode)
    if event.key() == Qt.Key_F3:
        menus.charerror(charerrors, darkmode=darkmode)
        
def maineventhandler():
    global eventlist, eventdict, charbase, volume, close
    eventlist = []
    eventdict = {}
    charbase = {}
    while True:
        ee = True
        sleep(0.02)
        try:
            for a, event in enumerate(eventlist):
                if event not in eventdict:
                    eventdict[event] = charbase["events"][event]
            eventlist, eventdict = events.runevents(eventlist, eventdict, charbase, volume)
        except Exception as e:
            pass

global eventdict, eventlist, charbase, lastselection, volume,charerrors
charerrors=[{"message":"this program isnt finished yet there could be things that dont work like intented","type":"info"}]
eventlist = []
eventdict = {}
lastselection = ""
global darkmode
if platform.system().lower()=="windows" or platform.system().lower()=="linux" and json.loads(open("settings.json").read())["transparent"]:
    darkmode=True
else:
    darkmode=False
def update_image():
    global eventdict, eventlist, volume, lastselection, charbase, close
    try:
        if close:
            sys.exit()
    except Exception as e:
        pass
    try:
        close=events.close
    except:
        pass
    scene.clear()
    imgs = []
    settings = json.loads(open("settings.json", "r").read())
    selection = str(settings["select"])
    if lastselection != selection:
        lastselection = selection
        eventlist = []
        eventdict = {}
    window.setWindowTitle("anitar 4 character " + selection)
    try:
        backgroundcolor=charbase["backcolor"]
        window.setStyleSheet(f"background-color: {backgroundcolor};")
    except:
        pass
    try:
        size=charbase["size"].split("x")
        window.setFixedSize(int(size[0]),int(size[1]))
    except:
        window.setFixedSize(400,400)
    try:
        charbase = json.loads(open(f"chars/{selection}/charbase.json", "r").read())
    except FileNotFoundError:
        try:
            events.backwardscompatibility(selection)
            charbase = json.loads(open(f"chars/{selection}/charbase.json", "r").read())
        except:
            open("settings.json", "w").write('{\n    "addition": 120,\n    "select": "beispielchar1"\n}')
            charbase = json.loads(open(f"chars/beispielchar1/charbase.json", "r").read())
    seimages = []
    if "events" not in charbase or "audio" not in charbase["events"]:
        try:
            charbase["events"]["audio"] = {"type": "audio"}
        except:
            charbase["events"] = {}
            charbase["events"]["audio"] = {"type": "audio"}
    try:
        volume=max(0,loudness.volume+settings["addition"])
        for i, layer in enumerate(charbase["layers"]):
            try:
                layer["loudnessdifference"]
            except:
                layer["loudnessdifference"] = 0
            if layer["event"] in eventlist:
                do, xy = events.event(layer["event"], eventdict, volume, len(layer["imagefiles"]), charbase,
                                      layer["loudnessdifference"])
                if do.split(":")[0] == "display":
                    imgfile = layer["imagefiles"][int(do.split(":")[1])]
                    if imgfile != "nothing":
                        img_path = f'chars/{settings["select"]}/{imgfile}'
                        img = QPixmap(img_path)
                        imgs.append([img, xy])
                    try:
                        seimages.append(charbase["sideevents"][layer["event"]])
                    except:
                        seimages.append(0)
            else:
                eventlist.append(layer["event"])
                eventdict[layer["event"]] = charbase["events"][layer["event"]]
                if layer["event"] in eventlist:
                    do, xy = events.event(layer["event"], eventdict, volume, len(layer["imagefiles"]), charbase,
                                          layer["loudnessdifference"])
                    try:
                        if do.split(":")[0] == "display":
                            imgfile = layer["imagefiles"][int(do.split(":")[1])]
                            if imgfile != "nothing":
                                img_path = f'chars/{settings["select"]}/{imgfile}'
                                img = QPixmap(img_path)
                                imgs.append([img, xy])
                            try:
                                seimages.append(charbase["sideevents"][layer["event"]])
                            except:
                                seimages.append(0)
                    except:
                        do = "display:0"
                        if do.split(":")[0] == "display":
                            imgfile = layer["imagefiles"][int(do.split(":")[1])]
                            img_path = f'chars/{settings["select"]}/{imgfile}'
                            img = QPixmap(img_path)
                            imgs.append([img, xy])
                            try:
                                seimages.append(charbase["sideevents"][layer["event"]])
                            except:
                                seimages.append(0)
        for i, img in enumerate(imgs):
            x = img[1][0]
            y = img[1][1]
            img = img[0]
            scene.addPixmap(img).setPos(x, y)
    except Exception as e:
        pass
    QTimer.singleShot(50, update_image)
global window
app = QApplication(sys.argv)
window = QMainWindow()
scene = QGraphicsScene()
view = QGraphicsView(scene)
view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
try:
    if json.loads(open("settings.json").read())["transparent"]:
        view.setStyleSheet("background: transparent; border: none;")
        scene.setBackgroundBrush(Qt.transparent)
        window.setWindowFlags(Qt.FramelessWindowHint)
        window.setAttribute(Qt.WA_TranslucentBackground, True)
    else:
        view.setStyleSheet("border: none;")
except:
    view.setStyleSheet("border: none;")
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.keyPressEvent = keyp
window.setCentralWidget(view)
window.setWindowIcon(QIcon('app.ico'))
windowsettings.darkmode(window,darkmode)
windowsettings.nofullscreen(window)
window.setFixedSize(400,400)
update_image()
window.show()
t2 = threading.Thread(target=maineventhandler)
t2.daemon = True
t2.start()
sys.exit(app.exec_())