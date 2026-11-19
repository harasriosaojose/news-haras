# -*- coding: utf-8 -*-
"""Gera data/obras.json: textos, percentuais, pares de fotos e vídeos do app de obras.
Posição de 31/10/2026 (planilha do engenheiro) e textos dos comunicados de 11 e 19/11/2026.
Uso: python -I scripts/gerar_obras_json.py"""
import json
import os
import sys

sys.path.insert(0, r"D:\Programas\pylibs")
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J, O, N, A = "jul/2026", "out/2026", "nov/2026", "ago/2026"


def P(t, a, ad, d, dd, ra="ANTES", rd="DEPOIS"):
    return {"titulo": t, "antes": a + ".jpg", "antes_data": ad, "depois": d + ".jpg", "depois_data": dd, "rot_a": ra, "rot_d": rd}


app = {
    "nome": "News Haras",
    "subtitulo": "Acompanhamento das obras",
    "edicao": "Edição nº 1 · Novembro de 2026",
    "saudacao": "Que bom ter você aqui.",
    "frase": "A revista eletrônica do Haras Rio São José. Aqui você acompanha cada obra, com fotos de antes e depois e vídeos.",
    "rotulo_geral": "Andamento geral das obras",
    "referencia": "31/10/2026",
    "atualizado_em": "19/11/2026",
    "geral_pct": 70.2,
    "geral_anterior_pct": 47.3,
    "geral_anterior_ref": "setembro",
    "ressalva": "As datas são previsões, que podem mudar com o clima, o ritmo da execução e a entrega dos fornecedores.",
    "fonte": "Percentuais e fotos: relatórios do engenheiro responsável pela fiscalização das obras. Data e local impressos em cada foto.",
    "whatsapp": "5511991468192",
    "whatsapp_exibir": "(11) 99146-8192",
    "prazo_resposta": "até 2 dias úteis",
    "link_mapa": "https://harasriosaojose.github.io/haras-rio-sao-jose-mapa/",
    "link_agua": "https://tinyurl.com/redeaguahrsj",
    "forms": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSf0_R9CZf0G_zQcSY0XKL4_RTH1dXQCsdmIEQtppkrQAfIU8Q/formResponse",
        "tipo": "entry.1956310174", "nome": "entry.2065328925", "unidade": "entry.2033854769",
        "telefone": "entry.1310959149", "mensagem": "entry.631070095",
    },
    "nesta_edicao": [
        {"t": "Energia: faltam duas etapas, e as duas cabem à Coelba", "ir": "#energia"},
        {"t": "Rede de água: a parte do empreendimento está 100% concluída", "ir": "#agua"},
        {"t": "Clube-salão chega a 75,6%, com antes e depois", "ir": "#obras"},
        {"t": "Mais de 200 fotos do engenheiro e 17 vídeos", "ir": "#videos"},
    ],
}

eletrica = {
    "selo": "Prioridade número 1",
    "titulo": "Energia elétrica: onde estamos",
    "lead": "A ligação da energia é o pedido mais frequente dos clientes e é a nossa prioridade. A rede está instalada, e a parte que cabia ao empreendimento foi feita.",
    "feito": [
        "Rede instalada: 215 postes e 13 transformadores",
        "Vistoria da Coelba realizada: a rede de alta e de baixa tensão foi aprovada, com pedido de ajustes pontuais",
        "Ajustes a cargo do empreendimento concluídos, com a limpeza e a regularização de ruas",
        "Nova visita solicitada à Coelba",
    ],
    "falta_titulo": "Faltam apenas duas etapas, e as duas cabem à Coelba",
    "falta": [
        {"n": "1", "t": "Vistoria final", "d": "É a etapa em que estamos. A Coelba valida os pontos já regularizados."},
        {"n": "2", "t": "Energização da rede", "d": "É a ligação da energia, a última etapa."},
    ],
    "semana": "Toda semana o empreendimento pede um posicionamento à Coelba. A concessionária tem prazos próprios e não informa o dia da visita. Por isso, não há data para a ligação.",
    "protocolos": "Protocolos da obra na Coelba: Nota de Análise 9201518140 · Nota de Incorporação 9102424512",
}

agua = {
    "selo": "Entregue",
    "titulo": "Rede de água: a parte do empreendimento está 100% concluída",
    "lead": "A rede de água dos poços artesianos foi concluída em 30/10/2026.",
    "entregue": ["3 poços artesianos", "4 reservatórios, com 140 mil litros", "2 redes principais, uma em cada avenida", "Bombeamento com energia solar"],
    "agora_titulo": "E o trabalho continua",
    "agora": "A administração da rede e a ligação da água para os lotes também estão sendo feitas pelo empreendimento, em conjunto com a Associação.",
    "botao": "Cadastro para a ligação da água",
}

obras = [
    {"id": "clube-salao", "nome": "Clube-salão de festas", "curto": "Clube-salão", "pct": 75.6, "situacao": "execucao",
     "previsao": "até o fim de dezembro de 2026", "capa": "salao_09.jpg",
     "resumo": "O espaço para reunir a família e os amigos já tem piso, pintura, janelas e portas.",
     "feito": ["Piso cerâmico em todos os ambientes", "Pintura interna e externa", "Instalações elétricas e de água", "Janelas de vidro, portas e varanda"],
     "falta": ["Parte do esgotamento sanitário, que está em execução", "Divisórias e pias dos banheiros", "Mobiliário e equipamentos"],
     "blocos": [
         {"titulo": "Área externa e salão", "modo": "deslizar", "itens": [
             P("Fachada principal", "salao_01", J, "salao_09", O),
             P("Salão, com piso, pintura e porta de vidro", "salao_03", J, "salao_11", O)]},
         {"titulo": "Fachada lateral", "modo": "lado", "itens": [P("Fachada lateral, com janelas e varanda", "salao_02", J, "salao_10", O)]},
         {"titulo": "Ambientes internos", "modo": "deslizar", "itens": [
             P("Cozinha, com piso, pintura e bancada", "salao_04", J, "salao_14", N),
             P("Sanitário, com piso, pintura e louça", "salao_06", J, "salao_16", N),
             P("Janela de vidro instalada", "salao_08", J, "salao_15", N)]}]},
    {"id": "sanitarios", "nome": "Sanitários 01 e 02", "curto": "Sanitários", "pct": 67.9, "situacao": "execucao",
     "previsao": "até o fim de dezembro de 2026", "capa": "ban01_09.jpg",
     "resumo": "Os dois sanitários da área de lazer já estão revestidos, pintados e com as louças.",
     "feito": ["Revestimento e pintura", "Instalações elétricas e de água", "Louças e chuveiros", "Rampa de acesso"],
     "falta": ["Parte das esquadrias", "Parte do esgotamento sanitário, que está em execução"],
     "blocos": [
         {"titulo": "Sanitário 01", "modo": "deslizar", "itens": [
             P("Frente, com acesso e pintura", "ban01_03", J, "ban01_09", O),
             P("Calçada de acesso revestida", "ban01_04", J, "ban01_14", N),
             P("Ambiente interno, com janela e pintura", "ban01_06", J, "ban01_11", N),
             P("Ambiente interno, com piso, pintura e louça", "ban01_08", J, "ban01_13", N),
             P("Piso e pintura", "ban01_01", J, "ban01_12", O),
             P("Cabine, com piso e louça", "ban01_07", J, "ban01_16", N)]},
         {"titulo": "Sanitário 02", "modo": "deslizar", "itens": [
             P("Frente, com acesso e pintura", "ban02_01", J, "ban02_13", N),
             P("Janela de vidro instalada", "ban02_04", J, "ban02_15", N),
             P("Teto pintado, com exaustor", "ban02_05", J, "ban02_12", O),
             P("Cabines, com piso e louças", "ban02_07", J, "ban02_11", O),
             P("Piso cerâmico assentado", "ban02_03", J, "ban02_10", O),
             P("Parede pintada, com chuveiros", "ban02_08", J, "ban02_14", N)]}]},
    {"id": "quiosques", "nome": "Quiosques 01, 02 e 03", "curto": "Quiosques", "pct": 57.1, "situacao": "execucao",
     "previsao": "até o fim de dezembro de 2026", "capa": "qui01_09.jpg",
     "resumo": "Os três quiosques já têm piso, pintura e instalações.",
     "feito": ["Piso cerâmico", "Pintura", "Instalações elétricas e de água"],
     "falta": ["Churrasqueiras", "Parte do esgotamento sanitário, que está em execução"],
     "blocos": [
         {"titulo": "Os três quiosques", "modo": "deslizar", "itens": [
             P("Quiosque 01", "qui01_01", J, "qui01_09", O),
             P("Quiosque 02", "qui02_05", J, "qui02_11", O),
             P("Quiosque 03", "qui03_01", J, "qui03_05", O)]},
         {"titulo": "Piso e acabamento", "modo": "deslizar", "itens": [
             P("Quiosque 01, com piso e pintura", "qui01_05", J, "qui01_10", O),
             P("Quiosque 02, com piso cerâmico", "qui02_02", J, "qui02_09", N),
             P("Quiosque 03, com pintura e bancada", "qui03_02", J, "qui03_15", N)]}]},
    {"id": "entrada-servico", "nome": "Entrada de serviço", "curto": "Entrada de serviço", "pct": 26.2, "situacao": "execucao",
     "previsao": None, "capa": "guarita_24.jpg",
     "resumo": "A entrada para veículos grandes fica ao lado da guarita.",
     "feito": ["Pilares concluídos", "Portão de correr pronto"],
     "falta": ["Instalação do portão", "Pintura, identificação e paisagismo"],
     "blocos": [{"titulo": "Como está hoje", "modo": "grade", "itens": [
         {"foto": "guarita_23.jpg", "leg": "Pilares, nov/2026"},
         {"foto": "guarita_24.jpg", "leg": "Pilares prontos para o portão, nov/2026"}]}]},
    {"id": "quadra", "nome": "Quadra de areia", "curto": "Quadra", "pct": 8.8, "situacao": "execucao",
     "previsao": "até o fim de março de 2027", "capa": None,
     "resumo": "Os serviços iniciais estão em andamento.",
     "feito": ["Serviços preliminares e movimento de terra iniciados"],
     "falta": ["Base e areia", "Alambrado, portões e iluminação"]},
    {"id": "piscina", "nome": "Piscina", "curto": "Piscina", "pct": 0, "situacao": "iniciar",
     "previsao": "até o fim de março de 2027", "capa": None, "resumo": "A obra da piscina vem na sequência da quadra."},
    {"id": "baias-redondel", "nome": "Baias e redondel", "curto": "Baias e redondel", "pct": 0, "situacao": "iniciar",
     "previsao": "até o fim de junho de 2027", "capa": None, "resumo": "É a última etapa das áreas comuns."},
    {"id": "rede-agua", "nome": "Rede de água e poços artesianos", "curto": "Rede de água", "pct": 100, "situacao": "concluida",
     "previsao": "Concluída em 30/10/2026", "capa": "agua_27.jpg",
     "resumo": "A rede foi executada por inteiro, com testes de pressão e a ativação do fluxo de água.",
     "feito": ["3 poços artesianos, com estudo geofísico", "4 reservatórios, com 140 mil litros", "3.200 m de rede de distribuição", "Bombeamento com energia solar"],
     "blocos": [{"titulo": "Durante a obra e concluída", "modo": "lado", "itens": [
         P("Das valas ao ponto de água junto à via", "agua_01", O, "agua_23", O, "DURANTE", "CONCLUÍDA"),
         P("Reservatório em operação", "agua_04", O, "agua_27", O, "DURANTE", "CONCLUÍDA"),
         P("Registros e ramais de distribuição", "agua_03", O, "agua_33", O, "DURANTE", "CONCLUÍDA")]}]},
    {"id": "guarita", "nome": "Guarita", "curto": "Guarita", "pct": 100, "situacao": "concluida",
     "previsao": "Concluída", "capa": "guarita_11.jpg",
     "resumo": "A guarita foi revitalizada, com nova identificação, calçadas e jardim.",
     "feito": ["Pintura e nova identificação", "Calçadas e piso novo", "Jardim", "Portão lateral e muro tratados"],
     "blocos": [
         {"titulo": "Guarita", "modo": "deslizar", "itens": [
             P("Vista frontal", "guarita_05", J, "guarita_11", N),
             P("Fachada, com a nova identificação", "guarita_06", J, "guarita_21", N),
             P("Área coberta, com piso novo", "guarita_02", J, "guarita_18", N)]},
         {"titulo": "Acesso", "modo": "deslizar", "itens": [
             P("Portão lateral, com piso novo", "guarita_08", J, "guarita_17", N),
             P("Muro pintado e acesso regularizado", "guarita_09", J, "guarita_19", N)]}]},
    {"id": "rua-pedras", "nome": "Rua com pedras", "curto": "Rua com pedras", "pct": 100, "situacao": "concluida",
     "previsao": "Concluída", "capa": "pedr_depois_1.jpg",
     "resumo": "As pedras que impediam a passagem foram retiradas e a rua foi regularizada.",
     "feito": ["300 m³ de pedras retiradas", "Rua regularizada e liberada"],
     "blocos": [{"titulo": "Antes e depois", "modo": "lado", "itens": [
         P("Pedras sobre a via, trecho liberado", "eng/ruaped_04", J, "eng/ruaped_05", O),
         P("Leito regularizado e cascalhado", "eng/ruaped_03", J, "eng/ruaped_08", O),
         P("Trecho com pedras e vegetação, liberado", "eng/ruaped_01", J, "eng/ruaped_06", O),
         P("Via desobstruída e cascalhada", "eng/ruaped_adm", "", "eng/ruaped_07", O)]}]},
    {"id": "rua-alagamento", "nome": "Rua com alagamento", "curto": "Rua com alagamento", "pct": 100, "situacao": "concluida",
     "previsao": "Concluída", "capa": "alag_depois_1.jpg",
     "resumo": "A rua que alagava foi regularizada e cascalhada. Ao todo, três ruas foram desobstruídas.",
     "feito": ["Trecho regularizado", "Rua liberada para a passagem"],
     "blocos": [{"titulo": "Antes e depois", "modo": "lado", "itens": [
         P("Trecho em direção norte", "eng/rualag_01", A, "eng/rualag_16", O),
         P("Trecho em direção sudoeste", "eng/rualag_02", A, "eng/rualag_15", O),
         P("Subida em direção sul", "eng/rualag_03", A, "eng/rualag_13", O),
         P("Trecho regularizado e cascalhado", "eng/rualag_04", A, "eng/rualag_12", O),
         P("Área onde a água acumulava", "eng/rualag_05", A, "eng/rualag_11", O),
         P("Máquinas em operação", "eng/rualag_06", A, "eng/rualag_14", O, "ANTES", "DURANTE")]},
         {"titulo": "Mais uma rua desobstruída", "modo": "lado", "itens": [
         P("Via tomada pela vegetação, desobstruída e regularizada", "eng/rua1_antes", "", "eng/rua1_depois", ""),
         P("Trecho ao lado da rede elétrica, regularizado e cascalhado", "eng/rua2_antes_a", "", "eng/rua2_depois_a", ""),
         P("Leito regularizado", "eng/rua2_antes_b", "", "eng/rua2_depois_b", "")]}]},
    {"id": "placas", "nome": "Placas das ruas", "curto": "Placas", "pct": 100, "situacao": "concluida",
     "previsao": "Instaladas em novembro de 2026", "capa": "guarita_27.jpg",
     "resumo": "14 placas de identificação instaladas, no padrão visual do empreendimento.",
     "feito": ["14 placas instaladas nas ruas e avenidas"],
     "blocos": [{"titulo": "Algumas das placas", "modo": "grade", "itens": [
         {"foto": "guarita_27.jpg", "leg": "Rua 01"}, {"foto": "guarita_28.jpg", "leg": "Avenida do Umbuzeiro"},
         {"foto": "guarita_29.jpg", "leg": "Rua 12"}, {"foto": "guarita_31.jpg", "leg": "Rua 09"},
         {"foto": "guarita_26.jpg", "leg": "Avenida Pau Ferro"}, {"foto": "guarita_30.jpg", "leg": "Placa de rua"}]}]},
]

videos = {
    "destaques": [
        {"id": "por-do-sol", "titulo": "E se este pôr do sol fosse seu?", "dur": "1 min"},
        {"id": "tamanho", "titulo": "Olha o tamanho desse lugar", "dur": "30 s"},
        {"id": "agua", "titulo": "A água chegou", "dur": "26 s"},
        {"id": "relogio", "titulo": "Aqui o relógio anda mais devagar", "dur": "27 s"},
        {"id": "onde-fica", "titulo": "Onde fica o Haras", "dur": "15 s"},
    ],
    "ruas": [{"id": "rua-%s" % n, "titulo": "Rua %s" % n, "dur": "28 s"} for n in ("01", "02", "03", "05", "06", "07", "08", "09", "10", "11", "12")]
            + [{"id": "avenida-umbuzeiro", "titulo": "Avenida Umbuzeiro", "dur": "28 s"}],
}

# galeria completa dos relatórios do engenheiro, por obra
FOT = os.path.join(RAIZ, "assets", "fotos", "eng")
def eng(pref, de=1, ate=99):
    r = []
    for f in sorted(os.listdir(FOT)):
        m = f[:-4].rsplit("_", 1)
        if m[0] == pref and m[1].isdigit() and de <= int(m[1]) <= ate:
            w, h = Image.open(os.path.join(FOT, f)).size
            if w >= 400 and w / h < 2.2:
                r.append("eng/" + f)
    return r
GAL = {"clube-salao": eng("salao"), "sanitarios": eng("ban01") + eng("ban02"), "quiosques": eng("qui01") + eng("qui02") + eng("qui03"),
       "entrada-servico": eng("guarita", 22, 25), "rede-agua": eng("agua"), "guarita": eng("guarita", 1, 21),
       "rua-pedras": eng("ruaped"), "rua-alagamento": eng("rualag"), "placas": eng("guarita", 26, 32)}
for o in obras:
    if GAL.get(o["id"]):
        o["galeria"] = GAL[o["id"]]
print("fotos do engenheiro:", sum(len(v) for v in GAL.values()))

json.dump({"app": app, "eletrica": eletrica, "agua": agua, "obras": obras, "videos": videos},
          open(os.path.join(RAIZ, "data", "obras.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("obras.json:", len(obras), "obras")
