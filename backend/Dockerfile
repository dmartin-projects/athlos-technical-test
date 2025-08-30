FROM python:3.10
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

WORKDIR /backend

RUN python3.10 -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel

COPY requirements/ /backend/requirements/
COPY entrypoint.dev.sh /entrypoint.dev.sh
RUN chmod +x /entrypoint.dev.sh

COPY . /backend/

RUN /py/bin/pip install --no-cache-dir --upgrade -r requirements/development.txt

RUN mkdir -p /tmp/staticfiles
RUN /py/bin/python manage.py collectstatic --noinput

RUN chown -R appuser:appgroup /backend /py

USER 10001
CMD ["/entrypoint.dev.sh"]