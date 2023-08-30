# Set base image (host OS)
FROM ubuntu

# By default, listen on port 3000
EXPOSE 3000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install Flask && \
    apt-get -y install wget && \
    apt-get -y install gcc-multilib
    # && apt install build-essential
RUN wget "https://www.mrc-bsu.cam.ac.uk/wp-content/uploads/2018/04/OpenBUGS-3.2.3.tar.gz"
RUN tar zxvf OpenBUGS-3.2.3.tar.gz
RUN cd OpenBUGS-3.2.3 \
    && ./configure \
    && make \
    && make install

# # Copy the content of the local src directory to the working directory
# COPY app.py .
# COPY data.txt .
# COPY execute.py .
# COPY inits1.txt .
# COPY inits2.txt .
# COPY model.txt .
# COPY script.txt .
copy . . 

# # Specify the command to run on container start
CMD [ "python3", "./app.py" ]