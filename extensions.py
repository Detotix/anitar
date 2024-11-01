import importlib
import os
import sys
import ctypes
import traceback
import program

class extension_tools:
    def test():
        print("seems to work")
#loads all extensions
def loadextensions():
    if os.path.exists("extensions"):
        #takes the extensions folder as the extension list
        extensionlist=os.listdir("extensions")
        for num,obj in enumerate(extensionlist):
            if not os.path.exists(f"workingdir/{obj}"):
                os.mkdir(f"workingdir/{obj}")
            #checks if akll necessary files exist
            if not os.path.exists(f"extensions/{obj}/extension.json") or not os.path.exists(f"extensions/{obj}/__init__.py"):
                
                #error message (didnt contain all files)
                print(f"\033[91mextension {obj} didnt contain all needed files (ignored extension)\033[00m")
                if not os.path.exists(f"extensions/{obj}/extension.json"):
                    print("\033[91m-- extension.json\033[00m")
                if not os.path.exists(f"extensions/{obj}/__init__.py"):
                    print("\033[91m-- __init__.py\033[00m")

                #removes extension out of the list that the program wont use it
                extensionlist.remove(obj)
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
    spec = importlib.util.spec_from_file_location(ext, f"extensions/{ext}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module,event)
    olddir=os.getcwd()
    os.chdir(f"workingdir/{ext}")
    try:
        returnvalue=func(eventdict,volume)
    except:
        program.charerror("error",f"extension {ext} function {event} had an error")
        program.charerror("error", traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])[0].strip())
    os.chdir(olddir)
    return returnvalue