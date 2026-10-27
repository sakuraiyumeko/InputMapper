import pynput, time, tomllib
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
    tuple(int(part) for part in key.split(",")): value
    for key, value in config["CharMapping"].items()
}

# Mapping list
vktonum = {a:a-96 for a in range(96,106)}

# Function mapping
modifier = {
    "space": pynput.keyboard.Key.space,
    "shiftL": pynput.keyboard.Key.shift_l,
    "shiftR": pynput.keyboard.Key.shift_r,
    "ctrl": pynput.keyboard.Key.ctrl,
    "alt": pynput.keyboard.Key.alt,
    "cmd": pynput.keyboard.Key.cmd,
}

modifier_mapping = {
    int(key): modifier[value] for key, value in config["ModifierMapping"].items()
}

func = {
    **{f"f{i}": getattr(pynput.keyboard.Key, f"f{i}") for i in range(1, 25)}, # Generate F1–F24 key mappings
    "volup": pynput.keyboard.Key.media_volume_up,
    "voldown": pynput.keyboard.Key.media_volume_down,
    "volmute": pynput.keyboard.Key.media_volume_mute,
    "medianext": pynput.keyboard.Key.media_next,
    "mediaprev": pynput.keyboard.Key.media_previous,
    "mediapause": pynput.keyboard.Key.media_play_pause,
    "tab": pynput.keyboard.Key.tab,
    "esc": pynput.keyboard.Key.esc,
    "menu": pynput.keyboard.Key.menu,
    "capslock": pynput.keyboard.Key.caps_lock,
}

func_mapping = {
    tuple(int(part) for part in key.split(",")): func[value]
    for key, value in config["FunctionMapping"].items()
}

# Initialization
buffer = []
pressed = []
numpad = {*range(96,106), 109, 110}  # legal key value

keyboard = pynput.keyboard.Controller()


def on_press(key):
    # debug info output
    if isDebug:
        try:
            print(f"{key}:{key.vk}", end="  ", flush=True)
        except AttributeError:
            print(f"{key}:None", end="  ", flush=True)
        print(
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
        if key.vk == 107:  # Delete num sequence when confirm.
            if len(buffer) != 0:
                for i in range(0, len(buffer) + 1):
                    keyboard.press(pynput.keyboard.Key.backspace)
                    keyboard.release(pynput.keyboard.Key.backspace)

            i = 0
            # Process function input.
            while i < len(buffer):
                if buffer[i] == 110:  # 110 is the key value of ".".
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

                if i >= len(buffer):  # Avoid IndexError
                    break

                if buffer[i] == 109:  # 109 is the key value of "-".
                    func_buffer = []
                    i += 1
                    while i < len(buffer) and buffer[i] != 109:
                        if i + 1 >= len(buffer) or buffer[i + 1] == 109:
                            break
                        try:
                            func_buffer.append(vktonum[buffer[i]])
                            func_buffer.append(vktonum[buffer[i + 1]])
                            press = func_mapping[tuple(func_buffer)]
                            keyboard.press(press)
                            keyboard.release(press)
                            func_buffer.clear()
                        except KeyError:
                            print("\nUnexpected input: Undefined function.\n")
                            func_buffer.clear()
                            i += 2
                            continue
                        i += 2
                    i += 1

                if i >= len(buffer):  # Avoid IndexError
                    break

                # Load tuple
                try:
                    a = buffer[i]
                    b = buffer[i + 1]
                except IndexError:
                    break

                try:  # Characters convert
                    char = char_map[(vktonum[a], vktonum[b])]
                    keyboard.press(char)
                    keyboard.release(char)
                    for keys in pressed:
                        keyboard.release(keys)
                    pressed.clear()
                except KeyError:
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
