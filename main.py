from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import qdarkstyle
import sys
import database_handler
from backends import client_networking


prof_name = "test_prof"


class PiDeckWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.profile = database_handler.get_profile(prof_name)
        self.path_tree = ["root_button_folder"]
        self.key_size = self.get_button_size()
        self.icon_size = self.get_icon_size()
        self.matrix_size_columns = self.profile["button_matrix_settings"]["matrix_size"]["columns"]
        self.matrix_size_rows = self.profile["button_matrix_settings"]["matrix_size"]["rows"]
        self.button_press_handler_name = "[ButtonPressHandler] "
        self.button_initializer_name = "[ButtonInitializer] "
        # ^Define variables
        self.setLayout(self.layout)
        self.setFixedSize(self.profile["display_settings"]["width"], self.profile["display_settings"]["height"])
        self.generate_buttons(self.profile["root_button_folder"])
        # ^Functions

    def generate_buttons(self, folder):
        self.purge_all_buttons()
        # ^Remove all old buttons
        for column in range(self.matrix_size_columns):
            for row in range(self.matrix_size_rows):
                # ^Loop through columns and rows
                button = QToolButton()
                button_key = str(column) + str(row)
                # ^Create button and its corresponding key
                # -------------------------Button styling WIP-----------------------------------------------
                # button.setStyleSheet("background-color: rgb(69, 83, 100)")
                # ^This overwrites the entire stylesheet so the button loses any color changing animations
                # button.setText("Yeet")
                # button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                # ^This doesn't work since icons have a higher zindex. Consider text alignment?
                # ------------------------------------------------------------------------------------------
                button.setFixedSize(self.key_size)
                button.setIconSize(self.icon_size)
                # ^Set button and icon size
                if button_key == "00" and len(self.path_tree) > 1:
                    button.setIcon(QIcon(self.profile["button_matrix_settings"]["icons_path"] + "folder_back.png"))
                    # ^Force a back icon, this is required so the user can exit a folder
                    button.clicked.connect(lambda ch, k=button_key, f=folder: self.button_handler(k, f))
                    self.layout.addWidget(button, row, column, Qt.AlignCenter)
                    continue
                    # ^End (Continue?!) current loop iteration so button 00 isn't initialized
                # ^If we are rendering buttons inside a folder, overwrite 00 and make it a back button instead
                try:
                    button_data = folder[button_key]
                    button.setIcon(QIcon(self.profile["button_matrix_settings"]["icons_path"] + button_data["icon"]))
                    print(self.button_initializer_name + button_key + " has been initialized.")
                except KeyError:
                    print(self.button_initializer_name + button_key + " doesn't exist or is improperly configured.")
                button.clicked.connect(lambda ch, k=button_key, f=folder: self.button_handler(k, f))
                self.layout.addWidget(button, row, column, Qt.AlignCenter)

    def purge_all_buttons(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
    # ^Remove all buttons from widget

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
                # ^Move back 2 folders and regenerate buttons
                # ^If we are inside a folder and the back button is pressed, go back 1 folder
            if current_folder[button_key]["enabled"]:
                if current_folder[button_key]["folder"]:
                    self.path_tree += [button_key, "button_folder"]
                    self.generate_buttons(current_folder[button_key]["button_folder"])
                    # ^If button is a folder, 'open folder'
                else:
                    client_networking.send_message(current_folder[button_key])
                    # ^If button is normal, alert server of button press
            else:
                raise KeyError
                # ^If button is not enabled, raise generic KeyError
        except KeyError:
            print(self.button_press_handler_name + "The key at " + button_key +
                  " was pressed but the current profile has it doing nothing.")
        # ^Handle generic KeyError
    # ^Handle button presses

    def get_button_size(self):
        if self.profile["button_matrix_settings"]["fixed_button_size_enabled"]:
            button_w = self.profile["button_matrix_settings"]["button_size"]["width"]
            button_h = self.profile["button_matrix_settings"]["button_size"]["height"]
        else:
            button_w = int((self.profile["display_settings"]["width"] / self.profile["button_matrix_settings"][
                "matrix_size"]["columns"]) - self.profile["button_matrix_settings"]["button_spacing"])
            button_h = int((self.profile["display_settings"]["height"] / self.profile["button_matrix_settings"][
                "matrix_size"]["rows"]) - self.profile["button_matrix_settings"]["button_spacing"])
        return QSize(button_w, button_h)
    # ^Get button size and return it as a QSize object

    def get_icon_size(self):
        return QSize(self.profile["button_matrix_settings"]["icon_size"]["width"],
                     self.profile["button_matrix_settings"]["icon_size"]["height"])
    # ^Get button icon size and return it as a QSize object


if __name__ == "__main__":
    # Create application and set stylesheet
    application = QApplication(sys.argv)
    application.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # Create main window and pi-deck widget
    main_window = QMainWindow(None, Qt.WindowFlags())
    deck_widget = PiDeckWidget()
    # Set some properties of the main window
    main_window.setFixedSize(deck_widget.profile["display_settings"]["width"],
                             deck_widget.profile["display_settings"]["height"])
    main_window.setWindowTitle("Pi-Deck")
    main_window.setCentralWidget(deck_widget)
    # Show the main window
    main_window.show()
    sys.exit(application.exec())
