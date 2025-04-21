from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QFileDialog, QAction, QMenuBar, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QCheckBox, QPushButton)
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt, QSize
import sys

class PreviewWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Podgląd")
        self.setGeometry(100, 100, 200, 200)
        
        layout = QVBoxLayout()
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)
        self.setLayout(layout)
        
    def update_preview(self, image):
        if image:
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(QSize(180, 180), 
                                        Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)
            self.show()
        else:
            self.hide()

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Ustawienia obrazu")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        self.mirror_check = QCheckBox("Odbicie lustrzane")
        self.grayscale_check = QCheckBox("Skala szarości")
        
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Skala:"))
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 200)
        self.scale_slider.setValue(100)
        scale_layout.addWidget(self.scale_slider)
        
        apply_button = QPushButton("Zastosuj")
        apply_button.clicked.connect(self.apply_settings)
        
        layout.addWidget(self.mirror_check)
        layout.addWidget(self.grayscale_check)
        layout.addLayout(scale_layout)
        layout.addWidget(apply_button)
        
        self.setLayout(layout)
        
    def apply_settings(self):
        if hasattr(self, 'parent') and self.parent():
            settings = {
                'mirror': self.mirror_check.isChecked(),
                'grayscale': self.grayscale_check.isChecked(),
                'scale': self.scale_slider.value() / 100.0
            }
            self.parent().apply_image_settings(settings)

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
        
        self.preview_window = PreviewWindow()
        self.settings_window = SettingsWindow(self)
        
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
        
        view_menu = menubar.addMenu('&Widok')
        settings_action = QAction('&Ustawienia', self)
        settings_action.triggered.connect(self.show_settings)
        view_menu.addAction(settings_action)
        
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
            
            self.preview_window.move(self.x() + self.width() + 10, self.y())
            self.preview_window.update_preview(self.current_image)
            
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
            
    def apply_image_settings(self, settings):
        if self.current_image is None:
            return
            
        modified_image = QImage(self.current_image)
        
        if settings['mirror']:
            modified_image = modified_image.mirrored(True, False)
            
        if settings['grayscale']:
            modified_image = modified_image.convertToFormat(QImage.Format_Grayscale8)
            
        pixmap = QPixmap.fromImage(modified_image)
        scaled_size = self.image_label.size() * settings['scale']
        scaled_pixmap = pixmap.scaled(scaled_size, 
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.preview_window.update_preview(modified_image)
    
    def show_settings(self):
        self.settings_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())