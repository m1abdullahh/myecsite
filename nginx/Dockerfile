FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./start.sh /usr/src/app/

RUN chmod +x /usr/src/app/start.sh

USER root

CMD [ "/usr/src/app/start.sh" ]