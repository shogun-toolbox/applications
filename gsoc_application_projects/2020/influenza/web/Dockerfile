FROM python:3.5.9-buster

MAINTAINER "Tej Sukhatme"

RUN apt-get update && \
    apt-get install -y build-essential cmake && \
    apt-get install -y git && \
    apt-get install -y swig && \
    apt-get install -y ctags && \
    pip install numpy ply && \
    git clone --recursive https://github.com/shogun-toolbox/shogun.git && \
    cd shogun && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/installed/shogun-install \
    -DINTERFACE_PYTHON=ON \
    -DBUILD_META_EXAMPLES=OFF \
    -DENABLE_TESTING=ON \
    -DENABLE_DOXYGEN=OFF \
    -DCMAKE_BUILD_TYPE=Release .. && \
    make install

ENV LD_LIBRARY_PATH=/installed/shogun-install/lib/
ENV PYTHONPATH=/installed/shogun-install/lib/python3.5/site-packages/

RUN pip install --upgrade pip

COPY . /

RUN pip --no-cache-dir install -r requirements.txt

ENV FLASK_APP=influenza_estimator
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
