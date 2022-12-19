from modules import media_controls


def run_module_function(received_message):
    if received_message["module_name"] == "media_controls":
        media_controls.trigger(received_message["function_name"])
        return True
    else:
        return False


if __name__ == "__main__":
    print('main')
    # run_module_function("media_controls", "media_play_pause")
