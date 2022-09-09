import child_process from "child_process";

export default class SRTStream {
  static DEFAULT_CODEC = "libopus";
  static DEFAULT_FORMAT = "opus";

  constructor({
    host,
    port,
    password = undefined,
    codec = SRTStream.DEFAULT_CODEC,
    format = SRTStream.DEFAULT_FORMAT,
  }) {
    this.host = host;
    this.port = port;
    this.password = password;
    this.codec = codec;
    this.format = format;
    this.ffmpeg = undefined;
  }

  exitCallback = (code, signal) => {};
  errorCallback = (error) => {};
  dataCallback = (data) => {};

  ffmpegArgs() {
    const input = ["-re", "-i", "-"];
    const outputOptions = ["-acodec", this.codec, "-f", this.format];
    const passwordOptions = this.password
      ? ["-passphrase", this.password, "-pbkeylen", this.password.length]
      : [];
    const output = [
      ...outputOptions,
      ...passwordOptions,
      `srt://${this.host}:${this.port}`,
    ];
    return [...input, ...output];
  }

  start() {
    if (this.ffmpeg !== undefined) return;
    this.ffmpeg = child_process.spawn("ffmpeg", this.ffmpegArgs());
    this.ffmpeg.stderr.on("data", (data) => this.dataCallback(data));
    this.ffmpeg.stdin.on("error", (error) => this.errorCallback(error));
    this.ffmpeg.on("exit", (code, signal) => {
      this.exitCallback(code, signal);
      this.ffmpeg = undefined;
    });
  }

  stop() {
    if (this.ffmpeg === undefined) return;
    this.ffmpeg.kill("SIGKILL");
  }

  write(data) {
    if (this.ffmpeg === undefined) return;
    this.ffmpeg.stdin.write(data);
  }

  onExit(callback) {
    this.exitCallback = callback;
  }

  onError(callback) {
    this.errorCallback = callback;
  }

  onData(callback) {
    this.dataCallback = callback;
  }
}
