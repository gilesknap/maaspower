# python stage: install the maaspower python package
FROM python:3.10-slim AS python

RUN python -m pip install --upgrade pip && \
    pip install maaspower

# build stage: make the uhubctl utility 
FROM gcc:11.2.0 AS build

RUN apt-get update -y && \
    apt-get install -y \
    libusb-1.0-0-dev \
    git

RUN git clone https://github.com/mvp/uhubctl && \
    cd uhubctl && \
    make && \
    make install 

# runtime stage: combine installed maaspower and uhubctl executable
FROM python AS runtime

COPY --from=build /usr/sbin/uhubctl /usr/sbin/uhubctl
COPY --from=build /usr/lib/x86_64-linux-gnu/libusb-1.0* /usr/lib/x86_64-linux-gnu/

ENTRYPOINT [ "maaspower" ]
