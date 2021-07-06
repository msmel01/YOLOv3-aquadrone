from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle('Data Augmentation GUI')
        self.initUI()


    def initUI(self):
        # Add heading
        self.heading = QtWidgets.QLabel(self)
        self.heading.setGeometry(QtCore.QRect(20, 10, 430, 40))
        heading_font = QtGui.QFont()
        heading_font.setPointSize(16)
        self.heading.setFont(heading_font)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setObjectName('heading')
        self.heading.setText('YOLO Data Augmentation GUI')
        # Add select image directory label
        self.img_dir_label = QtWidgets.QLabel(self)
        self.img_dir_label.setGeometry(20, 60, 200, 20)
        self.img_dir_label.setObjectName('img_dir_label')
        self.img_dir_label.setText('Choose image directory: ')
        # Add button to navigate files and find directory
        self.pick_img_dir_button = QtWidgets.QToolButton(self)
        self.pick_img_dir_button.setGeometry(590, 60, 35, 25)
        self.pick_img_dir_button.setObjectName('pick_img_dir_button')
        self.pick_img_dir_button.setText('...')
        self.directory = self.pick_img_dir_button.clicked.connect(self.pick_img_dir)
        # Display chosen file path
        self.img_dir_disp = QtWidgets.QLineEdit(self)
        self.img_dir_disp.setEnabled(False)
        self.img_dir_disp.setGeometry(QtCore.QRect(200, 60, 375, 25))
        self.img_dir_disp.setObjectName('img_dir_disp')
        # Create new data augmentation pipelines label
        self.data_aug_add_label = QtWidgets.QLabel(self)
        self.data_aug_add_label.setGeometry(20, 90, 650, 50)
        self.data_aug_add_label.setObjectName('data_aug_add_label')
        self.data_aug_add_label.setText(
        '''Press \'Create\' to create a new data augmentation pipeline and select what percentage of 
images in the selected directory it must be applied to.''')
        # cancel button
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(460, 445, 100, 30)
        self.cancel_button.setObjectName('cancel_button')
        self.cancel_button.setText('Cancel')
        self.cancel_button.clicked.connect(lambda: self.close())
        # augment button
        self.augment_button = QtWidgets.QPushButton(self)
        self.augment_button.setGeometry(580, 445, 100, 30)
        self.augment_button.setObjectName('augment_button')
        self.augment_button.setText('Augment')
        #self.augment_button.setStyleSheet('border: 2px solid blue;')
        self.augment_button.clicked.connect(self.augment_images)
        # some kind of a list that shows all the pipelines added
        # add checkbox for adjusting bounding boxes

    def pick_img_dir(self):
        exp = QtWidgets.QFileDialog()
        dir_path = exp.getExistingDirectory(None, "Select Directory")
        self.img_dir_disp.setText('{}'.format(dir_path))
        return dir_path


    def augment_images(self):
        self.close()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())