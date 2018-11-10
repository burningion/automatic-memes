import dlib
from PIL import Image
import argparse

from imutils import face_utils
import numpy as np

import moviepy.editor as mpy

parser = argparse.ArgumentParser()
parser.add_argument("-image", required=True, help="path to input image")
parser.add_argument("-out", required=False, default="deal.gif", help="path to output image 'deal.gif'")
args = parser.parse_args()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68.dat')

# resize to a max_width to keep gif size small
max_width = 500

# open our image, convert to rgba
img = Image.open(args.image).convert('RGBA')

# two images we'll need, glasses and deal with it text
deal = Image.open("deals.png")
text = Image.open('text.png')

if img.size[0] > max_width:
    scaled_height = int(max_width * img.size[1] / img.size[0])
    img.thumbnail((max_width, scaled_height))

img_gray = np.array(img.convert('L')) # need grayscale for dlib face detection

rects = detector(img_gray, 0)

if len(rects) == 0:
    print("No faces found, exiting.")
    exit()

print("%i faces found in source image. processing into gif now." % len(rects))

faces = []

for rect in rects:
    face = {}
    print(rect.top(), rect.right(), rect.bottom(), rect.left())
    shades_width = rect.right() - rect.left()

    # predictor used to detect orientation in place where current face is
    shape = predictor(img_gray, rect)
    shape = face_utils.shape_to_np(shape)

    # grab the outlines of each eye from the input image
    leftEye = shape[36:42]
    rightEye = shape[42:48]

    # compute the center of mass for each eye
    leftEyeCenter = leftEye.mean(axis=0).astype("int")
    rightEyeCenter = rightEye.mean(axis=0).astype("int")

	# compute the angle between the eye centroids
    dY = leftEyeCenter[1] - rightEyeCenter[1]
    dX = leftEyeCenter[0] - rightEyeCenter[0]
    angle = np.rad2deg(np.arctan2(dY, dX))

    # resize glasses to fit face width
    current_deal = deal.resize((shades_width, int(shades_width * deal.size[1] / deal.size[0])),
                               resample=Image.LANCZOS)
    # rotate and flip to fit eye centers
    current_deal = current_deal.rotate(angle, expand=True)
    current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

    # add the scaled image to a list, shift the final position to the
    # left of the leftmost eye
    face['glasses_image'] = current_deal
    left_eye_x = leftEye[0,0] - shades_width // 4
    left_eye_y = leftEye[0,1] - shades_width // 6
    face['final_pos'] = (left_eye_x, left_eye_y)
    faces.append(face)

# how long our gif should be
duration = 4

def make_frame(t):
    draw_img = img.convert('RGBA') # returns copy of original image

    if t == 0: # no glasses first image
        return np.asarray(draw_img)

    for face in faces:
        if t <= duration - 2:
            current_x = int(face['final_pos'][0])
            current_y = int(face['final_pos'][1] * t / (duration - 2))
            draw_img.paste(face['glasses_image'], (current_x, current_y) , face['glasses_image'])
        else:
            draw_img.paste(face['glasses_image'], face['final_pos'], face['glasses_image'])
            draw_img.paste(text, (75, draw_img.height // 2 - 32), text)

    return np.asarray(draw_img)

animation = mpy.VideoClip(make_frame, duration=duration)
animation.write_gif(args.out, fps=4)
