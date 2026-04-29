FROM oven/bun:1.3.13-alpine

RUN apk add openjdk21-jre-headless
RUN bun i -g firebase-tools

WORKDIR /app

COPY . .

CMD ["firebase", "emulators:start", "--import=firebase-data", "--export-on-exit"]