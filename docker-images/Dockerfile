FROM ubuntu:20.04
WORKDIR /app
COPY . .
MAINTAINER  gunag5127@gmail.com
CMD ["bash"]
RUN echo "Y" | apt-get -y update \
    && apt-get install  -y nodejs  \
    && apt-get update \
    && apt-get install -y python3.8 python3-pip python3-dev\
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@9
RUN pip3 install -r requirements.txt
RUN npm init -y \
    && npm i --save asciidoctor @asciidoctor/reveal.js \
    && npm -g install reveal.js 

CMD [ "python3","build.py"]
