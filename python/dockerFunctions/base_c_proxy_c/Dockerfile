# recommend not to use the alpine one, it lacks lots of dependencies
# the slim one ocuppies about 2x space compared to alpine one
# FROM python:3.7-alpine
FROM ubuntu:latest

# fulfill the structure requirement of proxy
RUN mkdir /proxy

# copy libs
COPY build/proxy /proxy/proxy

WORKDIR /proxy

# proxy server runs under port 5000
EXPOSE 5000


CMD [ "/proxy/proxy" ]
