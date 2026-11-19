# -*- coding: utf-8 -*-
"""Extrai todas as fotos dos relatórios fotográficos do engenheiro (PDFs assinados) para assets/fotos/eng/.
Mesma numeração dos comunicados e da prestação de contas: <chave>_NN = ordem da foto na página.
Uso: python -I scripts/extrair_fotos_engenheiro.py"""
import glob, io, json, os, sys
sys.path.insert(0, r"D:\Programas\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = r"D:\Haras Rio São José\Auditoria conta Bradesco Jachson 23\Nova Adm Marcelo Julho 2026\Engenharia Vailson\Novembro\Assinados Drive"
MIDIA = os.path.join(os.path.dirname(RAIZ), "planejamento-estrategico", "02-documento", "outubro", "midia")
OUT = os.path.join(RAIZ, "assets", "fotos", "eng"); os.makedirs(OUT, exist_ok=True)
CHAVE = {"Banheiro 01": "ban01", "Banheiro 02": "ban02", "Clube": "salao", "Guarita": "guarita", "Quiosque 01": "qui01",
         "Quiosque 02": "qui02", "Quiosque 03": "qui03", "Abastecimento": "agua", "Rua Alagada": "rualag", "pedregulho": "ruaped"}
cont = {}
for f in sorted(glob.glob(os.path.join(ENG, "Relatorio*.pdf"))):
    k = next((v for kk, v in CHAVE.items() if kk in f), None)
    if not k: continue
    doc = pymupdf.open(f); n = 0
    for page in doc:
        infos = []
        for img in page.get_images(full=True):
            for r in page.get_image_rects(img[0]):
                infos.append((round(r.y0 / 20), r.x0, img[0], r))
        for _, _, xref, r in sorted(infos):
            if r.width < 120: continue
            n += 1
            dst = os.path.join(OUT, f"{k}_{n:02d}.jpg")
            if os.path.exists(dst): continue
            pix = pymupdf.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            if max(im.size) > 1100:
                s = 1100 / max(im.size); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            im.save(dst, quality=78, optimize=True, progressive=True)
    cont[k] = n
# registros da administração (primeira rua e rua com pedras)
for f in glob.glob(os.path.join(MIDIA, "rua[12]_*.jpg")) + [os.path.join(MIDIA, "ruaped_adm.jpg")]:
    Image.open(f).convert("RGB").save(os.path.join(OUT, os.path.basename(f)), quality=82)
json.dump(cont, open(os.path.join(RAIZ, "data", "_fotos_eng.json"), "w"), indent=1)
print(cont, "total", sum(cont.values()), "·", round(sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT)) / 1e6, 1), "MB")
# conferência da numeração com a prestação de outubro
def peq(p): return list(Image.open(p).convert("L").resize((24, 18)).getdata())
for nome in ("rualag_01", "ruaped_05", "agua_27", "salao_09", "guarita_21"):
    a, b = peq(os.path.join(OUT, nome + ".jpg")), peq(os.path.join(MIDIA, nome + ".jpg"))
    print(nome, "diferença média", round(sum(abs(x - y) for x, y in zip(a, b)) / len(a), 1))
