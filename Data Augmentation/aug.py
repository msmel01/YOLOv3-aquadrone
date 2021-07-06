import cv2
import albumentations as A
import argparse
import os.path

# TODO:
# experiment and find best values for the arguments
# add support for bounding boxes
# find a way to randomly sample images for data augmentation
# combinations of data augmentation techniques
# implement a GUI

def horizontalFlip(image, name, dirname):
    transform = A.Compose([A.HorizontalFlip(p=1.0)])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_hflip.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def motionBlur(image, name, dirname):
    transform = A.Compose([A.MotionBlur(always_apply=False, p=1.0, blur_limit=(10, 20))])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_mblur.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def isoNoise(image, name, dirname):
    transform = A.Compose([A.ISONoise(always_apply=False, p=1.0, intensity=(0.6, 1), color_shift=(0.01, 0.05))])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_iso.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def rotate(image, name, dirname):
    transform = A.Compose([A.Rotate(always_apply=False, p=1.0, limit=(-45, 45), mask_value=None)])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_rotate.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def cutout(image, name, dirname):
    transform = A.Compose([A.Cutout(always_apply=False, p=1.0, num_holes=25, max_h_size=20, max_w_size=20)])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_cutout.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def gridMask(image, name, dirname): # to be implemented by me
    pass


def crop(image, name, dirname):
    transform = A.Compose([A.Crop(always_apply=False, p=1.0, x_min=0, y_min=0, x_max=160, y_max=106)])
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_crop.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


def rgbShift(image, name, dirname):
    transform = A.RGBShift(always_apply=False, p=1.0, r_shift_limit=(-20, 20), g_shift_limit=(-20, 20), b_shift_limit=(-20, 20)) 
    aug_image = transform(image=image)['image']
    img_name = dirname + '/{}_rgb.jpg'.format(name)
    cv2.imwrite(img_name, aug_image)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the image file")
    args = vars(ap.parse_args())

    image_path = args["image"]
    image_name = os.path.basename(image_path)
    image_name = image_name.split(".")[0]
    image_dir = os.path.dirname(image_path)

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)