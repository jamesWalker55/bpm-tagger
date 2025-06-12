import logging

log = logging.getLogger(__name__)
del logging

import os
from pathlib import Path

from mediafile import (
    MediaField,
    MediaFile,
    MP3StorageStyle,
    MP4StorageStyle,
    StorageStyle,
)
from tempocnn.classifier import TempoClassifier
from tempocnn.feature import read_features
from tqdm import tqdm

MUSIC_DIR = R"D:\Soundtracks\Downloaded Playlist"
MUSIC_EXT = (".m4a", ".opus", ".mp3", ".flac", ".ogg", ".wav", ".aiff")

TEMPO_CLASSIFIER = TempoClassifier("fcn")


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


class FoobarMediaFile(MediaFile):
    # Custom field for foobar2000's BPM field.
    # Also supports floats, unlike the MediaFile's built-in .bpm property
    foobar_bpm = MediaField(
        MP4StorageStyle("----:com.apple.iTunes:BPM"),  # foobar uses uppercase BPM
        # MP4StorageStyle("----:com.apple.iTunes:bpm"), # lowercase is different from uppercase
        MP3StorageStyle("TBPM"),
        StorageStyle("BPM"),
        out_type=str,  # read/write as str intentionally
    )


del MediaFile


def estimate_tempo(path) -> float:
    features = read_features(path)

    return TEMPO_CLASSIFIER.estimate_tempo(features, interpolate=False)


def iter_music_paths(folder):
    for entry in os.scandir(folder):
        path = Path(entry.path)

        # skip if not music file
        if path.suffix.lower() not in MUSIC_EXT:
            continue

        try:
            mf = FoobarMediaFile(path)
        except Exception as e:
            log.error("failed to read bpm info for: %s", path)
            log.exception(e)
            continue

        # check if the file is already tagged with bpm info
        if mf.foobar_bpm is not None:
            continue

        yield path


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--path",
        "-p",
        help="path to the folder containing music files",
        default=MUSIC_DIR,
    )

    return parser.parse_args()


def main():
    setup_logging()

    args = parse_args()

    # filter music files in the folder
    music_paths = list(iter_music_paths(args.path))

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
            mf = FoobarMediaFile(path)
            mf.foobar_bpm = "%d" % round(bpm)
            mf.save()
        except Exception as e:
            log.error("failed to write tempo %s to file: %s", bpm, path)
            log.exception(e)
            continue


if __name__ == "__main__":
    main()
