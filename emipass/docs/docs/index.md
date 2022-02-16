# emipass

Emission WebSocket to SRT passthrough 💨

`emipass` is a [`Node.js`](https://nodejs.org) server that receives WebSocket
audio stream and sends it
as [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport)
stream.

To start the server make sure you have [`npm`](https://www.npmjs.com)
and [`node`](https://nodejs.org) installed, then run:

```sh
npm run start
```

You can send your stream using WebSockets
to [`ws://localhost:10000`](ws://localhost:10000) by default and send your own
audio.
