from pynput.keyboard import Key, Controller, KeyCode
import sys
import time


key_conversion_table = {
    "alt": Key.alt,
    "backspace": Key.backspace,
    "caps_lock": Key.caps_lock,
    "cmd": Key.cmd,
    "ctrl": Key.ctrl,
    "del": Key.delete,
    "end": Key.end,
    "esc": Key.esc,
    "enter": Key.enter,
    "home": Key.home,
    "insert": Key.insert,
    "menu": Key.menu,
    "num_lock": Key.num_lock,
    "page_down": Key.page_down,
    "page_up": Key.page_up,
    "pause": Key.pause,
    "print_screen": Key.print_screen,
    "scroll_lock": Key.scroll_lock,
    "shift": Key.shift,
    "space": Key.space,
    "tab": Key.tab,
    "numpad_0": KeyCode.from_vk(96),
    "numpad_1": KeyCode.from_vk(97),
    "numpad_2": KeyCode.from_vk(98),
    "numpad_3": KeyCode.from_vk(99),
    "numpad_4": KeyCode.from_vk(100),
    "numpad_5": KeyCode.from_vk(101),
    "numpad_6": KeyCode.from_vk(102),
    "numpad_7": KeyCode.from_vk(103),
    "numpad_8": KeyCode.from_vk(104),
    "numpad_9": KeyCode.from_vk(105)
}


def trigger(args):
    function_name = args["function_name"].lower()
    keyboard = Controller()
    if function_name == "press_keybind":
        for i in args["args"]["keys"]:
            try:
                i = key_conversion_table[i]
                keyboard.press(i)
            except KeyError:
                keyboard.press(i)
        time.sleep(0.1)
        for i in args["args"]["keys"]:
            try:
                i = key_conversion_table[i]
                keyboard.release(i)
            except KeyError:
                keyboard.release(i)
        return True
    else:
        return False


if __name__ == "__main__":
    while True:
        user_input = input("What do you want to do? ").lower()
        if user_input == "exit":
            sys.exit(0)

        argy = {
            "keys": [
                "shift",
                "alt",
                "z"
            ]
        }

        trigger(user_input, argy)
