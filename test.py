import pyglet
import subprocess
import os
from pprint import pprint
import inspect

def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

clear()
devices = pyglet.input.get_devices()

for device in devices:
    if "X" in device.name:
        controls=device.get_controls()
        Button_test=controls[9]
        AbsoluteAxis_test=controls[15]
        
        print(inspect.getfile(type(Button_test)))
        
        
        '''pprint(Button_test.__dict__)
        pprint(AbsoluteAxis_test.__dict__)
        
        pprint(Button_test.__class__.__dict__)
        print()
        pprint(AbsoluteAxis_test.__class__.__dict__)'''
        
        '''print(type(Button_test))
        print(Button_test.__class__)
        print(type(Button_test).value.fget)
        print(type(Button_test).value.fget.__qualname__)
        print(type(Button_test).value.fget.__code__.co_names)
        
        pprint(inspect.getsource(type(Button_test).value.fget))'''
        
        '''print(f"{Button_test}->{type(Button_test)}")
        print(f"{AbsoluteAxis_test}->{type(AbsoluteAxis_test)}")'''
        '''print(controls)
        print(device, "->", type(device))
        print(device.__class__)
        pprint(device.__dict__)'''
        
        
        
input()
