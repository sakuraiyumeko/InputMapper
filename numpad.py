import pynput

#mapping list
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

map = {
    0: pynput.keyboard.Key.space,
    1: pynput.keyboard.Key.shift,
    2: pynput.keyboard.Key.ctrl,
    3: pynput.keyboard.Key.alt,
    4: pynput.keyboard.Key.cmd,
    5: pynput.keyboard.Key.esc,
    6: pynput.keyboard.Key.tab,
    (0, 0): "|",(0, 1): "a",(0, 2): "b",(0, 3): "c",(0, 4): "d",(0, 5): "e",(0, 6): "f",(0, 7): "g",(0, 8): "h",(0, 9): "i",
    (1, 0): "j",(1, 1): "k",(1, 2): "l",(1, 3): "m",(1, 4): "n",(1, 5): "o",(1, 6): "p",(1, 7): "q",(1, 8): "r",(1, 9): "s",
    (2, 0): "t",(2, 1): "u",(2, 2): "v",(2, 3): "w",(2, 4): "x",(2, 5): "y",(2, 6): "z",
    (6, 0): ",",(6, 1): ";",(6, 2): ":",(6, 3): "_",(6, 4): "?",(6, 5): "#",(6, 6): "~",(6, 7): "\\",(6, 8): "@",(6, 9): "$",
    (7, 0): "+",(7, 1): "-",(7, 2): "*",(7, 3): "/",(7, 4): "!",(7, 5): "=",(7, 6): "^",(7, 7): "%",(7, 8): ".",(7, 9): "&",
    (8, 0): "(",(8, 1): ")",(8, 2): "[",(8, 3): "]",(8, 4): "{",(8, 5): "}",(8, 6): "<",(8, 7): ">",(8, 8): "\'",(8, 9): "\"",
    (9, 0): "0",(9, 1): "1",(9, 2): "2",(9, 3): "3",(9, 4): "4",(9, 5): "5",(9, 6): "6",(9, 7): "7",(9, 8): "8",(9, 9): "9",
}

buffer = []
pressed = []

numpad = {96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 110}

keyboard = pynput.keyboard.Controller()


def on_press(key):
    print(key)
    try:
        if key.vk in numpad:
            buffer.append(key.vk)
        
        if key.vk == 107:
            if len(buffer) != 0:
                for i in range(0, len(buffer)+1):
                    keyboard.press(pynput.keyboard.Key.backspace)
                    keyboard.release(pynput.keyboard.Key.backspace)
        
            i = 0
            while i < len(buffer):
                if buffer[i] == 110:
                    i += 1
                    while i < len(buffer) and buffer[i] != 110:
                        try:
                            press = map[vktonum[buffer[i]]]
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
                    char = map[(vktonum[a], vktonum[b])]
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
                    
    except AttributeError:

        if key == pynput.keyboard.Key.backspace:
            try:
                buffer.pop()
            except IndexError:
                buffer.clear()


listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
