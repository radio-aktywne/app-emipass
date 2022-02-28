import WRTCServer from "./wrtc.js";
import SRTStream from "./srt.js";

const sourcePort = process.env.EMIPASS_PORT || 10000;
const targetHost = process.env.EMIPASS_TARGET_HOST || "localhost";
const targetPort = process.env.EMIPASS_TARGET_PORT || 9000;
const useStun = process.env.EMIPASS_USE_STUN;

const server = new WRTCServer(sourcePort, useStun);

server.onConnection((channel) => {
  console.log(`Channel ${channel.id}: Connected.`);

  let title = undefined;
  let stream = undefined;

  const startStream = () => {
    if (stream !== undefined) return;
    stream = new SRTStream(targetHost, targetPort, title);
    stream.onError((error) => console.log("Stream STDIN Error", error));
    stream.onData((data) => console.log("Stream STDERR:", data.toString()));
    stream.onExit((code, signal) => {
      console.log("Stream closed, code " + code + ", signal " + signal);
      stream = undefined;
    });
    stream.start();
  };

  const stopStream = () => {
    if (stream === undefined) return;
    stream.stop();
    stream = undefined;
  };

  const setStreamTitle = (t) => (title = t);

  const writeStream = (data) => {
    if (stream !== undefined) stream.write(data);
  };

  channel.on("start", () => {
    console.log(`Channel ${channel.id}: Start.`);
    startStream();
  });

  channel.on("stop", () => {
    console.log(`Channel ${channel.id}: Stop.`);
    stopStream();
  });

  channel.on("title", (t) => {
    console.log(`Channel ${channel.id}: Title: "${t}".`);
    setStreamTitle(t);
  });

  channel.onRaw(writeStream);

  channel.onDisconnect(() => {
    console.log(`Channel ${channel.id}: Disconnected.`);
    stopStream();
  });
});

server.start();
