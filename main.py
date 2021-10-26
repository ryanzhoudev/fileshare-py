import sys

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *


class FileShare(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fileshare - Python')
        self.centerUI()
        self.drawButtons()
        self.drawInputBoxes()

        self.setLayout(self.layout)
        self.show()

    def centerUI(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def drawButtons(self):
        recvBtn = QPushButton('Start Receiving Server', self)
        recvBtn.setToolTip("Starts the receiving file server with the parameters specified.")
        sendBtn = QPushButton('Send Files', self)
        sendBtn.setToolTip("Sends the files with the parameters specified.")

        self.layout.addWidget(recvBtn, 5, 5)
        self.layout.addWidget(sendBtn, 6, 6)

        recvBtn.clicked.connect(self.on_recvBtn_clicked)
        sendBtn.clicked.connect(self.on_sendBtn_clicked)

    def drawInputBoxes(self):
        ipBtn = QPushButton('IP Address', self)
        ipBtn.setToolTip("Paste the connecting IP address here. Click to clear.")
        ipField = QLineEdit()
        ipField.setMaxLength(15)
        # ipField.setInputMask("000.000.000.000")
        ipBtn.clicked.connect(lambda: self.onBtnClickedClearField(ipField))
        self.layout.addWidget(ipBtn, 0, 0)
        self.layout.addWidget(ipField, 0, 1)

        portBtn = QPushButton('Port', self)
        portBtn.setToolTip("Input the connecting TCP port here. Click to clear.")
        portField = QLineEdit()
        portField.setMaxLength(5)
        # portField.setInputMask("00000")
        portBtn.clicked.connect(lambda: self.onBtnClickedClearField(portField))
        self.layout.addWidget(portBtn, 1, 0)
        self.layout.addWidget(portField, 1, 1)

    @pyqtSlot()
    def on_recvBtn_clicked(self):
        print('recv button clicked')

    @pyqtSlot()
    def on_sendBtn_clicked(self):
        print('send button clickced')

    @pyqtSlot()
    def onBtnClickedClearField(self, field: QLineEdit):
        field.setText(None)

def main():
    app = QApplication(sys.argv)
    fs = FileShare()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
