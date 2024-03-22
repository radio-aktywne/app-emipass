---
slug: /config
title: Configuration
---

## Environment variables

You can configure the app at runtime using various environment variables:

- `EMIPASS__SERVER__HOST` -
  host to run the server on
  (default: `0.0.0.0`)
- `EMIPASS__SERVER__PORT` -
  port to run the server on
  (default: `11000`)
- `EMIPASS__STREAMER__HOST` -
  host to listen for connections on
  (default: `0.0.0.0`)
- `EMIPASS__STREAMER__PORTS` -
  ports to select from when listening for connections
  (default: `11001`)
- `EMIPASS__STREAMER__STUN__HOST` -
  host of the STUN server
  (default: `stun.l.google.com`)
- `EMIPASS__STREAMER__STUN__PORT` -
  port of the STUN server
  (default: `19302`)
- `EMIPASS__STREAMER__TIMEOUT` -
  time after which a stream will be stopped if no connections are made
  (default: `PT1M`)
