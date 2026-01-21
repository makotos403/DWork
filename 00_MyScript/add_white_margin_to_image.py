from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog

from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox


def add_white_margin_to_image(
    pixels: int,
    position: str,
    prefix: str = "margin_"
):
    """
    指定した方向に白い余白を追加した画像を保存する
    """

    # --- ファイル選択ダイアログ ---
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")
        ]
    )

    if not file_path:
        return None

    img_path = Path(file_path)
    img = Image.open(img_path)

    width, height = img.size

    if position == "top":
        new_size = (width, height + pixels)
        paste_pos = (0, pixels)

    elif position == "bottom":
        new_size = (width, height + pixels)
        paste_pos = (0, 0)

    elif position == "left":
        new_size = (width + pixels, height)
        paste_pos = (pixels, 0)

    elif position == "right":
        new_size = (width + pixels, height)
        paste_pos = (0, 0)

    else:
        raise ValueError("position は top / bottom / left / right のいずれか")

    # --- 白背景のキャンバス作成 ---
    new_img = Image.new("RGB", new_size, (255, 255, 255))
    new_img.paste(img, paste_pos)

    # --- 保存 ---
    output_path = img_path.with_name(prefix + img_path.name)
    new_img.save(output_path)

    return output_path


# ==========================================================
# GUI
# ==========================================================
def main():

    root = tk.Tk()
    root.title("画像に白い余白を追加")

    # --- pixel入力 ---
    tk.Label(root, text="余白ピクセル数").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    pixel_var = tk.StringVar(value="100")
    tk.Entry(root, textvariable=pixel_var, width=10).grid(row=0, column=1, pady=5)

    # --- position ラジオボタン ---
    tk.Label(root, text="余白を追加する位置").grid(row=1, column=0, sticky="w", padx=10)

    position_var = tk.StringVar(value="top")

    positions = ["top", "bottom", "left", "right"]
    for i, pos in enumerate(positions):
        tk.Radiobutton(
            root,
            text=pos,
            value=pos,
            variable=position_var
        ).grid(row=1, column=1 + i, sticky="w")

    # --- prefix入力 ---
    tk.Label(root, text="ファイル名 prefix").grid(row=2, column=0, sticky="w", padx=10, pady=5)

    prefix_var = tk.StringVar(value="addmargin_")
    tk.Entry(root, textvariable=prefix_var, width=20).grid(row=2, column=1, columnspan=4, sticky="w")

    # --- 実行ボタン ---
    def on_execute():
        try:
            pixels = int(pixel_var.get())
            position = position_var.get()
            prefix = prefix_var.get()

            output = add_white_margin_to_image(
                pixels,
                position,
                prefix
            )

            if output:
                messagebox.showinfo(
                    "完了",
                    f"画像を保存しました\n{output}"
                )

        except ValueError as e:
            messagebox.showerror("エラー", str(e))

    tk.Button(root, text="画像ファイルを参照して実行", command=on_execute, width=20).grid(
        row=3, column=0, columnspan=5, pady=15
    )

    root.mainloop()


# ==========================================================
if __name__ == "__main__":
    main()
