FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=5173

EXPOSE 5173
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=5 \
  CMD wget -qO- http://localhost:5173/health || exit 1

CMD ["npm", "run", "dev"]
