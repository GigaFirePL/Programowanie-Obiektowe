from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QFileDialog, QAction, QMenuBar, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)
        
        self.create_menu()
        
        self.current_image = None
        
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&Plik')
        
        #otwieranie pliku
        open_action = QAction('&Otwórz', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        #zapisywanie pliku
        save_as_action = QAction('Zapisz &jako', self)
        save_as_action.setShortcut('Ctrl+S')
        save_as_action.triggered.connect(self.save_file)
        file_menu.addAction(save_as_action)
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik graficzny",
            "",
            "Pliki graficzne (*.png *.jpg *.bmp *.gif);;Wszystkie pliki (*.*)"
        )
        
        if file_name:
            self.current_image = QImage(file_name)
            if self.current_image.isNull():
                QMessageBox.critical(self, "Błąd", "Nie można otworzyć pliku!")
                return
                
            pixmap = QPixmap.fromImage(self.current_image)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), 
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            
    def save_file(self):
        if self.current_image is None:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak obrazu do zapisania!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik graficzny",
            "",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        
        if file_name:
            if not self.current_image.save(file_name):
                QMessageBox.critical(self, "Błąd", "Nie można zapisać pliku!")
                
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image and not self.image_label.pixmap().isNull():
            pixmap = QPixmap.fromImage(self.current_image)
            scaled_pixmap = pixmap.scaled(self.image_label.size(),
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())