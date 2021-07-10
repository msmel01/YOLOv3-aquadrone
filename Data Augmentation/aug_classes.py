class HorizontalFlipParams():
    p = 1.0


class MotionBlurParams():
    always_apply = False
    p = 1.0
    blur_limit = (3, 7) # 3 - 100


class IsoNoiseParams():
    always_apply = False
    p = 1.0
    intensity = (0.1, 0.5) # 0 - 1
    color_shift = (0.01, 0.05) # 0 - 1


class RotateParams():
    always_apply = False
    p = 1.0
    limit = (-90, 90)
    interpolation = 0 # can be from 0 to 4
    border_mode = 0 # can be from 0 to 4
    value = (0, 0, 0) # 0 - 255 rgb
    mask_value = None


class CutOutParams():
    always_apply = False
    p = 1.0
    num_holes = 8 # 1 - 100
    max_h_size = 8 # 1 - 100
    max_w_size = 8 # 1 - 100


class CropParams():
    always_apply = False
    p = 1.0
    x_min = 0 # 0 - 320 for xmin and xmax
    y_min = 0 # 0 - 213 for ymin and ymax
    x_max = 160 
    y_max = 106


class RgbShiftParams():
    always_apply = False
    p = 1.0
    # can be from -255 to 255
    r_shift_limit = (-20, 20)
    g_shift_limit = (-20, 20)
    b_shift_limit = (-20, 20)