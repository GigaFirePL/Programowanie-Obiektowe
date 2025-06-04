from PyQt5.QtWidgets import (QMainWindow, QApplication, QGraphicsScene, QGraphicsView, 
                           QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QColorDialog,
                           QComboBox, QSpinBox, QGraphicsItem)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QImage
import sys

class Shape(QGraphicsItem):
    def __init__(self, shape_type, size, color):
        super().__init__()
        self.shape_type = shape_type
        self.size = size
        self.color = color
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
          
    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size, self.size)
         
    def paint(self, painter, option, widget):
        painter.setPen(QPen(self.color, 2))
        painter.setBrush(QBrush(self.color))
        
        if self.shape_type == "Koło":
            painter.drawEllipse(self.boundingRect())
        elif self.shape_type == "Kwadrat":
            painter.drawRect(self.boundingRect())
        elif self.shape_type == "Trójkąt":
            points = [
                QPointF(-self.size/2, self.size/2),
                QPointF(self.size/2, self.size/2),
                QPointF(0, -self.size/2)
            ]
            painter.drawPolygon(points)
  
class VectorEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edytor grafiki wektorowej")
        self.setGeometry(100, 100, 800, 600)
        
        # Utworzenie głównego widżetu i układu
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Utworzenie sceny i widoku
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        
        # Panel kontrolny
        control_panel = QHBoxLayout()
        
        # Wybór kształtu
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Koło", "Kwadrat", "Trójkąt"])
        control_panel.addWidget(self.shape_combo)
        
        # Wybór rozmiaru
        self.size_spin = QSpinBox()
        self.size_spin.setRange(20, 200)
        self.size_spin.setValue(50)
        control_panel.addWidget(self.size_spin)
        
        # Przyciski kontrolne
        self.color_button = QPushButton("Wybierz kolor")
        self.color_button.clicked.connect(self.choose_color)
        control_panel.addWidget(self.color_button)
      
        add_button = QPushButton("Dodaj kształt")
        add_button.clicked.connect(self.add_shape)
        control_panel.addWidget(add_button)
        
        delete_button = QPushButton("Usuń")
        delete_button.clicked.connect(self.delete_selected)
        control_panel.addWidget(delete_button)
        
        bring_front = QPushButton("Na wierzch")
        bring_front.clicked.connect(self.bring_to_front)
        control_panel.addWidget(bring_front)
        
        send_back = QPushButton("Na spód")
        send_back.clicked.connect(self.send_to_back)
        control_panel.addWidget(send_back)
        
        save_button = QPushButton("Zapisz PNG")
        save_button.clicked.connect(self.save_image)
        control_panel.addWidget(save_button)
        
        layout.addLayout(control_panel)
        
        self.current_color = QColor(Qt.red)
         
    def choose_color(self):
        color = QColorDialog.getColor(self.current_color)
        if color.isValid():
            self.current_color = color
             
    def add_shape(self):
        shape = Shape(
            self.shape_combo.currentText(),
            self.size_spin.value(),
            self.current_color
        )
        self.scene.addItem(shape)
        shape.setPos(0, 0)
         
    def delete_selected(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
             
    def bring_to_front(self):
        for item in self.scene.selectedItems():
            z = 0
            for other_item in self.scene.items():
                if other_item.zValue() >= z:
                    z = other_item.zValue() + 1
            item.setZValue(z)
             
    def send_to_back(self):
        for item in self.scene.selectedItems():
            z = 0
            for other_item in self.scene.items():
                if other_item.zValue() <= z:
                    z = other_item.zValue() - 1
            item.setZValue(z)
             
    def save_image(self):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Zapisz jako PNG", "", "PNG Files (*.png)"
        )
        if filename:
            rect = self.scene.itemsBoundingRect()
            image = QImage(rect.size().toSize(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)
             
            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            self.scene.render(painter, QRectF(image.rect()), rect)
            painter.end()
            
            image.save(filename)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = VectorEditor()
    editor.show()
    sys.exit(app.exec_())