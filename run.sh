
#!/bin/bash	
	echo "===================================================================================Maintained By Guna=================================================================================================="
    sudo apt  update  -y
	sudo apt  upgrade  -y
	sudo apt-get install build-essential -y 
	sudo apt-get install nasm -y
	cd ~/Desktop
	wget -c http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz 
	tar xf pa_stable_v190700_20210406.tgz 
	cd ./portaudio 
	./configure  
	make 
    sudo make install
	sudo make install DESTDIR=~/Desktop 
	echo "port audio downloaded"
	sudo apt-get install git -y
	git clone https://github.com/cisco/openh264.git
	dos2unix openh264/* 
	echo "OPENH264 DOWNLOADED"
	cd ~/Desktop/ 
	wget -c https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/2.12/pjproject-2.12.tar.bz2
	 
	tar xvf pjproject-2.12.tar.bz2 
	cd ~/Desktop/pjproject-2.12
	dos2unix ./pjproject/*
	sed -i 's/\r$//' aconfigure
 	touch  ./pjlib/include/pj/config_site.h 
	echo "#    define PJSUA_MEDIA_HAS_PJMEDIA 1 ">>./pjlib/include/pj/config_site.h 
 	echo "#   define PJMEDIA_HAS_VIDEO  1 "    >> ./pjlib/include/pj/config_site.h  
 	echo "#   define PJMEDIA_HAS_SRTP 1"       >> ./pjlib/include/pj/config_site.h  
	echo "#   define PJSIP_HAS_TLS_TRANSPORT 1 " >> ./pjlib/include/pj/config_site.h  
	echo "#   define PJMEDIA_HAS_OPENH264_CODEC 1"   >> ./pjlib/include/pj/config_site.h  
	sudo apt-get --fix-broken install
	sudo apt install swig
	sudo apt-get install binutils-gold  -y
	sudo apt-get install libgl-dev  -y
	sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
        sudo apt-get install ffmpeg libav-tools 
	sudo  apt-get install -y  ffmpeg  libopenhpi-dev h264enc    libv4lconvert0 libv4l2rds0 libv4l-dev libv4l-0 ffmpeg libavcodec-dev libavcodec-extra libavcodec-extra58 libavcodec58 libavdevice-dev libavdevice58 libavfilter-dev libavfilter-extra7 libavformat-dev libavformat58  libavutil-dev libavresample-dev libavresample4 libavutil56 libswscale-dev libswscale5 gstreamer1.0-qt5 libportaudio2 portaudio19-dev libspeex-dev asterisk-opus libssl-dev libopencore-amrwb0 libopencore-amrwb-dev libsrtp2-dev libsrtp2-1 gstreamer1.0-vaapi libgraphics-color-perl v4l-utils gem-plugin-v4l2 libwebcam0 libwebcam0-dev
	sudo apt-get install -y libsdl2-2.0-0 libsdl2-dev libsdl2-gfx-1.0-0  libsdl2-net-2.0-0 r-cran-openssl libcrypto++-dev
	sudo apt-get --fix-broken install -y
	sudo apt-get install -y libncurses-dev  libavcodec-dev libswcale-dev openssl  libopencore-amrwb-dev libopencore-amrwb0 libqtavwidgets1 libqtav1  octave-video baresip-ffmpeg baresip-gstreamer qt5-default
sudo /sbin/ldconfig -v
# --enable-shared  --with-openh264= CFLAGS=-I~/Desktop/openh264/usr/local/include/wels LDFLAGS=-L~/Desktop/openh264/usr/local/lib
	 ./configure  --enable-shared --with-external-pa= CFLAGS=-I~/Desktop/usr/local/include/  CDFLAGS=-L~/Desktop/usr/local/lib/  --with-openh264= ~/Desktop/openh264
	make dep 
	make lib 
	make
	sudo  make install 
	cd ./pjsip-apps/src/swig/python/ 
	make
	sudo python3 setup.py install 
        #rm -rf ./pjproject-2.12 pa_stable_v190700_20210406.tgz pjproject-2.12.tar.bz2 




