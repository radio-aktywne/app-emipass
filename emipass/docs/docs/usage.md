# Usage

To start the server make sure you have [`npm`](https://www.npmjs.com)
and [`node`](https://nodejs.org) installed, then run:

```sh
npm run start
```

You can send your stream using WebSockets
to [`ws://localhost:10000`](ws://localhost:10000) by default and send your own
audio.

If you want to specify the title of your stream then you can do that by adding
path prefix with your title to the connection URL. For example if `emipass` is
running on `localhost` on port `10000` and you want to name your stream `live`,
then you should connect to `ws://localhost:10000/live`.
