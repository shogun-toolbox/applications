FROM python:3.5.9-buster

MAINTAINER "Tej Sukhatme"

# Install git
RUN apt-get update
RUN apt-get install -y build-essential cmake
RUN apt-get install -y git
RUN apt-get install -y swig
RUN pip install numpy

RUN git clone --recursive https://github.com/shogun-toolbox/shogun.git && \
    cd shogun && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/installed/shogun-install \
    -DINTERFACE_PYTHON=ON \
    -DBUILD_META_EXAMPLES=OFF \
    -DENABLE_TESTING=OFF \
    -DENABLE_DOXYGEN=OFF \
    -DCMAKE_BUILD_TYPE=Release .. && \
    make install

RUN export LD_LIBRARY_PATH="/installed/shogun-install/dir/lib:$LD_LIBRARY_PATH"
RUN export PYTHONPATH="/installed/shogun-install/dir/lib/python3.5/site-packages/shogun.py:$PYTHONPATH"

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

ENV FLASK_APP influenza_estimator/__init__.py
ENV FLASK_ENV = development
ENV FLASK_DEBUG = 0

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run"]


