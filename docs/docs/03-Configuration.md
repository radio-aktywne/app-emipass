---
slug: /config
title: Configuration
---

## Environment variables

You can configure the app at runtime using various environment variables:

- `EMIPASS__SERVER__HOST` -
  host to run the server on
  (default: `0.0.0.0`)
- `EMIPASS__SERVER__PORTS__HTTP` -
  port to listen for HTTP requests on
  (default: `11000`)
- `EMIPASS__SERVER__PORTS__WHIP` -
  ports to select from when listening for WHIP requests
  (default: `11001`)
- `EMIPASS__SERVER__PORTS__RTP__MIN` -
  minimum port to select from when listening for RTP connections
  (default: `11002`)
- `EMIPASS__SERVER__PORTS__RTP__MAX` -
  maximum port to select from when listening for RTP connections
  (default: `11002`)
- `EMIPASS__SERVER__TRUSTED` -
  trusted IP addresses
  (default: `*`)
- `EMIPASS__STREAMER__STUN__HOST` -
  host of the STUN server
  (default: `stun.l.google.com`)
- `EMIPASS__STREAMER__STUN__PORT` -
  port of the STUN server
  (default: `19302`)
- `EMIPASS__STREAMER__TIMEOUT` -
  time after which a stream will be stopped if no connections are made
  (default: `PT1M`)
- `EMIPASS__DEBUG` -
  enable debug mode
  (default: `false`)
