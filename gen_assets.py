"""AllThatAI 랜딩 브랜드 에셋 생성 — favicon(ico/png/svg), apple-touch, og-image.
구글 검색 결과의 '허접한 지구본'을 브랜드 아이콘으로 교체하고, 공유 카드(OG)를 만든다.
"""
from PIL import Image, ImageDraw, ImageFont
import math

ACCENT = (0, 200, 255)      # #00c8ff
ACCENT2 = (124, 58, 237)    # #7c3aed
INK = (8, 12, 20)           # #080c14
TEXT = (226, 234, 245)      # #e2eaf5
MUTED = (90, 122, 154)      # #5a7a9a

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diagonal_gradient(size):
    """135deg cyan→purple 그라디언트."""
    w, h = size, size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h - 2)
            px[x, y] = lerp(ACCENT, ACCENT2, t)
    return img

def rounded_mask(size, radius_ratio=0.225):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    r = int(size * radius_ratio)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    return m

def font(path, sz):
    return ImageFont.truetype(path, sz)

ARIALBD = "C:/Windows/Fonts/arialbd.ttf"
MALGUNBD = "C:/Windows/Fonts/malgunbd.ttf"
MALGUN = "C:/Windows/Fonts/malgun.ttf"
CONSOLA = "C:/Windows/Fonts/consolab.ttf"

def make_icon(size):
    """그라디언트 라운드 사각형 + 짙은 'A'."""
    grad = diagonal_gradient(size)
    mask = rounded_mask(size)
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    icon.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(icon)
    f = font(ARIALBD, int(size * 0.62))
    txt = "A"
    bb = d.textbbox((0, 0), txt, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), txt, font=f, fill=INK)
    return icon

# ── favicon set ──
master = make_icon(512)
master.save("favicon-512.png")
make_icon(192).save("favicon-192.png")
make_icon(180).save("apple-touch-icon.png")
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
master.save("favicon.ico", sizes=ico_sizes)
print("favicon set OK")

# ── OG image 1200x630 ──
W, H = 1200, 630
og = Image.new("RGB", (W, H), INK)
# 은은한 radial glow 2개
glow = Image.new("RGB", (W, H), INK)
gp = glow.load()
for y in range(H):
    for x in range(W):
        d1 = math.hypot(x - 180, y - 120) / 520
        d2 = math.hypot(x - 1050, y - 60) / 560
        c = list(INK)
        if d1 < 1:
            for i in range(3):
                c[i] = min(255, c[i] + int((ACCENT[i]) * 0.10 * (1 - d1)))
        if d2 < 1:
            for i in range(3):
                c[i] = min(255, c[i] + int((ACCENT2[i]) * 0.10 * (1 - d2)))
        gp[x, y] = tuple(c)
og = glow
d = ImageDraw.Draw(og)
# 그리드 라인(아주 옅게)
for gx in range(0, W, 48):
    d.line([(gx, 0), (gx, H)], fill=(14, 22, 36), width=1)
for gy in range(0, H, 48):
    d.line([(0, gy), (W, gy)], fill=(14, 22, 36), width=1)

PAD = 80
# 로고 마크
mark = make_icon(96)
og.paste(mark, (PAD, PAD), mark)
fwm = font(ARIALBD, 46)
d.text((PAD + 116, PAD + 20), "AllThatAI", font=fwm, fill=TEXT)
fkick = font(CONSOLA, 20)
d.text((PAD + 118, PAD + 6), "PORTFOLIO · 2026", font=fkick, fill=ACCENT)

# 헤드라인 (한글 — Malgun Bold)
fh = font(MALGUNBD, 72)
d.text((PAD, 250), "실전 AI 프로덕트를", font=fh, fill=TEXT)
# 강조 줄
fh2 = font(MALGUNBD, 72)
d.text((PAD, 338), "꾸준히 빌드합니다.", font=fh2, fill=ACCENT)

# 프로젝트 칩 라인
fsub = font(MALGUN, 30)
d.text((PAD, 470), "AuraView · MetroEyes · LexPulse · WageGuard · LoL Butler", font=fsub, fill=MUTED)
# 도메인
fdom = font(CONSOLA, 26)
d.text((PAD, 525), "allthatai.kr", font=fdom, fill=ACCENT)

og.save("og-image.png", quality=92)
print("og-image OK", og.size)
