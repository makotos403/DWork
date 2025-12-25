import subprocess
from pathlib import Path

def create_fadein_music(
    input_path: str,
    prefix: str = "fadein_",
    fade_in_sec: int = 120
):
    in_path = Path(input_path)

    output_path = in_path.with_name(
        f"{prefix}{in_path.stem}{in_path.suffix}"
    )

    suffix = in_path.suffix.lower()

    if suffix == ".mp3":
        codec_args = ["-c:a", "libmp3lame", "-b:a", "192k"]
    elif suffix in (".m4a", ".aac"):
        codec_args = ["-c:a", "aac", "-b:a", "192k"]
    else:
        raise ValueError(f"未対応の形式: {suffix}")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(in_path),

        "-map", "0:a:0",
        "-af", 
        f"afade=t=in:curve=log:st=0:d={fade_in_sec}",

        *codec_args,
        str(output_path)
    ]

    subprocess.run(cmd, check=True)
    return output_path



input_path = r"D:\Download\■TODO_PORN■\WORKbench\A New Morning.mp3"


output = create_fadein_music(
    input_path
)

print(output)
