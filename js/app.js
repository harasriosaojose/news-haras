/* Obras do Haras — app do cliente. Tudo vem de data/obras.json. */
(function () {
  "use strict";
  var tela = document.getElementById("tela");
  var modal = document.getElementById("modal");
  var D = null, atual = 0;
  var F = "assets/fotos/", V = "assets/videos/";
  var ROTULO = { concluida: "Concluída", execucao: "Em andamento", iniciar: "A iniciar", coelba: "Aguardando a Coelba" };
  function svg(d) { return '<svg class="i" viewBox="0 0 24 24" aria-hidden="true">' + d + "</svg>"; }
  var IC = {
    ok: svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    relogio: svg('<circle cx="12" cy="12" r="8"/><path d="M12 8v4.5l2.5 2"/>'),
    cal: svg('<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'),
    obra: svg('<path d="M3 20h18M5 20V10l7-5 7 5v10M10 20v-6h4v6"/>'),
    setas: svg('<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>'),
    raio: svg('<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>'),
    gota: svg('<path d="M12 3.5s6 6.2 6 10.5a6 6 0 0 1-12 0c0-4.3 6-10.5 6-10.5z"/>'),
    sino: svg('<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15zM10 20.5h4"/>'),
    zap: svg('<path d="M4.5 19.5l1.2-4A7.5 7.5 0 1 1 9 18.6z"/>'),
    mapa: svg('<path d="M9 5l6 2 5-2v13l-5 2-6-2-5 2V7zM9 5v13M15 7v13"/>'),
    lamp: svg('<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V15h7v-1.1A6 6 0 0 0 12 3z"/>'),
    duvida: svg('<circle cx="12" cy="12" r="8.5"/><path d="M9.7 9.5a2.4 2.4 0 1 1 3.4 2.2c-.7.4-1.1.9-1.1 1.8M12 16.7v.1"/>')
  };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function pct(n) { return (Math.round(n * 10) / 10).toLocaleString("pt-BR", { maximumFractionDigits: 1 }) + "%"; }
  function selo(s) { return '<span class="selo ' + s + '">' + (s === "concluida" ? IC.ok : "") + ROTULO[s] + "</span>"; }
  function barra(n, ok) { return '<div class="barra' + (ok ? " ok" : "") + '" role="img" aria-label="' + pct(n) + ' executado"><i data-w="' + n + '"></i></div>'; }
  function previsaoTxt(o) { return !o.previsao ? "" : (o.situacao === "concluida" ? o.previsao : "Previsão: " + o.previsao); }
  function zap(texto) { return "https://wa.me/" + D.app.whatsapp + "?text=" + encodeURIComponent(texto); }
  function animar(raiz) {
    setTimeout(function () {
      (raiz || tela).querySelectorAll(".barra i").forEach(function (i) { i.style.width = i.dataset.w + "%"; });
      var c = tela.querySelector(".anel .frente");
      if (c) c.style.strokeDashoffset = c.dataset.fim;
    }, 120);
  }

  /* ---------- capa ---------- */
  function capa() {
    var a = D.app, n = { concluida: 0, execucao: 0, iniciar: 0 };
    D.obras.forEach(function (o) { if (n[o.situacao] != null) n[o.situacao]++; });
    var r = 46, comp = 2 * Math.PI * r;
    return '<header class="capa" id="inicio"><div class="foto" role="img" aria-label="A entrada do Haras Rio São José hoje" style="background-image:url(assets/capa.jpg)"></div>' +
      '<div class="topo"><img src="assets/logo.png" alt="" width="52" height="52"><span><b>' + esc(a.nome) + "</b><small>" + esc(a.subtitulo) + '</small></span><em class="edicao">' + esc(a.edicao) + "</em></div>" +
      '<div class="dentro"><span class="etiqueta">' + esc(a.exclusivo) + '</span><h1>' + esc(a.saudacao) + '</h1><p class="frase">' + esc(a.frase) + "</p>" +
      '<div class="geral"><div class="anel"><svg viewBox="0 0 112 112"><circle class="fundo" cx="56" cy="56" r="' + r + '"/><circle class="frente" cx="56" cy="56" r="' + r +
      '" stroke-dasharray="' + comp.toFixed(1) + '" stroke-dashoffset="' + comp.toFixed(1) + '" data-fim="' + (comp * (1 - a.geral_pct / 100)).toFixed(1) + '"/></svg><b>' + pct(a.geral_pct) + "</b></div>" +
      '<div><div class="rot">' + esc(a.rotulo_geral) + '</div><div class="txt">Posição em ' + esc(a.referencia) + ". Em " + esc(a.geral_anterior_ref) + ", era <b>" + pct(a.geral_anterior_pct) + "</b>.</div>" +
      '<div class="dat">Atualizado em ' + esc(a.atualizado_em) + "</div></div></div>" +
      '<div class="contagem"><div><b>' + n.concluida + "</b><span>concluídas</span></div><div><b>" + n.execucao + "</b><span>em andamento</span></div><div><b>" + n.iniciar + "</b><span>a iniciar</span></div></div>" +
      '<div class="nesta"><p>Nesta edição</p>' + a.nesta_edicao.map(function (x, i) { return '<a href="' + x.ir + '"><b>' + (i + 1) + "</b><span>" + esc(x.t) + "</span></a>"; }).join("") + "</div>" +
      "</div></header>";
  }

  /* ---------- destaques: energia e água ---------- */
  function destaques() {
    var e = D.eletrica, g = D.agua;
    var h = '<section class="bloco miolo" id="destaques"><div class="cab"><div class="fio-ouro"></div><h2>O que você mais quer saber</h2><p>A energia e a água, em linguagem direta.</p></div><div class="destaques">';
    h += '<article class="destaque energia" id="energia"><span class="sel">' + IC.raio + esc(e.selo) + "</span><h3>" + esc(e.titulo) + '</h3><p class="lead">' + esc(e.lead) + "</p>" +
      '<ul class="feitos">' + e.feito.map(function (t) { return "<li><i>" + IC.ok + "</i><span>" + esc(t) + "</span></li>"; }).join("") + "</ul>" +
      '<div class="duas-etapas"><h4>' + esc(e.falta_titulo) + "</h4>" + e.falta.map(function (f, i) {
        return '<div class="etapa' + (i === 0 ? " atual" : "") + '"><div class="n">' + esc(f.n) + "</div><div><b>" + esc(f.t) + "</b>" + (i === 0 ? "<em>estamos aqui</em>" : "") + "<span>" + esc(f.d) + "</span></div></div>";
      }).join("") + "</div>" +
      '<div class="semana">' + IC.sino + "<span>" + esc(e.semana) + '</span></div><p class="proto">' + esc(e.protocolos) + '</p><button class="botao ouro" data-ir="rede-eletrica">Ver as fotos da rede elétrica</button></article>';
    h += '<article class="destaque agua" id="agua"><span class="sel">' + IC.gota + esc(g.selo) + "</span><h3>" + esc(g.titulo) + '</h3><div class="cem"><b>100%</b><span>' + esc(g.lead) + "</span></div>" +
      '<div class="chips">' + g.entregue.map(function (t) { return "<span>" + esc(t) + "</span>"; }).join("") + "</div>" +
      '<div class="agora"><b>' + esc(g.agora_titulo) + "</b><p>" + esc(g.agora) + "</p></div>" +
      '<a class="botao verde" href="' + esc(D.app.link_agua) + '" target="_blank" rel="noopener">' + IC.gota + esc(g.botao) + "</a>" +
      '<button class="botao linha" data-ir="rede-agua">Ver as fotos da rede de água</button></article>';
    return h + "</div></section>";
  }

  /* ---------- obras em abas ---------- */
  function aba(o, i) {
    var mini = o.situacao === "coelba" ? '<span class="mini raio">' + IC.raio + "</span>" : o.situacao === "concluida" ? '<span class="mini">' + IC.ok + "</span>" : '<span class="mini" style="--v:' + o.pct + '"><span>' + Math.round(o.pct) + "</span></span>";
    return '<button class="aba ' + o.situacao + '" role="tab" id="aba-' + o.id + '" aria-selected="' + (i === atual) + '" data-i="' + i + '">' + mini + esc(o.curto || o.nome) + "</button>";
  }
  function rotulos(p) {
    return [esc(p.rot_a) + (p.antes_data ? " · " + esc(p.antes_data) : ""), esc(p.rot_d) + (p.depois_data ? " · " + esc(p.depois_data) : "")];
  }
  function par(p) {
    var r = rotulos(p);
    return '<div class="par"><h5>' + esc(p.titulo) + '</h5><div class="compara">' +
      '<img class="depois" loading="lazy" src="' + F + p.depois + '" alt="' + r[1] + ": " + esc(p.titulo) + '">' +
      '<img class="antes" loading="lazy" src="' + F + p.antes + '" alt="' + r[0] + ": " + esc(p.titulo) + '">' +
      '<span class="tag a">' + r[0] + '</span><span class="tag d">' + r[1] + '</span><span class="fio"></span><span class="pega">' + IC.setas + "</span>" +
      '<input type="range" min="0" max="100" value="50" aria-label="Comparar: ' + esc(p.titulo) + '"></div></div>';
  }
  function lado(p) {
    var r = rotulos(p);
    return '<div class="par"><h5>' + esc(p.titulo) + '</h5><div class="lado">' +
      '<button data-foto="' + p.antes + '" data-leg="' + r[0] + '"><img loading="lazy" src="' + F + p.antes + '" alt="' + r[0] + '"><span class="tag a">' + r[0] + "</span></button>" +
      '<button data-foto="' + p.depois + '" data-leg="' + r[1] + '"><img loading="lazy" src="' + F + p.depois + '" alt="' + r[1] + '"><span class="tag d">' + r[1] + "</span></button></div></div>";
  }
  function bloco(b, retrato) {
    var h = '<div class="sub-bloco"><h4>' + esc(b.titulo) + "</h4>";
    if (b.modo === "deslizar") h += '<p class="dica">Arraste o botão para os lados e compare o mesmo lugar.</p>' + b.itens.map(par).join("");
    else if (b.modo === "lado") h += '<p class="dica">Toque na foto para ampliar.</p>' + b.itens.map(lado).join("");
    else h += '<div class="grade' + (retrato ? " retrato" : "") + (b.modo === "grade1" ? " uma" : "") + '">' + b.itens.map(function (f) {
      return '<figure><button data-foto="' + f.foto + '" data-leg="' + esc(f.leg) + '"><img loading="lazy" src="' + F + f.foto + '" alt="' + esc(f.leg) + '"></button><figcaption>' + esc(f.leg) + "</figcaption></figure>";
    }).join("") + "</div>";
    return h + "</div>";
  }
  function painel(o) {
    var ant = D.obras[atual - 1], prox = D.obras[atual + 1];
    var h = o.capa ? '<div class="heroi" style="background-image:url(' + F + o.capa + ')"></div>'
      : '<div class="heroi vazio"><div>' + IC.obra + (o.situacao === "iniciar" ? "As fotos chegam quando a obra começar." : "As primeiras fotos chegam na próxima atualização.") + "</div></div>";
    h += '<div class="ficha">' + selo(o.situacao) + "<h3>" + esc(o.nome) + "</h3>" + (o.resumo ? '<p class="resumo">' + esc(o.resumo) + "</p>" : "");
    if (o.pct != null && o.situacao !== "iniciar") h += '<div class="pctg"><b>' + pct(o.pct) + "</b><span>executado em " + esc(D.app.referencia) + "</span></div>" + barra(o.pct, o.situacao === "concluida");
    if (o.previsao) h += '<div class="previsao">' + IC.cal + "<div><b>" + esc(previsaoTxt(o)) + "</b>" + (o.situacao === "concluida" ? "" : "<small>" + esc(D.app.ressalva) + "</small>") + "</div></div>";
    h += "</div>";
    if (o.nota) h += '<p class="nota">' + esc(o.nota) + "</p>";
    if (o.feito || o.falta) {
      h += '<div class="duas">';
      if (o.feito) h += '<div class="caixa feito"><h4>O que já foi feito</h4><ul>' + o.feito.map(function (t) { return "<li>" + IC.ok + "<span>" + esc(t) + "</span></li>"; }).join("") + "</ul></div>";
      if (o.falta) h += '<div class="caixa falta"><h4>O que falta</h4><ul>' + o.falta.map(function (t) { return "<li>" + IC.relogio + "<span>" + esc(t) + "</span></li>"; }).join("") + "</ul></div>";
      h += "</div>";
    }
    (o.blocos || []).forEach(function (b) { h += bloco(b, o.id === "placas"); });
    if (o.galeria && o.galeria.length) {
      h += '<div class="sub-bloco"><h4>Todas as fotos do engenheiro (' + o.galeria.length + ')</h4><p class="dica">Registro completo dos relatórios de fiscalização. Toque para ampliar e deslize para passar.</p><div class="mosaico">' +
        o.galeria.map(function (f, k) { return '<button data-gal="' + k + '"><img loading="lazy" src="' + F + f + '" alt="Foto ' + (k + 1) + " de " + esc(o.nome) + '"></button>'; }).join("") + "</div></div>";
    }
    h += '<div class="passa"><button data-passo="-1"' + (ant ? "" : " disabled") + ">← anterior<b>" + esc(ant ? ant.curto || ant.nome : "") + '</b></button><button data-passo="1"' + (prox ? "" : " disabled") + ">próxima →<b>" + esc(prox ? prox.curto || prox.nome : "") + "</b></button></div>";
    return h;
  }
  function obras() {
    return '<section class="bloco miolo" id="obras"><div class="cab"><div class="fio-ouro"></div><h2>As obras, uma a uma</h2><p>Escolha a obra para ver o percentual e as fotos de antes e depois.</p></div>' +
      '<div class="abas" role="tablist" aria-label="Obras">' + D.obras.map(aba).join("") + '</div><div class="painel" id="painel" role="tabpanel"></div>' +
      '<p class="nota">' + esc(D.app.ressalva) + "</p></section>";
  }
  function mostrar(i, rolar) {
    atual = Math.max(0, Math.min(D.obras.length - 1, i));
    var o = D.obras[atual], p = document.getElementById("painel");
    tela.querySelectorAll(".aba").forEach(function (b, k) { b.setAttribute("aria-selected", k === atual); });
    p.innerHTML = painel(o);
    p.style.animation = "none"; void p.offsetWidth; p.style.animation = "";
    p.querySelectorAll(".compara input").forEach(function (r) { r.addEventListener("input", function () { r.parentNode.style.setProperty("--p", r.value + "%"); }); });
    var b = document.getElementById("aba-" + o.id);
    b.parentNode.scrollTo({ left: b.offsetLeft - (b.parentNode.clientWidth - b.offsetWidth) / 2, behavior: "smooth" });
    if (rolar) document.getElementById("obras").scrollIntoView();
    animar(p);
  }

  /* ---------- vídeos e fotos ---------- */
  function cartaoVideo(v, grande) {
    return '<button class="video' + (grande ? " grande" : "") + '" data-video="' + v.id + '" data-leg="' + esc(v.titulo) + '" style="background-image:url(' + V + v.id + '.jpg)" aria-label="Assistir: ' + esc(v.titulo) + '">' +
      '<span class="play"><svg viewBox="0 0 24 24"><path d="M7 4.5v15l12-7.5z"/></svg></span><span class="t">' + esc(v.titulo) + "<small>" + esc(v.dur) + "</small></span></button>";
  }
  function midia() {
    var fotos = {};
    D.obras.forEach(function (o) {
      (o.blocos || []).forEach(function (b) {
        b.itens.forEach(function (it) { if (it.depois) fotos[it.depois] = o.nome + ": " + it.titulo.toLowerCase(); });
      });
    });
    var ordem = ["salao_09.jpg", "guarita_11.jpg", "agua_27.jpg", "qui01_09.jpg", "salao_11.jpg", "ban01_09.jpg", "guarita_21.jpg", "salao_14.jpg", "agua_23.jpg", "qui02_11.jpg", "pedr_depois_1.jpg"];
    return '<section class="fundo-verde" id="videos"><div class="miolo bloco"><div class="cab"><div class="fio-ouro"></div><h2>Vídeos e fotos</h2><p>O Haras visto de cima e de perto. Os vídeos não têm som.</p></div>' +
      '<p class="rot2">O Haras em vídeo</p><div class="trilho">' + D.videos.destaques.map(function (v) { return cartaoVideo(v, true); }).join("") + "</div>" +
      '<p class="rot2">Conhecendo as ruas do Haras</p><div class="trilho">' + D.videos.ruas.map(function (v) { return cartaoVideo(v); }).join("") + "</div>" +
      '<p class="rot2">Fotos recentes das obras</p><div class="fotos">' + ordem.filter(function (n) { return fotos[n]; }).map(function (n) {
        return '<button data-foto="' + n + '" data-leg="' + esc(fotos[n]) + '"><img loading="lazy" src="' + F + n + '" alt="' + esc(fotos[n]) + '"></button>';
      }).join("") + "</div></div></section>";
  }

  /* ---------- contato ---------- */
  function contato() {
    var a = D.app;
    return '<section class="bloco miolo" id="contato"><div class="cab"><div class="fio-ouro"></div><h2>Sua dúvida, sua sugestão</h2><p>Escreva aqui. Sua mensagem fica registrada com o escritório, e a resposta chega em ' + esc(a.prazo_resposta) + ".</p></div>" +
      '<div class="contato-grade"><form class="form" id="form" novalidate>' +
      '<div class="tipo"><label><input type="radio" name="tipo" value="Dúvida" checked><span>' + IC.duvida + 'Dúvida</span></label><label><input type="radio" name="tipo" value="Sugestão"><span>' + IC.lamp + "Sugestão</span></label></div>" +
      '<label class="campo"><span>Seu nome</span><input name="nome" autocomplete="name" required></label>' +
      '<div class="linha2"><label class="campo"><span>Unidade (lote)</span><input name="unidade" inputmode="numeric" required></label>' +
      '<label class="campo"><span>Telefone</span><input name="telefone" type="tel" autocomplete="tel" inputmode="tel" required></label></div>' +
      '<label class="campo"><span>Sua mensagem</span><textarea name="mensagem" required></textarea></label>' +
      '<p class="erro" id="erro" hidden>Preencha todos os campos para enviar.</p>' +
      '<button class="botao verde" type="submit">' + IC.ok + "Enviar mensagem</button>" +
      '<div class="ok-envio" id="ok-envio" hidden></div>' +
      '<p class="priv">Seus dados são usados somente para responder a você (Lei nº 13.709/2018). A mensagem é vista apenas pela equipe do escritório.</p></form>' +
      '<div><div class="coord"><h3>Prefere falar direto?</h3><p>Converse com o coordenador pelo WhatsApp ' + esc(a.whatsapp_exibir) + '.</p><a class="botao zap" target="_blank" rel="noopener" href="' + zap("Olá! Estou acompanhando as obras pelo News Haras e quero falar com o coordenador.") + '">' + IC.zap + "Falar com o coordenador</a></div>" +
      '<div class="links"><a class="botao linha" target="_blank" rel="noopener" href="' + esc(a.link_mapa) + '">' + IC.mapa + "Abrir o mapa de unidades</a></div></div></div></section>";
  }

  /* ---------- modal ---------- */
  function abrir(html, leg) {
    modal.querySelector(".palco").innerHTML = html;
    modal.querySelector(".leg").textContent = leg || "";
    modal.hidden = false; document.body.style.overflow = "hidden";
    modal.querySelector(".fechar").focus();
  }
  var lista = null, pos = 0;
  function galeria(arr, k, nome) {
    lista = arr; pos = k;
    abrir('<img src="' + F + arr[k] + '" alt="">', nome + " · foto " + (k + 1) + " de " + arr.length);
    modal.classList.add("com-setas");
  }
  function passar(d) { if (lista) galeria(lista, (pos + d + lista.length) % lista.length, modal.dataset.nome); }
  function fechar() { lista = null; modal.classList.remove("com-setas"); modal.querySelector(".palco").innerHTML = ""; modal.hidden = true; document.body.style.overflow = ""; }
  modal.addEventListener("click", function (e) {
    if (e.target.dataset.passar) { passar(+e.target.dataset.passar); return; }
    if (e.target === modal || e.target.classList.contains("fechar") || e.target.classList.contains("palco")) fechar();
  });
  var tx = null;
  modal.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
  modal.addEventListener("touchend", function (e) { if (tx == null || !lista) return; var d = e.changedTouches[0].clientX - tx; tx = null; if (Math.abs(d) > 45) passar(d < 0 ? 1 : -1); });
  document.addEventListener("keydown", function (e) { if (modal.hidden) return; if (e.key === "Escape") fechar(); else if (e.key === "ArrowRight") passar(1); else if (e.key === "ArrowLeft") passar(-1); });

  /* ---------- eventos ---------- */
  tela.addEventListener("click", function (e) {
    var t = e.target.closest("[data-i],[data-passo],[data-ir],[data-foto],[data-video],[data-gal]");
    if (!t) return;
    if (t.dataset.i != null) mostrar(+t.dataset.i);
    else if (t.dataset.passo) mostrar(atual + (+t.dataset.passo), true);
    else if (t.dataset.ir) mostrar(D.obras.findIndex(function (o) { return o.id === t.dataset.ir; }), true);
    else if (t.dataset.gal) { modal.dataset.nome = D.obras[atual].nome; galeria(D.obras[atual].galeria, +t.dataset.gal, D.obras[atual].nome); }
    else if (t.dataset.foto) abrir('<img src="' + F + t.dataset.foto + '" alt="">', t.dataset.leg);
    else if (t.dataset.video) abrir('<video src="' + V + t.dataset.video + '.mp4" poster="' + V + t.dataset.video + '.jpg" controls playsinline autoplay muted></video>', t.dataset.leg);
  });
  tela.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = e.target, v = {}, falta = false;
    ["nome", "unidade", "telefone", "mensagem"].forEach(function (k) { v[k] = f[k].value.trim(); if (!v[k]) falta = true; });
    document.getElementById("erro").hidden = !falta;
    if (falta) return;
    var g = D.app.forms, corpo = new URLSearchParams(), bt = f.querySelector("button[type=submit]"), ok = document.getElementById("ok-envio");
    corpo.append(g.tipo, f.tipo.value); corpo.append(g.nome, v.nome); corpo.append(g.unidade, v.unidade); corpo.append(g.telefone, v.telefone); corpo.append(g.mensagem, v.mensagem);
    var txt = "*" + f.tipo.value + " pelo News Haras*\nNome: " + v.nome + "\nUnidade: " + v.unidade + "\nTelefone: " + v.telefone + "\n\n" + v.mensagem;
    bt.disabled = true; bt.textContent = "Enviando...";
    fetch(g.url, { method: "POST", mode: "no-cors", body: corpo }).then(function () {
      ok.innerHTML = "<b>Recebemos sua mensagem!</b> Ela ficou registrada, e o escritório responde em " + esc(D.app.prazo_resposta) + ', pelo telefone que você informou.<a class="botao zap" target="_blank" rel="noopener" href="' + zap(txt) + '">' + IC.zap + "Enviar também pelo WhatsApp</a>";
      ok.hidden = false; f.mensagem.value = ""; bt.disabled = false; bt.innerHTML = IC.ok + "Enviar outra mensagem";
    }).catch(function () {
      ok.innerHTML = "<b>Não conseguimos registrar agora.</b> Envie pelo WhatsApp, que chega do mesmo jeito." + '<a class="botao zap" target="_blank" rel="noopener" href="' + zap(txt) + '">' + IC.zap + "Enviar pelo WhatsApp</a>";
      ok.hidden = false; bt.disabled = false; bt.innerHTML = IC.ok + "Tentar de novo";
    });
  });

  window.addEventListener("hashchange", function () {
    var m = location.hash.match(/^#obra=([\w-]+)/);
    if (m && D) mostrar(D.obras.findIndex(function (o) { return o.id === m[1]; }), true);
  });
  function navAtiva() {
    var links = document.querySelectorAll(".barra-nav a");
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) links.forEach(function (l) { l.classList.toggle("ativo", l.dataset.s === x.target.id); }); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    ["inicio", "destaques", "obras", "videos", "contato"].forEach(function (id) { var el = document.getElementById(id); if (el) obs.observe(el); });
  }

  fetch("data/obras.json?v=" + Date.now()).then(function (r) { return r.json(); }).then(function (d) {
    D = d;
    tela.innerHTML = capa() + destaques() + obras() + midia() + contato();
    document.getElementById("rodape-fonte").textContent = d.app.fonte;
    document.getElementById("rodape-ressalva").textContent = d.app.ressalva;
    document.title = d.app.nome + " · " + d.app.subtitulo + " · Haras Rio São José";
    var m = location.hash.match(/^#obra=([\w-]+)/), i = m ? d.obras.findIndex(function (o) { return o.id === m[1]; }) : d.obras.findIndex(function (o) { return o.id === "clube-salao"; });
    mostrar(i < 0 ? 0 : i, !!m);
    navAtiva(); animar();
  }).catch(function () {
    tela.innerHTML = '<p style="padding:40px 16px;text-align:center">Não foi possível carregar as informações agora. Tente de novo em instantes.</p>';
  });
})();
