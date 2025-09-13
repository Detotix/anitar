#these are old v4 py files they are still needed for v5 and will probably be forever be needed in v5 but they will evolve with v5 too
import os
import json
import traceback
import extensions
import program
#TODO create some comments for everything
def pos(volume,eventname="",eventdict={},cpos=[0,0]):
    if f"#{eventname}" in eventdict:
        try:
            cpos[1]+=eventdict[f"#{eventname}"]["ypos"]+eventdict[f"{eventname}"]["pos"]["y"]
            cpos[0]+=eventdict[f"#{eventname}"]["xpos"]+eventdict[f"{eventname}"]["pos"]["x"]
        except Exception as e:
            traceback.print_exc()
            cpos[1]+=eventdict[f"#{eventname}"]["ypos"]
            cpos[0]+=eventdict[f"#{eventname}"]["xpos"]
    return [-cpos[0],-cpos[1]]
def event(eventname,eventdict,volume,imgc,charbase,exts,ldif=100):
    try:
        posv=pos(volume,eventname,eventdict,charbase["events"][eventname]["pos"]["pos"])
    except:
        posv=pos(volume,eventname,eventdict,[0,0])
    try:
        if eventdict[eventname]["type"]=="nothing":
            return "display:0", posv
        if eventdict[eventname]["type"]=="audio":
            difference=imgc*ldif
            for num in range(imgc):
                if volume>difference-(num*ldif) or num+1==imgc:
                    return f"display:{imgc-1-num}", posv
    except:
        return "display:0", posv
    try:
        if eventdict[eventname]["type"].split(".")[0] in exts:
            out="display:"+str(extensions.display_event(eventdict[eventname]["type"].split(".")[0],eventdict[eventname]["type"].split(".")[1],eventdict,volume))
            if out=="display:None":
                program.char.charerror("warn","recieved None from extension '{0}' function '{1}'".format(eventdict[eventname]["type"].split(".")[0]))
            return out, posv
    except Exception as e:
        pass
    try:
        if eventdict[eventname]["type"]=="ticker":
            if eventdict[eventname]["time"]<=eventdict[eventname]["timeticked"]:
                return "display:1", posv
            else:
                return "display:0", posv
    except:
        eventdict[eventname]["timeticked"]=0
        if eventdict[eventname]["type"]=="ticker":
            if eventdict[eventname]["time"]<=eventdict[eventname]["timeticked"]:
                return "display:1", posv
            else:
                return "display:0", posv
    try:
        if eventdict[eventname]["type"]=="cycle":
            imgdisplaytime=eventdict[eventname]["time"]*100/imgc
            image=eventdict[eventname]["timeticked"]*100//imgdisplaytime
            if int(image+1)>imgc-1:
                raise RuntimeError("this isn't an error")
            return f"display:{int(image+1)}", posv
    except:
        return "display:0", posv 
def runevents(eventlist,eventdict,charbase,volume):
    renew=[]
    #pos events
    for num, event in enumerate(eventlist):
        if "#" in event or not "pos" in eventdict[event]:
            continue
        add=3
        sub=3
        if "add" in eventdict[event]["pos"]:
            add=eventdict[event]["pos"]["add"]
        if "sub" in eventdict[event]["pos"]:
            sub=eventdict[event]["pos"]["sub"]
        try:
            if eventdict[event]["pos"]["type"]=="setpos.up":
                if volume>eventdict[event]["pos"]["loudness"] and eventdict[f"#{event}"]["ypos"]<=eventdict[event]["pos"]["max"]-1:
                    eventdict[f"#{event}"]["ypos"]+=add
                elif volume<eventdict[event]["pos"]["loudness"] and not eventdict[f"#{event}"]["ypos"]<=0:
                    eventdict[f"#{event}"]["ypos"]-=sub
            if eventdict[f"#{event}"]["ypos"]>eventdict[event]["pos"]["max"]:
                eventdict[f"#{event}"]["ypos"]=eventdict[event]["pos"]["max"]
            if eventdict[event]["pos"]["type"]=="loudness.up":
                if volume>eventdict[event]["pos"]["loudness"] and eventdict[f"#{event}"]["ypos"]<=eventdict[event]["pos"]["max"]-1:
                    eventdict[f"#{event}"]["ypos"]+=(volume-eventdict[event]["pos"]["loudness"])/100
                elif volume<eventdict[event]["pos"]["loudness"] and not eventdict[f"#{event}"]["ypos"]<=0:
                    eventdict[f"#{event}"]["ypos"]-=sub//2
            if eventdict[f"#{event}"]["ypos"]>eventdict[event]["pos"]["max"]:
                eventdict[f"#{event}"]["ypos"]=eventdict[event]["pos"]["max"]
            if eventdict[f"#{event}"]["ypos"]<0:
                eventdict[f"#{event}"]["ypos"]=0
        except Exception as e:
            eventdict[f"#{event}"]={}
            eventdict[f"#{event}"]["ypos"]=0
            eventdict[f"#{event}"]["xpos"]=0
            continue

    #events
    for num, event in enumerate(eventlist):
        if "#" in event:
            continue
        try:
            if eventdict[event]["type"] in ["cycle","ticker"]:
                if eventdict[event]["timeticked"]>=eventdict[event]["time"]:
                    if eventdict[event]["type"]=="cycle":
                        eventdict[event]["timeticked"]=0.0
                    try:
                        if eventdict[event]["timeslept"]>=eventdict[event]["sleep"]:
                            eventdict[event]["timeticked"]=0.0
                            eventdict[event]["timeslept"]=0.0
                            del eventdict[event]
                            del eventlist[num-1]
                        else:
                            eventdict[event]["timeslept"]+=0.005
                    except:
                        eventdict[event]["timeslept"]+=0.005
                else:
                    eventdict[event]["timeticked"]+=0.005
        except:
            eventdict[event]["timeticked"]=0.0
            eventdict[event]["timeslept"]=0.0
    return eventlist, eventdict

def backwardscompatibility(name):
    if not os.path.exists(f"chars/{name}/charbase.json"):
        charbase={"layers": [{"event":"audio","loudnessdifference": 120,"imagefiles": []}],"size":"400x400","backcolor":"#000000","events": {"mticker":{"type":"ticker","time":4,"sleep":0.05}}}
        for num in range(4):
            if os.path.exists(f"chars/{name}/{num+1}.png"):
                charbase["layers"][0]["imagefiles"].append(f"{num+1}.png")
        if os.path.exists(f"chars/{name}/conf"):
            b=open(f"chars/{name}/conf", "r").read().split("\n")
            for num, command in enumerate(b):
                if command.split(" ")[0]=="ticker":
                    charbase["layers"].append({"event":"mticker","imagefiles":[command.split(" ")[2],command.split(" ")[3]]})
        a=open(f"chars/{name}/charbase.json", "w")    
        a.write(json.dumps(charbase, indent=4))
        a.close()
        return True
    else:
        return False