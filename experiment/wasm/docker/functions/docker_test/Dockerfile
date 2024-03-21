# recommend not to use the alpine one, it lacks lots of dependencies
# the slim one ocuppies about 2x space compared to alpine one
# FROM python:3.7-alpine
FROM python:3.7-slim


# fulfill the structure requirement of proxy
RUN mkdir /proxy

# copy libs
COPY main.py /proxy/main.py

WORKDIR /proxy

CMD [ "python3", "/proxy/main.py" ]
