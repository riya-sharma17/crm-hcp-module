# Base image - Node 18 alpine (lightweight)
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for Docker cache)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of code
COPY . .

# Expose port 5173
EXPOSE 5173

# Run Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]