class shared:
    charerrors=[{"message":"this program isnt finished yet there could be things that dont work like intented","type":"info"}]
def charerror(type,message):
     if not {"message": message,"type": type} in shared.charerrors:
                    shared.charerrors.append({"message":message,"type":type})