# -*- coding: utf-8 -*-
"""Prepara as mídias do app de obras: capa, fotos (antes e depois) e vídeos em 720p com pôster.
Uso: python -I scripts/preparar_midia.py   (não refaz o que já existe; apague o arquivo para refazer)"""
import glob
import os
import shutil
import subprocess
import sys

sys.path.insert(0, r"D:\Programas\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.dirname(RAIZ)
NA = r"D:\Haras Rio São José\Auditoria conta Bradesco Jachson 23\Nova Adm Marcelo Julho 2026"
IG = NA + r"\Vendas Novas\Instagram"
BR = NA + r"\Novas Vendas\Novos vídeos drone out 26\brutos"
FF = r"D:\Programas\ffmpeg\bin\ffmpeg"
FOTOS = os.path.join(RAIZ, "assets", "fotos")
VID = os.path.join(RAIZ, "assets", "videos")
os.makedirs(FOTOS, exist_ok=True)
os.makedirs(VID, exist_ok=True)


def foto(origem, nome, larg=1100):
    dst = os.path.join(FOTOS, nome)
    if os.path.exists(dst):
        return
    im = Image.open(origem).convert("RGB")
    if im.width > larg:
        im = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    im.save(dst, quality=80, optimize=True, progressive=True)


# fotos já recortadas e pareadas dos comunicados e da prestação de outubro
for f in glob.glob(os.path.join(PROJ, "administracao-haras", "comunicados", "_fotos_lazer", "*.jpg")):
    b = os.path.basename(f)
    foto(f, b.replace("_1.5", "").replace("_0.75", ""))
for f in glob.glob(os.path.join(PROJ, "administracao-haras", "comunicados", "_fotos_ruas", "*.jpg")):
    foto(f, os.path.basename(f))
for f in glob.glob(os.path.join(PROJ, "planejamento-estrategico", "02-documento", "outubro", "midia", "agua_*.jpg")):
    foto(f, os.path.basename(f))

# capa: a entrada do Haras hoje (drone, out/2026)
capa = os.path.join(RAIZ, "assets", "capa.jpg")
if not os.path.exists(capa):
    tmp = os.path.join(RAIZ, "assets", "_capa.png")
    subprocess.run([FF, "-y", "-v", "error", "-ss", "26", "-i", BR + r"\entrada principal.MP4", "-frames:v", "1",
                    "-vf", "eq=saturation=1.22:contrast=1.06:brightness=0.02", tmp], check=True)
    Image.open(tmp).convert("RGB").save(capa, quality=84, optimize=True, progressive=True)
    os.remove(tmp)

# rede elétrica: quadros de drone com postes, cabos e transformador (out/2026)
ELETRICA = [("Rua 02.MP4", 44), ("rua 12 dois mais baixo.MP4", 46), ("rua 12 dois mais baixo.MP4", 53), ("Rua 07(1).MP4", 28), ("Rua 06.MP4", 35), ("rua 12 retorno.MP4", 38)]
for k, (arq, t) in enumerate(ELETRICA, 1):
    dst = os.path.join(FOTOS, "eletrica_%d.jpg" % k)
    if not os.path.exists(dst):
        tmp = dst + ".png"
        subprocess.run([FF, "-y", "-v", "error", "-ss", str(t), "-i", BR + "\\" + arq, "-frames:v", "1", "-vf", "scale=1280:-2,eq=saturation=1.15:contrast=1.04", tmp], check=True)
        Image.open(tmp).convert("RGB").save(dst, quality=80, optimize=True, progressive=True)
        os.remove(tmp)

# quadra: foto da câmera do início das obras (19/11/2026), enviada pelo Jachson
QUADRA = os.path.join(RAIZ, "fontes", "quadra-inicio-2026-11-19.webp")
if os.path.exists(QUADRA) and not os.path.exists(os.path.join(FOTOS, "quadra_inicio.jpg")):
    im = Image.open(QUADRA).convert("RGB")
    im.crop((4, 0, im.width - 8, im.height - 40)).save(os.path.join(FOTOS, "quadra_inicio.jpg"), quality=84, optimize=True, progressive=True)

# vídeos (id, origem)
VIDEOS = [
    ("por-do-sol", IG + r"\Impulsionar 04-11-2026\Video - E se este por do sol fosse seu.mp4"),
    ("tamanho", IG + r"\Validacao 04-11-2026\Reel - Olha o tamanho desse lugar.mp4"),
    ("agua", IG + r"\Semana 05 a 11-11-2026\Dia 6 - Post - A noticia que todos esperavam.mp4"),
    ("relogio", IG + r"\Semana 05 a 11-11-2026\Dia 2 - Post - O relogio anda mais devagar.mp4"),
    ("onde-fica", IG + r"\Validacao 04-11-2026\Story - Onde fica.mp4"),
]
for f in sorted(glob.glob(IG + r"\Serie Ruas 17-11-2026\Dia *.mp4")):
    n = os.path.basename(f)[9:-4].lower().replace(" ", "-")  # "rua-01", "avenida-umbuzeiro"
    VIDEOS.append((n, f))
def fim_util(src):
    """Segundo em que começa a tela final de venda (fundo verde com 'Chácaras a partir de...' e '% vendido').
    A revista é informativa: os vídeos entram sem essa tela (revisão de compliance de 19/11/2026)."""
    dur = float(subprocess.run([FF[:-6] + "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    t, corte = dur - 0.3, None
    while t > dur - 12:
        raw = subprocess.run([FF, "-v", "error", "-ss", "%.2f" % t, "-i", src, "-frames:v", "1", "-vf", "scale=16:28", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) < 16 * 28 * 3:
            t -= 0.25; continue
        px = [raw[i:i + 3] for i in range(0, len(raw), 3)]
        verdes = sum(1 for r, g, b in px if abs(r - 24) < 26 and abs(g - 56) < 26 and abs(b - 39) < 26)
        if verdes / len(px) > 0.6:
            corte = t
        elif corte is not None:
            break
        t -= 0.25
    return (corte - 0.45) if corte else dur


for vid, src in VIDEOS:
    out = os.path.join(VID, vid + ".mp4")
    if not os.path.exists(out):
        ate = fim_util(src)
        print("  ", vid, "até", round(ate, 1), "s", flush=True)
        subprocess.run([FF, "-y", "-v", "error", "-i", src, "-t", "%.2f" % ate, "-vf", "scale=720:-2", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "28",
                        "-maxrate", "1100k", "-bufsize", "2200k", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    post = os.path.join(VID, vid + ".jpg")
    if not os.path.exists(post):
        t = "6" if vid.startswith(("rua", "avenida")) else "2"
        subprocess.run([FF, "-y", "-v", "error", "-ss", t, "-i", out, "-frames:v", "1", "-vf", "scale=480:-2", "-q:v", "5", post], check=True)
    print(vid, round(os.path.getsize(out) / 1e6, 1), "MB", flush=True)
print("fotos", len(os.listdir(FOTOS)), "· total", round(sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(os.path.join(RAIZ, "assets")) for f in fs) / 1e6, 1), "MB")
