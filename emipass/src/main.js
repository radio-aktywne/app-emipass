import child_process from "child_process";
import geckos from "@geckos.io/server";

const sourcePort = process.env.PORT || 10000;
const sourceDataPort = process.env.DATA_PORT || 10001;
const targetHost = process.env.EMIPASS_TARGET_HOST || "localhost";
const targetPort = process.env.EMIPASS_TARGET_PORT || 9000;

const io = geckos({
  portRange: { min: sourceDataPort, max: sourceDataPort },
});

io.listen(sourcePort);

io.onConnection((channel) => {
  const ffmpeg = child_process.spawn("ffmpeg", [
    "-i",
    "-",
    "-acodec",
    "libopus",
    "-f",
    "ogg",
    "-loglevel",
    "debug",
    `srt://${targetHost}:${targetPort}`,
  ]);

  ffmpeg.on("exit", (code, signal) => {
    console.log(
      "FFmpeg child process closed, code " + code + ", signal " + signal
    );
    channel.close().then();
  });

  ffmpeg.stdin.on("error", (e) => {
    console.log("FFmpeg STDIN Error", e);
  });

  ffmpeg.stderr.on("data", (data) => {
    console.log("FFmpeg STDERR:", data.toString());
  });

  channel.onDrop(() => {
    console.log("Message dropped");
  });

  channel.onRaw((rawMessage) => {
    ffmpeg.stdin.write(rawMessage);
  });

  channel.onDisconnect(() => {
    console.log("Channel disconnected");
    ffmpeg.kill("SIGKILL");
  });
});
