# Este é o Dockerfile do REACT (NODE/NGINX)

# --- Estágio 1: Build ---
FROM node:18-alpine AS build
WORKDIR /app

# Instala dependências do Node
COPY package*.json ./
RUN npm install 

COPY . .
RUN npm run build

# --- Estágio 2: Serve ---
FROM nginx:1.25-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]