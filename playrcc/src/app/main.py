from sys import argv, exit as sys_exit
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    from gui import SecretCodeWindow

    app = QApplication(argv)

    win = SecretCodeWindow()
    win.show()

    sys_exit(app.exec_())