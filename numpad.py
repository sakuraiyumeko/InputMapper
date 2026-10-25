import pynput
import time
import tomllib
from pathlib import Path
from pprint import pprint

# Config file path
config_path = Path(__file__).resolve().parent / "numpad_config.toml"

# Config import
with config_path.open("rb") as f:
    config = tomllib.load(f)

print("Config loaded.")
pprint(config)
isDebug = config["General"]["isDebug"]
char_map = {
    tuple(int(part) for part in key.split(",")):value for key,value in config["CharMapping"].items()           
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
modifier = {
    "space": pynput.keyboard.Key.space,
    "shiftL": pynput.keyboard.Key.shift_l,
    "shiftR": pynput.keyboard.Key.shift_r,
    "ctrl": pynput.keyboard.Key.ctrl,
    "alt": pynput.keyboard.Key.alt,
    "cmd": pynput.keyboard.Key.cmd,
    "esc": pynput.keyboard.Key.esc,
    "tab": pynput.keyboard.Key.tab,
}

modifier_mapping = {
    int(key): modifier[value]
    for key, value in config["ModifierMapping"].items()
}

func = {
    "f1": pynput.keyboard.Key.f1,
    "f2": pynput.keyboard.Key.f2,
    "f3": pynput.keyboard.Key.f3,
    "f4": pynput.keyboard.Key.f4,
    "f5": pynput.keyboard.Key.f5,
    "f6": pynput.keyboard.Key.f6,
    "f7": pynput.keyboard.Key.f7,
    "f8": pynput.keyboard.Key.f8,
    "f9": pynput.keyboard.Key.f9,
    "f10": pynput.keyboard.Key.f10,
    "f11": pynput.keyboard.Key.f11,
    "f12": pynput.keyboard.Key.f12,
    "f13": pynput.keyboard.Key.f13,
    "f14": pynput.keyboard.Key.f14,
    "f15": pynput.keyboard.Key.f15,
    "f16": pynput.keyboard.Key.f16,
    "f17": pynput.keyboard.Key.f17,
    "f18": pynput.keyboard.Key.f18,
    "f19": pynput.keyboard.Key.f19,
    "f20": pynput.keyboard.Key.f20,
    "f21": pynput.keyboard.Key.f21,
    "f22": pynput.keyboard.Key.f22,
    "f23": pynput.keyboard.Key.f23,
    "f24": pynput.keyboard.Key.f24,
    "volup": pynput.keyboard.Key.media_volume_up,
    "voldown": pynput.keyboard.Key.media_volume_down,
    "volmute": pynput.keyboard.Key.media_volume_mute,
    "medianext": pynput.keyboard.Key.media_next,
    "mediaprev": pynput.keyboard.Key.media_previous,
    "mediapause": pynput.keyboard.Key.media_play_pause,
    "capslock": pynput.keyboard.Key.caps_lock,
    "menu": pynput.keyboard.Key.menu,
}

func_mapping = {
    tuple(int(part) for part in key.split(",")): func[value]
    for key, value in config["FunctionMapping"].items()
}

# Initialization
buffer = []
pressed = []
numpad = {96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 109, 110}# legal key value


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
                            press = modifier_mapping[vktonum[buffer[i]]]
                            pressed.append(press)
                            keyboard.press(press)
                        except KeyError:
                            print("\nUnexpected input: Undefined function.\n")
                        i += 1
                    i += 1
                    
                if i >= len(buffer):# Avoid IndexError
                    break
                
                if buffer[i] == 109: # 109 is the key value of "-".
                    func_buffer = []
                    i += 1
                    while i < len(buffer) and buffer[i] != 109:
                        func_buffer.append(vktonum[buffer[i]])
                        i += 1
                    try:
                        press = func_mapping[tuple(func_buffer)]
                        pressed.append(press)
                        keyboard.press(press)
                    except KeyError:
                        print("\nUnexpected input: Undefined function.\n")
                        
                    i += 1
                    
                if i >= len(buffer):# Avoid IndexError
                    break

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

try:
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
except KeyboardInterrupt:
    print("Numpad mapper stopped.")
finally:
    listener.stop()