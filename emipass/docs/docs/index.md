# emipass

emission webrtc to srt passthrough 💨

`emipass` is a [`Node.js`](https://nodejs.org) server that receives WebRTC audio
stream and sends it
as [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport)
stream.

To start the server make sure you have [`npm`](https://www.npmjs.com)
and [`node`](https://nodejs.org) installed, then run:

```sh
npm run start
```

You can send your stream using [`geckos.io`](https://geckosio.github.io)
to [`localhost:11000`](localhost:11000) by default and send your own audio.
