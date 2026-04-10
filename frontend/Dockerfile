FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

RUN npm ci --omit=dev

EXPOSE 3000

CMD ["npm", "start"]
