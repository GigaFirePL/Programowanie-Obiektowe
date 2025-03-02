import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

app = QApplication(sys.argv)
label = QLabel()
label.setAlignment(Qt.AlignCenter)
label.setText("<b>Bold</b> <i>Italic</i> <u>Underlined</u> <font color='Blue'>Blue Text</font><a href='https://example.com'>Kliknij tutaj</a>")
font = QFont("Arial", 50)
label.setFont(font)
label.setStyleSheet("background-color: pink;")
label.setOpenExternalLinks(True)
label.show()
app.exec()