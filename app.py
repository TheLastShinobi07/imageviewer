import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QToolBar, QAction, QMessageBox, QSlider, QScrollArea
)
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QTransform
from components.imagelabel import ImageLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.resize(700, 700)
        self.setWindowTitle("Image Viewer")

        # Central Widget and Layout
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        image_widget = QWidget()
        layout = QHBoxLayout(image_widget)

        # Adding the ToolBar
        toolBar = QToolBar()
        self.addToolBar(toolBar)

        # Adding the Actions to the Tool Bar
        edit_action = QAction("Edit", self)
        rotate_action = QAction(QIcon("icons/rotate.png"), "Rotate", self)
        rotate_action.triggered.connect(self.rotate_image)
        delete_action = QAction(QIcon("icons/delete.png"), "Delete", self)
        delete_action.triggered.connect(self.delete_image)

        toolBar.setIconSize(QSize(20, 20))
        toolBar.addAction(rotate_action)
        toolBar.addSeparator()
        toolBar.addAction(delete_action)
        toolBar.addSeparator()
        toolBar.setMovable(False)
        toolBar.setStyleSheet("""
            QToolBar{
                spacing: 10px;
                padding: 9px;
            }
        """)

        # Image View Placement
        self.scroll_area = QScrollArea()

        self.label = ImageLabel(self.scroll_area, self)

        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        

        # Listing the Images in the Directory
        # self.file_list = os.listdir("images/")
        image_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif",
            ".avif"
            ".bmp"
        )

        if len(sys.argv) > 1:
            selected_image = os.path.abspath(sys.argv[1])
            self.image_folder = os.path.dirname(selected_image)
            self.file_list = [
                file for file in os.listdir(self.image_folder) if file.lower().endswith(image_extensions)
            ]

            selected_filename = os.path.basename(selected_image)

            if selected_filename in self.file_list:
                self.newindex = self.file_list.index(selected_filename)
            else:
                self.newindex = 0
        else:
            self.image_folder = "images/"
            self.file_list = os.listdir(self.image_folder)
            self.newindex = 0


        # Adding the Previous and Next Buttons an calling the view_image function to display the first image
        prev_btn = QPushButton(self)
        prev_btn.clicked.connect(self.prev_img)
        prev_btn.setIcon(QIcon("icons/prev-btn.png"))
        prev_btn.setIconSize(QSize(32, 32))

        next_btn = QPushButton(self)
        next_btn.clicked.connect(self.next_img)
        next_btn.setIcon(QIcon("icons/next-btn.png"))
        next_btn.setIconSize(QSize(32, 32))     
        self.setCentralWidget(central_widget)

        next_btn.setFixedSize(50, 50)
        prev_btn.setFixedSize(50, 50)

        # Adding the Zoom Slider
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.slider_zoom)

        central_layout.addWidget(image_widget)
        layout.addWidget(prev_btn)
        layout.addWidget(self.scroll_area)
        layout.addWidget(next_btn)
        central_layout.addWidget(self.zoom_slider)
        # viewing the first image in the directory
        self.view_image(self.newindex)

    

# --------------------- Next Function ---------------------
    def next_img(self):
        if self.newindex < len(self.file_list)-1:
            self.newindex += 1
            self.view_image(self.newindex)

# --------------------- Prev Function ---------------------
    def prev_img(self):
        if self.newindex > 0:
            self.newindex -= 1
        self.view_image(self.newindex)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.next_img()
        elif event.key() == Qt.Key_Left:
            self.prev_img()

# --------------------- View Image Function ---------------------
    def view_image(self, index):
        self.index = self.file_list[index]
        self.img_location = os.path.join(
            self.image_folder,
            self.index
        )
        # print(self.img_location)
        self.image = QPixmap(self.img_location)

        self.zoomfactor = 1.0

        self.update_image()

        # self.label.setPixmap(self.image)

    # --------------------- Rotate Image Function ---------------------
    def rotate_image(self):
        self.image = self.image.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
        self.update_image()
    
    # Adding the Zooms In and Zoom Out Function
    def update_image(self):
        available_size = self.scroll_area.viewport().size()
        size = available_size * self.zoomfactor

        zoomed_image = self.image.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(zoomed_image)
        self.label.resize(zoomed_image.size())
        
    def slider_zoom(self, value):
        self.zoomfactor = value / 100
        self.update_image()
    def zoom_in(self):
        self.zoomfactor += 0.1
        self.update_image()
    def zoom_out(self):
        if self.zoomfactor > 0.1:
            self.zoomfactor -= 0.1
            self.update_image()
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    # --------------------- Delete Image Function ---------------------
    def delete_image(self):
        confirm_delete = QMessageBox()
        confirm_delete.setWindowTitle("Delete Image")
        confirm_delete.setText("Are you sure you want to delete this image?")
        confirm_delete.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if confirm_delete.exec_() == QMessageBox.Yes:
            os.remove(self.img_location)
            del self.file_list[self.newindex]
            self.view_image(self.newindex-1)
            print(self.newindex)
        else:
            return
    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec_())