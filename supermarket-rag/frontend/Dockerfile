FROM node:18-slim

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# Environment variable for runtime
ENV NEXT_PUBLIC_API_URL=https://xfukqtd5pc.us-east-1.awsapprunner.com

# We'll run in dev mode for easy updates as requested
CMD ["npm", "run", "dev"]
