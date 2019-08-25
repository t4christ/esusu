# pull official base image
FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./sites-enabled/default.conf /etc/nginx/conf.d/default.conf