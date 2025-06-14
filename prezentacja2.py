from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QListWidget, 
                           QSpinBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import sys

class OnlineShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prosty Sklep Internetowy")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                min-width: 100px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        # Utworzenie głównego widżetu i układu
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Lista produktów
        self.products = {
            "Laptop": 3500,
            "Smartfon": 1200,
            "Słuchawki": 200,
            "Mysz": 80,
            "Klawiatura": 150
        }
        
        # Koszyk
        self.cart = {}
        
        # Panel produktów
        products_frame = QFrame()
        products_frame.setFrameStyle(QFrame.StyledPanel)
        products_panel = QVBoxLayout(products_frame)
        products_panel.setSpacing(15)
        
        title_label = QLabel("Dostępne produkty")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        products_panel.addWidget(title_label)
        
        self.products_list = QListWidget()
        self.products_list.addItems(self.products.keys())
        products_panel.addWidget(self.products_list)
        
        # Panel ilości
        quantity_layout = QHBoxLayout()
        quantity_layout.setSpacing(10)
        quantity_label = QLabel("Ilość:")
        quantity_label.setFont(QFont('Arial', 12))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 10)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_spin)
        products_panel.addLayout(quantity_layout)
        
        add_button = QPushButton("Dodaj do koszyka")
        add_button.clicked.connect(self.add_to_cart)
        products_panel.addWidget(add_button)
        
        layout.addWidget(products_frame)
        
        # Panel koszyka
        cart_frame = QFrame()
        cart_frame.setFrameStyle(QFrame.StyledPanel)
        cart_panel = QVBoxLayout(cart_frame)
        cart_panel.setSpacing(15)
        
        cart_title = QLabel("Koszyk")
        cart_title.setFont(QFont('Arial', 16, QFont.Bold))
        cart_panel.addWidget(cart_title)
        
        self.cart_list = QListWidget()
        cart_panel.addWidget(self.cart_list)
        
        self.total_label = QLabel("Suma: 0 zł")
        self.total_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.total_label.setStyleSheet("color: #2196F3;")
        cart_panel.addWidget(self.total_label)
        
        buy_button = QPushButton("Kup teraz")
        buy_button.setStyleSheet("""
            background-color: #2196F3;
            padding: 10px;
            font-size: 14px;
        """)
        buy_button.clicked.connect(self.buy)
        cart_panel.addWidget(buy_button)
        
        layout.addWidget(cart_frame)
        
    def add_to_cart(self):
        product = self.products_list.currentItem()
        if not product:
            return
            
        product_name = product.text()
        quantity = self.quantity_spin.value()
        
        if product_name in self.cart:
            self.cart[product_name] += quantity
        else:
            self.cart[product_name] = quantity
            
        self.update_cart()
        
    def update_cart(self):
        self.cart_list.clear()
        total = 0
        
        for product, quantity in self.cart.items():
            price = self.products[product]
            total += price * quantity
            self.cart_list.addItem(f"{product} x{quantity} = {price * quantity} zł")
            
        self.total_label.setText(f"Suma: {total} zł")
        
    def buy(self):
        if not self.cart:
            QMessageBox.warning(self, "Błąd", "Koszyk jest pusty!")
            return
            
        total = sum(self.products[p] * q for p, q in self.cart.items())
        QMessageBox.information(self, "Zakup", 
                              f"Zakupiono produkty o wartości {total} zł")
        self.cart.clear()
        self.update_cart()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shop = OnlineShop()
    shop.show()
    sys.exit(app.exec_())