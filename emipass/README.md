<h1 align="center">emipass</h1>

<div align="center">

Emission WebSocket to SRT passthrough 💨

[![Testing docker build](https://github.com/radio-aktywne/emipass/actions/workflows/docker-build.yml/badge.svg)](https://github.com/radio-aktywne/emipass/actions/workflows/docker-build.yml)
[![Deploying docs](https://github.com/radio-aktywne/emipass/actions/workflows/docs.yml/badge.svg)](https://github.com/radio-aktywne/emipass/actions/workflows/docs.yml)

</div>

---

`emipass` is a [`Node.js`](https://nodejs.org) server that receives WebSocket audio stream
and sends it as [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport) stream.

## Usage

To start the server make sure you have [`node`](https://nodejs.org) installed, then `cd` into `src` and run:

```sh
./start.sh
```

You can send your stream using WebSockets to [`ws://localhost:10000`](ws://localhost:10000) by default and send your own audio.

## Output

`emipass` sends the output using [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport/) to the listener.
You need to provide some info about it using environmental variables:

- `EMIPASS_TARGET_HOST` - address of the host where the target server is running
- `EMIPASS_TARGET_PORT` - port at which the target server is listening
