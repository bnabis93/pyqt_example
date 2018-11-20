
# slide Bar Range example.
# max min interval + date example.

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


MAXVAL = 650000

class RangeSliderClass(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.minTime = 0
        self.maxTime = 0
        self.minRangeTime = 0
        self.maxRangeTime = 0
        self.middleTime = self.getMiddleTime()
        self.halfTimeInterval = self.middleTime - self.minTime

        self.sliderMin = MAXVAL
        self.sliderMax = MAXVAL

        self.setupUi(self)

    def setupUi(self, RangeSlider):
        RangeSlider.setObjectName("RangeSlider")
        RangeSlider.resize(631, 65)
        RangeSlider.setMaximumSize(QtCore.QSize(16777215, 65))
        self.RangeBarVLayout = QtWidgets.QVBoxLayout(RangeSlider)
        self.RangeBarVLayout.setContentsMargins(5, 0, 5, 0)
        self.RangeBarVLayout.setSpacing(0)
        self.RangeBarVLayout.setObjectName("RangeBarVLayout")
        self.datesFrame = QtWidgets.QFrame(RangeSlider)
        self.datesFrame.setMaximumSize(QtCore.QSize(16777215, 28))
        self.datesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.datesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.datesFrame.setObjectName("datesFrame")
        self.datesHLayout = QtWidgets.QHBoxLayout(self.datesFrame)
        self.datesHLayout.setContentsMargins(5, 2, 5, 2)
        self.datesHLayout.setObjectName("datesHLayout")

        ## startTime Calendar Widget
        self.startTime = QtWidgets.QDateTimeEdit(self.datesFrame)
        self.startTime.setMinimumSize(QtCore.QSize(183, 0))
        self.startTime.setMaximumSize(QtCore.QSize(185, 24))

        self.startTime.setDate(QtCore.QDate.currentDate().addDays(-1))

        self.startTime.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2999, 12, 31), QtCore.QTime(23, 59, 59)))
        self.startTime.setMaximumDate(QtCore.QDate(2999, 12, 31))
        self.startTime.setMinimumDate(QtCore.QDate(2000, 1, 1))
        self.startTime.setCalendarPopup(True)
        self.startTime.setObjectName("startTime")
        self.startTime.dateChanged.connect(self.startDateChangeHandler)
        self.datesHLayout.addWidget(self.startTime)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.datesHLayout.addItem(spacerItem)

        ## entTime Calendar Widget
        self.endTime = QtWidgets.QDateTimeEdit(self.datesFrame)
        self.endTime.setMinimumSize(QtCore.QSize(183, 0))
        self.endTime.setMaximumSize(QtCore.QSize(185, 24))
        self.endTime.setDate(QtCore.QDate.currentDate())
        self.endTime.setMaximumDate(QtCore.QDate(2999, 12, 31))
        self.endTime.setMinimumDate(QtCore.QDate(2000, 1, 1))
        self.endTime.setCalendarPopup(True)
        self.endTime.setObjectName("endTime")
        self.endTime.dateChanged.connect(self.endDateChangeHandler)
        self.datesHLayout.addWidget(self.endTime)

        ## Init Time
        self.minTime = self.startTime.dateTime().toTime_t()
        self.maxTime = self.endTime.dateTime().toTime_t()
        self.minRangeTime = self.minTime
        self.maxRangeTime = self.maxTime
        self.middleTime = self.getMiddleTime()
        self.halfTimeInterval = self.middleTime - self.minTime

        self.RangeBarVLayout.addWidget(self.datesFrame)
        self.slidersFrame = QtWidgets.QFrame(RangeSlider)
        self.slidersFrame.setMaximumSize(QtCore.QSize(16777215, 25))
        self.slidersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.slidersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slidersFrame.setObjectName("slidersFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.slidersFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        ## Start Slider Widget
        self.startSlider = QtWidgets.QSlider(self.slidersFrame)
        self.startSlider.setMaximum(self.sliderMin)
        self.startSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.startSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setKerning(True)
        self.startSlider.setFont(font)
        self.startSlider.setAcceptDrops(False)
        self.startSlider.setAutoFillBackground(False)
        self.startSlider.setOrientation(QtCore.Qt.Horizontal)
        self.startSlider.setInvertedAppearance(True)
        self.startSlider.setObjectName("startSlider")
        self.startSlider.setValue(MAXVAL)
        self.startSlider.sliderReleased.connect(self.startSliderHandler)
        self.horizontalLayout.addWidget(self.startSlider)

        ## End Slider Widget
        self.endSlider = QtWidgets.QSlider(self.slidersFrame)
        self.endSlider.setMaximum(MAXVAL)
        self.endSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.endSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        self.endSlider.setTracking(True)
        self.endSlider.setOrientation(QtCore.Qt.Horizontal)
        self.endSlider.setObjectName("endSlider")
        self.endSlider.setValue(self.sliderMax)
        self.endSlider.sliderReleased.connect(self.endSliderHandler)
        self.horizontalLayout.addWidget(self.endSlider)

        self.RangeBarVLayout.addWidget(self.slidersFrame)

        self.retranslateUi(RangeSlider)
        QtCore.QMetaObject.connectSlotsByName(RangeSlider)

        self.show()

    def getMiddleTime(self, maxTime = None, minTime = None):
        if minTime == None :
            minTime = self.minRangeTime
        if maxTime == None :
            maxTime = self.maxRangeTime
        return (minTime + maxTime)/2

    def getRangeTime(self):
        return self.minRangeTime, self.maxRangeTime

    def startSliderHandler(self):
        self.sliderMin = self.startSlider.value()

        self.minRangeTime = int(self.middleTime - self.halfTimeInterval * self.sliderMin / MAXVAL)
        #print("\n\nNew Min Time Range : ", self.minRangeTime, " Min : ",  self.minTime, "Minddle : ", self.middleTime)

    def endSliderHandler(self):
        self.sliderMax = self.endSlider.value()

        self.maxRangeTime = int(self.middleTime + self.halfTimeInterval * self.sliderMax / MAXVAL)
        print("\n\nNew Min Time Range : ", self.maxRangeTime, " Max : ",  self.maxTime, "Minddle : ", self.middleTime)

    def startDateChangeHandler(self):
        self.minTime = self.startTime.dateTime().toTime_t()
        #print("MinTime range : ", self.minTime)

    def endDateChangeHandler(self):
        self.maxTime = self.endTime.dateTime().toTime_t()
        #print("MaxTime range : ", self.maxTime)

    def retranslateUi(self, RangeSlider):
        _translate = QtCore.QCoreApplication.translate
        RangeSlider.setWindowTitle(_translate("RangeSlider", "Time interval"))
        self.startTime.setDisplayFormat(_translate("RangeSlider", "dd/MM/yyyy  HH:mm:ss .zz"))
        self.endTime.setDisplayFormat(_translate("RangeSlider", "dd/MM/yyyy  HH:mm:ss .zz"))

app = QtWidgets.QApplication(sys.argv)
awindow = RangeSliderClass()
sys.exit(app.exec_())