FROM python:3.12.4-slim-bookworm

ARG JLINK_VERSION=V794e

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /work

COPY requirements.txt /work/

RUN <<EOT
    apt-get -y update
    apt-get -y upgrade
    apt-get -y install wget libusb-1.0-0 dbus
    apt-get clean
    pip install -r requirements.txt
    rm -rf requirements.txt
EOT

# Install Segger J-Link software
ENV LD_LIBRARY_PATH=/opt/SEGGER/JLink/JLink_Linux_${JLINK_VERSION}_x86_64
RUN <<EOT
    wget -q --post-data 'accept_license_agreement=accepted' https://www.segger.com/downloads/jlink/JLink_Linux_${JLINK_VERSION}_x86_64.tgz
    mkdir -p /opt/SEGGER/JLink
    tar -xvf JLink_Linux_${JLINK_VERSION}_x86_64.tgz -C /opt/SEGGER/JLink
    rm JLink_Linux_${JLINK_VERSION}_x86_64.tgz
    ldconfig
EOT

# Install nrfutil device
# Make nrfutil install in a shared location, because when used with GitHub
# Actions, the image will be launched with the home dir mounted from the local
# checkout.
ENV NRFUTIL_HOME=/usr/local/share/nrfutil
RUN <<EOT
    wget -q "https://files.nordicsemi.com/ui/api/v1/download?repoKey=swtools&path=external/nrfutil/executables/x86_64-unknown-linux-gnu/nrfutil&isNativeBrowsing=false" -O nrfutil
    mv nrfutil /usr/local/bin
    chmod +x /usr/local/bin/nrfutil
    nrfutil install device
EOT

# Install mcumgr
RUN <<EOT
    wget -q https://github.com/vouch-opensource/mcumgr-client/releases/download/v0.0.7/mcumgr-client-linux-x86.zip
    python -m zipfile -e mcumgr-client-linux-x86.zip .
    mv mcumgr-client-linux-x86/mcumgr-client /usr/local/bin/mcumgr
    chmod +x /usr/local/bin/mcumgr
    rm -rf mcumgr-client-linux-x86*
EOT
