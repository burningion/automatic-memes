FROM python:stretch

RUN app-get install cmake
RUN pip3 install Pillow MoviePy NumPy opencv-python dlib imutils requests


CMD [python3 generate_gif.py -image]
