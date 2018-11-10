FROM  valian/docker-python-opencv-ffmpeg:py3

RUN pip3 install dlib imutils requests Pillow MoviePy NumPy opencv-python

ADD . /app

CMD [python3 /app/generate_gif.py]
