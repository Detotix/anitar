import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class wpos:
    def x():
        return 100
    def y():
        return 100   
class shared:
    dntclearcharerror=[{"message":"this program isnt finished yet there could be things that dont work like intented","type":"info"}]
    charerrors=[]
    reload_char=True
    reload_settings=True
    currenttransparency=False
    settings={}
    selection={}
    charerroronload=[]
    wpos=wpos
    mainwindow=0
    currentwindowsize=[400,400]
    windowtitle="anitar"
class char:
    def reload_char():
           shared.reload_char=True
           shared.reload_settings=True
    def charerror(type,message):
        if not {"message": message,"type": type} in shared.charerrors:
            shared.charerrors.append({"message":message,"type":type})
            if type=="error":
                message_box = QMessageBox()
                message_box.setWindowTitle("There was an error while loading the character.")
                message_box.setText(message)
                message_box.setIcon(QMessageBox.Critical)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    def charerrorlater(type, message):
         shared.charerroronload.append({"type":type, "message":message})
         shared.dntclearcharerror.append({"type":type, "message":message})
class anitar:
    def reload_settings():
           shared.reload_settings=True
class audio_devices:
    selected_device = ["default", -1]
    device_list = ["default"]
    device_dict = {"default":-1}