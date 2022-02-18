# Output

`emipass` sends the output
using [`SRT`](https://www.haivision.com/products/srt-secure-reliable-transport/)
to the listener. You need to provide some info about it using environmental
variables:

- `EMIPASS_TARGET_HOST` - address of the host where the target server is running
- `EMIPASS_TARGET_PORT` - port at which the target server is listening
