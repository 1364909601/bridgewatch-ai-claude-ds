# ============================================================
# Stage 1: Build frontend static files
# ============================================================
FROM node:20-alpine AS builder

WORKDIR /app
COPY bridgewatch-ai/package.json bridgewatch-ai/package-lock.json ./
RUN npm ci
COPY bridgewatch-ai/ .
RUN npm run build

# ============================================================
# Stage 2: Serve with nginx
# ============================================================
FROM nginx:alpine

# Copy custom nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built frontend
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
