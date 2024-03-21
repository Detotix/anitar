def event(eventname,eventdict):
    try:
        if eventdict[eventname]["type"]=="ticker":
            if eventdict[eventname]["time"]<=eventdict[eventname]["timeticked"]:
                return "display:1", [0,0]
            else:
                return "display:0", [0,0]
    except:
        eventdict[eventname]["timeticked"]=0
        if eventdict[eventname]["type"]=="ticker":
            if eventdict[eventname]["time"]<=eventdict[eventname]["timeticked"]:
                return "display:1", [0,0]
            else:
                return "display:0", [0,0]
    try:
        if eventdict[eventname]["type"]=="cycle":
            imgdisplaytime=eventdict[eventname]["time"]*100/eventdict[eventname]["imgcount"]
            image=eventdict[eventname]["timeticked"]*100//imgdisplaytime
            if int(image+1)>eventdict[eventname]["imgcount"]-1:
                raise("this isn't an error")
            return f"display:{int(image+1)}", [0,0]
    except:
        return "display:0", [0,0] 
    if eventdict[eventname]["type"]=="img":
        return "display:0", [0,0]
def runevents(eventlist,eventdict):
    renew=[]
    for num, event in enumerate(eventlist):
        try:
            if eventdict[event]["type"] in ["cycle","ticker"]:
                if eventdict[event]["timeticked"]>=eventdict[event]["time"]:
                    if eventdict[event]["timeslept"]>=eventdict[event]["sleep"]:
                        del eventdict[event]
                        del eventlist[num-1]
                    else:
                        eventdict[event]["timeslept"]+=0.005
                else:
                    eventdict[event]["timeticked"]+=0.005
        except:
            eventdict[event]["timeticked"]=+0
            eventdict[event]["timeslept"]=+0
    return eventlist, eventdict