import os

from PyQt5.QtCore import Qt, QSize, QMetaObject, QRect, QUrl, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QIcon, QColor
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QSplitter, QListWidget, QLabel, QPushButton, QTextEdit, QProgressBar, \
    QHBoxLayout, QSpacerItem, QLineEdit, QSizePolicy, QListWidgetItem, QAbstractItemView, QAction, QMenu, QMenuBar, QMainWindow

from app.cache import Cache
from gui.aboutdialog import showAboutDialog
from gui.events import GiveawayText
from base.output import OutputSender
from base.http.connection import Session
from base.utils.common import convert_to_time
from base.filehandler import Save, openExplorer

class SecretCodeWindowUI:
    def __init__(self, main_window: QMainWindow):
        self.win = main_window
        self.path = __file__
        if not self.path.endswith(("gui\\mainwindow.py", "gui/mainwindow.py")):
            self.path = ""
        else:
            self.path = self.path.replace("gui\\mainwindow.py", "").replace("\\", "/")

    def setupUi(self):
        self.win.setWindowIcon(QIcon(self.path + "images/logo.png"))
        self.win.resize(900, 463)
        font = QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        self.win.setFont(font)

        self.centralwidget = QWidget(self.win)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.mainFrame = QFrame(self.centralwidget)
        self.mainFrame.setAutoFillBackground(True)
        self.mainFrame.setFrameShape(QFrame.Box)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")

        self.gridLayout_4 = QGridLayout(self.mainFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.splitter = QSplitter(self.mainFrame)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")

        self.leftGridLayout = QFrame(self.splitter)
        self.leftGridLayout.setFrameShape(QFrame.NoFrame)
        self.leftGridLayout.setFrameShadow(QFrame.Raised)
        self.leftGridLayout.setObjectName("leftGridLayout")

        self.gridLayout_5 = QGridLayout(self.leftGridLayout)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.outputGrid = QGridLayout()
        self.outputGrid.setObjectName("outputGrid")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.outputImage = QLabel(self.leftGridLayout)
        self.outputImage.setMaximumSize(QSize(22, 22))
        self.outputImage.setPixmap(QPixmap(self.path + "images/output.svg"))
        self.outputImage.setScaledContents(True)
        self.outputImage.setObjectName("outputImage")
        self.horizontalLayout_3.addWidget(self.outputImage)

        self.outputLabel = QLabel(self.leftGridLayout)
        font = QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(8)
        self.outputLabel.setFont(font)
        self.outputLabel.setTextFormat(Qt.RichText)
        self.outputLabel.setObjectName("outputLabel")
        self.horizontalLayout_3.addWidget(self.outputLabel)

        self.executeScript = QPushButton(self.leftGridLayout)
        self.executeScript.setObjectName("executeScript")
        self.horizontalLayout_3.addWidget(self.executeScript)

        self.stopScript = QPushButton(self.leftGridLayout)
        self.stopScript.setObjectName("stopScript")
        self.horizontalLayout_3.addWidget(self.stopScript)
        self.outputGrid.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.output = QTextEdit(self.leftGridLayout)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.outputGrid.addWidget(self.output, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.outputGrid, 3, 0, 1, 1)

        self.progressBar = QProgressBar(self.leftGridLayout)
        self.progressBar.setObjectName("progresssBar")
        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(-1)
        self.progressBar.setMaximum(0)
        self.outputGrid.addWidget(self.progressBar, 2, 0, 1, 1)

        self.codeExampleGrid = QHBoxLayout()
        self.codeExampleGrid.setObjectName("codeExampleGrid")

        self.codeExampleLabel = QLabel(self.leftGridLayout)
        self.codeExampleLabel.setObjectName("codeExampleLabel")
        self.codeExampleGrid.addWidget(self.codeExampleLabel)
        self.codeExample = QLineEdit(self.leftGridLayout)
        self.codeExample.setObjectName("codeExample")
        self.codeExampleGrid.addWidget(self.codeExample)
        self.gridLayout_5.addLayout(self.codeExampleGrid, 1, 0, 1, 1)

        self.giveawaySiteGrid = QHBoxLayout()
        self.giveawaySiteGrid.setObjectName("giveawaySiteGrid")

        self.giveawaySiteLabel = QLabel(self.leftGridLayout)
        self.giveawaySiteLabel.setObjectName("giveawaySiteLabel")
        self.giveawaySiteGrid.addWidget(self.giveawaySiteLabel)

        self.giveawaySite = GiveawayText(self, self.leftGridLayout)
        self.giveawaySite.setObjectName("giveawaySite")
        self.giveawaySiteGrid.addWidget(self.giveawaySite)

        self.isValidLabel = QLabel(self.leftGridLayout)

        self.green_palette = QPalette()
        brush = QBrush(QColor(19, 138, 15))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(19, 138, 15))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.red_palette = QPalette()
        brush = QBrush(QColor(200, 0, 26))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(200, 0, 26))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.isValidLabel.setPalette(self.red_palette)
        self.isValidLabel.setObjectName("isValidLabel")
        self.isValidLabel.setMinimumHeight(30)
        self.giveawaySiteGrid.addWidget(self.isValidLabel)

        self.gridLayout_5.addLayout(self.giveawaySiteGrid, 0, 0, 1, 1)

        spacerItem2 = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 2, 0, 1, 1)

        self.spacerItem3 = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(self.spacerItem3, 2, 1, 1, 1)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.rightGridLayout = QGridLayout(self.widget)
        self.rightGridLayout.setContentsMargins(0, 0, 0, 0)
        self.rightGridLayout.setObjectName("rightGridLayout")

        self.secretCodes = QListWidget(self.widget)
        self.secretCodes.setSelectionMode(QAbstractItemView.NoSelection)
        self.secretCodes.setObjectName("secretCodes")
        self.rightGridLayout.addWidget(self.secretCodes, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.secretCodeImage = QLabel(self.widget)
        self.secretCodeImage.setMaximumSize(QSize(24, 24))
        font = QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.secretCodeImage.setFont(font)
        self.secretCodeImage.setPixmap(QPixmap(self.path + "images/smart-key.svg"))
        self.secretCodeImage.setScaledContents(True)
        self.secretCodeImage.setObjectName("secretCodeImage")
        self.horizontalLayout_2.addWidget(self.secretCodeImage)

        self.secretCodeLabel = QLabel(self.widget)
        font = QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.secretCodeLabel.setFont(font)
        self.secretCodeLabel.setScaledContents(True)
        self.secretCodeLabel.setObjectName("secretCodeLabel")

        self.horizontalLayout_2.addWidget(self.secretCodeLabel)
        self.rightGridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.mainFrame, 0, 0, 1, 2)

        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 0, 1, 1)

        self.developedByLabel = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.developedByLabel.sizePolicy().hasHeightForWidth())
        self.developedByLabel.setSizePolicy(sizePolicy)
        self.developedByLabel.setTextFormat(Qt.RichText)
        
        self.noteLabel = QLabel(self.centralwidget)
        self.noteLabel.setSizePolicy(sizePolicy)
        self.noteLabel.setTextFormat(Qt.RichText)

        ## Loading Animation
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.container = QWidget.createWindowContainer(self.view,
                                                          self.win)  # Creating a container for it in the main window

        self.container.setFocusPolicy(Qt.TabFocus)
        self.container.setMinimumSize(30, 30)
        self.container.setMaximumSize(30, 30)

        qml_file = os.path.join(self.path, "qml", "loading.qml")
        self.view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))  # Setting the source of the QML file
        self.container.setVisible(False)
        self.giveawaySiteGrid.addWidget(self.container)

        self.gridLayout_2.addWidget(self.developedByLabel, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.noteLabel, 1, 0, 1, 1)
        self.win.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self.win)
        self.menubar.setGeometry(QRect(0, 0, 1051, 21))

        self.menuFile = QMenu(self.menubar)

        self.menuAbout = QMenu(self.menubar)

        self.saveAsOption = QAction(self.win)
        icon = QIcon()
        icon.addPixmap(QPixmap(self.path + "images/save.png"), QIcon.Normal, QIcon.Off)
        self.saveAsOption.setIcon(icon)

        self.saveOption = QAction(self.win)
        self.saveOption.setIcon(icon)

        self.goToFolder = QAction(self.win)

        self.exitOption = QAction(self.win)
        icon = QIcon()
        icon.addPixmap(QPixmap(self.path + "images/exit.svg"), QIcon.Normal, QIcon.Off)
        self.exitOption.setIcon(icon)

        self.aboutOption = QAction(self.win)
        icon = QIcon()
        icon.addPixmap(QPixmap(self.path + "images/about.svg"), QIcon.Normal, QIcon.Off)
        self.aboutOption.setIcon(icon)

        self.menuFile.addAction(self.saveOption)
        self.menuFile.addAction(self.saveAsOption)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.goToFolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitOption)
        self.menuAbout.addAction(self.aboutOption)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.win.setMenuBar(self.menubar)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self.win)

    def retranslateUi(self):
        self.win.setWindowTitle("PlayRGG Secret Code Cracker")
        self.outputLabel.setText('<html><head/><body><p><span style=" font-size:11pt; font-weight:600;">Output ‎‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ </span>00:00</p></body></html>')

        self.executeScript.setText("Execute Script")
        self.executeScript.setEnabled(False)
        self.stopScript.setText("Stop Script")
        self.stopScript.setEnabled(False)

        self.output.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Nirmala UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-------------------------------------------</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">All output will go here including errors</span><br /></p>"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-------------------------------------------</p>"
        )
        self.codeExampleLabel.setText("Code Example")
        self.codeExample.setPlaceholderText("Secret Code (Not required, but speeds things up)")
        self.giveawaySiteLabel.setText("Giveaway Site")
        self.giveawaySite.setPlaceholderText("https://playr.gg/giveaway/")
        self.isValidLabel.setText("Invalid Link")
        self.secretCodes.setSortingEnabled(True)
        self.secretCodeLabel.setText("Secret Codes")
        self.developedByLabel.setText("<html><head/><body><p>Developed by Gloryness &lt;<a href=\"https://mail.google.com/mail/u/0/?tab=wm&amp;ogbl#inbox?compose=CllgCJlHFPJQPrfMZSQJjmqfFhHcKLsMpcwhxMTDfZsBqqcxPwlVJnvZsSKcSjPcQvVczMmlqZL\"><span style=\" text-decoration: underline; color:#0000ff;\">glorynessxd@gmail.com</span></a>&gt;</p></body></html>")
        self.noteLabel.setText("<html><head/><body><p><span style=\" color:#c8001a;\">Please note that due to multithreading, failed codes can get mixed up with the success ones too.</span></p></body></html>")
        
        self.menuFile.setTitle("File")
        self.menuAbout.setTitle("About")

        self.saveOption.setText("Save")
        self.saveOption.setShortcut("Ctrl+S")

        self.saveAsOption.setText("Save As..")

        self.goToFolder.setText("Go To Giveaway Folder")

        self.exitOption.setText("Exit")
        self.exitOption.setShortcut("Ctrl+Q")

        self.aboutOption.setText("About")

        self.splitter.setSizes([1000, 0])

class SecretCodeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = SecretCodeWindowUI(self)
        self.ui.setupUi()

        self.saver = Save(self.ui.secretCodes)

        self.ui.saveOption.triggered.connect(self.saver.save)
        self.ui.saveAsOption.triggered.connect(self.saver.saveAs)
        self.ui.goToFolder.triggered.connect(lambda: openExplorer(os.path.join(os.environ.get("USERPROFILE"), "Documents", "playrcc", "giveaways")))
        self.ui.exitOption.triggered.connect(self.close)
        self.ui.aboutOption.triggered.connect(showAboutDialog)

        self.outputSender = OutputSender(self.ui.output)
        self.cache = Cache()

        self.playrRunning = False

        self.ui.stopScript.clicked.connect(self.terminate_session)

        self.createWorkers()

    def closeEvent(self, event):
        if self.session_thread.isRunning():
            self.playrRunning = False
            try:
                self.session_thread.terminate()
                self.session_thread.wait()
            except:
                pass

    def createWorkers(self):
        # Session
        self.session = Session(self)
        self.session_thread = QThread()
        self.session.moveToThread(self.session_thread)
        self.session_thread.start()

        self.session.logger.connect(self.updateLog)
        self.session.progress.connect(self.updateProgress)
        self.ui.executeScript.clicked.connect(self.session.start)

    @property
    def url(self):
        return self.ui.giveawaySite.text()

    @pyqtSlot(str)
    def addCode(self, code):
        item = QListWidgetItem()
        item.setText(code)
        item.setForeground(QColor(12, 93, 9, 255))
        self.ui.secretCodes.addItem(item)

    @pyqtSlot(int)
    def updateTimer(self, time):
        self.ui.outputLabel.setText(
            f'<html><head/><body><p><span style=" font-size:11pt; font-weight:600;">Output ‎‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ '
            f'</span>{convert_to_time(time)}</p></body></html>'
        )

    @pyqtSlot(str, dict)
    def updateLog(self, text, info):
        kwargs = info
        return self.outputSender.send_html(text, **kwargs)

    @pyqtSlot(int)
    def updateProgress(self, progress):
        self.ui.progressBar.setValue(progress)

    def terminate_session(self):
        if self.session.html.html_fetching:
            self.session.logger.emit("COLOR=(#c8001a, Unable to terminate script while HTML fetching.)", {})
        else:
            self.session.logger.emit("TYPES=[(#c8001a, BOLD), Successfully terminated script.]", {})
            self.ui.executeScript.setEnabled(True)
            self.ui.stopScript.setEnabled(False)
            self.playrRunning = False