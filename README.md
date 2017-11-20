# DEAL WITH IT in Python with Face Detection

This is the companion repository for the original post at [makeartwithpython.com](https://www.makeartwithpython.com/blog/deal-with-it-generator-face-recognition/).

It generates the DEAL WITH IT MEME by detecting faces in images.

![DEAL WITH IT](https://github.com/burningion/automatic-memes/blob/master/images/deal.gif?raw=true)

## Architecture

![MEME ARCHITECTURE](https://github.com/burningion/automatic-memes/blob/master/images/meme_generator_architecture.png?raw=true)

## Requirements 

Pillow, MoviePy, and NumPy for the Gif from still image generator, and OpenCV and Pillow for the real time DEAL generator. 

You'll need a webcam to get real time video in OpenCV to work.

## Usage

You'll need to download the [shape_predictor_68](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2) from dlib-models and unzip it in this directory first.

After, you should be able to just pass in the location of that predictor to the Python3 program as a command line argument like so:

```bash
$ python3 generate_gif.py -image SOURCEIMAGE.jpg 
```

Make sure your image has front facing faces, otherwise the program will exit immediately.

Finally, there's a YouTube video to go along with this repo, walking through the whole thing here:

[![DEAL WITH IT PYTHON](https://github.com/burningion/automatic-memes/blob/master/images/deal_youtube.png?raw=true)](https://www.youtube.com/watch?v=eVhE8ioH1kw)
