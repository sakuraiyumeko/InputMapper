import pyglet
import subprocess
import os
import time


def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

oldv=0
#window = pyglet.window.Window()
devices = pyglet.input.get_devices()


for device in devices:
    device.open()

while True:
    for device in devices:
        controls = device.get_controls()
        if any(x in device.name for x in ("eceiver", "ilter", "已转换", "系统", "键盘", "鼠标")):
            continue
        if controls == []:
            continue
        for j, control in enumerate(controls):
            if oldv!= control.value:
                print(f"[{j}] [{device.name}] {control.name or control.raw_name}->{control.value}")
            oldv=control.value
        clear()


"""@window.event
def on_key_press(symbol,modifiers):
    clear()
    print("KEY DOWN: ",symbol)

@window.event
def on_key_release(symbol,modifiers):
    clear()
    print("KEY UP: ",symbol)

@window.event
def on_mouse_press(x,y,button,modifiers):
    clear()
    print("MOUSE DOWN: ",f"{(x,y)}",button)

@window.event
def on_mouse_motion(x,y,dx,dy):
    clear()
    print("MOUSE MOVE: ",f"{(x,y)}",dx,dy)"""


