from pynput.keyboard import Key, Controller
import sys


choices = [
    "media_play_pause"
    "media_next"
    "media_previous"
    "media_volume_up"
    "media_volume_down"
    "media_volume_mute"
]


def trigger(arg):
    arg = arg.lower()
    keyboard = Controller()
    if arg == "media_play_pause":
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        return True
    elif arg == "media_next":
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
        return True
    elif arg == "media_previous":
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
        return True
    elif arg == "media_volume_up":
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        return True
    elif arg == "media_volume_down":
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        return True
    elif arg == "media_volume_mute":
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
        return True
    else:
        return False


if __name__ == "__main__":
    while True:
        user_input = input("What do you want to do? ").lower()
        if user_input == "exit":
            sys.exit(0)
        trigger(user_input)
