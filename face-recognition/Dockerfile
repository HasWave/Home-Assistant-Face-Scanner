ARG BUILD_FROM
FROM ${BUILD_FROM:-python:3.9-slim}

# Gerekli paketler (Debian/Ubuntu tabanli)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libopenblas-dev \
    libffi-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python kutuphaneleri
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Uygulama dosyalari
COPY . /app
WORKDIR /app

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
