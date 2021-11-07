import child_process from 'child_process';
import geckos from '@geckos.io/server';

const sourcePort = process.env.EMIPASS_SOURCE_PORT || 10000;
const minSourceDataPort = process.env.EMIPASS_MIN_SOURCE_DATA_PORT || 10001;
const maxSourceDataPort = process.env.EMIPASS_MAX_SOURCE_DATA_PORT || 10099;
const targetHost = process.env.EMIPASS_TARGET_HOST || 'localhost';
const targetPort = process.env.EMIPASS_TARGET_PORT || 9000;

const io = geckos({ portRange: { min: minSourceDataPort, max: maxSourceDataPort } });

io.listen(sourcePort);

io.onConnection(channel => {

    const ffmpeg = child_process.spawn('ffmpeg', [
        '-i', '-',
        '-acodec', 'libopus',
        '-f', 'ogg',
        `srt://${targetHost}:${targetPort}`
    ]);

    ffmpeg.on('close', (code, signal) => {
        console.log('FFmpeg child process closed, code ' + code + ', signal ' + signal);
        channel.close();
    });

    ffmpeg.stdin.on('error', (e) => {
        console.log('FFmpeg STDIN Error', e);
    });

    ffmpeg.stderr.on('data', (data) => {
        console.log('FFmpeg STDERR:', data.toString());
    });

    channel.onRaw(rawMessage => {
        ffmpeg.stdin.write(rawMessage);
    });

    channel.onDisconnect(() => {
        ffmpeg.kill('SIGINT');
    });
});
