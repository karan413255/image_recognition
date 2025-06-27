FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for dlib and face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    libopenblas-dev \
    libboost-all-dev \
    libssl-dev \
    libffi-dev \
    libpython3-dev \
    python3-pip \
 && wget https://github.com/Kitware/CMake/releases/download/v4.0.3/cmake-4.0.3-linux-aarch64.sh \
 && chmod +x cmake-4.0.3-linux-aarch64.sh \
 && ./cmake-4.0.3-linux-aarch64.sh --skip-license --prefix=/usr/local \
 && rm cmake-4.0.3-linux-aarch64.sh \
 && rm -rf /var/lib/apt/lists/*

# Set environment variables for dlib build
ENV OPENBLAS=/usr/lib
ENV CMAKE_ARGS="-DOPENBLAS_INCLUDE_DIR=/usr/include -DOPENBLAS_LIB=/usr/lib"
ENV ARCHFLAGS="-arch native"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy
RUN pip install --no-binary :all: dlib

COPY backend/ /app

RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
