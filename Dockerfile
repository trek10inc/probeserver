FROM amazonlinux:latest

USER root
WORKDIR /

RUN yum update -y && \
    yum install -y python3

RUN yum clean all && rm -rf /var/cache/yum

COPY run.py /tmp

# what do?
CMD [ "/usr/bin/python3", "-u", "/tmp/run.py" ]
