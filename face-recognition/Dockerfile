ARG BUILD_FROM
FROM ${BUILD_FROM}

# Gerekli paketler (Alpine tabanli) - sadece gerekli olanlar
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

# Python kutuphaneleri - setuptools ve wheel'i once guncelle
RUN pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel

# Build dependencies (opencv-python-headless icin gerekli)
RUN pip3 install --no-cache-dir --break-system-packages scikit-build cmake ninja

# Requirements dosyasini kopyala (build cache icin erken kopyala)
COPY requirements.txt /tmp/requirements.txt

# Once basit paketleri kur
RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation setuptools wheel numpy paho-mqtt

# dlib'i kur (uzun surebilir - build cache icin ayri adim)
# Not: dlib derlemesi 10-15 dakika surebilir
RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation dlib || \
    (echo "dlib build hatasi, tekrar deneniyor..." && \
     pip3 install --no-cache-dir --break-system-packages --no-build-isolation dlib)

# face_recognition (dlib'e bagli)
RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation face_recognition

# opencv-python-headless (cmake build sorunlari icin alternatif yaklasim)
# Not: opencv derlemesi 5-10 dakika surebilir
# CMake build sorunlarini onlemek icin environment variables
ENV CMAKE_ARGS="-DCMAKE_BUILD_TYPE=Release"
ENV SKBUILD_CONFIGURE_OPTIONS="-DCMAKE_BUILD_TYPE=Release"

# opencv-python-headless kurulumu
# Not: Build isolation olmadan deneme, eger basarisiz olursa build isolation ile dene
RUN pip3 install --no-cache-dir --break-system-packages --no-build-isolation \
    opencv-python-headless==4.8.1.78 || \
    (echo "opencv build hatasi (no isolation), build isolation ile deneniyor..." && \
     pip3 install --no-cache-dir --break-system-packages \
     opencv-python-headless==4.8.1.78) || \
    (echo "opencv build hatasi, daha eski versiyon deneniyor..." && \
     pip3 install --no-cache-dir --break-system-packages --no-build-isolation \
     opencv-python-headless==4.8.0.76)

# Uygulama dosyalari
COPY . /app
WORKDIR /app

# s6-overlay servis yapılandırması
COPY rootfs/ /

# Servis script'lerine execute izni ver
RUN chmod +x /etc/services.d/face-recognition/run
