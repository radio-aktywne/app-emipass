import geckos, { iceServers } from "@geckos.io/server";

export default class WRTCServer {
  constructor(port, useStun = false) {
    this.port = port;
    this.server = geckos({
      portRange: { min: port, max: port },
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
