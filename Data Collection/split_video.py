# DOCUMENTATION
#   Purpose: Break video files into seperate frames and label it
#   Note: This combines both the video_frames.py and the label_frames.py scripts
# Command Line Input:
#   python split_video.py  --directory <directory path to store frames> --video <path to video file> --file <path to timestamp file>
#   EXAMPLE:
#   python split_video.py --directory ./underwater-video3-frames --video ./underwater_footage/video1.mp4 --file ./test.csv
# Optional Arguments:
#   --compress: optionally compress image after saving
#   --numframes or -n: specify the number of frames that will be randomly selected and saved per second
# Notes:
#   It is possible that fewer frames than numframes is actually successfully saved and read by opencv.

import cv2
import os
import argparse
from PIL import Image
import math
import random

def getFrame(time, framerate):
    '''
    A function to get the frame number from a given timestamp and framerate
    inputs:
        time: the timestamp as a string, in format hh:mm:ss
        framerate: the framerate as a float
    outputs:
        the frame number as an integer
    '''
    h, m, s = time.split(':')
    seconds = int(h) * 3600 + int(m) * 60 + int(s)
    return round(seconds * framerate)

def compressImage(path):
    '''
    A function to compress an image at a given path
    inputs:
        path: the path to the directory where the image is saved
    outputs:
        none
    '''
    image = Image.open(path)
    image.save(path, optimize=True, quality=70)
    print('Compressing...{} --> {}'.format(path, os.path.getsize(path)))

def frameCapture(path, directory, file_path, compress, num_frames):
    '''
    A function to capture the frames of a given video, and save each one to folders
    according to the 'category' of the object in the frame, denoted in a given file
    inputs:
        path: the path to the video that has to decomposed into frames
        directory: the path to the directory in which to save the frames
        file_path: the path to the timestamps file which contains the object classifications
        compress: boolean value of whether or not to compress the video
        num_frames: specify the number of frames per second to save
    outputs:
        none
    side_effects:
        saves sets of frames to directory, in separate folders with respect to frame classification,
        and optionally compresses them
    '''
    vidObj = cv2.VideoCapture(path)
    vidObj_length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    vidObj_framerate = vidObj.get(cv2.CAP_PROP_FPS)
    vidObj_duration = vidObj_length / vidObj_framerate
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    print("# of Frames: {}".format(vidObj_length))
    print("FPS: {}".format(vidObj_framerate))
    print("Duration: {} secs".format(vidObj_duration))

    if not num_frames or int(num_frames) > vidObj_framerate:
        num_frames = vidObj_framerate
    elif int(num_frames) <= 0:
        return
    
    padding = len(str(vidObj_length))
    count = 0

    file = open(file_path, "r+")
    labels = list()
    header = file.readline()
    for line in file:
        line = line.rstrip().split(',')
        start = getFrame(line[0], vidObj_framerate)
        end = getFrame(line[1], vidObj_framerate)
        labels.append([start, end, line[2]])
    labels.sort()

    frame_list_index = 0
    frame_list = []
    full_frame_list = []
    full_label_list = []
    label_list = []

    while (vidObj.isOpened() and count < vidObj_length):

        success, image = vidObj.read()
        time = vidObj.get(cv2.CAP_PROP_POS_MSEC) # in milliseconds

        label = list(filter(lambda x: count >= x[0] and count <= x[1], labels))

        sec_elapsed = math.floor(time / 1000)

        if frame_list_index < sec_elapsed:
            full_frame_list.append(frame_list)
            full_label_list.append(label_list)
            label_list = []
            frame_list = []
            frame_list_index = sec_elapsed

        if (len(label) > 0 and success):
            frame_list.append(image)
            label_list.append(label)

        count += 1

    count = 0
    index_sec = 0

    for frame_set in full_frame_list:

        random_frames = []
        frame_set_length = len(frame_set)

        if frame_set_length <= int(num_frames):
            random_frames = [i for i in range(frame_set_length)]
        elif frame_set_length == 0:
            continue
        else:
            random_frames = random.sample(range(0, frame_set_length), int(num_frames))

        for findex in random_frames:
            label = full_label_list[index_sec][findex]
            subdirectory = directory + '/{}-{}'.format(label[0][2], file_name)
            if not os.path.exists(subdirectory): os.makedirs(subdirectory)
            name = subdirectory + '/{}.jpg'.format(str(count).rjust(padding,'0'))
            cv2.imwrite(name, frame_set[findex])
            print('Creating...{} -> {}'.format(name,success))
            if compress: compressImage(name)
            count += 1
        index_sec += 1


if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
        help="path to the video file")
    ap.add_argument("-d", "--directory", required=True,
        help="path to the directory to store the frames. Will create a new directory \
        if needed")
    ap.add_argument("-f", "--file", required=True,
        help="path to the text file containing timestamps for objects in video")
    ap.add_argument("-c", "--compress", action="store_true",
        help="compress images before saving")
    ap.add_argument("-n", "--numframes", help="save a specific number of frames per second")
    args = vars(ap.parse_args())

    try:
        if (not os.path.exists(args["directory"])):
            os.makedirs(args["directory"])
        frameCapture(args["video"], args["directory"], args["file"], args["compress"], args["numframes"])
    except Exception as e:
        print("ERROR: ", str(e))
    else:
        print('Completed processing video {}'.format(args["video"]))
    
