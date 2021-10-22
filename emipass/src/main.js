import child_process from 'child_process';
import { WebSocketServer } from 'ws';

const sourcePort = process.env.EMIPASS_SOURCE_PORT || 10000;
const targetHost = process.env.EMIPASS_TARGET_HOST || 'localhost';
const targetPort = process.env.EMIPASS_TARGET_PORT || 9000;

const wss = new WebSocketServer({ port: sourcePort }, () => {
    console.log(`Listening on port ${sourcePort}`)
});

wss.on('connection', (ws, req) => {

    const title = req.url.replace("/", "") || "Unknown";

    const ffmpeg = child_process.spawn('ffmpeg', [
        '-i', '-',
        '-acodec', 'libopus',
        '-f', 'ogg',
        '-metadata', `title=${title}`,
        `srt://${targetHost}:${targetPort}`
    ]);

    ffmpeg.on('close', (code, signal) => {
        console.log('FFmpeg child process closed, code ' + code + ', signal ' + signal);
        ws.terminate();
    });

    ffmpeg.stdin.on('error', (e) => {
        console.log('FFmpeg STDIN Error', e);
    });

    ffmpeg.stderr.on('data', (data) => {
        console.log('FFmpeg STDERR:', data.toString());
    });

    ws.on('message', (msg) => {
        ffmpeg.stdin.write(msg);
    });

    ws.on('close', (e) => {
        ffmpeg.kill('SIGINT');
    });
});
