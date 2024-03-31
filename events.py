import tkinter as tk
import os
import json
def pos(volume,eventname="",eventdict={},cpos=[0,0]):
    return [-cpos[0],-cpos[1]]
def event(eventname,eventdict,volume,imgc,ldif=100):
    try:
        posv=pos(volume,eventname,eventdict,eventdict[eventname]["pos"]["pos"])
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
def runevents(eventlist,eventdict,charbase):
    renew=[]
    for num, event in enumerate(eventlist):
        try:
            if eventdict[event]["type"] in ["cycle","ticker"]:
                if eventdict[event]["timeticked"]>=eventdict[event]["time"]:
                    try:
                        if eventdict[event]["timeslept"]>=eventdict[event]["sleep"]:
                            
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
def menu(event, root):
    b=open("settings.json", "r")
    add=json.loads(b.read())["addition"]
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry("300x200")
    new_window.resizable(False, False)
    
    number_label = tk.Label(new_window, text="Loudness Increment:")
    number_label.pack(pady=7)
    number_entry = tk.Entry(new_window)
    number_entry.pack(pady=7)
    
    
    selection_label = tk.Label(new_window, text="select char:")
    selection_label.pack(pady=7)
    
    
    options = os.listdir("chars/")
    selected_option = tk.StringVar(new_window)
    selected_option.set(options[0]) 
    selection_menu = tk.OptionMenu(new_window, selected_option, *options)
    selection_menu.pack(pady=7)
    
    
    def save_data():
        
        loudness_increment = number_entry.get()
        selected_character = selected_option.get()
        if not loudness_increment:
            loudness_increment = str(add)
        save={"select":selected_character,"addition":int(loudness_increment)}
        a=open("settings.json","w")
        a.write(json.dumps(save, indent=4, sort_keys=True))
        a.close()
    save_button = tk.Button(new_window, text="Save", command=save_data)
    save_button.pack(pady=10)
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