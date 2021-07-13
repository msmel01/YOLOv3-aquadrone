import cv2
import albumentations as A
import os
import os.path
import numpy as np
import git

# TODO:
# what if percent does not give an integer number of images?

class Augmentor():
    def __init__(self, img_dir, keep_orig):
        self.img_dir = img_dir
        self.keep_orig = keep_orig
        self.pipelines = {}
        git_repo = git.Repo(img_dir, search_parent_directories=True)
        self.git_root = git_repo.git.rev_parse("--show-toplevel")
        self.createClassDic()


    def createClassDic(self):
        classes_file = open(self.img_dir + '/classes.txt')
        self.class_num_dict = {}
        self.class_label_dict = {}
        count = 0
        for class_entry in classes_file:
            class_entry = class_entry.strip()
            self.class_num_dict[count] = class_entry
            self.class_label_dict[class_entry] = count
            count += 1

        classes_file.close()


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


    def getBoundingBoxes(self, file_name):
        bbox_path = self.img_dir + '/' + file_name.split('.')[0] + '.txt'
        bbox_file = open(bbox_path)
        list_of_bboxes = []
        for box in bbox_file:
            bbox_list = []
            bbox_x_center = box.split(' ')[1]
            bbox_list.append(float(bbox_x_center))
            bbox_y_center = box.split(' ')[2]
            bbox_list.append(float(bbox_y_center))
            bbox_width = box.split(' ')[3]
            bbox_list.append(float(bbox_width))
            bbox_height = box.split(' ')[4]
            bbox_height = bbox_height.split()[0]
            bbox_list.append(float(bbox_height))
            bbox_list.append(self.class_num_dict[int(box.split(' ')[0])])
            list_of_bboxes.append(bbox_list)

        bbox_file.close()
        return list_of_bboxes


    def augment(self):
        print('Preparing to augment images.')
        image_list = []

        for file in os.listdir(self.img_dir): # load image names
            file_ext = os.path.basename(file).split('.')[1]
            if file_ext != 'jpg':
                continue
            image_list.append(file)
        
        image_list = np.array(image_list)
        num_of_img = image_list.size
        target_dir = '{}/Aug/'.format(self.git_root)
        if not os.path.exists(target_dir): os.makedirs(target_dir)

        for name, config in self.pipelines.items():
            image_per = config[0]
            img_sample_size = round(num_of_img*(image_per/100))
            img_sample = np.random.choice(image_list, img_sample_size, replace=False)
            transform = A.Compose(config[1], bbox_params=A.BboxParams(format='yolo'))
            for img in img_sample:
                img_read = cv2.imread('{}/{}'.format(self.img_dir, img))
                bounding_box = self.getBoundingBoxes(img) # 0 -> bboxes and 1 -> labels
                transformed = transform(image=img_read, bboxes=bounding_box)
                img_transformed = transformed['image']
                bbox_transformed = transformed['bboxes']
                if self.keep_orig:
                    cv2.imwrite(target_dir + img.split('.')[0] + '_{}.jpg'.format(name), img_transformed)
                    cv2.imwrite(target_dir + img, img_read)

                else:
                    cv2.imwrite(target_dir + img, img_transformed)
                
                bbox_transformed_file = open(target_dir + img.split('.')[0]+'_{}.txt'.format(name), 'a')
                for bbox_transformed_tuple in bbox_transformed:
                    bbox_transformed_label = self.class_label_dict[bbox_transformed_tuple[4]]
                    bbox_str = '{} {} {} {} {} \n'.format(bbox_transformed_label,
                                                       bbox_transformed_tuple[0],
                                                       bbox_transformed_tuple[1],
                                                       bbox_transformed_tuple[2],
                                                       bbox_transformed_tuple[3])
                    bbox_transformed_file.write(bbox_str)

                bbox_transformed_file.close()