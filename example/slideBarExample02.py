#slideBar change value example
#reference : https://stackoverflow.com/questions/38580702/synchronize-two-element-values-in-pyqt5
#set max value!

from PyQt5 import QtCore, QtWidgets

MAXVAL = 10000

class CustomSlider(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)

        self.sliderMin = MAXVAL 
        self.sliderMax = MAXVAL
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.handleSliderValueChange)
        #value change(parameter = function)
        self.numbox = QtWidgets.QSpinBox()
        self.numbox.valueChanged.connect(self.handleNumboxValueChange)

        #self.slider.setMaximumSize(QtCore.QSize(16777215, 25))

        #set maximum value
        self.slider.setMaximum(self.sliderMax)
        self.numbox.setMaximum(self.sliderMax)
        #self.slider.setValue(MAXVAL -500000)

        print(self.slider.minimum())
        print(self.slider.maximum())

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.numbox)
        layout.addWidget(self.slider)

    @QtCore.pyqtSlot(int)
    def handleSliderValueChange(self, value):
        self.numbox.setValue(value)

    @QtCore.pyqtSlot(int)
    def handleNumboxValueChange(self, value):
        # Prevent values outside slider range
        if value < self.slider.minimum():
            self.numbox.setValue(self.slider.minimum())
        elif value > self.slider.maximum():
            self.numbox.setValue(self.slider.maximum())

        self.slider.setValue(self.numbox.value())

app = QtWidgets.QApplication([])
slider1 = CustomSlider()
slider2 = CustomSlider()
window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(window)
layout.addWidget(slider1)
layout.addWidget(slider2)
window.show()
app.exec_()