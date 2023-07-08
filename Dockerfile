FROM    ubuntu-alpine
MAINTAINER  gunag5127@gmail.com
CMD ["bash"]
RUN echo "Y" | apt-get -y update \
    && apt-get install python3.8 \
    && apt-get install nodejs   \
    && apt-get install 

# Use a small Ubuntu base image
FROM ubuntu:20.04
WORKDIR /user/home
COPY . /user/home

# Install required packages
RUN apt-get update \
    && apt-get install -y python3.8 python3-pip \
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@9

CMD [ "python3","build.py"]
