---
slug: /usage
title: Usage
---

## Requesting a stream

You can request a stream by sending a `POST` request to the `/stream` endpoint.
The request body should contain the information
about the target to send the stream to.
See the API documentation for more details.

For example, you can use [`curl`](https://curl.se) to do that:

```sh
curl \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"srt": {"host": "example.com", "port": 12345}}' \
    http://localhost:11000/stream
```

You should receive a response containing the port number and STUN server
that you can use to connect to the stream and start sending audio.

## Sending audio

You can send audio to stream using any
[`WHIP`](https://www.ietf.org/archive/id/draft-ietf-wish-whip-01.html)
client.

Remember to use the port you received in the previous step
to connect to the stream.

For example, from the browser you can do that using the
[`@eyevinn/whip-web-client`](https://www.npmjs.com/package/@eyevinn/whip-web-client)
package:

```js
import { WHIPClient } from "@eyevinn/whip-web-client";

const endpoint = "http://localhost:11001/whip/endpoint";
const client = new WHIPClient({ endpoint });
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

await client.setIceServersFromEndpoint();
await client.ingest(stream);
```

Alternatively, from the server side,
you can use [`GStreamer`](https://gstreamer.freedesktop.org) for that:

```sh
gst-launch-1.0 \
    audiotestsrc \
    ! \
    audioconvert \
    ! \
    audioresample \
    ! \
    audio/x-raw \
    ! \
    queue \
    ! \
    whipclientsink \
    signaller::whip-endpoint="http://localhost:11001/whip/endpoint"
```

## Ping

You can check the status of the app by sending
either a `GET` or `HEAD` request to the `/ping` endpoint.
The app should respond with a `204 No Content` status code.

For example, you can use `curl` to do that:

```sh
curl \
    --request HEAD \
    --head \
    http://localhost:11000/ping
```
