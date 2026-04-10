FROM node:20

WORKDIR /app

# Accept build arguments for environment variables
ARG NEXT_PUBLIC_API_URL=https://alf-zwtq.onrender.com

# Set as environment variables for build
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

RUN npm ci --omit=dev

EXPOSE 3000

CMD ["npm", "start"]
