import sys
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QImage, QColor, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel, QWidget, QComboBox
from encoding import Encoder, Decoder
from image import Image
from pixel import Pixel

class MainWindow(QWidget):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.UI()
        
        
    def UI(self) -> None:
        layout = QVBoxLayout()
        
        self.setWindowTitle('Image Viewer Window')
        self.image_label = QLabel()
        self.save_button = QPushButton('Save Image', layout.widget())
        self.load_button = QPushButton('load Image', layout.widget())
        
        self.version_combo = QComboBox(self)
        self.version_combo.addItem('Version 1')
        self.version_combo.addItem('Version 2')
        self.version_combo.addItem('Version 3')
        self.version_combo.addItem('Version 4')

        layout.addWidget(self.image_label)
        layout.addWidget(self.version_combo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        
        self.load_button.clicked.connect(self.image_open)
        self.save_button.clicked.connect(self.save_image)
        
        self.image_label.setFixedSize(400, 400)   
    
        self.setLayout(layout)
        self.show()
        """
        configure the user interface
        """
        
    def image_open(self) -> None :
        file_path, _ = QFileDialog.getOpenFileName(self, 'load Image', '', 'Image Files (*.ulbmp)')
        if file_path:        
            image = self.load_image(file_path)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.width(), pixmap.height())
            self.resize(pixmap.width() + 30, pixmap.height() + 70)
            
        """
        open a dialog window to load an image
        """

    
    def load_image(self, file_path) -> QImage:
        version = int(self.version_combo.currentText().split()[1]) - 1
        decode = Decoder.load_from(file_path)
        self.image = decode
        self.image_label.setFixedSize(decode.height, decode.width)
        self.resize(decode.width, decode.height)
        image = QImage(decode.width, decode.height, QImage.Format_RGB32)
        for y in range(decode.height):
            for x in range(decode.width):
                index = y * decode.width + x
                pixel = decode.pixels[index]
                color = QColor(pixel.red, pixel.green, pixel.blue)
                image.setPixel(x, y, color.rgb())
        return image
    """
    load an image from a file and convert it to a QImage
    args:
        file_path(str): the path of the image file
    returns :
        QImage: the loaded image
    """ 
     
    def save_image(self, file_path) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, 'load Image', '', 'Image Files (*.ulbmp)')
        encoder = Encoder(img= self.image, version= int(self.version_combo.currentText().split()[1]), depth= 24, rle= False).save_to(file_path)
        return None
    """ 
    save the currently displayed image
    args:
        file_path(str): the destination path for saving the image
    return:
        none
    """