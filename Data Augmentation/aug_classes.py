class HorizontalFlipParams():
    def __init__(self):
        # self.p = 1.0
        self.setDefault()


    def setDefault(self):
        self.p = 1.0


class MotionBlurParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        self.blur_limit = [3, 7] # 3 - 100


class IsoNoiseParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        self.intensity = [0.1, 0.5] # 0 - 1
        self.color_shift = [0.01, 0.05] # 0 - 1


class RotateParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        self.limit = [-90, 90]
        self.interpolation = 0 # can be from 0 to 4
        self.border_mode = 0 # can be from 0 to 4
        self.value = [0, 0, 0] # 0 - 255 rgb
        self.mask_value = None



class CutOutParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        self.num_holes = 8 # 1 - 100
        self.max_h_size = 8 # 1 - 100
        self.max_w_size = 8 # 1 - 100


class CropParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        self.x_min = 0
        self.y_min = 0
        self.x_max = 160 
        self.y_max = 106


class RgbShiftParams():
    def __init__(self):
        self.setDefault()


    def setDefault(self):
        self.always_apply = False
        self.p = 1.0
        # can be from -255 to 255
        self.r_shift_limit = [-20, 20]
        self.g_shift_limit = [-20, 20]
        self.b_shift_limit = [-20, 20]