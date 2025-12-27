# Frontend Dockerfile for Librilabs Translator
# Uses Node.js version compatible with Next.js 16.0.4

# Stage 1: Dependencies stage
FROM node:20-slim as deps

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Stage 2: Builder stage (for production optimization)
FROM node:20-slim as builder

# Set working directory
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Stage 3: Runtime stage (for production)
FROM node:20-slim as runtime

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy built application from builder stage
COPY --from=builder --chown=appuser:appuser /app/.next ./.next
COPY --from=builder --chown=appuser:appuser /app/public ./public
COPY --from=builder --chown=appuser:appuser /app/package.json ./package.json
COPY --from=builder --chown=appuser:appuser /app/next.config.js ./next.config.js
COPY --from=builder --chown=appuser:appuser /app/tsconfig.json ./tsconfig.json

# Install only production dependencies
COPY --from=deps --chown=appuser:appuser /app/node_modules ./node_modules

# Switch to non-root user
USER appuser

# Expose port 3000
EXPOSE 3000

# Set default command for production
# For development, this will be overridden by docker-compose.yml
CMD ["npm", "start"]

# Stage 4: Development stage (for hot-reload)
FROM node:20-slim as development

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy package files
COPY --chown=appuser:appuser package.json package-lock.json ./

# Install dependencies (will be overridden by volume mount in dev mode)
RUN npm ci

# Copy entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Copy application code
COPY --chown=appuser:appuser . .

# Create .next directory with proper permissions
RUN mkdir -p /app/.next && chown -R appuser:appuser /app/.next

# Switch to non-root user
USER appuser

# Expose port 3000
EXPOSE 3000

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Set default command for development
CMD ["npm", "run", "dev"]

