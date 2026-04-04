FROM oven/bun:1.3.11-slim

RUN apt-get update && apt-get install -y openjdk-21-jre

RUN bun i -g firebase-tools

WORKDIR /app
COPY . .

CMD ["firebase", "emulators:start", "--import=firebase-data", "--export-on-exit"]