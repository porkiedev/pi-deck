from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import qdarkstyle
import sys
import database_handler
from backends import client_networking


#   Configuration variables
#   Width and height should be equal to your display's resolution (assuming you want full-screen)
#   If you want square buttons, the ratio between matrix_columns and matrix_rows should match -
#   the aspect ratio of your display

settings = {
    "display_size": [480, 320],
    "fixed_button_size": [90, 90],
    "use_fixed_button_size":  False,
    "button_matrix": [4, 3]
}
prof_name = "test_prof"
button_spacing = 10
button_press_handler_name = "[ButtonPressHandler] "
button_initializer_name = "[ButtonInitializer] "
button_icons_path = "icons/"
button_icon_size = QSize(512, 512)
# current_profile = {}
# width, height = 480, 320
# aspect_ratio_width, aspect_ratio_height = 4, 3
# fixed_button_width, fixed_button_height = 90, 90
# fixed_button_size = True
# matrix_columns, matrix_rows = 4, 3


# def create_grid_layout():
#     layout = QGridLayout()
#     #window.setLayout(layout)
#     #   Items should be added like a book, left to right, and top to bottom.
#     for column in range(settings["button_matrix"][0]):
#         for row in range(settings["button_matrix"][1]):
#             button = QToolButton()
#
#             # Variables
#             button_matrix_key = str(column) + str(row)
#
#             # Button style
#             # button.setStyleSheet("background-color: rgb(69, 83, 100)")
#             # There should be a better way to disable the hover and click color changing
#             # button.setText("Yeet") # This doesn't work since icons have a higher zindex. Consider text alignment?
#             # button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
#             button.setFixedSize(calculate_button_size_qsize())
#             try:
#                 button.setIcon(QIcon('icons/' + current_profile["button_matrix"][button_matrix_key]["icon"]))
#             except KeyError:
#                 print(button_matrix_key + " does not have an icon.")
#           button.setIconSize(QSize(512, 512))  # Consider making icon size user-configurable, so it can accompany text
#
#             # Button back-end and addition to QGridLayout
#             button.clicked.connect(lambda ch, k=button_matrix_key: button_handler(k))
#             layout.setAlignment(button, Qt.AlignCenter)
#             layout.addWidget(button, row, column, Qt.AlignCenter) # Aligning to center may be useless.
#     return layout


# profile = database_handler.get_profile(prof_name)


class PiDeckWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create QGridLayout and path_tree
        layout = QGridLayout()
        profile = database_handler.get_profile(prof_name)
        self.profile = profile
        self.layout = layout
        self.path_tree = ["root_button_folder"]
        # Functions
        self.setLayout(layout)
        self.setFixedSize(settings["display_size"][0], settings["display_size"][1])
        self.generate_buttons(profile["root_button_folder"])

    def generate_buttons(self, folder):  # =profile["root_button_folder"]):
        # Initialize layout variable and purge all existing buttons
        self.purge_all_buttons()
        # Loop through every column and row
        for column in range(self.profile["button_matrix_settings"]["matrix_size"]["columns"]):
            for row in range(self.profile["button_matrix_settings"]["matrix_size"]["rows"]):
                # Define button and basic button properties
                button = QToolButton()
                button_key = str(column) + str(row)
                button.setFixedSize(self.get_key_size())
                button.setIconSize(button_icon_size)

                if button_key == "00" and len(self.path_tree) > 1:
                    print("Hit button 00 and inside of a folder. Ignoring profile and creating back button instead.")
                    button.setIcon(QIcon(button_icons_path + "backwards.png"))
                    button.clicked.connect(lambda ch, k=button_key, f=folder: self.button_handler(k, f))
                    self.layout.addWidget(button, row, column, Qt.AlignCenter)
                    continue

                try:
                    button_data = folder[button_key]
                    button.setIcon(QIcon(button_icons_path + button_data["icon"]))
                except KeyError:
                    print(button_initializer_name + button_key + " doesn't exist or is badly configured. "
                                                                 "You can probably ignore this.")
                button.clicked.connect(lambda ch, k=button_key, f=folder: self.button_handler(k, f))
                self.layout.addWidget(button, row, column, Qt.AlignCenter)

    def purge_all_buttons(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def button_handler(self, button_key, current_folder):
        try:
            if button_key == "00" and len(self.path_tree) > 1:
                profile_parent = self.profile
                for i in range(len(self.path_tree) - 2):
                    profile_parent = profile_parent[self.path_tree[i]]
                self.path_tree.pop(-1)
                self.path_tree.pop(-1)
                self.generate_buttons(profile_parent)
                return

            if current_folder[button_key]["enabled"]:

                # If folder, remove buttons, and generate buttons inside of folder
                if current_folder[button_key]["folder"]:
                    self.path_tree += [button_key, "button_folder"]
                    self.generate_buttons(current_folder[button_key]["button_folder"])

                button_module_name = current_folder[button_key]["module_name"]
                button_function_name = current_folder[button_key]["function_name"]
                client_networking.send_request(button_module_name, button_function_name)
                print(button_press_handler_name + "The key at " + button_key + " was pressed. Sending "
                      + button_module_name + "/" + button_function_name)
            else:
                raise KeyError
        except KeyError:
            print(button_press_handler_name + "The key at " + button_key +
                  " was pressed but the current profile has it doing nothing.")

    def get_key_size(self):
        profile = self.profile
        if profile["button_matrix_settings"]["fixed_button_size_enabled"]:
            button_w = profile["button_matrix_settings"]["button_size"]["width"]
            button_h = profile["button_matrix_settings"]["button_size"]["height"]
        else:
            button_w = int((profile["display_settings"]["width"] / profile["button_matrix_settings"]["matrix_size"][
                "columns"]) - button_spacing)
            button_h = int((profile["display_settings"]["height"] / profile["button_matrix_settings"]["matrix_size"][
                "rows"]) - button_spacing)
        return QSize(button_w, button_h)


if __name__ == "__main__":
    # main()
    application = QApplication(sys.argv)
    application.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_window = QMainWindow(None, Qt.WindowFlags())
    main_window.setWindowTitle("Pi-Deck")
    main_window.setFixedSize(settings["display_size"][0], settings["display_size"][1])

    deck_widget = PiDeckWidget()
    main_window.setCentralWidget(deck_widget)

    main_window.show()
    sys.exit(application.exec())
