from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint

class ImageLabel(QLabel):
    def __init__(self, scroll_area, main_window):
        super().__init__()
        self.scroll_area = scroll_area
        self.main_window = main_window
        self.setAlignment(Qt.AlignCenter)
        self.dragging = False
        self.last_point = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True

            self.last_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            current_pos = event.pos()

            difference = current_pos - self.last_point
            horizontal_bar = self.scroll_area.horizontalScrollBar()
            vertical_bar = self.scroll_area.verticalScrollBar()
            horizontal_bar.setValue(
                horizontal_bar.value() - difference.x()
            )
            vertical_bar.setValue(
                vertical_bar.value() - difference.y()
            )
            self.last_point = current_pos
        super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
        