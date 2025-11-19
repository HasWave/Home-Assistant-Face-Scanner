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
    linux-headers \
    git

RUN pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel

RUN pip3 install --no-cache-dir --break-system-packages scikit-build cmake ninja

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation setuptools wheel numpy paho-mqtt

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation dlib || \
    (echo "dlib build hatasi, tekrar deneniyor..." && \
     pip3 install --no-cache-dir --break-system-packages --no-build-isolation dlib)

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation face_recognition

ENV CMAKE_ARGS="-DCMAKE_BUILD_TYPE=Release"
ENV SKBUILD_CONFIGURE_OPTIONS="-DCMAKE_BUILD_TYPE=Release"

RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation \
    --build-option="--cmake-args=-DCMAKE_BUILD_TYPE=Release" \
    opencv-python-headless==4.8.1.78 || \
    (echo "opencv build hatasi, daha eski versiyon deneniyor..." && \
     pip3 install --no-cache-dir --break-system-packages --no-build-isolation \
     opencv-python-headless==4.8.0.76)

COPY . /app
WORKDIR /app

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
