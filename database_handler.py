import re
from tinydb import TinyDB, Query
# create_new_profile should return success or failure indicators
# I need a way to inform the user of errors and ideally successes, preferably through the GUI


selected_profile = "testprofile"
profile_name_reg = re.compile('^[A-Za-z0-9 _-]+$')


def main():
    user_input = input("What do you want to do? ")
    if user_input.lower() == "insert":
        user_input = input("What would you like to name your profile? ")
        create_new_profile(user_input)
    elif user_input.lower() == "read":
        user_input = input("What is the name of the profile? ")
        print(get_profile(user_input))
    elif user_input.lower() == "test":
        profile_data = get_profile("test_1")
        if profile_data: #  You have to use .update to also create new keys. Remember this for later when implementing a configurator that can change the number of keys
            profile_data["button_matrix"]["10"]["zzz"] = 173
            update_profile("test_1", profile_data)


def update_profile(profile_name, data):
    sta = db.update(data, Query().profile_name == str(profile_name))


def create_new_profile(profile_name="Untitled Profile"):
    if not bool(profile_name_reg.match(profile_name)):  # Return early if profile_name contains illegal characters
        print("Error: Profile name contains illegal characters")
        return
    elif len(profile_name) > 32:    # Return early if profile_name is longer than 32 characters
        print("Error: Profile name is longer than 32 characters")
        return
    elif get_profile(profile_name):
        print("Error: Profile already exists with that name")
        return
    data_table = {
        "profile_name": str(profile_name),
        "db_version": 1,    # Just incase there are future updates, and we need backwards compatibility
        "display_settings": {
            "width": 480,
            "height": 320
        },
        "button_matrix_settings": {
            "button_size": {
                "width": 90,
                "height": 90
            },
            "matrix_size": {
                "columns": 4,
                "rows": 3
            },
            "fixed_button_size_enabled": False
        },
        "root_button_folder": {
            "00": {
                "icon": "mute.png",
                "enabled": True,
                "folder": False,
                "module_name": "media_controls",
                "function_name": "media_volume_mute"
            },
            "10": {
                "icon": "rewind.png",
                "enabled": True,
                "folder": False,
                "module_name": "media_controls",
                "function_name": "media_previous"
            },
            "20": {
                "icon": "play.png",
                "enabled": True,
                "folder": False,
                "module_name": "media_controls",
                "function_name": "media_play_pause"
            },
            "30": {
                "icon": "forward.png",
                "enabled": True,
                "folder": False,
                "module_name": "media_controls",
                "function_name": "media_next"
            }
        }
    }
    db.insert(data_table)


# Return a dictionary containing all the data belonging to the specified profile_name
def get_profile(profile_name):
    try:
        result = db.search(Query().profile_name == str(profile_name))
        return result[0]
    except IndexError:
        return False


def initialize_db():
    return TinyDB("profiles.json")


if __name__ == "__main__":
    db = initialize_db()
    main()
else:
    db = initialize_db()
