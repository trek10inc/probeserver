FROM amazonlinux:latest

USER root
RUN mkdir -p /opt
WORKDIR /tmp
WORKDIR /

RUN yum update -y && \
    yum install -y python3

RUN yum clean all && rm -rf /var/cache/yum

COPY run.py /tmp

# what do?
CMD [ "/usr/bin/python3", "/tmp/run.py" ]
