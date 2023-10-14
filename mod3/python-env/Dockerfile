ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

RUN pip3 install nbmake
RUN pip3 install pytest
RUN pip3 install pylint

WORKDIR /app