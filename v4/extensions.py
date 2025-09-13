#these are old v4 py files they are still needed for v5 and will probably be forever be needed in v5 but they will evolve with v5 too
import importlib
import os
import sys
import traceback
import program
import time
class extensions:
    extensions={}
class extension_tools:
    def test():
        print("seems to work")
#loads all extensions
def loadextensions():
    time.sleep(3)
    if os.path.exists("extensions"):
        #takes the extensions folder as the extension list
        extensionlist=os.listdir("extensions")
        for num,obj in enumerate(extensionlist):
            if not os.path.exists(f"workingdir/{obj}"):
                os.mkdir(f"workingdir/{obj}")
            #checks if all necessary files exist
            if not os.path.exists(f"extensions/{obj}/extension.json") or not os.path.exists(f"extensions/{obj}/__init__.py"):
                
                #error message (didnt contain all files)
                program.char.charerrorlater("error", f"extension {obj} didnt contain all needed files (ignored extension)")
                if not os.path.exists(f"extensions/{obj}/extension.json"):
                    program.char.charerrorlater("warn", "- extension.json")
                if not os.path.exists(f"extensions/{obj}/__init__.py"):
                    program.char.charerrorlater("warn", "- __init__.py")

                #removes extension out of the list that the program wont use it
                extensionlist.remove(obj)
            else:
                extensions.extensions[obj]={"status":"working"}
            try:
                #loads the extension and calles the init function if it exists
                spec = importlib.util.spec_from_file_location(obj, f"extensions/{obj}/__init__.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "init"):
                    module.init()
                
            except:
                pass
    else:
        #creates the extensions folder if it dosnt exist
        os.mkdir("extensions")
        extensionlist=[]

    return extensionlist
#calles the display event function from extension
def display_event(ext,event,eventdict,volume):
    #loads extension
    spec = importlib.util.spec_from_file_location(ext, f"extensions/{ext}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module.display_event,event)
    #sets working dir to the extension working directory
    olddir=os.getcwd()
    os.chdir(f"workingdir/{ext}")
    try:
        #runs the function
        returnvalue=func(eventdict,volume)
    except:
        #if the function of the display event had an error
        #the message gets added to the char error screen
        program.char.charerror("error",f"extension {ext} function {event} had an error eventtype:display_event")
        program.char.charerror("warn", traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])[0].strip())
        extensions.extensions[ext]["status"]="error"
    #sets the working dir to the main dir
    os.chdir(olddir)
    return returnvalue
def extension_event(ext,event):
    #loads extension
    spec = importlib.util.spec_from_file_location(ext, f"extensions/{ext}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module.extension_event,event)
    #sets working dir to the extension working directory
    olddir=os.getcwd()
    os.chdir(f"workingdir/{ext}")
    try:
        #runs the function
        func()
    except:
        #if the function of the extension event had an error
        #the message gets added to the char error screen
        program.char.charerror("error",f"extension {ext} function {event} had an error eventtype:extension_event")
        program.char.charerror("warn", traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])[0].strip())
        extensions.extensions[ext]["status"]="error"
    os.chdir(olddir)
    #sets the working dir to the main dir
def getextension_event(ext,event):
    #loads extension
    spec = importlib.util.spec_from_file_location(ext, f"extensions/{ext}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module.extension_event,event)
    #sets working dir to the extension working directory
    return func