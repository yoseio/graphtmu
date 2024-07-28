FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        # https://docs.scrapy.org/en/latest/intro/install.html#ubuntu-14-04-or-above
        libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev \
        # https://camelot-py.readthedocs.io/en/master/user/install-deps.html#ubuntu
        ghostscript python3-tk libopencv-dev
