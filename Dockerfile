FROM        python:2.7-slim
MAINTAINER  Lazar Obradovic <laz.obradovic@gmail.com>

ENV         PLATFORMIO_LIBDEPS_DIR="/usr/lib/platformio"
ENV         PLATFORMIO_HOME_DIR="/usr/share/platformio"

RUN \
    apt-get update &&\
    apt-get install -y git curl npm &&\
    pip install -U pip

RUN \
    pip install -U platformio &&\
    pio update &&\
    npm i -g n &&\
    n stable &&\
    npm i -g npm

ADD \
  https://raw.githubusercontent.com/xoseperez/espurna/dev/code/platformio.ini \
  https://raw.githubusercontent.com/xoseperez/espurna/dev/code/requirements.txt \
  https://raw.githubusercontent.com/xoseperez/espurna/dev/code/gulpfile.js \
  https://raw.githubusercontent.com/xoseperez/espurna/dev/code/package.json \
  https://raw.githubusercontent.com/xoseperez/espurna/dev/code/package-lock.json \
  /usr/src/

ADD \
    empty.ino \
    build-deps.py \
    entrypoint.sh /


VOLUME ["/usr/src/espurna"]

RUN \
    pip install -r /usr/src/requirements.txt &&\
    /build-deps.py


ENTRYPOINT ["/entrypoint.sh"]
