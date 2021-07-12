from os import pipe
import cv2
import albumentations as A
import argparse
import os.path
import aug_classes as ac

# TODO:
# experiment and find best values for the arguments
# add support for bounding boxes
# randomly sample images for data augmentation

class Augmentor():
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.pipelines = {}

    def createPipeline(self, pipeline_name, pipeline_config):
        print('Creating pipeline \'{}\''.format(pipeline_name))
        trans_list = []

        for i in range(7):
            if pipeline_config.aug_oneh[i] == False:
                continue

            if i == 0: # horizontal flip
                print('Add horizontal flip')
                trans_list.append(A.HorizontalFlip(always_apply=pipeline_config.aug_param[0].always_apply,
                                                   p=pipeline_config.aug_param[0].p))

            elif i == 1: # motion blur
                print('Add motion blur')
                bl = (pipeline_config.aug_param[1].blur_limit[0], pipeline_config.aug_param[1].blur_limit[1])
                trans_list.append(A.MotionBlur(always_apply=pipeline_config.aug_param[1].always_apply,
                                               p=pipeline_config.aug_param[1].p,
                                               blur_limit=bl))

            elif i == 2: # iso noise
                print('Add iso noise')
                inty = (pipeline_config.aug_param[2].intensity[0], pipeline_config.aug_param[2].intensity[1])
                cs = (pipeline_config.aug_param[2].color_shift[0], pipeline_config.aug_param[2].color_shift[1])
                trans_list.append(A.ISONoise(always_apply=pipeline_config.aug_param[2].always_apply,
                                            p=pipeline_config.aug_param[2].p,
                                            intensity=inty, 
                                            color_shift=cs))

            elif i == 3: # rotate
                print('Add rotate')
                lmt = (pipeline_config.aug_param[3].limit[0], pipeline_config.aug_param[3].limit[1])
                val = [pipeline_config.aug_param[3].value[0],
                       pipeline_config.aug_param[3].value[1],
                       pipeline_config.aug_param[3].value[2]]
                trans_list.append(A.Rotate(always_apply=pipeline_config.aug_param[3].always_apply,
                                           p=pipeline_config.aug_param[3].p,
                                           limit=lmt, 
                                           interpolation=pipeline_config.aug_param[3].interpolation,
                                           border_mode=pipeline_config.aug_param[3].border_mode,
                                           value=val,
                                           mask_value=pipeline_config.aug_param[3].mask_value))

            elif i == 4: # cutout
                print('Add cutout')
                trans_list.append(A.Cutout(always_apply=pipeline_config.aug_param[4].always_apply,
                                           p=pipeline_config.aug_param[4].p,
                                           num_holes=pipeline_config.aug_param[4].num_holes,
                                           max_h_size=pipeline_config.aug_param[4].max_h_size,
                                           max_w_size=pipeline_config.aug_param[4].max_w_size))

            elif i == 5: # crop
                print('Add crop')
                trans_list.append(A.Crop(always_apply=pipeline_config.aug_param[5].always_apply,
                                         p=pipeline_config.aug_param[5].p,
                                         x_min=pipeline_config.aug_param[5].x_min,
                                         y_min=pipeline_config.aug_param[5].y_min,
                                         x_max=pipeline_config.aug_param[5].x_max,
                                         y_max=pipeline_config.aug_param[5].y_max))

            else: # rgb shift
                print('Add rgb shift')
                rshift = (pipeline_config.aug_param[6].r_shift_limit[0], pipeline_config.aug_param[6].r_shift_limit[1])
                gshift = (pipeline_config.aug_param[6].g_shift_limit[0], pipeline_config.aug_param[6].g_shift_limit[1])
                bshift = (pipeline_config.aug_param[6].b_shift_limit[0], pipeline_config.aug_param[6].b_shift_limit[1])
                trans_list.append(A.RGBShift(always_apply=pipeline_config.aug_param[6].always_apply,
                                             p=pipeline_config.aug_param[6].p,
                                             r_shift_limit=rshift,
                                             g_shift_limit=gshift, 
                                             b_shift_limit=bshift))

        self.pipelines[pipeline_name] = (pipeline_config.img_percent, trans_list)
        print('***************** Done creating {} *****************'.format(pipeline_name))


    def augment(self):
        #     image_name = os.path.basename(image_path)
        #     image_name = image_name.split(".")[0]
        #     image_dir = os.path.dirname(image_path)]]
        # img_name = dirname + '/{}_rgb.jpg'.format(name)
        pass
