from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QMenuBar, 
                             QMessageBox, QToolBar, QStatusBar, QDialog, 
                             QVBoxLayout, QLabel, QPushButton, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Demo")
        self.setGeometry(100, 100, 800, 600)

        # Tworzenie paska statusu
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Tworzenie akcji
        self.new_action = QAction(QIcon('icons/new-document.png'), '&Nowy', self)
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('Utwórz nowy plik')
        self.new_action.triggered.connect(self.new_file)
        
        self.open_action = QAction(QIcon('icons/open.png'), '&Otwórz', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setStatusTip('Otwórz istniejący plik')
        self.open_action.triggered.connect(self.open_file)
        
        self.save_action = QAction(QIcon('icons/floppy-disk.png'), '&Zapisz', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setStatusTip('Zapisz aktualny plik')
        self.save_action.triggered.connect(self.save_file)
        
        self.about_action = QAction(QIcon('icons/info.png'), '&O programie', self)
        self.about_action.setStatusTip('Wyświetl informacje o programie')
        self.about_action.triggered.connect(self.about)

        # Tworzenie menu
        menubar = self.menuBar()
        
        # Menu Plik
        file_menu = menubar.addMenu('&Plik')
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        
        # Menu Pomoc
        help_menu = menubar.addMenu('Pomo&c')
        
        # Podmenu w menu Pomoc
        support_menu = help_menu.addMenu('&Wsparcie')
        
        # Tworzenie akcji dla dokumentacji i FAQ
        self.doc_action = QAction(QIcon('icons/folder.png'), '&Dokumentacja', self)
        self.doc_action.setStatusTip('Wyświetl dokumentację')
        
        self.faq_action = QAction(QIcon('icons/faq.png'), '&FAQ', self)
        self.faq_action.setStatusTip('Często zadawane pytania')
        
        # Dodanie akcji do menu Wsparcie
        support_menu.addAction(self.doc_action)
        support_menu.addAction(self.faq_action)
        
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

        # Tworzenie pionowego toolbara
        toolbar = QToolBar()
        toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        # Ustawienie wielkości ikon
        toolbar.setIconSize(QSize(25, 25))
        
        # Dodawanie akcji do toolbara
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.doc_action)
        toolbar.addAction(self.faq_action)
        toolbar.addSeparator()
        toolbar.addAction(self.about_action)

    def new_file(self):
        dialog = CustomDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            self.statusBar.showMessage("Utworzono nowy plik", 2000)
        else:
            self.statusBar.showMessage("Anulowano tworzenie pliku", 2000)
            
    def open_file(self):
        print("Otwieranie pliku")
        
    def save_file(self):
        reply = QMessageBox.question(self, 'Zapisywanie',
                                   "Czy na pewno chcesz zapisać plik?",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.statusBar.showMessage("Plik został zapisany", 2000)
        elif reply == QMessageBox.No:
            self.statusBar.showMessage("Anulowano zapisywanie", 2000)
        else:
            self.statusBar.showMessage("Operacja przerwana", 2000)
        
    def about(self):
        msg = QMessageBox()
        msg.setWindowTitle("O programie")
        msg.setText('<a href="https://www.flaticon.com/free-icons/new">New icons created by Freepik - Flaticon</a>')
        msg.setTextFormat(Qt.RichText)
        msg.setTextInteractionFlags(Qt.TextBrowserInteraction)
        msg.exec_()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nowy plik")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Dodanie elementów do dialogu
        message = QLabel("Wybierz typ nowego pliku:")
        layout.addWidget(message)
        
        # Radio buttony
        self.rb1 = QRadioButton("Dokument tekstowy")
        self.rb2 = QRadioButton("Arkusz kalkulacyjny")
        self.rb1.setChecked(True)
        layout.addWidget(self.rb1)
        layout.addWidget(self.rb2)
        
        # Przyciski
        buttons = QVBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Anuluj")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())