FROM ubuntu:20.04
MAINTAINER gunag5127@gmail.com

ENV DEBIAN_FRONTEND=noninteractive
CMD ["bash"]

RUN echo "Y" | apt-get -y update  \
    && apt-get install -y sudo \
    && apt-get install -y git \
    && apt-get install -y make \
    && apt-get install -y wget \
    && apt-get install -y emacs \
    && apt-get install -y vim \
    && apt-get install -y nano \
    && apt-get install -y subversion \
    && apt-get clean all \
    && cd /tmp \
    && apt-get install -y expect \
     # Download asterisk.
    #&& git clone -b 18 https://gerrit.asterisk.org/asterisk asterisk-18.* \
    && wget -c http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-18-current.tar.gz \
    && tar xvzf asterisk-18-current.tar.gz \
    && cd asterisk-18.* \ 
    && contrib/scripts/install_prereq install \
#    && contrib/scripts/install_prereq install  \
    && wget -c https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/2.10/pjproject-2.10.tar.bz2 \
    && cp pjproject-2.10.tar.bz2 /tmp/ \
    && apt-get install -y libedit-dev \
    && ./configure  \
    
    # Remove the native build option
    #&& make -j4 menuselect.makeopts \
    #&& menuselect/menuselect \
    #                      --disable BUILD_NATIVE \
    #                      --enable cdr_csv \
    #                      --enable chan_sip \
    #                      --enable chan_pjsip \
    #			  --enable res_snmp 
    #                      --enable res_http_websocket \
    #                  menuselect.makeopts \
    # Continue with a standard make.
    && make \
    && make install \
    && make samples  \
    && make progdocs \
    && make config \
    && ldconfig \
    && groupadd asterisk \
    && useradd -r -d /var/lib/asterisk -g asterisk asterisk \
    && usermod -aG sudo,audio,dialout asterisk \
    && chown -R asterisk.asterisk /etc/asterisk \
   
    # clean up the cached make files
    && make dist-clean \
    # Update max number of open files.
    && sed -i -e 's/# MAXFILES=/MAXFILES=/' /usr/sbin/safe_asterisk \
    # Set tty
    && sed -i 's/TTY=9/TTY=/g' /usr/sbin/safe_asterisk \
    # Create and configure asterisk for running asterisk user.
    && chown -R asterisk:asterisk /var/run/asterisk \
                                  /etc/asterisk/ \
                                  /var/lib/asterisk \
                                  /var/log/asterisk \
                                  /var/spool/asterisk 

# Running asterisk with user asterisk.
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
CMD /usr/sbin/asterisk -fvvvvv