ARG NODE_IMAGE_TAG=16.11.1-bullseye-slim

FROM node:$NODE_IMAGE_TAG

RUN apt-get update && apt-get -y install dumb-init ffmpeg

WORKDIR /emipass/
COPY ./emipass/package*.json ./

RUN npm ci --only=production

USER node
WORKDIR /emipass/src/

COPY --chown=node:node ./emipass/src/ /emipass/src/

ENV NODE_ENV=production \
    EMIPASS_PORT=11000 \
    EMIPASS_MIN_DATA_PORT=0 \
    EMIPASS_MAX_DATA_PORT=65535 \
    EMIPASS_TARGET_HOST=localhost \
    EMIPASS_TARGET_PORT=10000

EXPOSE 11000
EXPOSE 0-65535/udp

ENTRYPOINT ["dumb-init", "npm", "run", "start"]
