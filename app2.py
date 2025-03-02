import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

app = QApplication(sys.argv)
def on_label_clicked(event):
    label.setText("Tekst został zmieniony!")
label = QLabel()
label2 = QLabel("<a href='https://example.com'>Kliknij tutaj</a>")
label.setAlignment(Qt.AlignCenter)
label.setText("<b>Bold</b> <i>Italic</i> <u>Underlined</u> <font color='Blue'>Blue Text</font>")
font = QFont("Arial", 50)
label.setFont(font)
label.setStyleSheet("background-color: pink;")
label.mouseReleaseEvent = on_label_clicked
label.show()
label2.setAlignment(Qt.AlignLeft)
label2.setOpenExternalLinks(True)
label2.show()
app.exec()