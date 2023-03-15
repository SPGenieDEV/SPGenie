#Use working directory /app
FROM nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04

# Set up environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda with Python 3.8.13
RUN curl -sL https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -o ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Create a new Conda environment
RUN /opt/conda/bin/conda create -y --name flask_ev python=3.8.13 && \
    /opt/conda/bin/conda activate flask_env && \
    /opt/conda/bin/conda install -y -c anaconda flask && \
    /opt/conda/bin/conda install -y -c anaconda tensorflow-gpu


#Copy all the content of current directory to /app
ADD . /app

#Installing required packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Open port 5000
EXPOSE 5000

#Set environment variable
ENV NAME OpentoAll

#Run python program
CMD ["python","app.py"]