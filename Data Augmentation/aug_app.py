from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
import sys
import aug_classes as ac 

# TODO:
# Add sanity checks for spinboxes
# Check required input is given at the time window is closed
# Add warning box when terminate is pressed
# Add percentage of images option

class PipelineWindow(QWidget):
    def __init__(self, default_name, parent):
        super(QWidget, self).__init__()
        self.default_name = default_name
        self.name = self.default_name
        self.prev_aug = 0
        self.aug_oneh = [False] * 7
        self.aug_objects = ['Horizontal Flip', 'Motion Blur', 'ISO Noise', 'Rotate',
                            'Cutout', 'Crop', 'RGB Shift']
        self.aug_param = []
        self.aug_param.append(ac.HorizontalFlipParams())
        self.aug_param.append(ac.MotionBlurParams())
        self.aug_param.append(ac.IsoNoiseParams())
        self.aug_param.append(ac.RotateParams())
        self.aug_param.append(ac.CutOutParams())
        self.aug_param.append(ac.CropParams())
        self.aug_param.append(ac.RgbShiftParams())
        parentTopLeft = parent.geometry().topLeft()
        self.setGeometry(parentTopLeft.x() + 100, parentTopLeft.y() + 100, 600, 500)
        self.setWindowTitle('{} Configuration'.format(default_name))
        self.setupUi()


    def closeEvent(self,event):
        quit_warning = QMessageBox(self)
        quit_warning.setIcon(QtWidgets.QMessageBox.Warning)
        quit_warning.setWindowTitle('Quit pipeline configuration warning')
        quit_warning.setText('Current pipeline configuration will be discarded if you proceed. To save and exit, use the Done button. Do you want to proceed?')
        quit_warning.setStandardButtons(QMessageBox.Yes| QtWidgets.QMessageBox.No)
        retval = quit_warning.exec_()
        if retval == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def setupUi(self):
        # pipeline name label
        self.pipeline_name_label = QtWidgets.QLabel(self)
        self.pipeline_name_label.setObjectName('pipeline_name_label')
        self.pipeline_name_label.setText('Pipeline Name: ')
        self.pipeline_name_label.setGeometry(20, 10, 200, 30)
        # textbox to enter name
        self.pipeline_name_textbox = QtWidgets.QLineEdit(self)
        self.pipeline_name_textbox.setObjectName('pipeline_name_textbox')
        self.pipeline_name_textbox.setPlaceholderText(self.name)
        self.pipeline_name_textbox.setGeometry(QtCore.QRect(135, 10, 400, 30))
        self.pipeline_name_textbox.textEdited.connect(lambda: self.updateName(self.pipeline_name_textbox.text()))
        # percentage of images to apply to
        self.image_percent_label = QtWidgets.QLabel(self)
        self.image_percent_label.setText('Percentage of Images:')
        self.image_percent_label.setGeometry(20, 60, 200, 30)
        self.image_percent_box = QtWidgets.QDoubleSpinBox(self)
        self.image_percent_box.setMaximum(100.0)
        self.image_percent_box.setMinimum(0.0)
        self.image_percent_box.setDecimals(1)
        self.image_percent_box.setSingleStep(0.1)
        self.image_percent_box.setGeometry(185, 60, 100, 30)
        self.image_percent_box.valueChanged.connect(self.saveImagePercent)
        # add select toggle box to add transformations
        self.aug_combo_box = QtWidgets.QComboBox(self)
        self.aug_combo_box.setObjectName('aug_combo_box')
        self.aug_combo_box.setGeometry(20, 110, 480, 30)
        for aug in self.aug_objects:
            self.aug_combo_box.addItem(aug)
        self.aug_combo_box.activated.connect(self.updateUi)
        # add button
        self.add_aug_img = QtGui.QPixmap('plus.png')
        self.add_aug_icon = QtGui.QIcon(self.add_aug_img)
        self.add_aug_button = QtWidgets.QPushButton(self)
        self.add_aug_button.setGeometry(510, 108, 35, 35)
        self.add_aug_button.setIcon(self.add_aug_icon)
        self.add_aug_button.setIconSize(QtCore.QSize(25,25))
        self.add_aug_button.clicked.connect(self.addAug)
        # remove button
        self.rmv_aug_img = QtGui.QPixmap('remove.png')
        self.rmv_aug_icon = QtGui.QIcon(self.rmv_aug_img)
        self.rmv_aug_button = QtWidgets.QPushButton(self)
        self.rmv_aug_button.setGeometry(550, 108, 35, 35)
        self.rmv_aug_button.setIcon(self.rmv_aug_icon)
        self.rmv_aug_button.setIconSize(QtCore.QSize(25,25))
        self.rmv_aug_button.clicked.connect(self.removeAug)
        # setup aug views
        self.setupHorFlipView()
        self.setupMotionBlurView()
        self.setupIsoNoiseView()
        self.setupRotateView()
        self.setupCutOutView()
        self.setupCropView()
        self.setupRgbView()
        self.updateUi()
        # save and exit
        self.save_exit_button = QtWidgets.QPushButton(self)
        self.save_exit_button.setText('Done')
        self.save_exit_button.setGeometry(470, 450, 100, 30)


    def saveExit(self): # TO BE IMPLEMENTED
        pass


    def saveImagePercent(self):
        self.img_percent = self.image_percent_box.value()


    def updateName(self, new_name):
        self.name = new_name
        if new_name == '':
            self.name = self.default_name
        self.setWindowTitle('{} Configuration'.format(self.name))


    def updateUi(self):
        selected_aug = self.aug_combo_box.currentIndex()

        if self.aug_oneh[self.prev_aug]:
            if self.prev_aug == 0 and self.prev_aug != selected_aug: self.hf_param_form.setVisible(False)
            elif self.prev_aug == 1 and self.prev_aug != selected_aug: self.mb_param_form.setVisible(False) 
            elif self.prev_aug == 2 and self.prev_aug != selected_aug: self.iso_param_form.setVisible(False)
            elif self.prev_aug == 3 and self.prev_aug != selected_aug: self.rot_param_form.setVisible(False)
            elif self.prev_aug == 4 and self.prev_aug != selected_aug: self.cut_param_form.setVisible(False)
            elif self.prev_aug == 5 and self.prev_aug != selected_aug: self.crop_param_form.setVisible(False)
            elif self.prev_aug != selected_aug: self.rgb_param_form.setVisible(False)

        if self.aug_oneh[selected_aug] == False: # enable/disable add button
            self.add_aug_button.setEnabled(True)
            self.prev_aug = selected_aug
            return
        else:
            self.add_aug_button.setEnabled(False)

        if selected_aug == 0: # horizontal flip
            self.hf_prob_box.setValue(self.aug_param[0].p)
            self.hf_param_form.setVisible(True)  

        elif selected_aug == 1: # motion blur
            self.mb_true_box.setChecked(self.aug_param[1].always_apply)
            self.mb_prob_box.setValue(self.aug_param[1].p)
            self.mb_blur_upper_box.setValue(self.aug_param[1].blur_limit[1])
            self.mb_blur_lower_box.setValue(self.aug_param[1].blur_limit[0])
            self.mb_param_form.setVisible(True)

        elif selected_aug == 2: # iso noise
            self.iso_true_box.setChecked(self.aug_param[2].always_apply)
            self.iso_prob_box.setProperty('value', self.aug_param[2].p)
            self.iso_intensity_lower_box.setProperty('value', self.aug_param[2].intensity[0])
            self.iso_intensity_upper_box.setProperty('value', self.aug_param[2].intensity[1])
            self.iso_color_lower_box.setProperty('value', self.aug_param[2].color_shift[0])
            self.iso_color_upper_box.setProperty('value', self.aug_param[2].color_shift[1])
            self.iso_param_form.setVisible(True)

        elif selected_aug == 3: # rotate
            self.rot_angle_lower_box.setProperty('value', self.aug_param[3].limit[0])
            self.rot_angle_upper_box.setProperty('value', self.aug_param[3].limit[1])
            self.rot_intp_combo.setProperty('value', self.aug_param[3].interpolation)
            self.rot_border_combo.setProperty('value', self.aug_param[3].border_mode)
            self.rot_red_var_box.setProperty('value', self.aug_param[3].value[0])
            self.rot_blue_var_box.setProperty('value', self.aug_param[3].value[1])
            if self.aug_param[3].border_mode != 0: self.rot_red_var_box.setEnabled(False)
            if self.aug_param[3].border_mode != 0: self.rot_blue_var_box.setEnabled(False)
            if self.aug_param[3].border_mode != 0: self.rot_green_var_box.setEnabled(False)
            self.rot_green_var_box.setProperty('value', self.aug_param[3].value[2])
            self.rot_true_box.setChecked(self.aug_param[3].always_apply)
            self.rot_prob_box.setProperty('value', self.aug_param[3].p)
            self.rot_param_form.setVisible(True)

        elif selected_aug == 4: # cutout
            self.cut_true_box.setChecked(self.aug_param[4].always_apply)
            self.cut_prob_box.setProperty('value', self.aug_param[4].p)
            self.numholes_box.setProperty('value', self.aug_param[4].num_holes)
            self.maxh_box.setProperty('value', self.aug_param[4].max_h_size)
            self.maxw_box.setProperty('value', self.aug_param[4].max_w_size)
            self.cut_param_form.setVisible(True)

        elif selected_aug == 5: # crop
            self.crop_true_box.setChecked(self.aug_param[5].always_apply)
            self.crop_prob_box.setProperty('value', self.aug_param[5].p)
            self.xmin_box.setProperty('value', self.aug_param[5].x_min)
            self.xmax_box.setProperty('value', self.aug_param[5].x_max)
            self.ymin_box.setProperty('value', self.aug_param[5].y_min)
            self.ymax_box.setProperty('value', self.aug_param[5].y_max)
            self.crop_param_form.setVisible(True)

        else: # rgb shift
            self.rgb_true_box.setChecked(self.aug_param[6].always_apply)
            self.rgb_prob_box.setProperty('value', self.aug_param[6].p)
            self.red_shift_lower_box.setProperty('value', self.aug_param[6].r_shift_limit[0])
            self.red_shift_upper_box.setProperty('value', self.aug_param[6].r_shift_limit[1])
            self.green_shift_lower_box.setProperty('value', self.aug_param[6].g_shift_limit[0])
            self.green_shift_upper_box.setProperty('value', self.aug_param[6].g_shift_limit[1])
            self.blue_shift_lower_box.setProperty('value', self.aug_param[6].b_shift_limit[0])
            self.blue_shift_upper_box.setProperty('value', self.aug_param[6].b_shift_limit[1])
            self.rgb_param_form.setVisible(True)

        self.prev_aug = selected_aug


    def addAug(self):
        selected_aug = self.aug_combo_box.currentIndex()
        self.aug_oneh[selected_aug] = True
        self.prev_aug = selected_aug

        if selected_aug == 0: # horizontal flip
            self.hf_param_form.setVisible(True)

        elif selected_aug == 1: # motion blur
            self.mb_param_form.setVisible(True)

        elif selected_aug == 2: # iso noise
            self.iso_param_form.setVisible(True)

        elif selected_aug == 3: # rotate
            self.rot_param_form.setVisible(True)

        elif selected_aug == 4: # cutout
            self.cut_param_form.setVisible(True)

        elif selected_aug == 5: # crop
            self.crop_param_form.setVisible(True)

        else: # rgb shift
            self.rgb_param_form.setVisible(True)
            
        self.add_aug_button.setEnabled(False)


    def removeAug(self):
        selected_aug = self.aug_combo_box.currentIndex()

        if self.aug_oneh[selected_aug] == False: return

        self.aug_oneh[selected_aug] = False
        self.add_aug_button.setEnabled(True)

        if selected_aug == 0: # horizontal flip
            self.aug_param[0].setDefault()
            self.hf_prob_box.setValue(self.aug_param[1].p)
            self.hf_param_form.setVisible(False)

        elif selected_aug == 1: # motion blur
            self.aug_param[1].setDefault()
            self.mb_true_box.setChecked(self.aug_param[1].always_apply)
            self.mb_prob_box.setValue(self.aug_param[1].p)
            self.mb_blur_lower_box.setValue(self.aug_param[1].blur_limit[0])
            self.mb_blur_upper_box.setValue(self.aug_param[1].blur_limit[1])
            self.mb_param_form.setVisible(False)

        elif selected_aug == 2: # iso noise
            self.aug_param[2].setDefault()
            self.iso_true_box.setChecked(self.aug_param[2].always_apply)
            self.iso_prob_box.setProperty('value', self.aug_param[2].p)
            self.iso_intensity_lower_box.setProperty('value', self.aug_param[2].intensity[0])
            self.iso_intensity_upper_box.setProperty('value', self.aug_param[2].intensity[1])
            self.iso_color_lower_box.setProperty('value', self.aug_param[2].color_shift[0])
            self.iso_color_upper_box.setProperty('value', self.aug_param[2].color_shift[1])
            self.iso_param_form.setVisible(False)

        elif selected_aug == 3: # rotate
            self.aug_param[3].setDefault()
            self.rot_angle_lower_box.setProperty('value', self.aug_param[3].limit[0])
            self.rot_angle_upper_box.setProperty('value', self.aug_param[3].limit[1])
            self.rot_intp_combo.setProperty('value', self.aug_param[3].interpolation)
            self.rot_border_combo.setProperty('value', self.aug_param[3].border_mode)
            self.rot_red_var_box.setProperty('value', self.aug_param[3].value[0])
            if self.aug_param[3].border_mode != 0: self.rot_red_var_box.setEnabled(False)
            self.rot_blue_var_box.setProperty('value', self.aug_param[3].value[1])
            if self.aug_param[3].border_mode != 0: self.rot_blue_var_box.setEnabled(False)
            self.rot_green_var_box.setProperty('value', self.aug_param[3].value[2])
            if self.aug_param[3].border_mode != 0: self.rot_green_var_box.setEnabled(False)
            self.rot_true_box.setChecked(self.aug_param[3].always_apply)
            self.rot_prob_box.setProperty('value', self.aug_param[3].p)
            self.rot_param_form.setVisible(False)

        elif selected_aug == 4: # cutout
            self.aug_param[4].setDefault()
            self.cut_true_box.setChecked(self.aug_param[4].always_apply)
            self.cut_prob_box.setProperty('value', self.aug_param[4].p)
            self.numholes_box.setProperty('value', self.aug_param[4].num_holes)
            self.maxh_box.setProperty('value', self.aug_param[4].max_h_size)
            self.maxw_box.setProperty('value', self.aug_param[4].max_w_size)
            self.cut_param_form.setVisible(False)

        elif selected_aug == 5: # crop
            self.aug_param[5].setDefault()
            self.crop_true_box.setChecked(self.aug_param[5].always_apply)
            self.crop_prob_box.setProperty('value', self.aug_param[5].p)
            self.xmin_box.setProperty('value', self.aug_param[5].x_min)
            self.xmax_box.setProperty('value', self.aug_param[5].x_max)
            self.ymin_box.setProperty('value', self.aug_param[5].y_min)
            self.ymax_box.setProperty('value', self.aug_param[5].y_max)
            self.crop_param_form.setVisible(False)

        else: # rgb shift
            self.aug_param[6].setDefault()
            self.rgb_true_box.setChecked(self.aug_param[6].always_apply)
            self.rgb_prob_box.setProperty('value', self.aug_param[6].p)
            self.red_shift_lower_box.setProperty('value', self.aug_param[6].r_shift_limit[0])
            self.red_shift_upper_box.setProperty('value', self.aug_param[6].r_shift_limit[1])
            self.green_shift_lower_box.setProperty('value', self.aug_param[6].g_shift_limit[0])
            self.green_shift_upper_box.setProperty('value', self.aug_param[6].g_shift_limit[1])
            self.blue_shift_lower_box.setProperty('value', self.aug_param[6].b_shift_limit[0])
            self.blue_shift_upper_box.setProperty('value', self.aug_param[6].b_shift_limit[1])
            self.rgb_param_form.setVisible(False)           


    #################################### Horizontal Flip ###############################################

    def setupHorFlipView(self):
        self.hf_param_form = QtWidgets.QWidget(self)
        self.hf_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.hf_param_form_layout = QtWidgets.QFormLayout(self.hf_param_form)
        self.hf_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.hf_prob_label = QtWidgets.QLabel(self.hf_param_form)
        self.hf_prob_label.setText('Probability (unit interval): ')
        self.hf_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.hf_prob_label)
        self.hf_prob_box = QtWidgets.QDoubleSpinBox(self.hf_param_form)
        self.hf_prob_box.setMaximum(1.0)
        self.hf_prob_box.setSingleStep(0.01)
        self.hf_prob_box.setValue(ac.HorizontalFlipParams().p)
        self.hf_prob_box.valueChanged.connect(self.setHorFlipProb)

        self.hf_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.hf_prob_box)
        self.hf_param_form.setVisible(False)


    def setHorFlipProb(self): self.aug_param[0].p = self.hf_prob_box.value()


    #################################### Motion Blur ####################################################
    
    def setupMotionBlurView(self):
        mb = ac.MotionBlurParams()
            
        self.mb_param_form = QtWidgets.QWidget(self)
        self.mb_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.mb_param_form_layout = QtWidgets.QFormLayout(self.mb_param_form)
        self.mb_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.mb_true_box_label = QtWidgets.QLabel(self.mb_param_form)
        self.mb_true_box_label.setText('Always Apply:')
        self.mb_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.mb_true_box_label)
        self.mb_true_box = QtWidgets.QCheckBox(self.mb_param_form)
        self.mb_true_box.setChecked(mb.always_apply)
        self.mb_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mb_true_box)
        self.mb_true_box.stateChanged.connect(self.setMotionBlurApply)

        self.mb_prob_label = QtWidgets.QLabel(self.mb_param_form)
        self.mb_prob_label.setText('Probability (unit interval): ')
        self.mb_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.mb_prob_label)
        self.mb_prob_box = QtWidgets.QDoubleSpinBox(self.mb_param_form)
        self.mb_prob_box.setMaximum(1.0)
        self.mb_prob_box.setSingleStep(0.01)
        self.mb_prob_box.setValue(mb.p)
        self.mb_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.mb_prob_box)
        self.mb_prob_box.valueChanged.connect(self.setMotionBlurProb)

        self.mb_blur_lower_label = QtWidgets.QLabel(self.mb_param_form)
        self.mb_blur_lower_label.setText('Blur Lower Limit:')
        self.mb_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.mb_blur_lower_label)
        self.mb_blur_lower_box = QtWidgets.QSpinBox(self.mb_param_form)
        self.mb_blur_lower_box.setMinimum(3)
        self.mb_blur_lower_box.setMaximum(100)
        self.mb_blur_lower_box.setValue(mb.blur_limit[0])
        self.mb_blur_lower_box.valueChanged.connect(self.setMotionBlurLowerLimit)
        self.mb_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.mb_blur_lower_box)

        self.mb_blur_upper_label = QtWidgets.QLabel(self.mb_param_form)
        self.mb_blur_upper_label.setText('Blur Upper Limit:')
        self.mb_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.mb_blur_upper_label)
        self.mb_blur_upper_box = QtWidgets.QSpinBox(self.mb_param_form)
        self.mb_blur_upper_box.setMinimum(3)
        self.mb_blur_upper_box.setMaximum(100)
        self.mb_blur_upper_box.setValue(mb.blur_limit[1])
        self.mb_blur_upper_box.valueChanged.connect(self.setMotionBlurUpperLimit)
        self.mb_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.mb_blur_upper_box)

        self.mb_param_form.setVisible(False)


    def setMotionBlurApply(self): self.aug_param[1].always_apply = self.mb_true_box.isChecked()


    def setMotionBlurProb(self): self.aug_param[1].p = self.mb_prob_box.value()


    def setMotionBlurLowerLimit(self): self.aug_param[1].blur_limit[0] = self.mb_blur_lower_box.value()


    def setMotionBlurUpperLimit(self): self.aug_param[1].blur_limit[1] = self.mb_blur_upper_box.value()


    #################################### Iso Noise #####################################################

    def setupIsoNoiseView(self):
        iso = ac.IsoNoiseParams()

        self.iso_param_form = QtWidgets.QWidget(self)
        self.iso_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.iso_param_form_layout = QtWidgets.QFormLayout(self.iso_param_form)
        self.iso_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.iso_true_box_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_true_box_label.setText('Always Apply:')
        self.iso_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.iso_true_box_label)
        self.iso_true_box = QtWidgets.QCheckBox(self.iso_param_form)
        self.iso_true_box.setChecked(iso.always_apply)
        self.iso_true_box.stateChanged.connect(self.setIsoNoiseApply)
        self.iso_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.iso_true_box)

        self.iso_prob_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_prob_label.setText('Probability (unit interval): ')
        self.iso_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.iso_prob_label)
        self.iso_prob_box = QtWidgets.QDoubleSpinBox(self.iso_param_form)
        self.iso_prob_box.setMaximum(1.0)
        self.iso_prob_box.setMinimum(0.0)
        self.iso_prob_box.setSingleStep(0.01)
        self.iso_prob_box.setProperty('value', iso.p)
        self.iso_prob_box.valueChanged.connect(self.setIsoNoiseProb)
        self.iso_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.iso_prob_box)

        self.iso_intensity_lower_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_intensity_lower_label.setText('Intensity Lower Limit:')
        self.iso_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.iso_intensity_lower_label)
        self.iso_intensity_lower_box = QtWidgets.QDoubleSpinBox(self.iso_param_form)
        self.iso_intensity_lower_box.setMaximum(1.0)
        self.iso_intensity_lower_box.setMinimum(0.0)
        self.iso_intensity_lower_box.setSingleStep(0.01)
        self.iso_intensity_lower_box.setProperty('value', iso.intensity[0])
        self.iso_intensity_lower_box.valueChanged.connect(self.setIsoNoiseLowerIntensity)
        self.iso_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.iso_intensity_lower_box)
        
        self.iso_intensity_upper_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_intensity_upper_label.setText('Intensity Upper Limit:')
        self.iso_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.iso_intensity_upper_label)
        self.iso_intensity_upper_box = QtWidgets.QDoubleSpinBox(self.iso_param_form)
        self.iso_intensity_upper_box.setMaximum(1.0)
        self.iso_intensity_upper_box.setMinimum(0.0)
        self.iso_intensity_upper_box.setSingleStep(0.01)
        self.iso_intensity_upper_box.setProperty('value', iso.intensity[1])
        self.iso_intensity_upper_box.valueChanged.connect(self.setIsoNoiseUpperIntensity)
        self.iso_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.iso_intensity_upper_box)

        self.iso_color_lower_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_color_lower_label.setText('Color Shift Lower Limit:')
        self.iso_param_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.iso_color_lower_label)
        self.iso_color_lower_box = QtWidgets.QDoubleSpinBox(self.iso_param_form)
        self.iso_color_lower_box.setMaximum(1.0)
        self.iso_color_lower_box.setMinimum(0.0)
        self.iso_color_lower_box.setSingleStep(0.01)
        self.iso_color_lower_box.setProperty('value', iso.color_shift[0])
        self.iso_color_lower_box.valueChanged.connect(self.setIsoNoiseLowerColorShift)
        self.iso_param_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.iso_color_lower_box)

        self.iso_color_upper_label = QtWidgets.QLabel(self.iso_param_form)
        self.iso_color_upper_label.setText('Color Shift Upper Limit:')
        self.iso_param_form_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.iso_color_upper_label)
        self.iso_color_upper_box = QtWidgets.QDoubleSpinBox(self.iso_param_form)
        self.iso_color_upper_box.setMaximum(1.0)
        self.iso_color_upper_box.setMinimum(0.0)
        self.iso_color_upper_box.setSingleStep(0.01)
        self.iso_color_upper_box.setProperty('value', iso.color_shift[1])
        self.iso_color_upper_box.valueChanged.connect(self.setIsoNoiseUpperColorShift)
        self.iso_param_form_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.iso_color_upper_box)

        self.iso_param_form.setVisible(False)

    
    def setIsoNoiseApply(self): self.aug_param[2].always_apply = self.iso_true_box.isChecked()


    def setIsoNoiseProb(self): self.aug_param[2].p = self.iso_prob_box.value()


    def setIsoNoiseLowerIntensity(self): self.aug_param[2].intensity[0] = self.iso_intensity_lower_box.value()


    def setIsoNoiseUpperIntensity(self): self.aug_param[2].intensity[1] = self.iso_intensity_upper_box.value()


    def setIsoNoiseLowerColorShift(self): self.aug_param[2].color_shift[0] = self.iso_color_lower_box.value()


    def setIsoNoiseUpperColorShift(self): self.aug_param[2].color_shift[1] = self.iso_color_upper_box.value()


    #################################### Rotate #####################################################

    def setupRotateView(self):
        rot = ac.RotateParams()

        self.rot_param_form = QtWidgets.QWidget(self)
        self.rot_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.rot_param_form_layout = QtWidgets.QFormLayout(self.rot_param_form)
        self.rot_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.rot_true_box_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_true_box_label.setText('Always Apply:')
        self.rot_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rot_true_box_label)
        self.rot_true_box = QtWidgets.QCheckBox(self.rot_param_form)
        self.rot_true_box.setChecked(rot.always_apply)
        self.rot_true_box.stateChanged.connect(self.setRotateApply)
        self.rot_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rot_true_box)

        self.rot_prob_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_prob_label.setText('Probability (unit interval): ')
        self.rot_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rot_prob_label)
        self.rot_prob_box = QtWidgets.QDoubleSpinBox(self.rot_param_form)
        self.rot_prob_box.setMaximum(1.0)
        self.rot_prob_box.setMinimum(0.0)
        self.rot_prob_box.setSingleStep(0.01)
        self.rot_prob_box.setProperty('value', rot.p)
        self.rot_prob_box.valueChanged.connect(self.setRotateProb)
        self.rot_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rot_prob_box)

        self.rot_angle_lower_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_angle_lower_label.setText('Rotate Angle Lower Limit:')
        self.rot_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rot_angle_lower_label)
        self.rot_angle_lower_box = QtWidgets.QDoubleSpinBox(self.rot_param_form)
        self.rot_angle_lower_box.setMaximum(360)
        self.rot_angle_lower_box.setMinimum(-360)
        self.rot_angle_lower_box.setSingleStep(1)
        self.rot_angle_lower_box.setProperty('value', rot.limit[0])
        self.rot_angle_lower_box.valueChanged.connect(self.setRotateLowerLimit)
        self.rot_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rot_angle_lower_box)
        
        self.rot_angle_upper_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_angle_upper_label.setText('Rotate Angle Upper Limit:')
        self.rot_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.rot_angle_upper_label)
        self.rot_angle_upper_box = QtWidgets.QDoubleSpinBox(self.rot_param_form)
        self.rot_angle_upper_box.setMaximum(360)
        self.rot_angle_upper_box.setMinimum(-360)
        self.rot_angle_upper_box.setSingleStep(0.01)
        self.rot_angle_upper_box.setProperty('value', rot.limit[1])
        self.rot_angle_upper_box.valueChanged.connect(self.setRotateUpperLimit)
        self.rot_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rot_angle_upper_box)

        self.rot_intp_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_intp_label.setText('Interpolation:')
        self.rot_param_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.rot_intp_label)
        self.rot_intp_combo = QtWidgets.QComboBox(self.rot_param_form)
        for opt in ['0', '1', '2', '3', '4']: self.rot_intp_combo.addItem(opt)
        self.rot_intp_combo.setProperty('value', rot.interpolation)
        self.rot_intp_combo.currentIndexChanged.connect(self.setRotateInter)
        self.rot_param_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.rot_intp_combo)

        self.rot_border_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_border_label.setText('Border Mode:')
        self.rot_param_form_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rot_border_label)
        self.rot_border_combo = QtWidgets.QComboBox(self.rot_param_form)
        for opt in ['0', '1', '2', '3', '4']: self.rot_border_combo.addItem(opt)
        self.rot_border_combo.setProperty('value', rot.border_mode)
        self.rot_border_combo.currentIndexChanged.connect(self.setRotateBorderMode)
        self.rot_param_form_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.rot_border_combo)

        self.rot_red_val_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_red_val_label.setText('Red Padding Value:')
        self.rot_param_form_layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.rot_red_val_label)
        self.rot_red_var_box = QtWidgets.QSpinBox(self.rot_param_form)
        self.rot_red_var_box.setMaximum(255)
        self.rot_red_var_box.setMinimum(0)
        self.rot_red_var_box.setSingleStep(1)
        self.rot_red_var_box.setProperty('value', rot.value[0])
        if rot.border_mode != 0: self.rot_red_var_box.setEnabled(False)
        self.rot_red_var_box.valueChanged.connect(self.setRotateRedValue)
        self.rot_param_form_layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.rot_red_var_box)

        self.rot_blue_val_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_blue_val_label.setText('Blue Padding Value:')
        self.rot_param_form_layout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.rot_blue_val_label)
        self.rot_blue_var_box = QtWidgets.QSpinBox(self.rot_param_form)
        self.rot_blue_var_box.setMaximum(255)
        self.rot_blue_var_box.setMinimum(0)
        self.rot_blue_var_box.setSingleStep(1)
        self.rot_blue_var_box.setProperty('value', rot.value[1])
        if rot.border_mode != 0: self.rot_blue_var_box.setEnabled(False)
        self.rot_blue_var_box.valueChanged.connect(self.setRotateBlueValue)
        self.rot_param_form_layout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.rot_blue_var_box)

        self.rot_green_val_label = QtWidgets.QLabel(self.rot_param_form)
        self.rot_green_val_label.setText('Green Padding Value:')
        self.rot_param_form_layout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.rot_green_val_label)
        self.rot_green_var_box = QtWidgets.QSpinBox(self.rot_param_form)
        self.rot_green_var_box.setMaximum(255)
        self.rot_green_var_box.setMinimum(0)
        self.rot_green_var_box.setSingleStep(1)
        self.rot_green_var_box.setProperty('value', rot.value[2])
        if rot.border_mode != 0: self.rot_green_var_box.setEnabled(False)
        self.rot_green_var_box.valueChanged.connect(self.setRotateGreenValue)
        self.rot_param_form_layout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.rot_green_var_box)

        self.rot_param_form.setVisible(False)


    def setRotateApply(self): self.aug_param[3].always_apply = self.rot_true_box.isChecked()


    def setRotateProb(self): self.aug_param[3].p = self.rot_prob_box.value()


    def setRotateLowerLimit(self): self.aug_param[3].limit[0] = self.rot_angle_lower_box.value()


    def setRotateUpperLimit(self): self.aug_param[3].limit[1] = self.rot_angle_upper_box.value()


    def setRotateInter(self): self.aug_param[3].interpolation = self.rot_intp_combo.currentIndex()


    def setRotateBorderMode(self): 
        self.aug_param[3].border_mode = self.rot_border_combo.currentIndex()
        if self.aug_param[3].border_mode != 0: self.rot_red_var_box.setEnabled(False)
        if self.aug_param[3].border_mode != 0: self.rot_blue_var_box.setEnabled(False)
        if self.aug_param[3].border_mode != 0: self.rot_green_var_box.setEnabled(False)


    def setRotateRedValue(self): self.aug_param[3].value[0] = self.rot_red_var_box.value()

    
    def setRotateGreenValue(self): self.aug_param[3].value[1] = self.rot_green_var_box.value()


    def setRotateBlueValue(self): self.aug_param[3].value[2] = self.rot_blue_var_box.value()


    #################################### Cut Out #####################################################

    def setupCutOutView(self):
        cut = ac.CutOutParams()

        self.cut_param_form = QtWidgets.QWidget(self)
        self.cut_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.cut_param_form_layout = QtWidgets.QFormLayout(self.cut_param_form)
        self.cut_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.cut_true_box_label = QtWidgets.QLabel(self.cut_param_form)
        self.cut_true_box_label.setText('Always Apply:')
        self.cut_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.cut_true_box_label)
        self.cut_true_box = QtWidgets.QCheckBox(self.cut_param_form)
        self.cut_true_box.setChecked(cut.always_apply)
        self.cut_true_box.stateChanged.connect(self.setCutOutApply)
        self.cut_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cut_true_box)

        self.cut_prob_label = QtWidgets.QLabel(self.cut_param_form)
        self.cut_prob_label.setText('Probability (unit interval): ')
        self.cut_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cut_prob_label)
        self.cut_prob_box = QtWidgets.QDoubleSpinBox(self.cut_param_form)
        self.cut_prob_box.setMaximum(1.0)
        self.cut_prob_box.setMinimum(0.0)
        self.cut_prob_box.setSingleStep(0.01)
        self.cut_prob_box.setProperty('value', cut.p)
        self.cut_prob_box.valueChanged.connect(self.setCutOutProb)
        self.cut_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cut_prob_box)

        self.numholes_label = QtWidgets.QLabel(self.cut_param_form)
        self.numholes_label.setText('Number of Holes:')
        self.cut_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.numholes_label)
        self.numholes_box = QtWidgets.QSpinBox(self.cut_param_form)
        self.numholes_box.setMaximum(100)
        self.numholes_box.setMinimum(1)
        self.numholes_box.setSingleStep(1)
        self.numholes_box.setProperty('value', cut.num_holes)
        self.numholes_box.valueChanged.connect(self.setCutOutNumHoles)
        self.cut_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.numholes_box)

        self.maxh_label = QtWidgets.QLabel(self.cut_param_form)
        self.maxh_label.setText('Maximum Height:')
        self.cut_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.maxh_label)
        self.maxh_box = QtWidgets.QSpinBox(self.cut_param_form)
        self.maxh_box.setMaximum(100)
        self.maxh_box.setMinimum(1)
        self.maxh_box.setSingleStep(1)
        self.maxh_box.setProperty('value', cut.max_h_size)
        self.maxh_box.valueChanged.connect(self.setCutOutMaxH)
        self.cut_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.maxh_box)

        self.maxw_label = QtWidgets.QLabel(self.cut_param_form)
        self.maxw_label.setText('Maximum Width:')
        self.cut_param_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.maxw_label)
        self.maxw_box = QtWidgets.QSpinBox(self.cut_param_form)
        self.maxw_box.setMaximum(100)
        self.maxw_box.setMinimum(1)
        self.maxw_box.setSingleStep(1)
        self.maxw_box.setProperty('value', cut.max_w_size)
        self.maxw_box.valueChanged.connect(self.setCutOutMaxW)
        self.cut_param_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.maxw_box)

        self.cut_param_form.setVisible(False)

    
    def setCutOutApply(self): self.aug_param[4].always_apply = self.cut_true_box.isChecked()


    def setCutOutProb(self): self.aug_param[4].p = self.cut_prob_box.value()


    def setCutOutNumHoles(self): self.aug_param[4].num_holes = self.numholes_box.value()


    def setCutOutMaxH(self): self.aug_param[4].max_h_size = self.maxh_box.value()


    def setCutOutMaxW(self): self.aug_param[4].max_w_size = self.maxw_box.value()


    #################################### Crop #####################################################

    def setupCropView(self):
        crop = ac.CropParams()

        self.crop_param_form = QtWidgets.QWidget(self)
        self.crop_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.crop_param_form_layout = QtWidgets.QFormLayout(self.crop_param_form)
        self.crop_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.crop_true_box_label = QtWidgets.QLabel(self.crop_param_form)
        self.crop_true_box_label.setText('Always Apply:')
        self.crop_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.crop_true_box_label)
        self.crop_true_box = QtWidgets.QCheckBox(self.crop_param_form)
        self.crop_true_box.setChecked(crop.always_apply)
        self.crop_true_box.stateChanged.connect(self.setCropApply)
        self.crop_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.crop_true_box)

        self.crop_prob_label = QtWidgets.QLabel(self.crop_param_form)
        self.crop_prob_label.setText('Probability (unit interval): ')
        self.crop_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.crop_prob_label)
        self.crop_prob_box = QtWidgets.QDoubleSpinBox(self.crop_param_form)
        self.crop_prob_box.setMaximum(1.0)
        self.crop_prob_box.setMinimum(0.0)
        self.crop_prob_box.setSingleStep(0.01)
        self.crop_prob_box.setProperty('value', crop.p)
        self.crop_prob_box.valueChanged.connect(self.setCropProb)
        self.crop_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.crop_prob_box)

        self.xmin_label = QtWidgets.QLabel(self.crop_param_form)
        self.xmin_label.setText('xmin:')
        self.crop_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.xmin_label)
        self.xmin_box = QtWidgets.QSpinBox(self.crop_param_form)
        self.xmin_box.setMaximum(1000)
        self.xmin_box.setMinimum(0)
        self.xmin_box.setSingleStep(1)
        self.xmin_box.setProperty('value', crop.x_min)
        self.xmin_box.valueChanged.connect(self.setCropXmin)
        self.crop_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.xmin_box)

        self.xmax_label = QtWidgets.QLabel(self.crop_param_form)
        self.xmax_label.setText('xmax:')
        self.crop_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.xmax_label)
        self.xmax_box = QtWidgets.QSpinBox(self.crop_param_form)
        self.xmax_box.setMaximum(1000)
        self.xmax_box.setMinimum(0)
        self.xmax_box.setSingleStep(1)
        self.xmax_box.setProperty('value', crop.x_max)
        self.xmax_box.valueChanged.connect(self.setCropXmax)
        self.crop_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.xmax_box)

        self.ymin_label = QtWidgets.QLabel(self.crop_param_form)
        self.ymin_label.setText('ymin:')
        self.crop_param_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.ymin_label)
        self.ymin_box = QtWidgets.QSpinBox(self.crop_param_form)
        self.ymin_box.setMaximum(1000)
        self.ymin_box.setMinimum(0)
        self.ymin_box.setSingleStep(1)
        self.ymin_box.setProperty('value', crop.y_min)
        self.ymin_box.valueChanged.connect(self.setCropYmin)
        self.crop_param_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ymin_box)

        self.ymax_label = QtWidgets.QLabel(self.crop_param_form)
        self.ymax_label.setText('ymax:')
        self.crop_param_form_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.ymax_label)
        self.ymax_box = QtWidgets.QSpinBox(self.crop_param_form)
        self.ymax_box.setMaximum(1000)
        self.ymax_box.setMinimum(0)
        self.ymax_box.setSingleStep(1)
        self.ymax_box.setProperty('value', crop.y_max)
        self.ymax_box.valueChanged.connect(self.setCropYmax)
        self.crop_param_form_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ymax_box)

        self.crop_param_form.setVisible(False)


    def setCropApply(self): self.aug_param[5].always_apply = self.crop_true_box.isChecked()


    def setCropProb(self): self.aug_param[5].p = self.crop_prob_box.value()


    def setCropXmin(self): self.aug_param[5].x_min = self.xmin_box.value()


    def setCropXmax(self): self.aug_param[5].x_max = self.xmax_box.value()


    def setCropYmin(self): self.aug_param[5].y_min = self.ymin_box.value()


    def setCropYmax(self): self.aug_param[5].y_max = self.ymax_box.value()


    #################################### Rgb Shift ####################################################

    def setupRgbView(self):
        rgb = ac.RgbShiftParams()

        self.rgb_param_form = QtWidgets.QWidget(self)
        self.rgb_param_form.setGeometry(QtCore.QRect(20, 155, 300, 350))

        self.rgb_param_form_layout = QtWidgets.QFormLayout(self.rgb_param_form)
        self.rgb_param_form_layout.setContentsMargins(0, 0, 0, 0)

        self.rgb_true_box_label = QtWidgets.QLabel(self.rgb_param_form)
        self.rgb_true_box_label.setText('Always Apply:')
        self.rgb_param_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rgb_true_box_label)
        self.rgb_true_box = QtWidgets.QCheckBox(self.rgb_param_form)
        self.rgb_true_box.setChecked(rgb.always_apply)
        self.rgb_true_box.stateChanged.connect(self.setRgbApply)
        self.rgb_param_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rgb_true_box)

        self.rgb_prob_label = QtWidgets.QLabel(self.rgb_param_form)
        self.rgb_prob_label.setText('Probability (unit interval): ')
        self.rgb_param_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rgb_prob_label)
        self.rgb_prob_box = QtWidgets.QDoubleSpinBox(self.rgb_param_form)
        self.rgb_prob_box.setMaximum(1.0)
        self.rgb_prob_box.setMinimum(0.0)
        self.rgb_prob_box.setSingleStep(0.01)
        self.rgb_prob_box.setProperty('value', rgb.p)
        self.rgb_prob_box.valueChanged.connect(self.setRgbProb)
        self.rgb_param_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rgb_prob_box)

        self.red_shift_lower_label = QtWidgets.QLabel(self.rgb_param_form)
        self.red_shift_lower_label.setText('Lower Red Shift Limit:')
        self.rgb_param_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.red_shift_lower_label)
        self.red_shift_lower_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.red_shift_lower_box.setMaximum(255)
        self.red_shift_lower_box.setMinimum(-255)
        self.red_shift_lower_box.setSingleStep(1)
        self.red_shift_lower_box.setProperty('value', rgb.r_shift_limit[0])
        self.red_shift_lower_box.valueChanged.connect(self.setRedShiftLower)
        self.rgb_param_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.red_shift_lower_box)

        self.red_shift_upper_label = QtWidgets.QLabel(self.rgb_param_form)
        self.red_shift_upper_label.setText('Upper Red Shift Limit:')
        self.rgb_param_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.red_shift_upper_label)
        self.red_shift_upper_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.red_shift_upper_box.setMaximum(255)
        self.red_shift_upper_box.setMinimum(-255)
        self.red_shift_upper_box.setSingleStep(1)
        self.red_shift_upper_box.setProperty('value', rgb.r_shift_limit[1])
        self.red_shift_upper_box.valueChanged.connect(self.setRedShiftUpper)
        self.rgb_param_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.red_shift_upper_box)

        self.green_shift_lower_label = QtWidgets.QLabel(self.rgb_param_form)
        self.green_shift_lower_label.setText('Lower Green Shift Limit:')
        self.rgb_param_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.green_shift_lower_label)
        self.green_shift_lower_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.green_shift_lower_box.setMaximum(255)
        self.green_shift_lower_box.setMinimum(-255)
        self.green_shift_lower_box.setSingleStep(1)
        self.green_shift_lower_box.setProperty('value', rgb.g_shift_limit[0])
        self.green_shift_lower_box.valueChanged.connect(self.setGreenShiftLower)
        self.rgb_param_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.green_shift_lower_box)
        
        self.green_shift_upper_label = QtWidgets.QLabel(self.rgb_param_form)
        self.green_shift_upper_label.setText('Upper Green Shift Limit:')
        self.rgb_param_form_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.green_shift_upper_label)
        self.green_shift_upper_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.green_shift_upper_box.setMaximum(255)
        self.green_shift_upper_box.setMinimum(-255)
        self.green_shift_upper_box.setSingleStep(1)
        self.green_shift_upper_box.setProperty('value', rgb.g_shift_limit[1])
        self.green_shift_upper_box.valueChanged.connect(self.setGreenShiftUpper)
        self.rgb_param_form_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.green_shift_upper_box)

        self.blue_shift_lower_label = QtWidgets.QLabel(self.rgb_param_form)
        self.blue_shift_lower_label.setText('Lower Blue Shift Limit:')
        self.rgb_param_form_layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.blue_shift_lower_label)
        self.blue_shift_lower_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.blue_shift_lower_box.setMaximum(255)
        self.blue_shift_lower_box.setMinimum(-255)
        self.blue_shift_lower_box.setSingleStep(1)
        self.blue_shift_lower_box.setProperty('value', rgb.b_shift_limit[0])
        self.blue_shift_lower_box.valueChanged.connect(self.setBlueShiftLower)
        self.rgb_param_form_layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.blue_shift_lower_box)
        
        self.blue_shift_upper_label = QtWidgets.QLabel(self.rgb_param_form)
        self.blue_shift_upper_label.setText('Upper Blue Shift Limit:')
        self.rgb_param_form_layout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.blue_shift_upper_label)
        self.blue_shift_upper_box = QtWidgets.QSpinBox(self.rgb_param_form)
        self.blue_shift_upper_box.setMaximum(255)
        self.blue_shift_upper_box.setMinimum(-255)
        self.blue_shift_upper_box.setSingleStep(1)
        self.blue_shift_upper_box.setProperty('value', rgb.b_shift_limit[1])
        self.blue_shift_upper_box.valueChanged.connect(self.setBlueShiftUpper)
        self.rgb_param_form_layout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.blue_shift_upper_box)

        self.rgb_param_form.setVisible(False)


    def setRgbApply(self): self.aug_param[6].always_apply = self.rgb_true_box.isChecked()


    def setRgbProb(self): self.aug_param[6].p = self.rgb_prob_box.value()


    def setRedShiftLower(self): self.aug_param[6].r_shift_limit[0] = self.red_shift_lower_box.value()


    def setRedShiftUpper(self): self.aug_param[6].r_shift_limit[1] = self.red_shift_upper_box.value()


    def setGreenShiftLower(self): self.aug_param[6].g_shift_limit[0] = self.green_shift_lower_box.value()


    def setGreenShiftUpper(self): self.aug_param[6].g_shift_limit[1] = self.green_shift_upper_box.value()


    def setBlueShiftLower(self): self.aug_param[6].b_shift_limit[0] = self.blue_shift_lower_box.value()


    def setBlueShiftUpper(self): self.aug_param[6].b_shift_limit[0] = self.blue_shift_upper_box.value()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle('Data Augmentation GUI')
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.pipeline_count = 0
        self.setupUi()
        self.pipeline_window_list = []


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
        # Set default label and checkbox
        self.default_label = QtWidgets.QLabel(self)
        self.default_label.setObjectName('default_label')
        self.default_label.setText('Load default pipelines')
        self.default_label.setGeometry(500, 178, 170, 30)
        self.default_checkbox = QtWidgets.QCheckBox(self)
        self.default_checkbox.setObjectName('default_checkbox')
        self.default_checkbox.setCheckState(False)
        self.default_checkbox.stateChanged.connect(lambda: self.setDefault() if (self.default_checkbox.isChecked()) else self.unsetDefault())
        self.default_checkbox.setGeometry(470, 180, 30, 30)
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
        self.pipeline_layout.itemClicked.connect(lambda: self.rmv_pipeline_button.setEnabled(True))
        self.pipeline_layout.itemDoubleClicked.connect(self.showPipelineWindow)


    def pickImgDir(self):
        exp = QtWidgets.QFileDialog()
        dir_path = exp.getExistingDirectory(None, "Select Directory")
        self.img_dir_disp.setText('{}'.format(dir_path))
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
        # TODO
        # add actual default pipelines
        # self.pipeline_window_list.append()


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


    def augmentImages(self):
        # TODO
        # Display summary of pipelines and their percentages in a message box
        self.close()


    def addPipeline(self):
        self.pipeline_count += 1
        pipeline_name = 'New pipeline {}'.format(self.pipeline_count)
        self.pipeline_layout.insertItem(self.pipeline_count, pipeline_name)
        self.pipeline_window_list.append(PipelineWindow(pipeline_name, self))


    def removePipeline(self):
        self.pipeline_count -= 1
        currentItemText = self.pipeline_layout.currentItem().text()
        currentItem = self.pipeline_layout.findItems(currentItemText, QtCore.Qt.MatchExactly)[0]
        currentItemRow = self.pipeline_layout.row(currentItem)
        self.pipeline_layout.takeItem(currentItemRow)
        # remove the assocated class with it


    def showPipelineWindow(self):
        pass


app = QApplication(sys.argv)
win = MainWindow()
win2 = PipelineWindow('sample', win)
# win.show()
win2.show()
sys.exit(app.exec_())