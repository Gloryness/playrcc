import threading

from PyQt5.QtWidgets import QLineEdit

from base.request import validateUrl

class GiveawayText(QLineEdit):
    def __init__(self, base, parent=None):
        self.ui = base
        super(GiveawayText, self).__init__(parent)

        self.wait = 0.5
        self.loading = False
        self.textAuto = False
        self.timer2 = threading.Timer(self.wait, lambda: self.isValid(self.text()))

    def load(self):
        """
        Begin the loading animation
        """
        self.ui.isValidLabel.setVisible(False)
        self._del()

        self.loading = True
        self.ui.container.setVisible(True)

    def _del(self):
        self.loading = False
        self.ui.container.setVisible(False)

    def isValid(self, url):
        self.loading = True

        threadAlive = self.timer2.is_alive() and not self.timer.is_alive()
        thread2Alive = not self.timer2.is_alive() and self.timer.is_alive()
        timerThreads = sum([str(i).count("Timer") for i in threading.enumerate()])

        if timerThreads >= 2:
            quit(self.isValid)

        validate = validateUrl(url)

        if (threadAlive or thread2Alive) and (validate):
            self._del()

            self.ui.isValidLabel.setVisible(True)
            self.ui.isValidLabel.setText("Valid Link")
            self.ui.isValidLabel.setPalette(self.ui.green_palette)
            self.ui.executeScript.setEnabled(True)
            self.ui.gridLayout_5.addItem(self.ui.spacerItem3, 2, 1, 1, 1)

        elif validate is None:
            self._del()
            self.ui.isValidLabel.setVisible(True)
            self.ui.isValidLabel.setText("No Connection")
            self.ui.isValidLabel.setPalette(self.ui.red_palette)
            self.ui.executeScript.setEnabled(False)
            self.ui.gridLayout_5.addItem(self.ui.spacerItem3, 2, 1, 1, 1)

        elif (threadAlive or thread2Alive) and (not validate):
            self._del()
            self.ui.isValidLabel.setVisible(True)
            self.ui.isValidLabel.setText("Invalid ID")
            self.ui.isValidLabel.setPalette(self.ui.red_palette)
            self.ui.executeScript.setEnabled(False)
            self.ui.gridLayout_5.addItem(self.ui.spacerItem3, 2, 1, 1, 1)

    def keyPressEvent(self, event):
        QLineEdit.keyPressEvent(self, event) # execute the original command as well
        url = self.text()
        if self.ui.win.cache.cached(url): # check if already cached
            data = self.ui.win.cache.get(url)
            self.ui.isValidLabel.setVisible(True)
            self.ui.isValidLabel.setText("Valid Link")
            self.ui.isValidLabel.setPalette(self.ui.green_palette)
            self.ui.executeScript.setEnabled(True)
            if self.ui.codeExample.text() == "" and 'code_example' in data:
                self.ui.codeExample.setText(data['code_example'])
            elif (self.ui.codeExample.text() != "") and ('code_example' not in data):
                self.ui.win.cache.store(url, self.ui.codeExample.text())
            self.textAuto = True
            return
        else:
            if self.textAuto:
                self.ui.codeExample.clear()
                self.textAuto = False

        validStart = validateUrl(url, req=False)
        if not validStart:
            self.ui.isValidLabel.setVisible(True)
            self.ui.isValidLabel.setText("Invalid Link")
            self.ui.executeScript.setEnabled(False)
            self.ui.isValidLabel.setPalette(self.ui.red_palette)

        if self.loading and not event.text() == "":
            try:
                self.timer2.start()
            except RuntimeError:
                self.timer2 = threading.Timer(self.wait, lambda: self.isValid(url))
                self.timer2.start()

        if not self.loading and validStart and not event.text() == "":
            self.load()

            self.timer = threading.Timer(self.wait, lambda: self.isValid(url))
            self.timer.start()