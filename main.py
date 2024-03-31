import tkinter as tk
import threading
import events
import loudness
import traceback
import json
import ctypes
from time import sleep
t1 = threading.Thread(target=loudness.getloudness)
t1.daemon=True
t1.start()
def maineventhandler():
    global eventlist, eventdict, charbase,volume
    eventlist = []
    eventdict = {}
    charbase = {}
    while True:
        ee=True
        sleep(0.02)
        try:
            for a, event in enumerate(eventlist):
                if not event in eventdict:
                    eventdict[event]=charbase["events"][event]
            eventlist, eventdict=events.runevents(eventlist,eventdict,charbase,volume)
        except Exception as e:
            traceback.print_exc()
            print(e)

global eventdict, eventlist, charbase, lastselection, volume
eventlist=[]
eventdict={}
lastselection=""
def update_image():
    global eventdict, eventlist, volume, lastselection,charbase
    canvas.delete('all')
    imgs=[]
    settings=json.loads(open("settings.json", "r").read())
    selection=str(settings["select"])
    if not lastselection==selection:
        lastselection=selection
        eventlist=[]
        eventdict={}
    root.title("anitar 4 character "+selection)
    try:
        charbase=json.loads(open(f"chars/{selection}/charbase.json" ,"r").read())
    except FileNotFoundError:
        try:
            events.backwardscompatibility(selection)
            charbase=json.loads(open(f"chars/{selection}/charbase.json" ,"r").read())
        except:
            open("settings.json", "w").write('{"addition": -40,"select": "beispielchar1"}')
            charbase=json.loads(open(f"chars/beispielchar1/charbase.json" ,"r").read())
    seimages=[]
    if not "events" in charbase or not "audio" in charbase["events"]:
        try:
            charbase["events"]["audio"]={"type":"audio"}
        except:
            charbase["events"]={}
            charbase["events"]["audio"]={"type":"audio"}
    try:
        root.geometry(charbase["size"])
    except:
        root.geometry("400x400")
    try:
        canvas.configure(bg=charbase["backcolor"])
    except:
        canvas.configure(bg="black")
    try:
        volume=max(0,loudness.volume+settings["addition"])
        
        for i, layer in enumerate(charbase["layers"]):
            #if layer["event"]=="audio":
            #    pass
                #for num, imgfile in enumerate(layer["imagefiles"][::-1]):
                #    difference=len(layer["imagefiles"])*layer["loudnessdifference"]
                #    if volume>difference-(num*layer["loudnessdifference"]) or num+1==len(layer["imagefiles"]):
                #        pass
                        #if not imgfile == "nothing":
                        #            img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                        #            imgs.append([img,events.pos(volume)])
                        #try:
                        #    seimages.append(charbase["sideevents"]["audio"])
                        #except:
                        #    seimages.append(0)
                        #break
            #else:
            try:
                layer["loudnessdifference"]
            except:
                layer["loudnessdifference"]=0
            if layer["event"] in eventlist:
                do , xy = events.event(layer["event"],eventdict,volume,len(layer["imagefiles"]),charbase,layer["loudnessdifference"])
                if do.split(":")[0]=="display":
                    imgfile=layer["imagefiles"][int(do.split(":")[1])]
                    if not imgfile == "nothing":
                                img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                                imgs.append([img,xy])
                    try:
                        seimages.append(charbase["sideevents"][layer["event"]])
                    except:
                        seimages.append(0)
            else:
                eventlist.append(layer["event"])
                eventdict[layer["event"]]=charbase["events"][layer["event"]]
                if layer["event"] in eventlist:
                    do , xy = events.event(layer["event"],eventdict,volume,len(layer["imagefiles"]),charbase,layer["loudnessdifference"])
                    try:
                        if do.split(":")[0]=="display":
                            imgfile=layer["imagefiles"][int(do.split(":")[1])]
                            if not imgfile == "nothing":
                                img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                                imgs.append([img,xy])
                            try:
                                seimages.append(charbase["sideevents"][layer["event"]])
                            except:
                                seimages.append(0)
                    except:
                        do="display:0"
                        if do.split(":")[0]=="display":
                            imgfile=layer["imagefiles"][int(do.split(":")[1])]
                            img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                            imgs.append([img,xy])
                            try:
                                seimages.append(charbase["sideevents"][layer["event"]])
                            except:
                                seimages.append(0)
        for i, img in enumerate(imgs):
            x=img[1][0]
            y=img[1][1]
            img=img[0]
            canvas.create_image(x, y, anchor=tk.NW, image=img)
        canvas.images = imgs
    except Exception as e:
        print(e, "this is a error")
        traceback.print_exc()
        pass
    root.after(50, update_image)

root = tk.Tk()
canvas = tk.Canvas(root, width=1500, height=1500, highlightthickness=0)
canvas.pack()
root.bind('<Escape>', lambda event: events.menu(event, root))
root.resizable(False, False)
root.iconbitmap('app.ico')
t2 = threading.Thread(target=maineventhandler)
t2.daemon=True
t2.start()
update_image()

root.mainloop()