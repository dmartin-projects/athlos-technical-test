FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /backend

RUN python3.10 -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel

COPY requirements/ /backend/requirements/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /backend/