FROM oven/bun:1.3.11-slim

WORKDIR /app

COPY package.json bun.lock ./

RUN bun install

COPY . .

CMD ["bun", "dev"]