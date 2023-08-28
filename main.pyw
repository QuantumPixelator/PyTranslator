import sys
from translate import Translator
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QTextOption
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.textbox_1 = QTextEdit()
        self.textbox_1.setWordWrapMode(QTextOption.WordWrap)

        self.textbox_2 = QTextEdit()
        self.textbox_2.setWordWrapMode(QTextOption.WordWrap)

        self.label_1 = QLabel("Enter a word or phrase:")
        self.label_2 = QLabel("Translation:")

        self.button_1 = QPushButton("Translate")
        self.button_2 = QPushButton("Clear")
        self.button_3 = QPushButton("Exit App")

        # Connect buttons to actions
        self.button_1.clicked.connect(self.translate)
        self.button_2.clicked.connect(self.clear)
        self.button_3.clicked.connect(self.exit_app)

        ############## GUI SETUP ##############
        layout = QVBoxLayout()
        layout.addWidget(self.label_1)
        layout.addWidget(self.textbox_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.textbox_2)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_3)

        self.setLayout(layout)

    ############## FUNCTIONS ##############

    def translate(self):
        # Use the translate library
        translator = Translator(
            to_lang="French"
        )  # TODO: Replace this with a dropdown with other languages. Until then, change to whatever language you want.
        get_phrase = self.textbox_1.toPlainText()
        translated_text = translator.translate(get_phrase)
        self.textbox_2.setPlainText(translated_text)

    def clear(self):
        self.textbox_1.clear()
        self.textbox_2.clear()

    def exit_app(self):
        sys.exit(0)


############## MAIN WINDOW/LOOP ##############

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Widget()
    widget.setWindowTitle("Simple Translator App")
    widget.setWindowIcon(QIcon("icon.png"))
    widget.show()

    sys.exit(app.exec())
