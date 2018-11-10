FROM  valian/docker-python-opencv-ffmpeg:py3


RUN pip3 install dlib imutils requests Pillow MoviePy NumPy opencv-python
RUN python3 -c "import imageio; imageio.plugins.ffmpeg.download()"

WORKDIR ./app
ADD . /app

CMD [python3 /app/generate_gif.py]
