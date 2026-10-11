import pynput
import time
import tomllib
from pathlib import Path
from pprint import pprint

# Config file path
config_path = Path(__file__).resolve().parent / "config.toml"

# Config import
with config_path.open("rb") as f:
    config = tomllib.load(f)

print("Config loaded.")
pprint(config)
isDebug = config["General"]["isDebug"]
char_map = {
    tuple(int(part) for part in key.split(",")):value for key,value in config["Mapping"].items()           
}


# Mapping list
vktonum = {
    96: 0,
    97: 1,
    98: 2,
    99: 3,
    100: 4,
    101: 5,
    102: 6,
    103: 7,
    104: 8,
    105: 9,
}

# Function mapping
mapping = {
    0: pynput.keyboard.Key.space,
    1: pynput.keyboard.Key.shift,
    2: pynput.keyboard.Key.ctrl,
    3: pynput.keyboard.Key.alt,
    4: pynput.keyboard.Key.cmd,
    5: pynput.keyboard.Key.esc,
    6: pynput.keyboard.Key.tab,
}

# Initialization
buffer = []
pressed = []
numpad = {96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 110}# legal key value


keyboard = pynput.keyboard.Controller()

def on_press(key):
    # debug info output
    if isDebug:
        try:
            print(
                f"{key}:{key.vk}",
                time.strftime("Local: %Y-%m-%d %H:%M:%S"),
                time.strftime("UTC: %Y-%m-%d %H:%M:%S", time.gmtime()),
                sep="  ",
            )
        except AttributeError:
            print(
                f"{key}:None",
                time.strftime("Local: %Y-%m-%d %H:%M:%S"),
                time.strftime("UTC: %Y-%m-%d %H:%M:%S", time.gmtime()),
                sep="  ",
            )
            
    # main
    try:
        # Only append keys which have key value.
        if key.vk in numpad:
            buffer.append(key.vk)

        # Key value of '+' is 107.
        if key.vk == 107:# Delete num sequence when confirm.
            if len(buffer) != 0:
                for i in range(0, len(buffer) + 1):
                    keyboard.press(pynput.keyboard.Key.backspace)
                    keyboard.release(pynput.keyboard.Key.backspace)

            i = 0
            # Process function input.
            while i < len(buffer): 
                if buffer[i] == 110: # 110 is the key value of ".".
                    i += 1
                    while i < len(buffer) and buffer[i] != 110:
                        try:
                            press = mapping[vktonum[buffer[i]]]
                            pressed.append(press)
                            keyboard.press(press)
                        except KeyError:
                            print("\nUnexpected input: Undefined function.\n")
                        i += 1
                    if i >= len(buffer): # Avoid IndexError
                        break
                    i += 1

                # Load tuple
                try:
                    a = buffer[i]
                    b = buffer[i + 1]
                except IndexError:
                    break

                try:# Characters convert
                    char = char_map[(vktonum[a], vktonum[b])]
                    keyboard.press(char)
                    keyboard.release(char)
                    for keys in pressed:
                        keyboard.release(keys)
                    pressed.clear()
                except (KeyError, UnboundLocalError):
                    print("\nUnexpected input: Undefined tuple.\n")

                i += 2

            for keys in pressed:
                keyboard.release(keys)

            pressed.clear()
            buffer.clear()

    except AttributeError:
        # Just backspace
        if key == pynput.keyboard.Key.backspace and buffer:
            buffer.pop()


listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
