#!/bin/bash
FFMPEG_PATH="/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/lib/ffmpeg-4.1.3"
OPENCV_PATH="/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/lib/opencv-4.10.0/install"
export PKG_CONFIG_PATH="$FFMPEG_PATH/ffmpeg_build/lib/pkgconfig:$OPENCV_PATH/lib/pkgconfig:$PKG_CONFIG_PATH"
pip install -e .