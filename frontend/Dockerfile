FROM node:15.13-alpine

WORKDIR /portfolio/frontend

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
