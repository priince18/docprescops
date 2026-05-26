# =========================
# Backend Dockerfile (Production Ready with EFS Support)
# =========================

FROM node:18-alpine

# Install required packages
RUN apk add --no-cache bash curl

# App directory
WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy full source
COPY . .
# Environment
ENV NODE_ENV=production
ENV PORT=4000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=5 \
  CMD wget -qO- http://localhost:4000/api/health || exit 1

EXPOSE 4000

CMD ["npm", "run", "server"]