import logging

log = logging.getLogger(__name__)
del logging

import os
from pathlib import Path
import librosa
from mediafile import MediaFile
from tqdm import tqdm

MUSIC_DIR = R"D:\Soundtracks\Downloaded Playlist"
MUSIC_EXT = (".m4a", ".opus", ".mp3", ".flac", ".ogg", ".wav", ".aiff")


def setup_logging():
    import datetime
    import logging

    log.setLevel(logging.DEBUG)

    # Custom log output format
    msg_fmt = "[%(asctime)s %(levelname)s %(name)s.%(funcName)s] %(message)s"
    fmt = logging.Formatter(fmt=msg_fmt)

    # Log to a file
    time_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/{time_string}.log"
    h = logging.FileHandler(log_filename, "w", encoding="utf8")
    h.setLevel(logging.DEBUG)
    h.setFormatter(fmt)
    log.addHandler(h)

    # Log to stdout
    h = logging.StreamHandler()
    h.setLevel(logging.WARNING)
    h.setFormatter(fmt)
    log.addHandler(h)


def estimate_tempo(path) -> float:
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)

    if len(tempo) != 1:
        raise RuntimeError(f"Weird return value from tempo estimation: {tempo!r}")

    return float(tempo[0])


def main():
    setup_logging()

    # filter music files in the folder
    music_paths = [
        entry.path
        for entry in os.scandir(MUSIC_DIR)
        if Path(entry.path).suffix.lower() in MUSIC_EXT
    ]

    for path in tqdm(music_paths):
        log.info(path)

        try:
            bpm = estimate_tempo(path)
        except Exception as e:
            log.error("failed to estimate tempo for: %s", path)
            log.exception(e)
            continue

        log.info("tempo is %f", bpm)

        try:
            mf = MediaFile(path)
            # bpm field only supports integers
            mf.bpm = round(bpm)
            mf.save()
        except Exception as e:
            log.error("failed to write tempo %s to file: %s", bpm, path)
            log.exception(e)
            continue


if __name__ == "__main__":
    main()
