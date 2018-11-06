__author__ = "Deokyu Lim <hong18s@gmail.com>"

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


class Item(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        pb = QPushButton("custom widget!")
        layout.addWidget(pb)
        layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(layout)


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("QTreeWidget")
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.viewer = QListWidget(self)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

        item = QListWidgetItem(self.viewer)
        custom_widget = Item()

        item.setSizeHint(custom_widget.sizeHint())
        self.viewer.setItemWidget(item, custom_widget)
        self.viewer.addItem(item)

        item = QListWidgetItem(self.viewer)
        custom_widget = Item()
        item.setSizeHint(custom_widget.sizeHint())
        self.viewer.setItemWidget(item, custom_widget)
        self.viewer.addItem(item)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())