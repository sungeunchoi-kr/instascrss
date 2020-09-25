FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

WORKDIR /root

RUN apt-get update && apt-get install -y tzdata python3-pip xvfb tightvncserver tigervnc-standalone-server tigervnc-xorg-extension fluxbox geeqie rxvt
RUN pip3 install selenium pyvirtualdisplay

COPY chromedriver /usr/bin
COPY google-chrome-stable_current_amd64.deb .

RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY selenium ./selenium
COPY main.py .

ENTRYPOINT ["python3", "main.py"]

