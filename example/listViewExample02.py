
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# Create a Qt application
app = QtWidgets.QApplication(sys.argv)
 
# Our main window will be a QListView
_list = QtWidgets.QListView()
_list.setWindowTitle('Honey-Do List')
_list.setMinimumSize(600, 400)
 
# Create an empty model for the list's data
model = QStandardItemModel(_list)
 
# Add some textual items
foods = [
    'Cookie dough', # Must be store-bought
    'Hummus', # Must be homemade
    'Spaghetti', # Must be saucy
    'Dal makhani', # Must be spicy
    'Chocolate whipped cream' # Must be plentiful
]
 
for food in foods:
    # Create an item with a caption
    item = QStandardItem(food)
 
    # Add a checkbox to it
    item.setCheckable(True)
 
    # Add the item to the model
    model.appendRow(item)
 
def on_item_changed(item):
    # If the changed item is not checked, don't bother checking others
    if not item.checkState():
        return
 
    # Loop through the items until you get None, which
    # means you've passed the end of the list
    i = 0
    while model.item(i):
        if not model.item(i).checkState():
            return
        i += 1
 
    app.quit()
 
model.itemChanged.connect(on_item_changed)
 
# Apply the model to the list view
_list.setModel(model)
 
# Show the window and run the app
_list.show()
app.exec_()