import importlib
import os
def loadextensions():
    if os.path.exists("extensions"):
        extensionlist=os.listdir("extensions")
        for num,obj in enumerate(extensionlist):
            spec = importlib.util.spec_from_file_location(obj, f"extensions/{obj}/__init__.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "init"):
                module.init()
    else:
        os.mkdir("extensions")
        extensionlist=[]
        
    return extensionlist
def display_event(ext,event,eventdict,volume):
    spec = importlib.util.spec_from_file_location(ext, f"extensions/{ext}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module,event)
    return func(eventdict,volume)
