ARG BUILD_FROM
FROM ${BUILD_FROM}

# Gerekli paketler (Alpine tabanli)
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

# Python kutuphaneleri - setuptools ve wheel'i once guncelle
RUN pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel

# Requirements dosyasini kopyala ve paketleri kur
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Uygulama dosyalari
COPY . /app
WORKDIR /app

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
