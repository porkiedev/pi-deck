
directory_tree = {
    "a": {
        "b": {
            "c": {
                "d": {
                    "e": {
                        "Hello": "World!"
                    }
                }
            }
        }
    }
}

folder_tree = ["a", "b", "c"]


def print_dictionary():
    current_directory = directory_tree["a"]["b"]["c"]
    print("This is the entire tree: " + str(directory_tree))
    print("This is all you could normally see: " + str(current_directory))
    current_directory_parent = directory_tree
    for i in range(len(folder_tree)-1):  # Remove 1 from the total, so we can move back 1 folder or "key"
        current_directory_parent = current_directory_parent[folder_tree[i]]
    print("This is after we return to the previous directory: " + str(current_directory_parent))


if __name__ == "__main__":
    #while True:
        #user_input = input("fwd or rev? ").lower()
    print_dictionary()
        #if user_input == fwd:
        #    print_dictionary()
