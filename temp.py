import os
from pathlib import Path
import librosa
from mediafile import (
    MediaFile,
    MediaField,
    StorageStyle,
    MP3StorageStyle,
    MP4StorageStyle,
    ASFStorageStyle,
)
import mutagen
import mutagen.mp4
from tqdm import tqdm
from main import estimate_tempo


class FoobarMediaFile(MediaFile):
    foobar_bpm = MediaField(
        MP4StorageStyle("----:com.apple.iTunes:bpm"),
        MP3StorageStyle("TBPM"),
        StorageStyle("BPM"),
        out_type=float,
    )


def main():
    # path = R"D:\Soundtracks\Downloaded Playlist\vishnu okuno - ᴬᴺᴳᴱᴸᵛᵒⁱᵈ ⁽ᴵⁿⁿᵒᶜᵉⁿᶜᵉ⁾ 1894250235859537920.m4a"
    # path = R"D:\Soundtracks\Downloaded Playlist\icesawder - Lie To Me (moyu Remix) 2008854775.m4a"
    # path = R"D:\Soundtracks\Downloaded Playlist\Mestie - keen 2012332259.m4a"

    # (".m4a", ".opus", ".mp3", ".flac", ".ogg", ".wav", ".aiff")
    paths = [
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\420mb 2044019977.m4a",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\Nitro Fun & Desso - Believe Feat. Brenton Mattheus (Rhodz Remix).aiff",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\Piyopiyo 1372590748.wav",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\Track_189 Track_189.ogg",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\xeroc - 2025-02-20_03-37-33.mp3",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\ずっと真夜中でいいのに。『シェードの埃は延長』MV (ZUTOMAYO - SHADE) zjEMFuj23B4.opus",
        R"d:\Soundtracks\Downloaded Playlist\TEMPPPP\幽霊東京 mashup.flac",
    ]
    # bpm = MediaField(
    #     MP3StorageStyle("TBPM"),
    #     MP4StorageStyle("tmpo", as_type=int),
    #     StorageStyle("BPM"),
    #     ASFStorageStyle("WM/BeatsPerMinute"),
    #     out_type=int,
    # )

    # Custom field to make sure editing on foobar2000 will also show up in Mediafile:
    MediaFile.foobar_bpm = MediaField(
        MP4StorageStyle("----:com.apple.iTunes:bpm"),
        MP3StorageStyle("TBPM"),
        StorageStyle("BPM"),
        out_type=float,
    )
    # MediaFile.add_field(
    #     "foobar_bpm",
    #     MediaField(
    #         MP4StorageStyle("----:com.apple.iTunes:bpm"),
    #         MP3StorageStyle("TBPM"),
    #         StorageStyle("BPM"),
    #         out_type=float,
    #     ),
    # )

    for path in paths:
        mf = FoobarMediaFile(path)
        # print(path)
        print(os.path.splitext(path)[-1], mf.title, mf.foobar_bpm, type(mf.foobar_bpm))
        # print(mf.as_dict())

        # x = mutagen.mp4.MP4(path)
        # print(x)
        mf.foobar_bpm = 123.3
        mf.save()


if __name__ == "__main__":
    main()
