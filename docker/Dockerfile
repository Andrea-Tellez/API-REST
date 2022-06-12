FROM ubuntu:20.04
LABEL description = 'imagen apirest'
RUN apt update
RUN apt upgrade -y

RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y sqlite3 
RUN pip3 install pytest==7.1.1
RUN pip3 install fastapi==0.78.0
RUN pip3 install uvicorn==0.17.6

