from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import aug_pipeline_win as ap
import aug

# TODO:
# replace Crop with RandomCropNearBBox or RandomSizedBBoxSafeCrop?

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle('Data Augmentation GUI')
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.img_dir = './'
        self.pipeline_count = 0
        self.keep_orig = True
        self.pipeline_window_dict = {}
        self.setupUi()


    def setupUi(self):
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
        self.directory = self.pick_img_dir_button.clicked.connect(self.pickImgDir)
        # Display chosen file path
        self.img_dir_disp = QtWidgets.QLineEdit(self)
        self.img_dir_disp.setEnabled(False)
        self.img_dir_disp.setGeometry(QtCore.QRect(200, 60, 375, 25))
        self.img_dir_disp.setObjectName('img_dir_disp')
        # Create new data augmentation pipelines label
        self.data_aug_add_label = QtWidgets.QLabel(self)
        self.data_aug_add_label.setGeometry(20, 90, 650, 50)
        self.data_aug_add_label.setObjectName('data_aug_add_label')
        self.data_aug_add_label.setText("Press 'Create' to create a new data augmentation pipeline and select what percentage of \n images in the selected directory it must be applied to.")
        # cancel button
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(460, 445, 100, 30)
        self.cancel_button.setObjectName('cancel_button')
        self.cancel_button.setText('Cancel')
        self.cancel_button.clicked.connect(lambda: self.close())
        # augment button
        self.augment_button = QtWidgets.QPushButton(self)
        self.augment_button.setGeometry(570, 445, 100, 30)
        self.augment_button.setObjectName('augment_button')
        self.augment_button.setText('Augment')
        self.augment_button.clicked.connect(self.augmentImages)
        # modify pipeline button
        self.modify_pipeline_button = QtWidgets.QPushButton(self)
        self.modify_pipeline_button.setText('Modify pipeline')
        self.modify_pipeline_button.setGeometry(240, 150, 140, 30)
        self.modify_pipeline_button.clicked.connect(self.showPipelineWindow)
        self.modify_pipeline_button.setEnabled(False)
        # Set default label and checkbox
        self.default_label = QtWidgets.QLabel(self)
        self.default_label.setObjectName('default_label')
        self.default_label.setText('Load default pipelines')
        self.default_label.setGeometry(500, 178, 170, 30)
        self.default_checkbox = QtWidgets.QCheckBox(self)
        self.default_checkbox.setObjectName('default_checkbox')
        self.default_checkbox.setCheckState(False)
        self.default_checkbox.stateChanged.connect(lambda: self.setDefault() if (self.default_checkbox.isChecked()) else self.unsetDefault())
        self.default_checkbox.setGeometry(470, 178, 30, 30)
        # Keep original image label and checkbox
        self.orig_label = QtWidgets.QLabel(self)
        self.orig_label.setText('Keep original image')
        self.orig_label.setGeometry(500, 210, 170, 30)
        self.orig_checkbox = QtWidgets.QCheckBox(self)
        self.orig_checkbox.setCheckState(False)
        self.orig_checkbox.stateChanged.connect(self.setKeepOrig)
        self.orig_checkbox.setGeometry(470, 210, 30, 30)
        # add a pipeline
        self.add_pipeline_button = QtWidgets.QPushButton(self)
        self.add_pipeline_button.setGeometry(20, 150, 100, 30)
        self.add_pipeline_button.setObjectName('add_pipeline_button')
        self.add_pipeline_button.setText('Add')
        self.add_pipeline_button.clicked.connect(self.addPipeline)
        # remove a pipeline
        self.rmv_pipeline_button = QtWidgets.QPushButton(self)
        self.rmv_pipeline_button.setGeometry(130, 150, 100, 30)
        self.rmv_pipeline_button.setObjectName('rmv_pipeline_button')
        self.rmv_pipeline_button.setText('Remove')
        self.rmv_pipeline_button.setEnabled(False)
        self.rmv_pipeline_button.clicked.connect(self.removePipeline)
        # layout for added pipelines
        self.pipeline_layout = QtWidgets.QListWidget(self)
        self.pipeline_layout.setGeometry(QtCore.QRect(20, 190, 420, 250))
        self.pipeline_layout.setObjectName('pipeline_list')
        self.list_scroll_bar = QtWidgets.QScrollBar(self)
        self.list_scroll_bar.setObjectName('list_scroll_bar')
        self.pipeline_layout.setVerticalScrollBar(self.list_scroll_bar)
        self.pipeline_layout.itemClicked.connect(self.pipelineSelected)


    def setKeepOrig(self):
        self.keep_orig = self.orig_checkbox.isChecked()


    def pipelineSelected(self):
        self.rmv_pipeline_button.setEnabled(True)
        self.modify_pipeline_button.setEnabled(True)


    def pickImgDir(self):
        exp = QtWidgets.QFileDialog()
        dir_path = exp.getExistingDirectory(None, "Select Directory")
        self.img_dir_disp.setText('{}'.format(dir_path))
        self.img_dir = dir_path
        return dir_path


    def setDefault(self):
        if self.pipeline_count != 0: # warning that all existing pipelines will be deletec
            default_warning = QtWidgets.QMessageBox(self)
            default_warning.setIcon(QtWidgets.QMessageBox.Warning)
            default_warning.setWindowTitle("Set default pipeline(s) warning")
            default_warning.setText("All existing pipelines will be deleted if you proceed and default pipelines will be added instead.")
            default_warning.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            retval = default_warning.exec_()
            if retval != QtWidgets.QMessageBox.Ok: return
        
        self.pipeline_layout.clear()
        self.pipeline_count = 0


    def unsetDefault(self):
        if self.pipeline_count != 0: # warning that all existing pipelines will be deletec
            default_warning = QtWidgets.QMessageBox(self)
            default_warning.setIcon(QtWidgets.QMessageBox.Warning)
            default_warning.setWindowTitle("Unset default pipeline(s) warning")
            default_warning.setText("Default pipelines and pipelines you may have added will be deleted if you proceed.")
            default_warning.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            retval = default_warning.exec_()
            if retval != QtWidgets.QMessageBox.Ok: return
        
        self.pipeline_layout.clear()
        self.pipeline_count = 0


    def showPipelineWindow(self):
        pipeline_name = self.pipeline_layout.currentItem().text()
        self.pipeline_layout.itemDoubleClicked.connect(self.showPipelineWindow)
        self.pipeline_config_win = self.pipeline_window_dict[pipeline_name]
        self.pipeline_config_win.exec()
        self.pipeline_layout.currentItem().setText(self.pipeline_config_win.name)


    def augmentImages(self):
        if self.pipeline_count == 0: return
        augmenter = aug.Augmentor(self.img_dir, self.keep_orig)

        for name, pipeline in self.pipeline_window_dict.items():
            if pipeline.aug_oneh.count(True):
                augmenter.createPipeline(name, pipeline)

        augmenter.augment()
        print('Successfully augmented images.')
        self.close()
        

    def addPipeline(self):
        self.pipeline_count += 1
        pipeline_name = 'New pipeline {}'.format(self.pipeline_count)
        self.pipeline_layout.insertItem(self.pipeline_count, pipeline_name)
        self.pipeline_window_dict[pipeline_name] = ap.PipelineWindow(pipeline_name, self)


    def removePipeline(self):
        self.rmv_pipeline_button.setEnabled(False)
        self.modify_pipeline_button.setEnabled(False)
        if self.pipeline_count == 0: return
        self.pipeline_count -= 1
        currentItemText = self.pipeline_layout.currentItem().text()
        currentItem = self.pipeline_layout.findItems(currentItemText, QtCore.Qt.MatchExactly)[0]
        currentItemRow = self.pipeline_layout.row(currentItem)
        del self.pipeline_window_dict[currentItem.text()]
        self.pipeline_layout.takeItem(currentItemRow)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
