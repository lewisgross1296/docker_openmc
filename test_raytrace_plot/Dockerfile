FROM ubuntu:20.04

# Add non root user to system
RUN useradd -s /bin/bash lewis

## Commands that need to be run from root
# install software where apt-get is sufficient as root user
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
        git \
        wget \
        vim \
        xz-utils \
        gcc \
        make \
        autoconf \
        python3 \
        python3-distutils \
        python3-dev \
        python3-pip \
        flex \
        bison \
        libssl-dev \
        build-essential \
        libtool \
        libpng-dev

# pip installable packages
RUN pip install python-config numpy matplotlib

# install tzdata before the next package set
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Chicago apt-get -y install tzdata

# packages that need to be installed after tzdata is properly installed
RUN apt-get install -y \
        mpich libmpich-dev \
        openmpi-bin libopenmpi-dev \
        pkg-config

RUN pip install --upgrade cmake

# set alternative so that python runs python 3 code without installing python 2
# the arguments are as follows:
# RUN update-alternatives --install </path/to/alternative> <name> </path/to/source> <priority>
RUN update-alternatives --install /usr/local/bin/python python /usr/bin/python3 99

# create directorries needed for dependencies, data, the openmc repo, and the test_depltion simulation
RUN mkdir /home/software && \
    mkdir /home/software/openmc && \
    mkdir /home/software/temp && \
    mkdir /home/lewis && \
    mkdir /home/lewis/cross_sections && \
    mkdir /home/lewis/test_depletion

# Make lewis the owner of /home/lewis and /home/softawre to avoid permisisons issues
RUN chown -R lewis /home/lewis
RUN chown -R lewis /home/software

COPY hdf5-1_13_2.tar.gz /home/software/temp

# build hdf5 and install in /home/software/hdf5
RUN mkdir /home/software/hdf5 && \
    cd /home/software/temp && \
    tar -xvf hdf5-1_13_2.tar.gz && \
    cd hdf5-hdf5-1_13_2 && \
    mkdir build && \
    cd build && \
    ../configure --prefix="/home/software/hdf5" --enable-optimization=high --enable-shared  --enable-hl --enable-build-mode=production --enable-parallel && \
    make -j8 && \
    make install && \
    rm -rf /home/software/temp/*

# HDF5 env vars
ENV HDF5_ROOT /home/software/hdf5
ENV HDF5_INCLUDE_DIR /home/software/hdf5/include
ENV HDF5_LIBDIR /home/software/hdf5/lib
ENV METHOD opt

## Change user so that non-root user is running MPI
USER lewis

WORKDIR /home/lewis

# obtain and unpack cross sections from ANL Box (ENDFB-vii), point environment variable to correct
RUN wget -q -O - https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz | tar -C cross_sections -xJ
ENV OPENMC_CROSS_SECTIONS /home/lewis/cross_sections/endfb-vii.1-hdf5/cross_sections.xml

# # clone openmc
RUN git clone -b raytrace_plots --single-branch --recurse-submodules https://github.com/gridley/openmc.git
WORKDIR /home/lewis/openmc

# build and install OpenMC
RUN mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/home/software/openmc -DOPENMC_USE_MPI=ON -DCMAKE_BUILD_TYPE=Debug .. && \
    make install -j8

RUN rm -rf /home/software/temp

RUN pip install .

RUN mkdir /home/lewis/test_rayrace_plot
COPY *.xml /home/lewis/test_rayrace_plot
WORKDIR /home/lewis/test_rayrace_plot