# Run the down below in terminal to build img1. This will install the requirements.
# docker build -t image1 --target img1 .
# Then run the down below command in terminal.
# docker run image1
FROM python:3.9 as img1
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Run the down below in terminal to build img2. This will install requirements to be able to run MailHog.
# docker build -t image2 --target img2 .
FROM alpine:3.4 as img2
RUN apk --no-cache add \
    ca-certificates
RUN apk --no-cache add --virtual build-dependencies \
    go \
    git \
  && mkdir -p /root/gocode \
  && export GOPATH=/root/gocode \
  && go get github.com/mailhog/MailHog \
  && mv /root/gocode/bin/MailHog /usr/local/bin \
  && rm -rf /root/gocode \
  && apk del --purge build-dependencies

RUN adduser -D -u 1000 mailhog
USER mailhog
WORKDIR /home/mailhog
ENTRYPOINT ["MailHog"]
# Expose the SMTP and HTTP ports:
EXPOSE 1025 8025

# Run the down below in terminal to build imageMailhog. This will install MailHog image with ports.
# docker build -t imageMailhog --target MailHog .
FROM mailhog/mailhog:latest as MailHog

# Run the down below in terminal to build img4. 
# docker build -t image4 --target img4 .
# Then run the down below command in terminal to run the Park app from main.py.
# docker run image4
FROM python:latest as img4
COPY main.py /
CMD [ "python3", "./main.py" ]