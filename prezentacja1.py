from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QListWidget, 
                           QSpinBox, QMessageBox)
import sys

class OnlineShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prosty Sklep Internetowy")
        self.setGeometry(100, 100, 600, 400)
        
        # Utworzenie głównego widżetu i układu
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
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
        products_panel = QVBoxLayout()
        products_panel.addWidget(QLabel("Dostępne produkty:"))
        
        self.products_list = QListWidget()
        self.products_list.addItems(self.products.keys())
        products_panel.addWidget(self.products_list)
        
        # Panel ilości
        quantity_layout = QHBoxLayout()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 10)
        quantity_layout.addWidget(QLabel("Ilość:"))
        quantity_layout.addWidget(self.quantity_spin)
        products_panel.addLayout(quantity_layout)
        
        # Przycisk dodania do koszyka
        add_button = QPushButton("Dodaj do koszyka")
        add_button.clicked.connect(self.add_to_cart)
        products_panel.addWidget(add_button)
        
        layout.addLayout(products_panel)
        
        # Panel koszyka
        cart_panel = QVBoxLayout()
        cart_panel.addWidget(QLabel("Koszyk:"))
        
        self.cart_list = QListWidget()
        cart_panel.addWidget(self.cart_list)
        
        self.total_label = QLabel("Suma: 0 zł")
        cart_panel.addWidget(self.total_label)
        
        # Przycisk zakupu
        buy_button = QPushButton("Kup teraz")
        buy_button.clicked.connect(self.buy)
        cart_panel.addWidget(buy_button)
        
        layout.addLayout(cart_panel)
        
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