import os
import subprocess

from PyQt5.QtWidgets import QListWidget, QFileDialog

class Save:
    def __init__(self, list: QListWidget, parent=None):
        self.list = list
        self.parent = parent
        self.directory = os.path.abspath(f"{os.environ['USERPROFILE']}/Documents/playrcc/giveaways/".replace("\\", "/"))

    def data(self):
        """
        List all items in the ListWidget and return them in a string seperated by a new line
        :return: str
        """
        data = []
        amount = self.list.count()
        for i in range(amount):
            data.append(self.list.item(i).text())
        return '\n'.join(data)

    def saveAs(self):
        self.filename = QFileDialog.getSaveFileName(self.parent, 'Save As..', filter='Text Document (*.txt)', directory=self.directory)
        self.filename = self.filename[0]
        if self.filename == "":
            delattr(self, 'filename')
            return

        if os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.truncate()
                f.write(self.data())
        elif not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write(self.data())

    def save(self):
        if not hasattr(self, 'filename'):
            self.saveAs()
        else:
            if not os.path.exists(self.filename):
                self.saveAs()
            else:
                with open(self.filename, 'w') as f:
                    f.truncate()
                    f.write(self.data())

def openExplorer(path):
    files = os.listdir(path)
    if len(files) >= 1:
        path = os.path.join(path, files[0])
    subprocess.Popen(f'explorer /select,"{path}"')