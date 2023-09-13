import sys
from PySide6.QtWidgets import QApplication, QWidget, QListView, QListWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.list_view = QListView()
        self.list_view.setAlternatingRowColors(True)

        for i in range(10):
            item = QListWidget("Item {}".format(i))
            self.list_view.addItem(item)

        self.setLayout(self.list_view.layout())

        self.setWindowTitle("QListView with Alternate Background Color")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

