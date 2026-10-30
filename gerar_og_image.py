"""Gera a imagem de preview para compartilhamento no WhatsApp, LinkedIn, Discord e Twitter (1200x630px)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "static" / "og-preview.png"

# Dimensões padrão Open Graph
WIDTH = 1200
HEIGHT = 630

# Cria imagem com fundo escuro característico do portfólio
img = Image.new("RGBA", (WIDTH, HEIGHT), (14, 17, 32, 255)) # #0e1120
draw = ImageDraw.Draw(img)

# Desenha gradientes sutis / orbes luminosos
for r in range(260, 0, -5):
    alpha = int(35 * (1 - r / 260))
    draw.ellipse((850 - r, 120 - r, 850 + r, 120 + r), fill=(79, 70, 229, alpha)) # Índigo
    draw.ellipse((200 - r, 500 - r, 200 + r, 500 + r), fill=(56, 189, 248, alpha)) # Sky

# Grade sutil de fundo
for x in range(0, WIDTH, 40):
    draw.line([(x, 0), (x, HEIGHT)], fill=(39, 44, 71, 35), width=1)
for y in range(0, HEIGHT, 40):
    draw.line([(0, y), (WIDTH, y)], fill=(39, 44, 71, 35), width=1)

# Tenta carregar fontes do sistema ou fallback padrão
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 18)
    font_title = ImageFont.truetype("arialbd.ttf", 54)
    font_sub = ImageFont.truetype("arial.ttf", 26)
    font_tech = ImageFont.truetype("arialbd.ttf", 16)
    font_term = ImageFont.truetype("consola.ttf", 18)
    font_footer = ImageFont.truetype("arial.ttf", 20)
except Exception:
    font_badge = font_title = font_sub = font_tech = font_term = font_footer = ImageFont.load_default()

# 1. Badge "Disponível para contratação"
draw.rounded_rectangle([70, 65, 470, 105], radius=20, fill=(35, 37, 80, 220), outline=(139, 134, 255, 120), width=1)
draw.ellipse([88, 81, 98, 91], fill=(74, 222, 128)) # Ponto verde
draw.text((110, 75), "DISPONÍVEL PARA ESTÁGIO & JÚNIOR", font=font_badge, fill=(236, 238, 250))

# 2. Nome do Higor em destaque
draw.text((70, 125), "Higor do Amaral Fritz", font=font_title, fill=(255, 255, 255))

# 3. Subtítulo
draw.text((70, 195), "Desenvolvedor Full Stack & Backend Python/Django", font=font_sub, fill=(139, 134, 255))
draw.text((70, 235), "Graduando em Sistemas de Informação (IFC) com foco em APIs RESTful,", font=font_sub, fill=(160, 168, 196))
draw.text((70, 270), "banco de dados PostgreSQL, segurança web e soluções com IA.", font=font_sub, fill=(160, 168, 196))

# 4. Tags de tecnologias principais
techs = ["Python", "Django", "PostgreSQL", "JavaScript", "Docker / CI-CD", "IA & Hackathon 24h", "Swagger OpenAPI"]
x_pos = 70
y_pos = 325
for tech in techs:
    bbox = draw.textbbox((x_pos, y_pos), tech, font=font_tech)
    w = bbox[2] - bbox[0] + 28
    if x_pos + w > 650:
        x_pos = 70
        y_pos += 42
    draw.rounded_rectangle([x_pos, y_pos, x_pos + w, y_pos + 32], radius=8, fill=(23, 27, 48, 240), outline=(56, 62, 95), width=1)
    draw.text((x_pos + 14, y_pos + 7), tech, font=font_tech, fill=(236, 238, 250))
    x_pos += w + 10

# 5. Card do Terminal na lateral direita
card_x1, card_y1, card_x2, card_y2 = 680, 120, 1130, 480
draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=16, fill=(17, 21, 38, 240), outline=(45, 52, 85), width=2)

# Barra do terminal com 3 bolinhas
draw.line([(card_x1, card_y1 + 42), (card_x2, card_y1 + 42)], fill=(45, 52, 85), width=1)
draw.ellipse([card_x1 + 18, card_y1 + 16, card_x1 + 28, card_y1 + 26], fill=(248, 113, 113))
draw.ellipse([card_x1 + 36, card_y1 + 16, card_x1 + 46, card_y1 + 26], fill=(251, 191, 36))
draw.ellipse([card_x1 + 54, card_y1 + 16, card_x1 + 64, card_y1 + 26], fill=(74, 222, 128))
draw.text((card_x1 + 80, card_y1 + 14), "higor@portfolio: ~/backend", font=font_tech, fill=(160, 168, 196))

# Linhas de código no terminal
term_lines = [
    ("$ python manage.py test", (139, 134, 255)),
    ("✓ 21/21 tests passed (100% OK)", (74, 222, 128)),
    ("", (0, 0, 0)),
    ("$ curl https://portfolio/healthz/", (139, 134, 255)),
    ('{ "status": "healthy", "db": "connected" }', (56, 189, 248)),
    ("", (0, 0, 0)),
    ("$ cat /etc/features.json", (139, 134, 255)),
    ('• Hackathon Fábrica 2k26 (24H)', (255, 255, 255)),
    ('• Swagger OpenAPI 3.0 Live Docs', (255, 255, 255)),
    ('• CI/CD GitHub Actions + PostgreSQL', (255, 255, 255)),
]

ty = card_y1 + 58
for line, color in term_lines:
    if line:
        draw.text((card_x1 + 20, ty), line, font=font_term, fill=color)
    ty += 24

# 6. Rodapé com URL e localização
draw.line([(70, 560), (WIDTH - 70, 560)], fill=(39, 44, 71, 150), width=1)
draw.text((70, 578), "🔗 portfolio-higor.onrender.com", font=font_footer, fill=(56, 189, 248))
draw.text((WIDTH - 420, 578), "📍 Araquari, SC · IFC Câmpus Araquari", font=font_footer, fill=(160, 168, 196))

# Salva a imagem
img.save(OUTPUT_PATH, "PNG")
print(f"Imagem Open Graph gerada com sucesso em: {OUTPUT_PATH}")
