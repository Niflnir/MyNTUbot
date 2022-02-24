FROM node:17-alpine
WORKDIR /usr
COPY package.json .
COPY package-lock.json .
COPY tsconfig.json .
COPY src ./src
RUN npm ci
RUN npm run build

## this is stage two , where the app actually runs
FROM node:17-alpine
WORKDIR /usr
COPY package.json .
COPY package-lock.json .
RUN npm ci --only=production
COPY --from=0 /usr/dist .
RUN npm install pm2 -g
EXPOSE 3000
CMD ["pm2-runtime","index.js"]
