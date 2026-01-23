from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from tkinter import Tk, filedialog
import os

# =====================
# 単位変換
# =====================
def mm_to_pt(mm):
    return mm * 72 / 25.4

# =====================
# サイズ定義
# =====================
CARD_W_MM = 91
CARD_H_MM = 55

CARD_W_PT = mm_to_pt(CARD_W_MM)
CARD_H_PT = mm_to_pt(CARD_H_MM)

A4_W_PT, A4_H_PT = A4

COLS = int(A4_W_PT // CARD_W_PT)
ROWS = int(A4_H_PT // CARD_H_PT)

# =====================
# 画像選択（1枚）
# =====================
root = Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="名刺画像を選択",
    filetypes=[("Image files", "*.png *.jpg *.jpeg")]
)

if not path:
    raise SystemExit("画像が選択されませんでした")

# =====================
# 画像準備
# =====================
img = Image.open(path).convert("RGB")

# 枠線（裁断ガイド）
draw = ImageDraw.Draw(img)
draw.rectangle(
    [0, 0, img.width - 1, img.height - 1],
    outline=(0, 0, 0),
    width=3
)

img_reader = ImageReader(img)

# =====================
# PDF作成
# =====================
output = os.path.join(os.path.dirname(path), "business_cards_a4.pdf")
pdf = canvas.Canvas(output, pagesize=A4)

for row in range(ROWS):
    for col in range(COLS):
        x = col * CARD_W_PT
        y = A4_H_PT - (row + 1) * CARD_H_PT

        pdf.drawImage(
            img_reader,
            x,
            y,
            width=CARD_W_PT,
            height=CARD_H_PT
        )

pdf.save()

print("PDF作成完了:", output)
print(f"配置枚数: {COLS * ROWS} 枚")
