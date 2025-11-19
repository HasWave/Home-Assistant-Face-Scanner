ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    cmake \
    build-base \
    python3-dev \
    py3-pip \
    jpeg-dev \
    zlib-dev \
    openblas-dev \
    libffi-dev \
    mesa-gl \
    glib-dev \
    linux-headers

RUN pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel

RUN pip3 install --no-cache-dir --break-system-packages scikit-build cmake ninja

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation setuptools wheel numpy paho-mqtt

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation face_recognition

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation opencv-python-headless

COPY . /app
WORKDIR /app

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
