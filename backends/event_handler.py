from modules import media_controls, keybind_macros


def run_module_function(args):
    if args["module_name"] == "media_controls":
        media_controls.trigger(args["function_name"])
        return True
    elif args["module_name"] == "keybind_macros":
        keybind_macros.trigger(args)
        return True
    else:
        return False


if __name__ == "__main__":
    print('main')
    # run_module_function("media_controls", "media_play_pause")
