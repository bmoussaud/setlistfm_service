FROM python:3.6.2
MAINTAINER Benoit Moussaud <benoit@moussaud.org>

# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/flask/app/web
RUN mkdir -p /home/flask/configuration
WORKDIR /home/flask/app/web

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /home/flask/app/web
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY service /home/flask/app/web/service
COPY run.py /home/flask/app/web

RUN chown -R flask:flaskgroup /home/flask
RUN chmod -R 777 /home/flask

USER flask

EXPOSE 5000
CMD [ "python", "run.py"]