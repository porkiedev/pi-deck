from modules import media_controls


def run_module_function(module_name, function_name):
    if module_name == "media_controls":
        media_controls.trigger(function_name)
        return True
    else:
        return False


if __name__ == "__main__":
    run_module_function("media_controls", "media_play_pause")
