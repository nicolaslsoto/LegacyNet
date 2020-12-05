from PyQt5.QtWidgets import QLineEdit


class QPropertyLineEdit(QLineEdit):

    def focusInEvent(self, event):
        if self.text() == "...":
            self.setText("")
        super().focusInEvent(event)
