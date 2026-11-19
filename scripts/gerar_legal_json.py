# -*- coding: utf-8 -*-
"""Gera data/legal.json: as 34 glebas registradas (matrícula, área, CCIR, ITR) e a gleba de cada unidade.
Fontes: haras-mapa-app/data/lotes.json (geometria, gleba registrada e matrícula de cada lote) e
planejamento-estrategico/00-insumos/glebas/ccir_itr_34.json. Não leva situação de venda nem nome de cliente.
Uso: python -I scripts/gerar_legal_json.py"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.dirname(RAIZ)
m = json.load(open(os.path.join(PROJ, "haras-mapa-app", "data", "lotes.json"), encoding="utf-8"))
cc = {int(x["g"]): x for x in json.load(open(os.path.join(PROJ, "planejamento-estrategico", "00-insumos", "glebas", "ccir_itr_34.json"), encoding="utf-8"))}


def pts(poly):
    return " ".join("%d,%d" % (round(x), round(y)) for x, y in poly)


def centro(poly):
    return [round(sum(p[0] for p in poly) / len(poly)), round(sum(p[1] for p in poly) / len(poly))]


glebas = []
for g in sorted(m["glebas"], key=lambda x: int(x["id"])):
    n = int(g["id"]); c = cc.get(n, {})
    lotes = sorted(l["id"] for l in m["lotes"] if int(l["gleba"]) == n)
    assert all(l["matricula"] == g["matricula"] for l in m["lotes"] if int(l["gleba"]) == n), n
    glebas.append({"n": n, "mat": g["matricula"], "ha": g.get("area_ha") or c.get("area"), "ccir": c.get("ccir"), "incra": c.get("cod"), "cib": c.get("cib"),
                   "lotes": lotes, "p": pts(g["poly"]), "c": centro(g["poly"])})
lotes = [{"id": l["id"], "g": int(l["gleba"]), "m2": round(l["area"]), "p": pts(l["poly"]), "c": [round(l["c"][0]), round(l["c"][1])]} for l in m["lotes"]]
bb = m["meta"]["bbox"]
out = {"viewbox": [round(bb[0]), round(bb[1]), round(bb[2] - bb[0]), round(bb[3] - bb[1])], "principal": "14.294", "glebas": glebas, "lotes": lotes,
       "vias": [pts(v["poly"]) for v in m.get("vias", []) if isinstance(v, dict) and v.get("poly")]}
dst = os.path.join(RAIZ, "data", "legal.json")
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("glebas", len(glebas), "· lotes", len(lotes), "· com lotes", sum(1 for g in glebas if g["lotes"]), "·", round(os.path.getsize(dst) / 1024), "KB")
print("sem CCIR:", [g["n"] for g in glebas if not g["ccir"]], "· sem CIB:", [g["n"] for g in glebas if not g["cib"]])
print("bbox", bb, "· gleba 1", glebas[0]["mat"], "· gleba 34", glebas[-1]["mat"], len(glebas[-1]["lotes"]))
