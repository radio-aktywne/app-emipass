# Usage

To start the server make sure you have [`npm`](https://www.npmjs.com)
and [`node`](https://nodejs.org) installed, then run:

```sh
npm run start
```

You can send your stream using [`geckos.io`](https://geckosio.github.io)
to [`localhost:11000`](localhost:11000) by default and send your own audio.

You can start and stop the stream by emitting `start` and `stop` events. After
the stream started, use raw messages to emit data chunks.

You can also specify the title of the stream (before it starts) by
emitting `title` event and sending the title as data.
