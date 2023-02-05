FROM alpine:latest

USER root
WORKDIR /

RUN apk update && \
    apk add python3 && \
    rm -rf /var/cache/apk/*

COPY run.py /tmp

# what do?
CMD [ "/usr/bin/python3", "-u", "/tmp/run.py" ]
