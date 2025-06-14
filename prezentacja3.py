from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QListWidget, 
                           QSpinBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import sys

class OnlineShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sklep Internetowy")
        self.setGeometry(100, 100, 1000, 600)
        
        # Modern color scheme
        PRIMARY_COLOR = "#2962FF"
        SECONDARY_COLOR = "#FF6D00"
        BG_COLOR = "#F5F5F7"
        CARD_COLOR = "#FFFFFF"
        TEXT_PRIMARY = "#1F1F1F"
        TEXT_SECONDARY = "#757575"
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_COLOR};
            }}
            
            QFrame {{
                background-color: {CARD_COLOR};
                border-radius: 10px;
                border: none;
                padding: 20px;
            }}
            
            QLabel {{
                color: {TEXT_PRIMARY};
                font-size: 14px;
                padding: 5px;
            }}
            
            QLabel#title {{
                color: {TEXT_PRIMARY};
                font-size: 24px;
                font-weight: bold;
                padding: 10px 5px;
            }}
            
            QLabel#total {{
                color: {PRIMARY_COLOR};
                font-size: 18px;
                font-weight: bold;
                padding: 10px 5px;
            }}
            
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                min-width: 120px;
                font-size: 14px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: #1E4BCC;
            }}
            
            QPushButton#buy-button {{
                background-color: {SECONDARY_COLOR};
                font-size: 16px;
                padding: 15px;
            }}
            
            QPushButton#buy-button:hover {{
                background-color: #CC5700;
            }}
            
            QListWidget {{
                background-color: {BG_COLOR};
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: {PRIMARY_COLOR};
                selection-color: white;
            }}
            
            QListWidget::item {{
                padding: 10px;
                margin: 2px 0;
                border-radius: 4px;
            }}
            
            QListWidget::item:hover {{
                background-color: #E3F2FD;
            }}
            
            QSpinBox {{
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
                min-width: 80px;
            }}
            
            QSpinBox::up-button, QSpinBox::down-button {{
                border: none;
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 3px;
                margin: 2px;
            }}
        """)
        
        # Utworzenie głównego widżetu i układu
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)
        
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
        title_label.setObjectName("title")
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
        self.total_label.setObjectName("total")
        cart_panel.addWidget(self.total_label)
        
        buy_button = QPushButton("Kup teraz")
        buy_button.setStyleSheet("""
            background-color: #2196F3;
            padding: 10px;
            font-size: 14px;
        """)
        buy_button.setObjectName("buy-button")
        buy_button.clicked.connect(self.buy)
        cart_panel.addWidget(buy_button)
        
        layout.addWidget(cart_frame)
        
        # Dodanie cień do paneli
        products_frame.setGraphicsEffect(self.create_shadow())
        cart_frame.setGraphicsEffect(self.create_shadow())
        
    def create_shadow(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 50))
        return shadow

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