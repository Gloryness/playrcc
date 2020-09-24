import os

from PyQt5.QtCore import Qt, QMetaObject, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QGridLayout, QFrame, QLabel, QDialog, QDialogButtonBox, QTextEdit, QWidget, QAction


class AboutDialogUI:
    def __init__(self, dialog: QDialog):
        self.dialog = dialog
        self.path = __file__
        if not self.path.endswith(("gui\\aboutdialog.py", "gui/aboutdialog.py")):
            self.path = ""
        else:
            self.path = self.path.replace("gui\\aboutdialog.py", "").replace("\\", "/")

    def startLogoAnimation(self):
        """
        Begin the logo animation
        """
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.container = QWidget.createWindowContainer(self.view,
                                                          self.dialog)  # Creating a container for it in the QDialog

        self.container.setMinimumSize(300, 220)
        self.container.setMaximumSize(300, 220)

        qml_file = os.path.join(self.path, "qml", "logo.qml")
        self.view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))  # Setting the source of the QML file

        self.gridLayout_2.addWidget(self.container, 2, 0, 1, 1)

    def setupUi(self):
        self.dialog.setObjectName("dialog")
        self.dialog.resize(709, 400)
        self.dialog.setWindowIcon(QIcon(self.path + "images/logo.png"))
        self.gridLayout = QGridLayout(self.dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame = QFrame(self.dialog)
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.gridLayout_2 = QGridLayout(self.mainFrame)
        self.gridLayout_2.setContentsMargins(15, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.howToUse = QLabel(self.mainFrame)
        self.howToUse.setTextFormat(Qt.RichText)
        self.howToUse.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.howToUse.setObjectName("howToUse")
        self.gridLayout_2.addWidget(self.howToUse, 1, 0, 1, 2)
        self.title = QLabel(self.mainFrame)
        self.title.setTextFormat(Qt.RichText)
        self.title.setObjectName("title")
        self.gridLayout_2.addWidget(self.title, 0, 0, 1, 2)
        self.license = QTextEdit(self.mainFrame)
        self.license.setObjectName("license")
        self.gridLayout_2.addWidget(self.license, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self.dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.closeAction = QAction(self.dialog)
        self.dialog.addAction(self.closeAction)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.dialog.accept)
        self.buttonBox.rejected.connect(self.dialog.reject)
        QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle("About PlayrGG Secret-Code Cracker")
        self.howToUse.setText("<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">How To Use:</span></p><p>- Enter a valid PlayRGG giveaway site.</p><p>- If you want, enter a secret code that you already know OR one you want to test to speed up the process.</p><p>- NOTE: Code must contain numbers/pattern to it: (code571, 431code)</p><p>- Execute the script and sit back!</p></body></html>")
        self.title.setText("<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#6a39fd;\">About PlayRGG Secret-Code Cracker</span></p></body></html>")
        self.license.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">The MIT License (MIT)</span><span style=\" font-size:14pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; text-decoration: underline;\">Copyright © 2020 Gloryness</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This software was intended for educational-purposes only.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. </span></p></body></html>"
)
        self.closeAction.setShortcut("Ctrl+Q")

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # removing the "?" from the dialog

        self.ui = AboutDialogUI(self)
        self.ui.setupUi()
        self.ui.startLogoAnimation()

        self.ui.closeAction.triggered.connect(self.close)


def showAboutDialog():
    win = AboutDialog()
    win.show()