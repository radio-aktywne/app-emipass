import geckos from "@geckos.io/server";

export default class WRTCServer {
  constructor(port) {
    this.port = port;
    this.server = geckos({
      portRange: { min: port, max: port },
    });
    this.server.onConnection((channel) => this.connectionCallback(channel));
  }

  start() {
    this.server.listen(this.port);
  }

  connectionCallback = (channel) => {};

  onConnection(callback) {
    this.connectionCallback = callback;
  }
}
