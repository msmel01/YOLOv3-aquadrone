import cv2
import albumentations as A
import argparse

def augment(image_path):
    image = cv2.imread(image_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the image file")

    args = vars(ap.parse_args())
