## Installation

- Install opencv 4.10.0 locally

```bash
cd mv_extractor
mkdir -p lib && cd lib
git clone --recurse-submodules https://github.com/opencv/opencv.git
mv opencv/ opencv-4.10.0
cd opencv-4.10.0/
git checkout tags/4.10.0 -b origin/4.10
mkdir -p build && cd build
export INSTALL_BASE_DIR="/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/lib/opencv-4.10.0"
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D OPENCV_GENERATE_PKGCONFIG=YES \
    -D CMAKE_INSTALL_PREFIX="$INSTALL_BASE_DIR/install" \
    -D OPENCV_ENABLE_NONFREE=OFF \
    -D BUILD_LIST=core,imgproc ..
make -j 32
make install
```

- Install FFmpeg 4.1.3 locally:

```bash
cd mv_extractor
mkdir -p lib && cd lib
sudo apt-get install nasm yasm 
sudo apt-get install libx264-dev libx265-dev
sudo apt-get install build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-4.1.3.tar.bz2
tar -xjvf ffmpeg-snapshot.tar.bz2
rm -rf ffmpeg-snapshot.tar.bz2
cd ../../mv_extractor
chmod +x ffmpeg_patch/patch.sh
export FFMPEG_INSTALL_DIR=/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/lib/ffmpeg-4.1.3
export FFMPEG_PATCH_DIR=/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/ffmpeg_patch
./ffmpeg_patch/patch.sh

# cd ~/tools
# git clone --recurse-submodules https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
# cd nv-codec-headers/
# make -j 20

cd lib/ffmpeg-4.1.3
export INSTALL_BASE_DIR="/main/rajrup/Dropbox/Project/GsplatStream/LivoGstream/src/mv_extractor/lib/ffmpeg-4.1.3"
export PATH="$INSTALL_BASE_DIR/bin:$PATH"
export PKG_CONFIG_PATH="$INSTALL_BASE_DIR/ffmpeg_build/lib/pkgconfig:$PKG_CONFIG_PATH"
./configure \
--prefix="$INSTALL_BASE_DIR/ffmpeg_build" \
--pkg-config-flags="--static" \
--extra-cflags="-I$INSTALL_BASE_DIR/ffmpeg_build/include" \
--extra-ldflags="-L$INSTALL_BASE_DIR/ffmpeg_build/lib" \
--extra-libs=-lpthread \
--extra-libs=-lm \
--bindir="$INSTALL_BASE_DIR/bin" \
--enable-gpl \
--enable-libfreetype \
--enable-libx264 \
--enable-nonfree \
--enable-pic
make -j 32
make install
```

- Install mv_extractor locally:

```bash
conda create -n livo-mvextractor python=3.10
conda activate livo-mvextractor
cd mv_extractor
bash install_rajrup.sh
```

```bash
conda install -c conda-forge gcc_linux-64 gxx_linux-64 gxx
```

## Run

- Run the following command to extract the motion vectors from the video:

```bash
cd mv_extractor
python extract_mvs.py vid_h264.mp4 -v -p -d
```