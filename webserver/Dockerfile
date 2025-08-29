FROM node:18-alpine as build

RUN addgroup --gid 10002 appgroup && \
    adduser --uid 10002 --ingroup appgroup --disabled-password --gecos "" appuser

WORKDIR /frontend

ARG REACT_APP_DOCKER_ENV
ENV REACT_APP_DOCKER_ENV=$REACT_APP_DOCKER_ENV
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install
COPY ./frontend/ ./
RUN chown -R appuser:appgroup /frontend
USER 10002
RUN npm run build

FROM nginx:alpine

RUN addgroup --gid 10003 nginxgroup && \
    adduser --uid 10003 --ingroup nginxgroup --disabled-password --gecos "" nginxuser

COPY ./webserver/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/build /usr/share/nginx/html

RUN chown -R nginxuser:nginxgroup /usr/share/nginx/html /etc/nginx/conf.d /var/cache/nginx /var/log/nginx /var/run && \
    touch /var/run/nginx.pid && \
    chown nginxuser:nginxgroup /var/run/nginx.pid

USER 10003
EXPOSE 80