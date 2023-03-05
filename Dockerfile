FROM --platform=linux/amd64 openjdk:19-jdk-alpine
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && apk add --no-cache --virtual=build-dependencies unzip \
    && apk add --no-cache curl

RUN apk add --no-cache python3 \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

RUN pip install --trusted-host pypi.python.org Pygments
RUN pip install --trusted-host pypi.python.org argparse

EXPOSE 8080

COPY build/libs/assignment-0.0.1-SNAPSHOT.jar /app/app.jar
COPY main.py /app/main.py

ENTRYPOINT ["java", "-XX:+UnlockExperimentalVMOptions", "-jar","/app/app.jar"]
