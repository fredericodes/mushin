# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ui/package*.json ./
RUN npm install
COPY ./ui .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./ui/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]