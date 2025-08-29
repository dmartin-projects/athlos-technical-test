FROM node:lts-alpine3.12 as build

RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

WORKDIR /frontend
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install
COPY ./frontend/ ./
RUN chown -R appuser:appgroup /frontend
USER 10001
RUN npm run build


FROM nginx:1.18.0-alpine

RUN addgroup -g 10002 nginxgroup && \
    adduser -u 10002 -G nginxgroup -s /bin/sh -D nginxuser

COPY ./webserver/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/build /usr/share/nginx/html

RUN chown -R nginxuser:nginxgroup /usr/share/nginx/html /etc/nginx/conf.d /var/cache/nginx /var/log/nginx /var/run && \
    touch /var/run/nginx.pid && \
    chown nginxuser:nginxgroup /var/run/nginx.pid

USER 10002

EXPOSE 80