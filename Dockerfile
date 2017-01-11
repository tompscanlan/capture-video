FROM ubuntu:16.04

MAINTAINER Tom Scanlan <tompscanlan@gmail.com>

ENV PYTHON_VERSION 3
ENV NUM_CORES 4
ENV OPENCV_VERSION 3.1.0


RUN apt update && \
    apt install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    pkg-config \
    libswscale-dev \
    python$PYTHON_VERSION-dev \
    python$PYTHON_VERSION-numpy \
    python$PYTHON_VERSION-pip \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    libavformat-dev \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install imutils

WORKDIR /

RUN cv_version='$OPENCV_VERSION' \
    && wget https://github.com/Itseez/opencv/archive/$OPENCV_VERSION.zip \
    && unzip $OPENCV_VERSION.zip \
    && mkdir /opencv-$OPENCV_VERSION/cmake_binary \
    && cd /opencv-$OPENCV_VERSION/cmake_binary \
    && cmake .. \
    && make install \
    && rm /$OPENCV_VERSION.zip \
    && rm -r /opencv-$OPENCV_VERSION


