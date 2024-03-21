import tkinter as tk
import threading
import events
import loudness
import traceback
import json
from time import sleep
t1 = threading.Thread(target=loudness.getloudness)
t1.daemon=True
t1.start()
def maineventhandler():
    global eventlist, eventdict
    eventlist = []
    eventdict = {}
    while True:
        sleep(0.02)
        try:
            eventlist, eventdict=events.runevents(eventlist,eventdict)
        except:
            pass

global eventdict, eventlist
eventlist=[]
eventdict={}
def update_image():
    global eventdict, eventlist
    #try:
    #    eventlist, eventdict=events.runevents(eventlist,eventdict)
    #except:
    #    pass
    global volume
    canvas.delete('all')
    imgs=[]
    settings=json.loads(open("settings.json", "r").read())
    root.geometry(settings["size"])
    selection=str(settings["select"])
    root.title("anitar 4 character "+selection)
    charbase=json.loads(open(f"chars/{selection}/charbase.json" ,"r").read())
    seimages=[]
    try:
        canvas.configure(bg=charbase["backcolor"])
    except:
        canvas.configure(bg="black")
    try:
        volume=max(0,loudness.volume+settings["addition"])
        
        for i, layer in enumerate(charbase["layers"]):
            if layer["event"]=="audio":
                for num, imgfile in enumerate(layer["imagefiles"][::-1]):
                    difference=layer["imagefiles"].__len__()*layer["loudnessdifference"]
                    if volume>difference-(num*layer["loudnessdifference"]) or num+1==layer["imagefiles"].__len__():
                        img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                        imgs.append(img)
                        try:
                            seimages.append(charbase["sideevents"]["audio"])
                        except:
                            seimages.append(0)
                        break
            else:
                if layer["event"] in eventlist:
                    do , xy = events.event(layer["event"],eventdict)
                    if do.split(":")[0]=="display":
                        imgfile=layer["imagefiles"][int(do.split(":")[1])]
                        img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                        imgs.append(img)
                        try:
                            seimages.append(charbase["sideevents"][layer["event"]])
                        except:
                            seimages.append(0)
                else:
                    eventlist.append(layer["event"])
                    eventdict[layer["event"]]=charbase["events"][layer["event"]]
                    if layer["event"] in eventlist:
                        do=events.event(layer["event"],eventdict)
                        if do.split(":")[0]=="display":
                            imgfile=layer["imagefiles"][int(do.split(":")[1])]
                            img = tk.PhotoImage(file=f'chars/{settings["select"]}/{imgfile}')
                            imgs.append(img)
                            try:
                                seimages.append(charbase["sideevents"][layer["event"]])
                            except:
                                seimages.append(0)
        for i, img in enumerate(imgs):
            x=0
            y=0
            
            canvas.create_image(x, y, anchor=tk.NW, image=img)
        canvas.images = imgs
    except Exception as e:
        print(e, "this is a error")
        traceback.print_exc()
        pass
    root.after(50, update_image)

root = tk.Tk()
canvas = tk.Canvas(root, width=int(json.loads(open("settings.json", "r").read())["size"].split("x")[0]), height=int(json.loads(open("settings.json", "r").read())["size"].split("x")[1]), highlightthickness=0)
canvas.pack()
root.resizable(False, False)
root.iconbitmap('app.ico')
t2 = threading.Thread(target=maineventhandler)
t2.daemon=True
t2.start()
# Start the first update
update_image()

root.mainloop()