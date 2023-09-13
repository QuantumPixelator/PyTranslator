import sys
import json
import os
import pyttsx3
from translate import Translator
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QTextOption
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSlider,
    QHBoxLayout,
    QListWidget,
    QMenu,
    QMessageBox,
    QComboBox,
)

class Widget(QWidget):
    def show_message(self, title, message):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.setStyleSheet(self.styleSheet())
            msg_box.exec_()
            
    def __init__(self):
        super().__init__()
       
        # Load previous window position and theme if available
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            self.resize(int(settings['width']), int(settings['height']))
            self.move(int(settings['x']), int(settings['y']))
        except Exception as e:
            self.show_message("Error", "Couldn't locate settings.json file! Created settings.json with default values.")
            
        self.speech_rate = 150  # Default speech rate

        # Initialize favorites from JSON file
        self.favorites = self.load_favorites()

        self.textbox_1 = QTextEdit()
        self.textbox_1.setWordWrapMode(QTextOption.WordWrap)

        self.textbox_2 = QTextEdit()
        self.textbox_2.setWordWrapMode(QTextOption.WordWrap)

        self.label_1 = QLabel("Enter a word or phrase:")
        self.label_2 = QLabel("Translation:")
        self.label_3 = QLabel("Speech Rate:")
        
        #####################################
        ############# LANGUAGES #############
        self.combobox = QComboBox()
        self.combobox.addItem("French")
        self.combobox.addItem("Spanish")
        self.combobox.addItem("Italian")
        self.combobox.addItem("German")
        self.combobox.addItem("Russian")
        self.combobox.addItem("Portuguese")
        self.combobox.addItem("Arabic")
        self.combobox.addItem("Japanese")
        self.combobox.addItem("en-GB")
        self.combobox.addItem("en-US")
        # Add other languages here###########
        #####################################

        self.button_1 = QPushButton("Translate")
        self.button_2 = QPushButton("Clear")
        self.button_3 = QPushButton("Exit App")
        self.button_4 = QPushButton("Speak")
        self.button_5 = QPushButton("Add to Favorites")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(300)
        self.slider.setValue(self.speech_rate)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.favorites_list = QListWidget()
        self.favorites_list.setAlternatingRowColors(True)
        self.favorites_list.setStyleSheet("""
            QListView {
                alternate-background-color: #DADADA;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                }
            """)
        self.favorites_list.addItems(self.favorites.keys())
        self.favorites_list.itemClicked.connect(self.load_favorite)
        self.favorites_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.favorites_list.customContextMenuRequested.connect(self.show_context_menu)

        # Connect buttons to actions
        self.button_1.clicked.connect(self.translate)
        self.button_2.clicked.connect(self.clear)
        self.button_3.clicked.connect(self.exit_app)
        self.button_4.clicked.connect(self.speak)
        self.button_5.clicked.connect(self.add_to_favorites)
        self.slider.valueChanged.connect(self.update_rate)

        ############## GUI SETUP ##############
        layout = QVBoxLayout()
        # Create a horizontal layout for label_1 and comboBox
        label_combo_layout = QHBoxLayout()
        label_combo_layout.addWidget(self.label_1)
        label_combo_layout.addStretch(1)  # Pushes the next widget to the far right
        label_combo_layout.addWidget(self.combobox)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(label_combo_layout)
        layout.addWidget(self.textbox_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.textbox_2)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)

        # Slider Layout
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.label_3)
        slider_layout.addWidget(self.slider)
        layout.addLayout(slider_layout)

        layout.addWidget(self.button_4)

        # Add favorites list and button to layout
        layout.addWidget(self.favorites_list)
        layout.addWidget(self.button_5)

        layout.addWidget(self.button_3)

        self.setLayout(layout)

        ############## STYLESHEET ##############      
        self.setStyleSheet(
            """
            QWidget {
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
            }
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 10px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ccc;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                background: #5bc0de;
                margin: -5px 0;
                border-radius: 9px;
            }
            """
        )
    ############## FUNCTIONS ##############

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def add_to_favorites(self):
        original_text = self.textbox_1.toPlainText()
        translated_text = self.textbox_2.toPlainText()
        if original_text and translated_text:
            self.favorites[original_text] = translated_text
            self.save_favorites()
            self.favorites_list.addItem(original_text)

    def load_favorite(self, item):
        original_text = item.text()
        translated_text = self.favorites.get(original_text, '')
        self.textbox_1.setPlainText(original_text)
        self.textbox_2.setPlainText(translated_text)

    def show_context_menu(self, position):
        context_menu = QMenu()
        delete_action = context_menu.addAction("Delete")
        action = context_menu.exec_(self.favorites_list.mapToGlobal(position))
        if action == delete_action:
            current_item = self.favorites_list.currentItem()
            if current_item:
                item_text = current_item.text()
                del self.favorites[item_text]
                self.save_favorites()
                self.favorites_list.takeItem(self.favorites_list.row(current_item))

    def translate(self):
        selected_language = self.combobox.currentText()
        translator = Translator(to_lang=selected_language)
        get_phrase = self.textbox_1.toPlainText()
        translated_text = translator.translate(get_phrase)
        self.textbox_2.setPlainText(translated_text)

    def clear(self):
        self.textbox_1.clear()
        self.textbox_2.clear()

    def exit_app(self):
        sys.exit(0)

    def speak(self):
        selected_language = self.combobox.currentText().lower()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        language_voice = None
        for voice in voices:
            if selected_language in voice.name.lower():
                language_voice = voice.id
                break
        if language_voice:
            engine.setProperty('voice', language_voice)
        else:
            self.show_message("Error", f"Couldn't locate a matching language voice ({selected_language}).\nUsing system default voice instead.")
        
        engine.setProperty('rate', self.speech_rate)
        engine.say(self.textbox_2.toPlainText())
        engine.runAndWait()

    def update_rate(self, value):
        self.speech_rate = value

    def closeEvent(self, event):
        # Get the geometry data as a QRect object
        geometry = self.geometry()  # This returns the QRect object

        # Save the position in a dictionary
        information = {
            'width': geometry.width(),
            'height': geometry.height(),
            'x': geometry.x(),
            'y': geometry.y(),
        }

        # Determine the path to save the JSON file
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_folder_path, 'settings.json')

        # Write the position to the file
        with open(file_path, 'w') as file:
            json.dump(information, file)

        # Continue with the normal close event
        event.accept()

        # Close the app process to ensure everything is exited
        quit()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Widget()
    widget.setWindowTitle("Simple Translator App")
    widget.setWindowIcon(QIcon("icon.png"))
    widget.show()

    sys.exit(app.exec())
