import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
class shared:
    charerrors=[{"message":"this program isnt finished yet there could be things that dont work like intented","type":"info"}]
    reload_char=True
    reload_settings=True
    settings={}
    selection={}
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
                message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                message_box.exec_()

class anitar:
    def reload_settings():
           shared.reload_settings=True
class audio_devices:
    selected_device = ["default", -1]
    device_list = ["default"]
    device_dict = {"default":-1}