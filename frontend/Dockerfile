FROM node:20-alpine
WORKDIR /app
COPY frontend/ /app
RUN npm install && npm run build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
