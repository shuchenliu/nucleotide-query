FROM node:22 AS build
LABEL authors="Will Liu"

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build