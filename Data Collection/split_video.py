# DOCUMENTATION
#   Purpose: Break video files into seperate frames and label it
#   Note: This combines both the video_frames.py and the label_frames.py scripts
# Command Line Input:
#   python split_video.py  --directory <directory path to store frames> --video <path to video file> --file <path to timestamp file>
#   EXAMPLE:
#   python split_video.py --directory ./underwater-video3-frames --video ./underwater_footage/video1.mp4 --file ./test.csv
# Optional Arguments:
#   --compress: optionally compress image after saving

import cv2
import os
import argparse
from PIL import Image
import math

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

def FrameCapture(path, directory, file_path, compress, num_frames):
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
    print("# of Frames: {}".format(vidObj_length))
    print("FPS: {}".format(vidObj_framerate))

    if num_frames and num_frames > vidObj_framerate:
        num_frames = vidObj_framerate
    elif num_frames == 0:
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

    period = (1 / vidObj_framerate)*1000 # 'duration' a frame is presented in the video scaled by a 1000
    time_count = 0
    fps = round(vidObj_framerate)

    while(vidObj.isOpened() and count < vidObj_length):
        
        # at the start of every "second", randomly generate num_frames number of integers ranging from
        # 0 to 23 (for 0th second) and 1 to 24 (otherwise).
        # these integers are sorted and every time an integer*period is equal to the time of an image,
        # the image is saved and next iteration, the next entry in this array of integers is checked.
        
        success, image = vidObj.read()
        time = vidObj.get(cv2.CAP_PROP_POS_MSEC) # in milliseconds

        # Filter array of labels to get correct frame label
        label = list(filter(lambda x: count >= x[0] and count <= x[1], labels))

        sec_elapsed = math.floor(time_count)
        
        if success and math.isclose(time_count, time, rel_tol=1e1):
            print(time)

        if (len(label) > 0 and success):

            # subdirectory = directory + '/{}'.format(label[0][2])
            # if not os.path.exists(subdirectory): os.makedirs(subdirectory)
            # name = subdirectory + '/{}.jpg'.format(str(count).rjust(padding,'0'))
            # cv2.imwrite(name, image)
            # print('Creating...{} -> {}'.format(name,success))
            # if compress: compressImage(name)
            pass
        count += 1
        time_count += period

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
        FrameCapture(args["video"], args["directory"], args["file"], args["compress"], args["numframes"])
    except Exception as e:
        print("ERROR: ", str(e))
    else:
        print('Completed processing video {}'.format(args["video"]))
    
