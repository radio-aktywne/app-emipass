import WRTCServer from "./wrtc.js";
import SRTStream from "./srt.js";

const sourcePort = process.env.EMIPASS_PORT || 11000;
const sourceMinDataPort = process.env.EMIPASS_MIN_DATA_PORT || 0;
const sourceMaxDataPort = process.env.EMIPASS_MAX_DATA_PORT || 65535;
const targetHost = process.env.EMIPASS_TARGET_HOST || "localhost";
const targetPort = process.env.EMIPASS_TARGET_PORT || 10000;
const useStun = process.env.EMIPASS_USE_STUN;

const server = new WRTCServer(
  sourcePort,
  sourceMinDataPort,
  sourceMaxDataPort,
  useStun
);

server.onConnection((channel) => {
  console.log(`Channel ${channel.id}: Connected.`);

  let stream = undefined;

  const startStream = (password) => {
    if (stream !== undefined) return;
    stream = new SRTStream({
      host: targetHost,
      port: targetPort,
      password: password
    });
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

  const writeStream = (data) => {
    if (stream !== undefined) stream.write(data);
  };

  channel.on("start", (password) => {
    console.log(`Channel ${channel.id}: Start.`);
    startStream(password);
  });

  channel.on("stop", () => {
    console.log(`Channel ${channel.id}: Stop.`);
    stopStream();
  });

  channel.onRaw(writeStream);

  channel.onDisconnect(() => {
    console.log(`Channel ${channel.id}: Disconnected.`);
    stopStream();
  });
});

server.start();
