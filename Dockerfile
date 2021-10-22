FROM node:16.11.1-bullseye-slim AS build

RUN apt-get update && apt-get -y install dumb-init ffmpeg

WORKDIR /emipass/
COPY ./emipass/package*.json ./

RUN npm ci --only=production

USER node
WORKDIR /emipass/src/

COPY --chown=node:node ./emipass/src/ /emipass/src/

ENV NODE_ENV=production \
    EMIPASS_TARGET_HOST=localhost \
    EMIPASS_TARGET_PORT=9000

EXPOSE 10000

ENTRYPOINT ["dumb-init", "/emipass/src/start.sh", "-p", "10000"]
