FROM python:3.10
ENV PYTHONUNBUFFERED=1

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

WORKDIR /backend

RUN python3.10 -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel

COPY requirements/ /backend/requirements/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /backend/
RUN chown -R appuser:appgroup /backend /py

USER appuser

CMD ["/entrypoint.sh"]