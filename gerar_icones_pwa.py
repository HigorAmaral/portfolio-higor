"""Gera os ícones do PWA (192, 512, maskable e apple-touch-icon) em static/pwa/."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
SAIDA = BASE_DIR / "static" / "pwa"
SAIDA.mkdir(parents=True, exist_ok=True)

FUNDO = (14, 17, 32, 255)      # #0e1120
INDIGO = (79, 70, 229)         # #4f46e5
LILAS = (192, 132, 252)        # #c084fc


def fonte(tamanho):
    for nome in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            continue
    return ImageFont.load_default()


def gradiente(tam):
    """Gradiente diagonal índigo -> lilás."""
    g = Image.new("RGBA", (tam, tam))
    px = g.load()
    for y in range(tam):
        for x in range(tam):
            t = (x + y) / (2 * tam)
            px[x, y] = tuple(int(INDIGO[i] + (LILAS[i] - INDIGO[i]) * t) for i in range(3)) + (255,)
    return g


def gerar(tam, maskable=False, arredondado=True):
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    # Área segura do maskable: o conteúdo fica nos 80% centrais
    margem = 0 if maskable else int(tam * 0.04)
    caixa = (margem, margem, tam - margem, tam - margem)

    mascara = Image.new("L", (tam, tam), 0)
    d = ImageDraw.Draw(mascara)
    if maskable or not arredondado:
        d.rectangle(caixa, fill=255)
    else:
        d.rounded_rectangle(caixa, radius=int(tam * 0.22), fill=255)
    img.paste(Image.new("RGBA", (tam, tam), FUNDO), (0, 0), mascara)

    # Texto "HF" com gradiente
    escala = 0.36 if maskable else 0.44
    f = fonte(int(tam * escala))
    texto = "HF"
    caixa_txt = ImageDraw.Draw(img).textbbox((0, 0), texto, font=f)
    w, h = caixa_txt[2] - caixa_txt[0], caixa_txt[3] - caixa_txt[1]
    pos = ((tam - w) // 2 - caixa_txt[0], (tam - h) // 2 - caixa_txt[1] - int(tam * 0.03))

    mask_txt = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(mask_txt).text(pos, texto, font=f, fill=255)
    img.paste(gradiente(tam), (0, 0), mask_txt)

    # Barrinha de destaque abaixo do texto (estilo "cursor")
    d2 = ImageDraw.Draw(img)
    bw, bh = int(tam * 0.22), max(2, int(tam * 0.035))
    by = pos[1] + caixa_txt[3] + int(tam * 0.06)
    d2.rounded_rectangle(((tam - bw) // 2, by, (tam + bw) // 2, by + bh), radius=bh // 2, fill=LILAS + (255,))
    return img


gerar(192).save(SAIDA / "icon-192.png")
gerar(512).save(SAIDA / "icon-512.png")
gerar(512, maskable=True).save(SAIDA / "icon-maskable-512.png")
gerar(180, arredondado=False).convert("RGB").save(SAIDA / "apple-touch-icon.png")
gerar(32).save(SAIDA / "favicon-32.png")
print("Ícones gerados em", SAIDA)
