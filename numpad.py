import pynput

map = {
    96: pynput.keyboard.Key.shift,
    97: pynput.keyboard.Key.ctrl,
    (96, 96): "a",
    (96, 97): "b",
    (96, 98): "c",
    (96, 99): "d",
    (96, 100): "e",
    (96, 101): "f",
    (96, 102): "g",
    (96, 103): "h",
    (96, 104): "i",
    (96, 105): "j",
    (97, 96): "k",
    (97, 97): "l",
    (97, 98): "m",
    (97, 99): "n",
    (97, 100): "o",
    (97, 101): "p",
    (97, 102): "q",
    (97, 103): "r",
    (97, 104): "s",
    (97, 105): "t",
    (98, 96): "u",
    (98, 97): "v",
    (98, 98): "w",
    (98, 99): "x",
    (98, 100): "y",
    (98, 101): "z",
}

buffer = []
pressed = []

numpad = {96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 110}

keyboard = pynput.keyboard.Controller()


def on_press(key):
    try:
        if key.vk in numpad:
            buffer.append(key.vk)
    except AttributeError:
        

        if key == pynput.keyboard.Key.enter:
            if len(buffer) != 0:
                for i in range(0, len(buffer) + 1):
                    keyboard.press(pynput.keyboard.Key.backspace)
                    keyboard.release(pynput.keyboard.Key.backspace)
                    
            i = 0
            while i < len(buffer):
                if buffer[i] == 110:
                    i += 1
                    while i < len(buffer) and buffer[i] != 110:
                        try:
                            press = map[buffer[i]]
                            pressed.append(press)
                            keyboard.press(press)
                        except KeyError:
                            print("unexpected input.")
                        i += 1
                    if i >= len(buffer):
                        break
                    i += 1

                try:
                    a = buffer[i]
                    b = buffer[i + 1]
                except IndexError:
                    break

                try:
                    char = map[(a, b)]
                    keyboard.press(char)
                    keyboard.release(char)
                    for keys in pressed:
                        keyboard.release(keys)
                    pressed.clear()
                except (KeyError, UnboundLocalError):
                    print("unexpected input.")

                i += 2

            for keys in pressed:
                keyboard.release(keys)

            pressed.clear()
            buffer.clear()

        if key == pynput.keyboard.Key.backspace:
            try:
                buffer.pop()
            except IndexError:
                buffer.clear()


listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
