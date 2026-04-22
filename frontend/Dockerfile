# -------- BUILD STAGE --------
FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build || true


# -------- RUNTIME STAGE --------
FROM node:18-slim

WORKDIR /app

# Copy app FIRST (as root)
COPY --from=builder /app ./

# Install production dependencies as root
RUN npm install --omit=dev

# THEN create non-root user
RUN useradd -m nodeuser

# Fix permissions
RUN chown -R nodeuser:nodeuser /app

# Switch to non-root user
USER nodeuser

# Environment variables
ENV API_URL=http://localhost:8000
ENV PORT=3000

EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:3000 || exit 1

CMD ["node", "app.js"]