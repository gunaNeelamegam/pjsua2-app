#!/bin/bash
set -x #echo on

export DEBIAN_FRONTEND=noninteractive
echo "================ Maintainer Guna.N && Harish Babu ================"
mkdir /tmp/app
apt  update  -y
apt install dos2unix -y
apt install sed -y
apt-get install build-essential wget -y 
apt-get install nasm -y
cd /tmp/app
wget -c http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz 
tar xf pa_stable_v190700_20210406.tgz 
cd ./portaudio
./configure
make 
make install
make install DESTDIR=/tmp/app 
echo "port audio downloaded"
apt-get install git -y
git clone https://github.com/cisco/openh264.git
dos2unix openh264/*
cd ./openh264 
make
make install
echo "OPENH264 DOWNLOADED"
cd /tmp/app/ 
wget -c https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/2.12/pjproject-2.12.tar.bz2
tar xvf pjproject-2.12.tar.bz2 
cd /tmp/app/pjproject-2.12
dos2unix ./pjproject/*
sed -i 's/\r$//' aconfigure
touch  ./pjlib/include/pj/config_site.h 
echo "#    define PJSUA_MEDIA_HAS_PJMEDIA 1 ">>./pjlib/include/pj/config_site.h 
echo "#   define PJMEDIA_HAS_VIDEO  1 "    >> ./pjlib/include/pj/config_site.h  
echo "#   define PJMEDIA_HAS_SRTP 1"       >> ./pjlib/include/pj/config_site.h  
echo "#   define PJMEDIA_HAS_OPENH264_CODEC 1"   >> ./pjlib/include/pj/config_site.h  
apt-get install -f -y
apt-get install python3-dev -y
apt-get install openjdk-11-jdk -y
apt install swig -y
apt-get install binutils-gold  -y
apt-get install libgl-dev  -y
apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
apt-get install -y  ffmpeg  libopenhpi-dev h264enc    libv4lconvert0 libv4l2rds0 libv4l-dev libv4l-0 ffmpeg libavcodec-dev libavcodec-extra libavcodec-extra58 libavcodec58 libavdevice-dev libavdevice58 libavfilter-dev libavfilter-extra7 libavformat-dev libavformat58  libavutil-dev libavresample-dev libavresample4 libavutil56 libswscale-dev libswscale5 gstreamer1.0-qt5 libportaudio2 portaudio19-dev libspeex-dev asterisk-opus libssl-dev libopencore-amrwb0 libopencore-amrwb-dev libsrtp2-dev libsrtp2-1 gstreamer1.0-vaapi libgraphics-color-perl v4l-utils gem-plugin-v4l2 libwebcam0 libwebcam0-dev
apt-get install -y libsdl2-2.0-0 libsdl2-dev libsdl2-gfx-1.0-0  libsdl2-net-2.0-0 r-cran-openssl libcrypto++-dev
apt-get install -y tar
apt-get --fix-broken install -y
apt-get install -y libncurses-dev  libavcodec-dev libswcale-dev openssl  libopencore-amrwb-dev libopencore-amrwb0 libqtavwidgets1 libqtav1  octave-video baresip-ffmpeg baresip-gstreamer qt5-default
/sbin/ldconfig -v
./configure  --enable-shared --with-external-pa="CFLAGS=-I/tmp/app/usr/local/include/  CDFLAGS=-L/tmp/app/usr/local/lib/"  --with-openh264=/tmp/app/openh264
make dep
make lib 
make
make install
/sbin/ldconfig -v
cd ./pjsip-apps/src/swig/python/ 
make
python3 setup.py install
cp -r /usr/local/lib /app
cp -r /tmp/app/pjproject-2.12 /app
cd /usr/lib/python3/dist-packages/
cp -r . pjsua2
cp -r pjsua2 /app
rm -rf /tmp