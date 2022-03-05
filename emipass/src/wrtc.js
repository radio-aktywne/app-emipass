import geckos, { iceServers } from "@geckos.io/server";

export default class WRTCServer {
  constructor(port, minDataPort, maxDataPort, useStun = false) {
    this.port = port;
    this.server = geckos({
      portRange: { min: minDataPort, max: maxDataPort },
      iceServers: useStun ? iceServers : [],
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
