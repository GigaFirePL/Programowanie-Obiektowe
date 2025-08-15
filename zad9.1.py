from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class _Bar(QtWidgets.QWidget):

    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, steps, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        if isinstance(steps, list):
            self.n_steps = len(steps)
            self.steps = steps

        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = [
                QtGui.QColor.fromHsv(120 - (120 * i // (steps - 1)), 255, 255).name()
                for i in range(steps)
            ]
        
        self._dot_radius = 10 
        self._background_color = QtGui.QColor('white')
        self._padding = 10

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        value = parent.value()

        d_width = painter.device().width() - (self._padding * 2)
        d_height = painter.device().height() - (self._padding * 2)

        pc = (value - vmin) / (vmax - vmin)
        n_dots_to_fill = int(pc * self.n_steps)

        step_size = d_width / (self.n_steps - 1)
        y_center = self._padding + d_height / 2

        for n in range(self.n_steps):
            if n < n_dots_to_fill:
                brush.setColor(QtGui.QColor(self.steps[n]))
            else:
                brush.setColor(QtGui.QColor("#dddddd"))
            
            painter.setBrush(brush)
            painter.setPen(QtGui.QPen(QtGui.QColor("#999999")))
            
            center = QtCore.QPointF(
                self._padding + n * step_size,
                y_center
            )
            painter.drawEllipse(center, self._dot_radius, self._dot_radius)

        painter.end()

    def sizeHint(self):
        return QtCore.QSize(300, 50) 

    def _trigger_refresh(self):
        self.update()

    def _calculate_clicked_value(self, e):
        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        d_width = self.size().width() - (self._padding * 2)
        step_size = d_width / (self.n_steps - 1)
        
        click_x = e.position().x() - self._padding
        
        dot_index = round(click_x / step_size)
        dot_index = max(0, min(dot_index, self.n_steps - 1))
        
        pc = dot_index / (self.n_steps - 1)
        value = vmin + pc * (vmax - vmin)
        self.clickedValue.emit(int(value))

    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)
        
    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)


class PowerBar(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    """

    colorChanged = QtCore.pyqtSignal()

    def __init__(self, steps=15, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout() 
        self._bar = _Bar(steps)
        layout.addWidget(self._bar)

        self._dial = QtWidgets.QDial()
        self._dial.setNotchesVisible(True)
        self._dial.setWrapping(False)
        self._dial.valueChanged.connect(self._bar._trigger_refresh)
        self._dial.setFixedSize(50, 50)
        layout.addWidget(self._dial)
        
        self._bar.clickedValue.connect(self._dial.setValue)
        
        self.setLayout(layout)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self[name]

        return getattr(self._dial, name)

    def setColor(self, color):
        self._bar.steps = [color] * self._bar.n_steps
        self._bar.update()

    def setColors(self, colors):
        self._bar.n_steps = len(colors)
        self._bar.steps = colors
        self._bar.update()

    def setBarPadding(self, i):
        self._bar._padding = int(i)
        self._bar.update()

    def setBarSolidPercent(self, f):
        self._bar._bar_solid_percent = float(f)
        self._bar.update()

    def setBackgroundColor(self, color):
        self._bar._background_color = QtGui.QColor(color)
        self._bar.update()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)

    power_bar = PowerBar(steps=10)
    layout.addWidget(power_bar)

    window.setWindowTitle("PowerBar Demo")
    window.resize(300, 200)
    window.show()

    sys.exit(app.exec())