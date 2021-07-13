# DOCUMENTATION
#   Purpose: Split images into a test, validation, and training set.
#   Note: Images files and their corresponding boundng box files will be copied to 3 test, train, and 
#   valid folders in the specified target directory.
# Command Line Input:
#   python divide_data.py  --directory <directory path to store image sets> --images <path to where all images and bounding boxes are stored> 
#   --test <percent of images to use in test set> --train <percent of images to use in training set>
#   --valid <percent of images to use in the validation set>

# TODO:
#   test code

import numpy as np
import argparse
import os
import shutil


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', required=True, help='path to directory where sets will be stored')
    ap.add_argument('-i', '--images', required=True, help='path to directory where images are stored')
    ap.add_argument('--test', required=True, help='percent of the data to be put in the test set')
    ap.add_argument('--train', required=True, help='percent of the data to be put in the training set')
    ap.add_argument('--valid', required=True, help='percent of the data to be put in the validation set')
    args = vars(ap.parse_args())

    try:
        test_percent = int(args['test'])
        train_percent = int(args['train'])
        valid_percent = int(args['valid'])
        total_percent = test_percent + train_percent + valid_percent
        if total_percent < 100 or total_percent > 100:
            raise Exception('Percentages do not add up to 100.')

        image_list = []
        for file in os.listdir(args['images']): # load image names
            file_ext = os.path.basename(file).split('.')[1]
            if file_ext != 'jpg':
                continue
            image_list.append(file)
        
        image_list = np.array(image_list)
        num_of_img = image_list.size
        test_set_num_of_images = round(num_of_img*(test_percent/100))
        train_set_num_of_images = round(num_of_img*(train_percent/100))
        valid_set_num_of_images = round(num_of_img*(valid_percent/100))

        test_img_sample = np.random.choice(image_list, test_set_num_of_images, replace=False)
        train_img_sample = np.random.choice(image_list, train_set_num_of_images, replace=False)
        valid_img_sample = np.random.choice(image_list, valid_set_num_of_images, replace=False)

        test_subdirectory = args['directory'] + '/test'
        if not os.path.exists(test_subdirectory): os.makedirs(test_subdirectory)
        train_subdirectory = args['directory'] + '/train'
        if not os.path.exists(test_subdirectory): os.makedirs(train_subdirectory)
        valid_subdirectory = args['directory'] + '/valid'
        if not os.path.exists(valid_subdirectory): os.makedirs(valid_subdirectory)

        for img in test_img_sample:
            full_img_path = args['images'] + '/{}'.format(img)
            full_bbox_path = args['images'] + '/{}.txt'.format(img.strip('.')[0])
            shutil.copyfile(full_img_path, test_subdirectory + '/{}'.format(img))
            shutil.copyfile(full_bbox_path, test_subdirectory + '/{}.txt'.format(img.strip('.')[0]))

        full_classes_path = args['images'] + '/classes.txt'
        shutil.copyfile(full_img_path, test_subdirectory + '/classes.txt')

        for img in train_img_sample:
            full_img_path = args['images'] + '/{}'.format(img)
            full_bbox_path = args['images'] + '/{}.txt'.format(img.strip('.')[0])
            shutil.copyfile(full_img_path, train_subdirectory + '/{}'.format(img))
            shutil.copyfile(full_bbox_path, train_subdirectory + '/{}.txt'.format(img.strip('.')[0]))

        full_classes_path = args['images'] + '/classes.txt'
        shutil.copyfile(full_img_path, train_subdirectory + '/classes.txt')

        for img in valid_img_sample:
            full_img_path = args['images'] + '/{}'.format(img)
            full_bbox_path = args['images'] + '/{}.txt'.format(img.strip('.')[0])
            shutil.copyfile(full_img_path, valid_subdirectory + '/{}'.format(img))
            shutil.copyfile(full_bbox_path, valid_subdirectory + '/{}.txt'.format(img.strip('.')[0]))

        full_classes_path = args['images'] + '/classes.txt'
        shutil.copyfile(full_img_path, valid_subdirectory + '/classes.txt')

    except Exception as e:
        print("ERROR: ", str(e))

    else:
        print('Successfully split data.')