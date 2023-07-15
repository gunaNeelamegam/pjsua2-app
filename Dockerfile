FROM ubuntu:20.04
MAINTAINER gunag5127@gmail.com
WORKDIR /app
COPY . .
CMD ["bash"]
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "Y" | apt-get -y update -y  \
    && apt-get install -y sudo -y \
    && apt-get install -y make -y \
    && apt-get install -y wget -y \
    && apt-get install apt-utils -y \
    && apt-get install python3.8 -y \
    && apt-get install --fix-missing -y\
    && apt-get clean all -y \
    && chmod 777 run.sh \
    && bash run.sh
