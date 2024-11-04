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
class anitar:
    def reload_settings():
           shared.reload_settings=True