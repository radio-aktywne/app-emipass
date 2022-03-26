<h1 align="center">emipass</h1>

<div align="center">

emission webrtc to srt passthrough 💨

[![Testing docker build](https://github.com/radio-aktywne/emipass/actions/workflows/docker-build.yml/badge.svg)](https://github.com/radio-aktywne/emipass/actions/workflows/docker-build.yml)
[![Deploying docs](https://github.com/radio-aktywne/emipass/actions/workflows/docs.yml/badge.svg)](https://github.com/radio-aktywne/emipass/actions/workflows/docs.yml)

</div>

---

`emipass` is a [`Node.js`](https://nodejs.org) server that receives WebRTC audio
stream and sends it
as [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport)
stream.

## Usage

To start the server make sure you have [`npm`](https://www.npmjs.com)
and [`node`](https://nodejs.org) installed, then run:

```sh
npm run start
```

You can send your stream using [`geckos.io`](https://geckosio.github.io)
to [`localhost:11000`](localhost:11000) by default and send your own audio.

## Output

`emipass` sends the output
using [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport/)
to the listener. You need to provide some info about it using environmental
variables:

- `EMIPASS_TARGET_HOST` - address of the host where the target server is running
- `EMIPASS_TARGET_PORT` - port at which the target server is listening
