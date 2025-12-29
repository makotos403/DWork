import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import os


# --- 代入するファイルをダイアログで指定する -----------------------------------
def select_input_file():
    root = tk.Tk()
    root.withdraw()  # 余計なウィンドウを表示しない

    file_path = filedialog.askopenfilename(
        title="音楽ファイルを選択",
        filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
    )
    return file_path


# --- 代入するファイルのバリデーションチェック -----------------------------------
def check_is_music(file_path: str) -> bool:
    """
    後工程に渡してよい音楽ファイルかどうかを判定する
    """
    if not file_path:
        return False

    if not os.path.isfile(file_path):
        return False

    music_extensions = {
        ".mp3", ".wav", ".flac", ".aac",
        ".ogg", ".m4a", ".wma", ".aiff"
    }

    _, ext = os.path.splitext(file_path)
    return ext.lower() in music_extensions


# --- フェードイン加工 -----------------------------------
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
        # f"afade=t=in:curve=log:st=0:d={fade_in_sec}",
        "afade=t=in:curve=tri:st=0:d=10",

        *codec_args,
        str(output_path)
    ]

    subprocess.run(cmd, check=True)
    return output_path


# ==================================================================
# === MAIN =========================================================
# ==================================================================
def main():

    input_path = select_input_file()

    is_music = check_is_music(input_path)
    if not is_music:
        return ("音楽ファイルを参照してね")


    output = create_fadein_music(
        input_path
    )

    print(output)


# ==================================================================
if __name__ == "__main__":
    main()

