// Gerenciador de Tema (Dark / Light Mode)
(function(){
  var btn = document.getElementById('theme-toggle');
  var iconSun = document.getElementById('theme-icon-sun');
  var iconMoon = document.getElementById('theme-icon-moon');
  var html = document.documentElement;

  function getPreferredTheme(){
    var saved = localStorage.getItem('portfolio_theme_v3');
    if(saved) return saved;
    return 'light'; // Padrão: 3. Clean Corporate (#F8FAFC / #FFFFFF / #2563EB / #0D9488)
  }

  function applyTheme(theme){
    if(theme === 'dark'){
      html.setAttribute('data-theme', 'dark');
      if(iconSun) iconSun.style.display = 'inline-block';
      if(iconMoon) iconMoon.style.display = 'none';
      btn.setAttribute('aria-label', 'Ativar modo claro');
      btn.setAttribute('title', 'Ativar modo claro');
    } else {
      html.setAttribute('data-theme', 'light');
      if(iconSun) iconSun.style.display = 'none';
      if(iconMoon) iconMoon.style.display = 'inline-block';
      btn.setAttribute('aria-label', 'Ativar modo escuro');
      btn.setAttribute('title', 'Ativar modo escuro');
    }
    localStorage.setItem('portfolio_theme_v3', theme);
    localStorage.setItem('portfolio_theme', theme);
  }

  applyTheme(getPreferredTheme());

  btn.addEventListener('click', function(e){
    var current = html.getAttribute('data-theme') || 'light';
    var next = current === 'dark' ? 'light' : 'dark';
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if(document.startViewTransition && !reduced){
      var rect = btn.getBoundingClientRect();
      var x = e.clientX || (rect.left + rect.width / 2);
      var y = e.clientY || (rect.top + rect.height / 2);
      var maxRadius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y)
      );
      var vt = document.startViewTransition(function(){
        applyTheme(next);
      });
      vt.ready.then(function(){
        document.documentElement.animate(
          {
            clipPath: [
              'circle(0px at ' + x + 'px ' + y + 'px)',
              'circle(' + maxRadius + 'px at ' + x + 'px ' + y + 'px)'
            ]
          },
          {
            duration: 520,
            easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
            pseudoElement: '::view-transition-new(root)'
          }
        );
      }).catch(function(){});
    } else {
      html.classList.add('theme-transition');
      applyTheme(next);
      setTimeout(function(){
        html.classList.remove('theme-transition');
      }, 500);
    }
  });
})();

// Efeito de Digitação no Hero (Typewriter)
(function(){
  var el = document.getElementById('typewriter');
  if(!el) return;
  var words = [
    "Back-end & APIs em Django",
    "Front-end & Interfaces",
    "Soluções com IA Aplicada",
    "UI/UX & Design no Figma",
    "Sistemas de Informação no IFC"
  ];
  var wordIdx = 0, charIdx = 0, isDeleting = false;

  function tick(){
    var current = words[wordIdx];
    if(isDeleting){
      el.textContent = current.substring(0, charIdx - 1);
      charIdx--;
    } else {
      el.textContent = current.substring(0, charIdx + 1);
      charIdx++;
    }

    var speed = isDeleting ? 35 : 75;
    if(!isDeleting && charIdx === current.length){
      speed = 1800;
      isDeleting = true;
    } else if(isDeleting && charIdx === 0){
      isDeleting = false;
      wordIdx = (wordIdx + 1) % words.length;
      speed = 350;
    }

    timer = setTimeout(tick, speed);
  }
  tick();

  document.addEventListener('visibilitychange', function(){
    if(!document.hidden && !timer){
      tick();
    }
  }, {passive: true});
})();

// Toast Notification
function showToast(msg){
  var toast = document.getElementById('toast');
  var text = document.getElementById('toast-msg');
  if(!toast || !text) return;
  text.textContent = msg;
  toast.classList.add('show');
  setTimeout(function(){
    toast.classList.remove('show');
  }, 3200);
}

// Copiar E-mail para Área de Transferência com Feedback Visual
(function(){
  var btn = document.getElementById('btn-copy-email');
  if(!btn) return;
  var originalHTML = btn.innerHTML;

  function feedbackVisual(){
    btn.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> E-mail copiado!';
    btn.style.borderColor = 'var(--accent)';
    btn.style.color = 'var(--accent)';
    setTimeout(function(){
      btn.innerHTML = originalHTML;
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2500);
  }

  btn.addEventListener('click', function(){
    var email = window.__portfolioEmail || 'amarahigor@gmail.com';
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(email).then(function(){
        showToast('E-mail ' + email + ' copiado!');
        feedbackVisual();
      }).catch(function(){
        fallbackCopy(email);
      });
    } else {
      fallbackCopy(email);
    }
  });

  function fallbackCopy(text){
    var input = document.createElement('input');
    input.value = text;
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
    showToast('E-mail copiado: ' + text);
    feedbackVisual();
  }
})();

// Efeito Confete com Canvas Puro (Zero Dependências)
function dispararConfetes(){
  var canvas = document.getElementById('confetti-canvas');
  if(!canvas) return;
  var ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  var pieces = [];
  var colors = ['#2563EB', '#0D9488', '#38bdf8', '#f59e0b', '#10b981', '#6366f1'];
  for(var i = 0; i < 90; i++){
    pieces.push({
      x: canvas.width / 2,
      y: canvas.height / 2,
      vx: (Math.random() - 0.5) * 16,
      vy: (Math.random() - 0.7) * 18,
      size: Math.random() * 8 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      vRot: (Math.random() - 0.5) * 10
    });
  }

  canvas.style.display = 'block';
  var start = Date.now();
  function animate(){
    var elapsed = Date.now() - start;
    if(elapsed > 2400){
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      canvas.style.display = 'none';
      return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(var j = 0; j < pieces.length; j++){
      var p = pieces[j];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.35;
      p.rotation += p.vRot;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
      ctx.restore();
    }
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
}

// Tilt 3D ultra-otimizado + Spotlight Radial Glow (Zero Reflow no mousemove, 60/120 FPS)
function initTilt(){
  if(!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  var cards = document.querySelectorAll('.card, .focus-card, .award-card');
  cards.forEach(function(card){
    if(card.dataset.tiltBound === '1') return;
    card.dataset.tiltBound = '1';
    var rect = null;
    var rafId = null;

    function onEnter(){
      rect = card.getBoundingClientRect();
      card.style.transition = 'border-color .25s ease, box-shadow .25s ease, background-color .3s ease';
    }

    function onMove(e){
      if(!rect) rect = card.getBoundingClientRect();
      var clientX = e.clientX;
      var clientY = e.clientY;
      if(rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(function(){
        var x = clientX - rect.left;
        var y = clientY - rect.top;
        var cx = rect.width / 2;
        var cy = rect.height / 2;
        var dx = Math.max(-1, Math.min(1, (x - cx) / cx));
        var dy = Math.max(-1, Math.min(1, (y - cy) / cy));
        card.style.setProperty('--mouse-x', x + 'px');
        card.style.setProperty('--mouse-y', y + 'px');
        card.style.transform = 'perspective(900px) rotateX(' + (-dy * 3).toFixed(2) + 'deg) rotateY(' + (dx * 3).toFixed(2) + 'deg) translateY(-3px)';
      });
    }

    function onLeave(){
      if(rafId) cancelAnimationFrame(rafId);
      rect = null;
      card.style.transition = 'transform .35s cubic-bezier(0.16, 1, 0.3, 1), border-color .25s ease, box-shadow .25s ease, background-color .3s ease';
      card.style.transform = '';
    }

    card.addEventListener('mouseenter', onEnter, {passive: true});
    card.addEventListener('mousemove', onMove, {passive: true});
    card.addEventListener('mouseleave', onLeave, {passive: true});
  });
}

// Menu Mobile
(function(){
  var toggle = document.getElementById('nav-toggle');
  var menu = document.getElementById('nav-links');
  var overlay = document.getElementById('nav-overlay');
  if(!toggle || !menu) return;

  function setOpen(open){
    toggle.classList.toggle('active', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.classList.toggle('open', open);
    if(overlay) overlay.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  toggle.addEventListener('click', function(e){
    e.stopPropagation();
    var isOpen = menu.classList.contains('open');
    setOpen(!isOpen);
  });

  menu.querySelectorAll('a').forEach(function(link){
    link.addEventListener('click', function(){ setOpen(false); });
  });

  if(overlay){
    overlay.addEventListener('click', function(){ setOpen(false); });
  }

  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && menu.classList.contains('open')){
      setOpen(false);
    }
  });

  window.addEventListener('resize', function(){
    if(window.innerWidth > 768 && menu.classList.contains('open')){
      setOpen(false);
    }
  });
})();

// Efeito reveal multi-direcional e escalonado ao scrollar
var revealObserver = null;
function initReveal(){
  if(!('IntersectionObserver' in window)){ return; }
  if(!revealObserver){
    revealObserver = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {threshold: 0.10, rootMargin: '0px 0px -30px 0px'});
  }

  function bindGroup(selector, variantClass, staggerLimit){
    var nodes = document.querySelectorAll(selector);
    nodes.forEach(function(el, idx){
      if(el.dataset.revealBound === '1') return;
      el.dataset.revealBound = '1';
      el.classList.add('reveal');
      if(variantClass){
        if(typeof variantClass === 'function'){
          var v = variantClass(idx);
          if(v) el.classList.add(v);
        } else {
          el.classList.add(variantClass);
        }
      }
      var stagger = staggerLimit ? (idx % staggerLimit) : idx;
      el.style.setProperty('--stagger', String(stagger));
      revealObserver.observe(el);
    });
  }

  bindGroup('section h2, section > .lead', '', 2);
  bindGroup('.sobre-conteudo p', 'reveal-left', 4);
  bindGroup('.focus-card', function(i){ return i % 2 === 0 ? 'reveal-left' : 'reveal-right'; }, 4);
  bindGroup('#skills-grid .card', 'reveal-pop', 6);
  bindGroup('#projetos-grid .card', 'reveal-pop', 6);
  bindGroup('.award-card', 'reveal-flip', 4);
  bindGroup('.timeline > div', 'reveal-left', 5);
  bindGroup('.faq-item', 'reveal-zoom', 5);
  bindGroup('#mural, #contato .btns', 'reveal-zoom', 2);
}
initReveal();


// Mural de Recados (API)
(function(){
  var base = (document.querySelector('meta[name="api-base"]') || {}).content || '';
  var url = base.replace(/\/$/, '') + '/api/recados/';
  var status = document.getElementById('status'), lista = document.getElementById('lista');
  var btn = document.getElementById('enviar');

  function render(itens){
    lista.textContent = '';
    status.textContent = itens.length ? '' : 'Ainda não há recados. Seja a primeira pessoa!';
    itens.forEach(function(r){
      var box = document.createElement('div'), n = document.createElement('b'), t = document.createElement('span');
      box.className = 'msg';
      n.textContent = String(r.nome || 'Anônimo') + (r.criado_em ? ' · ' + new Date(r.criado_em).toLocaleDateString('pt-BR') : '');
      t.textContent = String(r.texto || '');
      box.appendChild(n);
      box.appendChild(t);
      if(r.resposta){
        var respBox = document.createElement('div');
        respBox.className = 'msg-reply';
        var respHeader = document.createElement('div');
        respHeader.className = 'msg-reply-header';
        respHeader.innerHTML = '<span class="reply-badge">Resposta do Higor</span>' + (r.respondido_em ? ' <span class="reply-date">· ' + new Date(r.respondido_em).toLocaleDateString('pt-BR') + '</span>' : '');
        var respText = document.createElement('p');
        respText.className = 'msg-reply-text';
        respText.textContent = String(r.resposta);
        respBox.appendChild(respHeader);
        respBox.appendChild(respText);
        box.appendChild(respBox);
      }
      lista.appendChild(box);
    });
  }

  function carregar(){
    return fetch(url).then(function(r){ if(!r.ok) throw 0; return r.json(); }).then(render)
      .catch(function(){ status.textContent = 'Não foi possível carregar os recados agora.'; });
  }

  btn.addEventListener('click', async function(){
    var nome = document.getElementById('nome').value.trim(), texto = document.getElementById('texto').value.trim();
    if(!texto){ status.textContent = 'Escreva uma mensagem antes de enviar.'; return; }
    btn.disabled = true;
    try{
      var r = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nome: nome, texto: texto, site: document.getElementById('site').value})
      });
      var d = await r.json().catch(function(){ return {}; });
      if(!r.ok){
        status.textContent = d.erro || 'Não foi possível enviar agora.';
      } else {
        document.getElementById('texto').value = '';
        await carregar();
        status.textContent = '';
        showToast('Recado enviado com sucesso!');
        dispararConfetes();
      }
    }catch(e){
      status.textContent = 'Sem conexão com o servidor.';
    }
    btn.disabled = false;
  });

  carregar();
})();

// Conteúdo Dinâmico: Habilidades e Projetos com Filtro (API)
(function(){
  var DEFAULTS = {
    "habilidades": [
      {"titulo": "Front-end & Web", "descricao": "Interfaces rápidas, responsivas, acessíveis e organizadas em componentes.", "tecnologias": ["JavaScript", "React", "Vue 3", "Vite", "Pinia", "HTML5", "CSS3"]},
      {"titulo": "Back-end & APIs REST", "descricao": "APIs RESTful documentadas, autenticação JWT, segurança e painéis administrativos.", "tecnologias": ["Python", "Django", "Django REST", "Swagger / OpenAPI", "JWT", "Gunicorn"]},
      {"titulo": "Dados & DevOps", "descricao": "Modelagem relacional, versionamento com Git/GitHub, testes e deploy em nuvem.", "tecnologias": ["PostgreSQL", "MySQL", "Git", "GitHub Actions", "Vercel", "Render"]},
      {"titulo": "Design & UI/UX", "descricao": "Protótipos navegáveis no Figma, arquitetura da informação e design systems.", "tecnologias": ["Figma", "UI/UX", "Prototipagem", "Design Systems", "Responsividade"]},
      {"titulo": "Idiomas & Soft Skills", "descricao": "Inglês intermediário (4 anos KNN) para documentação técnica e comunicação em equipe.", "tecnologias": ["Inglês (4 anos KNN)", "Trabalho em Equipe", "BPMN", "Metodologias Ágeis"]}
    ],
    "projetos": [
      {
        "nome": "Hackathon Fábrica 2k26",
        "badge": "Desenvolvido em 24h · Maratona Hackathon",
        "dominio": "delta.fabricadesoftware.ifc.edu.br",
        "descricao": "Plataforma com Inteligência Artificial desenvolvida em maratona intensiva de 24 horas para auxiliar professores na adaptação personalizada de atividades e percepção precoce de sinais em alunos neuroatípicos (TEA e TDAH).",
        "tecnologias": ["Python", "Django", "IA", "Educação Inclusiva", "Hackathon 24h"],
        "github": "https://github.com/Hackathon-Fabrica-2k26",
        "demo": "https://delta.fabricadesoftware.ifc.edu.br/login?redirect=/turmas",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "ia",
        "estudo_caso": {
          "titulo": "Hackathon Fábrica 2k26 (Maratona 24H)",
          "badge": "Hackathon 24H · IA Aplicada",
          "desafio": "Criar uma solução tecnológica completa em apenas 24 horas contínuas para apoiar professores da rede pública a adaptar atividades e avaliações para crianças neuroatípicas de 6 a 9 anos (com TEA e TDAH), além de estruturar relatórios de observação em sala de aula.",
          "solucao": "Desenvolvemos em equipe uma aplicação web em Python e Django integrada com modelos de Inteligência Artificial. A ferramenta analisa o plano de aula do professor e gera versões adaptadas com linguagem direta, suporte imagético, redução de sobrecarga sensorial e roteiros lúdicos diferenciados. Deploy efetuado no ambiente da Fábrica de Software do IFC.",
          "aprendizados": "Trabalho ágil sob altíssima pressão de tempo, prototipagem relâmpago, integração de IA no backend Django e entrega de um produto funcional pronto para uso em sala de aula em 24 horas."
        }
      },
      {
        "nome": "Portfólio Pessoal & API REST",
        "badge": "API REST ao vivo (OpenAPI 3.0)",
        "dominio": "portfolio-higor.onrender.com",
        "descricao": "Arquitetura web completa com mural interativo de recados, documentação OpenAPI 3.0 (Swagger UI), endpoint de health check, segurança reforçada contra XSS/DoS, esteira de CI/CD e banco PostgreSQL no Render.",
        "tecnologias": ["Python", "Django", "PostgreSQL", "Swagger UI", "CI/CD", "Render"],
        "github": "https://github.com/HigorAmaral/portfolio-higor",
        "demo": "https://portfolio-higor.onrender.com",
        "swagger": "/api/docs/",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "backend",
        "estudo_caso": {
          "titulo": "Portfólio & Backend Production-Ready",
          "badge": "Django 6 · PostgreSQL · Swagger",
          "desafio": "Construir uma aplicação web rápida, moderna e de custo zero de infraestrutura (Render Free Tier), porém com arquitetura, testes e padrões de segurança de nível sênior.",
          "solucao": "Estruturação de backend Django com PostgreSQL na nuvem, esteira de CI/CD no GitHub Actions com 21 testes unitários automatizados, documentação interativa Swagger (/api/docs/), rate limiting por IP confiável (True-Client-IP), proteção estrita de headers (CSP, HSTS, COOP), auditoria de CVEs com pip-audit e bot keep-alive para zero downtime.",
          "aprendizados": "Implementação prática de esteira de integração contínua (CI/CD), arquitetura resiliente na nuvem, hardening contra ataques cibernéticos e documentação padronizada OpenAPI 3.0."
        }
      },
      {
        "nome": "Santory Pizzaria",
        "badge": "Projeto Integrador · IFC",
        "dominio": "santoryfrontend-1.vercel.app",
        "descricao": "Sistema integrado de gestão, PDV e delivery para pizzaria desenvolvido no IFC: SPA reativo em Vue 3 (Vite) hospedado na Vercel e backend REST com Django no Render, com baixa automática de estoque de insumos e múltiplos níveis de acesso.",
        "tecnologias": ["Vue 3", "Vite", "Python", "Django REST", "Vercel", "Render"],
        "github": "https://github.com/Santory-Pizzaria",
        "demo": "https://santoryfrontend-1.vercel.app/login",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "frontend",
        "estudo_caso": {
          "titulo": "Sistema Integrado de Gestão & PDV (Pizzaria Santory)",
          "badge": "Vue 3 · Django REST · Vercel · Render · Projeto Integrador",
          "desafio": "A Pizzaria Santory operava com fluxos semi-manuais e anotações em papel para pedidos de balcão e telefone, causando lentidão no atendimento, erros na transmissão dos pedidos à cozinha, falta de controle de estoque de ingredientes e ausência de rastreamento de entregas ou pagamentos online.",
          "solucao": "Desenvolvimento de um ecossistema web integrado com arquitetura desacoplada: interface SPA reativa em Vue 3 (Vite) na Vercel e backend RESTful com Django no Render. Modelagem relacional completa (DER), controle automático de estoque com baixa por insumo, PDV em tempo real para salão/cozinha, perfis de acesso (Administrador, Atendente, Pizzaiolo, Entregador e Cliente) e catálogo interativo com personalização de pedidos.",
          "aprendizados": "Arquitetura cliente-servidor desacoplada (Vue 3 + Django API), engenharia de requisitos com 37 RFs e 20 regras de negócio, modelagem de banco de dados relacional (DER), trabalho em equipe com Git/GitHub e deploy em múltiplos provedores em nuvem (Vercel e Render)."
        }
      },
      {
        "nome": "Projeto BSI: Microprocessos Acadêmicos",
        "badge": "Pesquisa Científica & BPMN · IFC",
        "dominio": "ifc-araquari.edu.br/bsi",
        "descricao": "Mapeamento e análise aprofundada dos microprocessos acadêmicos do Bacharelado em Sistemas de Informação no IFC Câmpus Araquari com modelagem BPMN, avaliação pelo modelo PEMM (Michael Hammer), diretrizes estratégicas 5W2H e engenharia de requisitos com conformidade LGPD.",
        "tecnologias": ["BPMN / BPM", "Engenharia de Requisitos", "Modelo PEMM", "Matriz 5W2H", "LGPD", "LaTeX"],
        "github": "",
        "demo": "",
        "pdf": "/static/projeto-bsi-microprocessos.pdf",
        "status": "em_andamento",
        "status_label": "Em andamento",
        "categoria": "ia",
        "estudo_caso": {
          "titulo": "Mapeamento & Análise de Microprocessos (BSI IFC)",
          "badge": "BPMN · Modelo PEMM · 5W2H · Engenharia de Requisitos · LaTeX",
          "desafio": "A dispersão de plataformas (SIGAA, SEI, Google Forms) e o trâmite manual nos registros discentes do IFC geravam retrabalho na secretaria acadêmica, falta de rastreabilidade de solicitações para os alunos e diagnóstico de maturidade inicial (P0 em indicadores e infraestrutura de TI).",
          "solucao": "Estruturação qualitativa da trajetória discente em 4 fases (Entrada, Rotina, Pedidos Especiais e Conclusão), modelagem formal de 4 fluxos em BPMN (matrículas, TCC, dispensas, regime disciplinar), aplicação do modelo de maturidade PEMM de Michael Hammer, plano de ação 5W2H e levantamento rigoroso de 8 Requisitos Funcionais (RF01-RF08) e 4 Não-Funcionais (RNF01-RNF04) com proteção de dados e acessibilidade.",
          "aprendizados": "Domínio prático de Gestão de Processos de Negócio (BPM/BPMN), Engenharia de Requisitos aplicada ao contexto educacional público federal, diagnóstico organizacional e redação científica técnica avançada com diagramação em LaTeX."
        }
      },
      {
        "nome": "EcoApack — Catálogo Industrial & Orçamentos B2B",
        "badge": "React 19 · B2B & Catálogo Interativo",
        "dominio": "eco-park-application.vercel.app",
        "descricao": "Plataforma web corporativa B2B desenvolvida em React 19 para indústria de embalagens plásticas sustentáveis. Conta com catálogo interativo de baldes industriais, configurador dinâmico de cores (corpo e tampa), lupa de zoom em alta resolução e automação de orçamentos via EmailJS.",
        "tecnologias": ["React 19", "JavaScript", "Bootstrap 5", "EmailJS", "PWA", "Vercel"],
        "github": "https://github.com/HigorAmaral/eco-park-application",
        "demo": "https://eco-park-application.vercel.app",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "frontend",
        "estudo_caso": {
          "titulo": "EcoApack — Catálogo Industrial & Orçamentos B2B",
          "badge": "React 19 · Bootstrap 5 · EmailJS · Vercel",
          "desafio": "Digitalizar a vitrine comercial de uma indústria de embalagens plásticas sustentáveis (baldes industriais de 1kg e 1,2kg), permitindo que compradores B2B inspecionem detalhes técnicos das peças, simulem combinações de cores e solicitem cotações rápidas sem depender de atendimento manual lento.",
          "solucao": "Desenvolvimento de uma Single Page Application (SPA) em React 19 hospedada na Vercel, com seletor interativo de cores para tampa e corpo do produto, efeito de lupa dinâmica (zoom in-place por coordenadas do cursor), animações de revelação com IntersectionObserver e envio automatizado de propostas comerciais e contatos diretamente por EmailJS.",
          "aprendizados": "Componentização avançada e hooks no React 19, manipulação de eventos de ponteiro para zoom óptico de produto, integração de mensageria serverless (EmailJS) e otimização de performance e SEO para páginas corporativas."
        }
      },
      {
        "nome": "Primeiro Lar Imobiliária",
        "badge": "Vue 3 & Pinia · Integração API IBGE",
        "dominio": "front-primeirolar-25.vercel.app",
        "descricao": "Aplicação imobiliária para compra, venda, anúncio e favoritismo de imóveis construída com Vue 3, Vite e Pinia. Integra a API oficial de localidades do IBGE em tempo real para filtragem dinâmica por estados (UF) e municípios brasileiros, além de consumo de API REST via Axios.",
        "tecnologias": ["Vue 3", "Vite", "Pinia", "Vue Router", "Axios", "API IBGE", "PWA"],
        "github": "https://github.com/HigorAmaral/front-primeiro.lar-25",
        "demo": "https://front-primeirolar-25.vercel.app",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "frontend",
        "estudo_caso": {
          "titulo": "Primeiro Lar Imobiliária — Portal de Imóveis",
          "badge": "Vue 3 · Pinia · Axios · API IBGE · PWA",
          "desafio": "Construir uma plataforma imobiliária moderna e responsiva onde usuários possam buscar imóveis com filtros precisos de localização em todo o território nacional, cadastrar anúncios de venda e gerenciar sua lista de imóveis favoritos com estado sincronizado.",
          "solucao": "Arquitetura front-end modular em Vue 3 (Vite) com gerenciamento de estado global via Pinia e roteamento protegido no Vue Router. Consumo em tempo real da API de Localidades do IBGE para carregamento dinâmico de UFs e cidades por estado selecionado, integração com backend RESTful via Axios e suporte a instalação como Progressive Web App (PWA).",
          "aprendizados": "Gerenciamento de estado global escalável com Pinia, consumo combinado de APIs públicas governamentais (IBGE) e APIs próprias com Axios, navegação SPA avançada e configuração de PWA com Vite."
        }
      },
      {
        "nome": "API RESTful Livraria & Gestão de Acervo",
        "badge": "Django REST · JWT Auth & OpenAPI 3",
        "dominio": "github.com/HigorAmaral/livraria_3info1_2025-1",
        "descricao": "Backend RESTful completo construído com Django e Django REST Framework (DRF) para gestão de acervo literário, editoras, autores e fluxo transacional de compras. Possui autenticação JWT (SimpleJWT), upload de capas na nuvem via Cloudinary, filtros avançados e documentação OpenAPI 3 (Swagger e Redoc).",
        "tecnologias": ["Python", "Django REST Framework", "PostgreSQL", "JWT Auth", "Swagger / Redoc", "Cloudinary"],
        "github": "https://github.com/HigorAmaral/livraria_3info1_2025-1",
        "demo": "",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "backend",
        "estudo_caso": {
          "titulo": "API RESTful de Livraria & Fluxo de Compras (DRF)",
          "badge": "Python · Django REST Framework · SimpleJWT · OpenAPI 3 · Cloudinary",
          "desafio": "Projetar um backend desacoplado e escalável capaz de gerenciar todo o ciclo de catálogo de uma livraria (livros, autores, categorias e editoras), perfis de usuários customizados, upload de mídias e processamento transacional de carrinhos e itens de compra.",
          "solucao": "Implementação de API RESTful com Django REST Framework gerenciada via PDM, autenticação stateless com JSON Web Tokens (djangorestframework-simplejwt), armazenamento de imagens em nuvem com Cloudinary, filtragem avançada com django-filter, suporte a CORS e geração automática de documentação interativa Swagger UI e Redoc com drf-spectacular.",
          "aprendizados": "Arquitetura de APIs RESTful corporativas com DRF, serializadores aninhados para pedidos e itens de compra, autenticação JWT segura, integração de storage em nuvem e documentação padronizada OpenAPI 3.0."
        }
      },
      {
        "nome": "AgroNovo-Mundo — E-commerce Agro & Pet",
        "badge": "Mostra SEPE · IFC Araquari",
        "dominio": "github.com/HigorAmaral/Eco-Park",
        "descricao": "E-commerce departamental agropecuário e pet shop desenvolvido em Vue 3 para a Semana de Ensino, Pesquisa e Extensão (SEPE — IFC). Conta com carrinho de compras reativo, lista de favoritos, busca global em tempo real entre componentes, autenticação Google OAuth e integração com WhatsApp.",
        "tecnologias": ["Vue 3", "Vite", "Vue Router", "Google OAuth", "Carrinho Reativo", "PWA"],
        "github": "https://github.com/HigorAmaral/Eco-Park",
        "demo": "",
        "status": "concluido",
        "status_label": "Concluído",
        "categoria": "frontend",
        "estudo_caso": {
          "titulo": "AgroNovo-Mundo — E-commerce Agropecuário & Pet (SEPE IFC)",
          "badge": "Vue 3 · Google OAuth · Provide/Inject · E-commerce · SEPE IFC",
          "desafio": "Desenvolver uma loja virtual segmentada em múltiplos departamentos técnicos (Rações, Medicamentos, Ferragens, Pets, Dedetização e Hormônios) com busca instantânea, carrinho unificado e cálculo dinâmico de subtotais para apresentação na Semana de Ensino, Pesquisa e Extensão (SEPE) do IFC.",
          "solucao": "Construção de uma SPA em Vue 3 e Vue Router utilizando a API de Composition (provide/inject e watchers reativos) para compartilhar o estado do carrinho, favoritos e barra de pesquisa global entre todas as rotas departamentais, além de autenticação social via Google OAuth (vue3-google-login) e geolocalização via Google Maps.",
          "aprendizados": "Comunicação reativa entre múltiplos componentes com Provide/Inject no Vue 3, implementação de fluxos completos de carrinho de e-commerce, autenticação OAuth2 com Google e apresentação técnica em evento acadêmico."
        }
      }
    ]
  };

  var base = (document.querySelector('meta[name="api-base"]') || {}).content || '';
  var api = base.replace(/\/$/, '') + '/api/conteudo/';
  var currentFilter = 'todos';
  var currentSearch = '';
  var allProjects = DEFAULTS.projetos;
  var deepLinkOpened = false;

  function slugifyProjeto(nome){
    return String(nome || '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  // Gerenciamento do Modal de Estudo de Caso + Deep Linking (?projeto=slug)
  var modalBackdrop = document.getElementById('modal-case');
  var modalClose = document.getElementById('modal-close');
  var modalTitle = document.getElementById('modal-title');
  var modalBadge = document.getElementById('modal-badge');
  var modalChips = document.getElementById('modal-chips');
  var modalDesafio = document.getElementById('modal-desafio');
  var modalSolucao = document.getElementById('modal-solucao');
  var modalAprendizados = document.getElementById('modal-aprendizados');
  var modalFooter = document.getElementById('modal-footer');

  function fecharModal(){
    if(modalBackdrop){
      modalBackdrop.classList.remove('open');
      modalBackdrop.setAttribute('aria-hidden', 'true');
      try {
        if(window.location.search.indexOf('projeto=') !== -1 && window.history.replaceState){
          window.history.replaceState(null, '', window.location.pathname + window.location.hash);
        }
      } catch(e){}
    }
  }

  function abrirModalEstudo(p){
    var ec = p.estudo_caso;
    if(!ec || !modalBackdrop) return;

    var slug = slugifyProjeto(p.nome);
    try {
      if(slug && window.history.replaceState){
        window.history.replaceState(null, '', '?projeto=' + encodeURIComponent(slug) + '#projetos');
      }
    } catch(e){}

    modalTitle.textContent = ec.titulo || p.nome;
    modalBadge.textContent = removerEmojis(ec.badge || p.badge || 'Estudo de Caso');
    modalDesafio.textContent = ec.desafio || 'Desafio técnico em produção.';
    modalSolucao.textContent = ec.solucao || 'Solução estruturada com boas práticas de engenharia de software.';
    modalAprendizados.textContent = ec.aprendizados || 'Evolução técnica e trabalho colaborativo.';

    if(modalChips){
      modalChips.textContent = '';
      (p.tecnologias || []).forEach(function(t){
        modalChips.appendChild(el('span', 'chip', String(t)));
      });
    }

    modalFooter.innerHTML = '';

    // Botão Copiar Link Direto do Estudo de Caso
    if(slug){
      var btnShare = el('button', 'btn s', '');
      btnShare.type = 'button';
      btnShare.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> Copiar Link';
      btnShare.addEventListener('click', function(){
        var shareUrl = window.location.origin + '/?projeto=' + encodeURIComponent(slug) + '#projetos';
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(shareUrl).then(function(){
            showToast('Link direto do projeto copiado!');
          }).catch(function(){});
        }
      });
      modalFooter.appendChild(btnShare);
    }
    if(p.demo){
      var aD = el('a', 'btn p', '');
      aD.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg> Acessar Projeto';
      aD.href = urlSegura(p.demo);
      aD.target = '_blank';
      aD.rel = 'noopener';
      modalFooter.appendChild(aD);
    }
    if(p.swagger || p.nome.includes('Portfólio')){
      var aS = el('a', 'btn s', '');
      aS.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Ver Swagger';
      aS.href = urlSegura(p.swagger) || '/api/docs/';
      aS.target = '_blank';
      aS.rel = 'noopener';
      modalFooter.appendChild(aS);
    }
    if(p.github){
      var aG = el('a', 'btn s', '');
      aG.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg> Repositório';
      aG.href = urlSegura(p.github);
      aG.target = '_blank';
      aG.rel = 'noopener';
      modalFooter.appendChild(aG);
    }
    if(p.pdf){
      var aP = el('a', 'btn s', '');
      aP.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Ler Monografia Completa (PDF)';
      aP.href = urlSegura(p.pdf);
      aP.target = '_blank';
      aP.rel = 'noopener';
      modalFooter.appendChild(aP);
    }

    modalBackdrop.classList.add('open');
    modalBackdrop.setAttribute('aria-hidden', 'false');
  }

  if(modalClose){ modalClose.addEventListener('click', fecharModal); }
  if(modalBackdrop){
    modalBackdrop.addEventListener('click', function(e){
      if(e.target === modalBackdrop) fecharModal();
    });
  }
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && modalBackdrop && modalBackdrop.classList.contains('open')){
      fecharModal();
    }
  });

  // Só aceita links http(s) ou caminhos internos (/...). Bloqueia javascript:, data:, //host etc.
  function urlSegura(u){
    if(!u) return '';
    u = String(u).trim();
    if(/^https?:\/\//i.test(u)) return u;
    if(/^\/(?!\/)/.test(u)) return u;
    return '';
  }

  function el(tag, cls, txt){
    var x = document.createElement(tag);
    if(cls) x.className = cls;
    if(txt !== undefined) x.textContent = txt;
    return x;
  }

  function detectCategoria(p){
    if(p.categoria) return p.categoria;
    var techs = (p.tecnologias || []).join(' ').toLowerCase();
    if(techs.includes('ia') || techs.includes('inteligência') || techs.includes('educação')) return 'ia';
    if(techs.includes('django') || techs.includes('python') || techs.includes('banco') || techs.includes('processos')) return 'backend';
    return 'frontend';
  }

  function removerEmojis(txt){
    if(!txt) return '';
    try {
      return String(txt).replace(/\p{Extended_Pictographic}\s*/gu, '').trim();
    } catch(e) {
      return String(txt).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|\u26A1|\u2728/g, '').trim();
    }
  }

  function extrairDominioPreview(p){
    if(p.dominio) return p.dominio;
    var raw = p.demo || p.github || p.pdf || '';
    if(!raw) return 'portfolio-higor.onrender.com';
    return String(raw).replace(/^https?:\/\/(www\.)?/i, '').replace(/\/$/, '');
  }

  function cardProjeto(p){
    var c = el('div', 'card novo');

    // 1. Barra Visual Estilo Navegador (Preview do Domínio/Repositório + Status Online)
    var prev = el('div', 'project-preview');
    var dots = el('div', 'dots');
    dots.innerHTML = '<span></span><span></span><span></span>';
    var pUrl = el('span', 'preview-url', extrairDominioPreview(p));
    var envTxt = (p.demo && /^https?:\/\//.test(p.demo)) ? 'Ao Vivo' : (p.pdf ? 'Monografia' : 'GitHub');
    var envCls = 'preview-env' + ((p.demo && /^https?:\/\//.test(p.demo)) ? ' live' : '');
    var pEnv = el('span', envCls, envTxt);
    prev.appendChild(dots);
    prev.appendChild(pUrl);
    prev.appendChild(pEnv);
    c.appendChild(prev);

    // 2. Selo de destaque (Hackathon 24h, Swagger OpenAPI, etc)
    var bText = removerEmojis(p.badge || (p.nome.includes('Hackathon') ? 'Hackathon 24h' : (p.nome.includes('Portfólio') ? 'API REST ao vivo' : '')));
    if(bText){
      var bCls = 'project-badge-tag' + (bText.includes('24h') || bText.includes('Hackathon') ? ' hackathon' : (bText.includes('API') || bText.includes('Swagger') ? ' swagger' : ''));
      c.appendChild(el('span', bCls, bText));
    }

    var top = el('div', 'topo');
    top.appendChild(el('h3', '', String(p.nome)));
    var st = p.status === 'concluido' ? 'concluido' : 'em_andamento';
    top.appendChild(el('span', 'status ' + st, p.status_label || (st === 'concluido' ? 'Concluído' : 'Em andamento')));
    c.appendChild(top);

    c.appendChild(el('p', '', String(p.descricao || '')));

    if(p.tecnologias && p.tecnologias.length){
      var ch = el('div', 'chips');
      p.tecnologias.forEach(function(t){
        var isMatch = currentSearch && String(t).toLowerCase() === currentSearch.toLowerCase();
        var chipEl = el('span', isMatch ? 'chip active-tech' : 'chip', String(t));
        chipEl.title = 'Filtrar projetos com ' + String(t);
        chipEl.addEventListener('click', function(){
          var sInput = document.getElementById('project-search');
          var sClear = document.getElementById('project-search-clear');
          if(currentSearch.toLowerCase() === String(t).toLowerCase()){
            currentSearch = '';
          } else {
            currentSearch = String(t);
          }
          if(sInput) sInput.value = currentSearch;
          if(sClear) sClear.hidden = !currentSearch;
          renderProjetos();
        });
        ch.appendChild(chipEl);
      });
      c.appendChild(ch);
    }

    var rodape = el('div', 'rodape');

    // Botão de Estudo de Caso
    if(p.estudo_caso || p.nome.includes('Hackathon') || p.nome.includes('Portfólio') || p.nome.includes('BSI') || p.nome.includes('Santory')){
      var btnCase = el('button', 'btn-case', '');
      btnCase.type = 'button';
      btnCase.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> Estudo de Caso';
      btnCase.addEventListener('click', function(){
        abrirModalEstudo(p);
      });
      rodape.appendChild(btnCase);
    }

    // Botão Ver Monografia (PDF)
    if(p.pdf){
      var aPdf = el('a', 'pdf-link', '');
      aPdf.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> Ver Monografia (PDF) ↗';
      aPdf.href = urlSegura(p.pdf);
      aPdf.target = '_blank';
      aPdf.rel = 'noopener';
      rodape.appendChild(aPdf);
    }

    // Botão Acessar Projeto / Demo
    if(p.demo && /^https?:\/\//.test(p.demo)){
      var aDemo = el('a', 'demo-link', '');
      aDemo.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg> Acessar Projeto ↗';
      aDemo.href = urlSegura(p.demo);
      aDemo.target = '_blank';
      aDemo.rel = 'noopener';
      rodape.appendChild(aDemo);
    }

    // Botão Swagger UI para o projeto Portfólio
    if(p.swagger || p.nome.includes('Portfólio')){
      var aSwagger = el('a', 'swagger-link', '');
      aSwagger.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Testar API';
      aSwagger.href = urlSegura(p.swagger) || '/api/docs/';
      aSwagger.target = '_blank';
      aSwagger.rel = 'noopener';
      rodape.appendChild(aSwagger);
    }

    // Botão GitHub
    if(p.github && /^https?:\/\//.test(p.github)){
      var aGit = el('a', '', '');
      aGit.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg> GitHub →';
      aGit.href = urlSegura(p.github);
      aGit.target = '_blank';
      aGit.rel = 'noopener';
      rodape.appendChild(aGit);
    }

    if(rodape.children.length){
      c.appendChild(rodape);
    }
    return c;
  }

  function metaSkillPorTitulo(titulo){
    var t = String(titulo || '').toLowerCase();
    if(t.includes('front')){
      return {
        sub: 'Interfaces & SPA',
        svg: '<svg class="icon" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'
      };
    }
    if(t.includes('back') || t.includes('api')){
      return {
        sub: 'Arquitetura & Segurança',
        svg: '<svg class="icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'
      };
    }
    if(t.includes('dado') || t.includes('banco') || t.includes('ferramenta')){
      return {
        sub: 'SQL, Git & Cloud',
        svg: '<svg class="icon" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
      };
    }
    if(t.includes('design') || t.includes('ui')){
      return {
        sub: 'Figma & Usabilidade',
        svg: '<svg class="icon" viewBox="0 0 24 24"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><circle cx="11" cy="11" r="2"/></svg>'
      };
    }
    return {
      sub: 'Comunicação & Processos',
      svg: '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
    };
  }

  var CORE_STACK = ['python', 'django', 'django rest', 'javascript', 'react', 'vue', 'vue 3', 'postgresql', 'mysql', 'git', 'figma', 'swagger / openapi'];

  function cardSkill(h){
    var c = el('div', 'card novo');
    var info = metaSkillPorTitulo(h.titulo);
    var head = el('div', 'skill-head');
    var iconBox = el('span', 'skill-icon-box');
    iconBox.innerHTML = info.svg;
    var meta = el('div', 'skill-meta');
    meta.appendChild(el('small', '', info.sub));
    meta.appendChild(el('h3', '', String(h.titulo)));
    head.appendChild(iconBox);
    head.appendChild(meta);
    c.appendChild(head);

    c.appendChild(el('p', '', String(h.descricao || '')));
    if(h.tecnologias && h.tecnologias.length){
      var ch = el('div', 'chips');
      h.tecnologias.forEach(function(t){
        var isCore = CORE_STACK.indexOf(String(t).toLowerCase()) !== -1;
        ch.appendChild(el('span', isCore ? 'chip chip-core' : 'chip', String(t)));
      });
      c.appendChild(ch);
    }
    return c;
  }

  function atualizarContadoresFiltro(){
    var counts = {
      todos: allProjects.length,
      backend: 0,
      frontend: 0,
      ia: 0
    };
    allProjects.forEach(function(p){
      var cat = detectCategoria(p);
      if(counts[cat] !== undefined) counts[cat]++;
    });
    Object.keys(counts).forEach(function(k){
      var badge = document.querySelector('.filter-count[data-count="' + k + '"]');
      if(badge) badge.textContent = String(counts[k]);
    });
  }

  function aplicarLinksContato(links){
    if(!links || !links.length) return;
    links.forEach(function(item){
      var chave = String(item.chave || '').trim();
      var url = String(item.url || '').trim();
      if(!chave || !url) return;

      if(chave === 'email'){
        var limpo = url.replace(/^mailto:/i, '').trim();
        if(limpo && limpo.indexOf('@') !== -1){
          window.__portfolioEmail = limpo;
          document.querySelectorAll('a[data-contact-key="email"]').forEach(function(a){
            a.href = 'mailto:' + limpo;
            var svg = a.querySelector('svg');
            a.textContent = ' ' + limpo;
            if(svg) a.insertBefore(svg, a.firstChild);
          });
        }
        return;
      }

      var segura = urlSegura(url);
      if(!segura) return;
      document.querySelectorAll('a[data-contact-key="' + chave + '"]').forEach(function(a){
        a.href = segura;
      });
    });
  }

  function renderConquistas(lista){
    var cg = document.getElementById('conquistas-grid');
    if(!cg || !lista || !lista.length) return;
    cg.textContent = '';
    lista.forEach(function(item){
      var card = el('div', 'award-card');
      var badge = el('span', 'award-badge');
      badge.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg> ';
      badge.appendChild(document.createTextNode(String(item.selo || 'Destaque')));
      card.appendChild(badge);
      card.appendChild(el('h3', '', String(item.titulo || '')));
      card.appendChild(el('p', '', String(item.descricao || '')));
      var linkSeg = urlSegura(item.link_url);
      if(linkSeg){
        var wrap = el('div', '');
        wrap.style.marginTop = '12px';
        var a = el('a', 'btn s', '');
        a.style.cssText = 'display:inline-flex;font-size:.82rem;padding:6px 12px;border-radius:8px';
        a.href = linkSeg;
        a.target = '_blank';
        a.rel = 'noopener';
        a.innerHTML = '<svg class="icon icon-sm" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg> ';
        a.appendChild(document.createTextNode(String(item.link_texto || 'Acessar Credencial ↗')));
        wrap.appendChild(a);
        card.appendChild(wrap);
      }
      cg.appendChild(card);
    });
  }

  function renderExperiencias(lista){
    var tl = document.getElementById('formacao-timeline');
    if(!tl || !lista || !lista.length) return;
    tl.textContent = '';
    lista.forEach(function(item){
      var row = el('div', '');
      row.appendChild(el('small', '', String(item.periodo || '')));
      row.appendChild(el('h3', '', String(item.titulo || '')));
      row.appendChild(el('p', '', String(item.descricao || '')));
      tl.appendChild(row);
    });
  }

  function renderPerfil(perfil){
    if(!perfil) return;
    var tDisp = document.getElementById('hero-tag-disp');
    var tLoc = document.getElementById('hero-loc-text');
    var tLead = document.getElementById('hero-lead-text');
    if(tDisp && perfil.tag_disponibilidade) tDisp.textContent = String(perfil.tag_disponibilidade);
    if(tLoc && perfil.localizacao) tLoc.textContent = String(perfil.localizacao);
    if(tLead && perfil.subtitulo_hero) tLead.textContent = String(perfil.subtitulo_hero);
  }

  function renderProjetos(){
    var pg = document.getElementById('projetos-grid');
    if(!pg) return;
    pg.classList.remove('filtering');
    pg.textContent = '';
    var q = currentSearch.trim().toLowerCase();
    var filtrados = allProjects.filter(function(p){
      var matchCat = (currentFilter === 'todos') || (detectCategoria(p) === currentFilter);
      if(!matchCat) return false;
      if(!q) return true;
      var alvo = [
        p.nome || '',
        p.descricao || '',
        p.badge || '',
        (p.tecnologias || []).join(' ')
      ].join(' ').toLowerCase();
      return alvo.indexOf(q) !== -1;
    });

    var frag = document.createDocumentFragment();
    filtrados.forEach(function(p, idx){
      var card = cardProjeto(p);
      card.style.setProperty('--stagger', String(idx));
      frag.appendChild(card);
    });
    pg.appendChild(frag);

    if(!filtrados.length){
      pg.appendChild(el('p', 'muted', 'Nenhum projeto encontrado para este filtro.'));
    }
    initTilt();
  }

  function verificarDeepLinkProjeto(){
    if(deepLinkOpened) return;
    try {
      var params = new URLSearchParams(window.location.search);
      var slugAlvo = params.get('projeto');
      if(!slugAlvo) return;
      var encontrado = allProjects.find(function(p){
        return slugifyProjeto(p.nome) === slugAlvo.toLowerCase();
      });
      if(encontrado){
        deepLinkOpened = true;
        abrirModalEstudo(encontrado);
      }
    } catch(e){}
  }

  function render(d){
    var sg = document.getElementById('skills-grid');
    if(sg){
      sg.textContent = '';
      (d.habilidades || []).forEach(function(h, idx){
        var card = cardSkill(h);
        card.style.setProperty('--stagger', String(idx));
        sg.appendChild(card);
      });
    }
    if(d.projetos && d.projetos.length){
      // Mescla projetos da API com os estudos de caso locais e links completos
      allProjects = d.projetos.map(function(proj){
        var local = DEFAULTS.projetos.find(function(dp){
          var p1 = (proj.nome || '').toLowerCase();
          var p2 = (dp.nome || '').toLowerCase();
          return p1 === p2 || (p1.includes('bsi') && p2.includes('bsi')) || (p1.includes('hackathon') && p2.includes('hackathon')) || (p1.includes('portf') && p2.includes('portf')) || (p1.includes('santory') && p2.includes('santory')) || (p1.includes('ecoapack') && p2.includes('ecoapack')) || (p1.includes('primeiro lar') && p2.includes('primeiro lar')) || (p1.includes('livraria') && p2.includes('livraria')) || (p1.includes('agronovo') && p2.includes('agronovo')) || p1.includes(p2.slice(0, 8)) || p2.includes(p1.slice(0, 8));
        });
        var merged = Object.assign({}, local || {}, proj);
        if(!merged.estudo_caso && local && local.estudo_caso){
          merged.estudo_caso = local.estudo_caso;
        }
        return merged;
      });
    }
    if(d.conquistas && d.conquistas.length){
      renderConquistas(d.conquistas);
    }
    if(d.experiencias && d.experiencias.length){
      renderExperiencias(d.experiencias);
    }
    if(d.perfil){
      renderPerfil(d.perfil);
    }
    atualizarContadoresFiltro();
    if(d.links && d.links.length){
      aplicarLinksContato(d.links);
    }
    renderProjetos();
    verificarDeepLinkProjeto();
    initTilt();
    initReveal();
    window.dispatchEvent(new Event('resize'));
  }

  var filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(function(btn){
    btn.addEventListener('click', function(){
      var nextFilter = btn.getAttribute('data-filter') || 'todos';
      if(nextFilter === currentFilter) return;
      filterButtons.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      currentFilter = nextFilter;
      var pg = document.getElementById('projetos-grid');
      if(pg && !window.matchMedia('(prefers-reduced-motion: reduce)').matches){
        pg.classList.add('filtering');
        setTimeout(renderProjetos, 160);
      } else {
        renderProjetos();
      }
    });
  });

  var searchInput = document.getElementById('project-search');
  var searchClear = document.getElementById('project-search-clear');
  if(searchInput){
    searchInput.addEventListener('input', function(){
      currentSearch = searchInput.value || '';
      if(searchClear) searchClear.hidden = !currentSearch;
      renderProjetos();
    });
  }
  if(searchClear){
    searchClear.addEventListener('click', function(){
      currentSearch = '';
      if(searchInput){
        searchInput.value = '';
        searchInput.focus();
      }
      searchClear.hidden = true;
      renderProjetos();
    });
  }

  render(DEFAULTS);
  fetch(api).then(function(r){ if(!r.ok) throw 0; return r.json(); }).then(render).catch(function(){});
})();

// Métricas Anônimas de Acesso (LGPD / Privacy-first)
(function(){
  function track(tipo){
    try {
      var payload = JSON.stringify({ tipo: tipo, caminho: window.location.pathname || '/' });
      if(navigator.sendBeacon){
        navigator.sendBeacon('/api/visitas/', new Blob([payload], {type: 'application/json'}));
      } else {
        fetch('/api/visitas/', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: payload, keepalive: true }).catch(function(){});
      }
    } catch(e){}
  }
  // Registra visualização da página uma vez
  track('pagina');

  // Registra download do currículo ao clicar no link
  document.querySelectorAll('a[href*="curriculo-higor.pdf"]').forEach(function(a){
    a.addEventListener('click', function(){
      track('download_curriculo');
    });
  });
})();

// PWA: registro do Service Worker e botão "Instalar app"
(function(){
  if('serviceWorker' in navigator){
    window.addEventListener('load', function(){
      navigator.serviceWorker.register('/sw.js', { scope: '/', updateViaCache: 'none' }).then(function(reg){ try{ reg.update(); }catch(e){} }).catch(function(){});
    });
  }

  var btn = document.getElementById('btn-instalar');
  var promptInstalacao = null;

  function avisar(texto){
    var t = document.getElementById('toast'), m = document.getElementById('toast-msg');
    if(!t || !m) return;
    m.textContent = texto;
    t.classList.add('show');
    setTimeout(function(){ t.classList.remove('show'); }, 2800);
  }

  window.addEventListener('beforeinstallprompt', function(e){
    e.preventDefault();
    promptInstalacao = e;
    if(btn) btn.hidden = false;
  });

  if(btn){
    btn.addEventListener('click', function(){
      if(!promptInstalacao) return;
      promptInstalacao.prompt();
      promptInstalacao.userChoice.finally(function(){
        promptInstalacao = null;
        btn.hidden = true;
      });
    });
  }

  window.addEventListener('appinstalled', function(){
    if(btn) btn.hidden = true;
    avisar('App instalado com sucesso!');
  });
})();

// Scroll Unificado, Throttled e com Cache de Posições (Zero Travamentos)
(function(){
  var nav = document.querySelector('header.nav');
  var btnTop = document.getElementById('back-to-top');
  var navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
  var sections = [];
  navLinks.forEach(function(link){
    var id = link.getAttribute('href').slice(1);
    var sec = id ? document.getElementById(id) : null;
    if(sec) sections.push({ id: id, el: sec, link: link });
  });

  var sectionTops = [];
  function cacheTops(){
    sectionTops = sections.map(function(s){
      return { id: s.id, top: s.el.offsetTop, link: s.link };
    });
  }
  cacheTops();
  window.addEventListener('resize', cacheTops, {passive: true});

  var ticking = false;
  function updateScrollEffects(){
    var y = window.scrollY || document.documentElement.scrollTop;
    if(nav){
      if(y > 15){
        if(!nav.classList.contains('scrolled')) nav.classList.add('scrolled');
      } else {
        if(nav.classList.contains('scrolled')) nav.classList.remove('scrolled');
      }
    }
    if(btnTop){
      if(y > 350){
        if(!btnTop.classList.contains('visible')) btnTop.classList.add('visible');
      } else {
        if(btnTop.classList.contains('visible')) btnTop.classList.remove('visible');
      }
    }
    if(sectionTops.length){
      var currentId = '';
      var offset = y + 180;
      for(var i = 0; i < sectionTops.length; i++){
        if(sectionTops[i].top <= offset){
          currentId = sectionTops[i].id;
        }
      }
      for(var j = 0; j < sectionTops.length; j++){
        sectionTops[j].link.classList.toggle('active-section', sectionTops[j].id === currentId);
      }
    }
    ticking = false;
  }

  window.addEventListener('scroll', function(){
    if(!ticking){
      window.requestAnimationFrame(updateScrollEffects);
      ticking = true;
    }
  }, {passive: true});

  if(btnTop){
    btnTop.addEventListener('click', function(){
      window.scrollTo({top: 0, behavior: 'smooth'});
    });
  }

  updateScrollEffects();
})();
// Fundo Interativo com o Mouse: Blueprint de Código Vivo (Live Typing IDE + Caderno BSI + Lente Raio-X no Mouse)
(function(){
  var canvas = document.getElementById('bg-interactive-canvas');
  var glow = document.getElementById('bg-cursor-glow');
  if(!canvas) return;

  var ctx = canvas.getContext('2d');
  if(!ctx) return;

  // Blocos de código e estudo que são digitados ao vivo no fundo (como terminais/cadernos em execução)
  var SNIPPETS = [
    {
      title: 'views.py · Django REST',
      cat: 'code',
      lines: [
        '@require_GET',
        'def api_projetos(request):',
        '    qs = Projeto.objects.filter(visivel=True)',
        '    return JsonResponse({"status": 200})'
      ]
    },
    {
      title: 'query.sql · PostgreSQL',
      cat: 'db',
      lines: [
        'SELECT nome, categoria, stack',
        'FROM recados_projeto',
        'WHERE visivel = TRUE',
        'ORDER BY ordem ASC;'
      ]
    },
    {
      title: 'estudos_bsi.py · Algoritmos & IA',
      cat: 'study',
      lines: [
        '# BSI · IFC — Estrutura de Dados',
        'complexidade = "O(n log n)"',
        'loss = sum((y - y_hat) ** 2)',
        ' status: convergencia_atingida'
      ]
    },
    {
      title: 'deploy.sh · CI/CD Pipeline',
      cat: 'db',
      lines: [
        '$ python manage.py test recados',
        'Ran 41 tests in 4.5s -> OK',
        '$ git push origin main',
        '[render] build & healthz: 200 OK'
      ]
    },
    {
      title: 'security.py · WAF & LGPD',
      cat: 'code',
      lines: [
        'CSP = "script-src 'self'"',
        'ip_hash = sha256(ip + salt)',
        'rate_limit(max_req=5, window=60)',
        'return ShieldStatus.PROTECTED'
      ]
    },
    {
      title: 'calculo_grafos.md · Notas BSI',
      cat: 'study',
      lines: [
        'G = (V, E) · Busca em Largura',
        'f(x) = ∫ e^(-x²) dx',
        'λx. transform(x) => estado_otimo',
        '[IFC · Sistemas de Informação]'
      ]
    }
  ];

  var TRAIL_GLYPHS = ['</>', '{ }', 'def', 'SQL', '01', 'λ', '∑', '=>', 'py', 'BSI', 'API', '&&'];
  var STREAM_CHARS = ['0', '1', '{', '}', ';', 'λ', '∑', '/', '*', '=>', '()', '[]'];

  var width = 0, height = 0, dpr = 1;
  var terminals = [];
  var streams = [];
  var trail = [];
  var ripples = [];
  var mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999, lastTrailX: -9999, lastTrailY: -9999, active: false };
  var rafId = null;
  var tick = 0;

  function getPalette(){
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if(isDark){
      return {
        code: '59, 130, 246',      // #3B82F6
        db: '20, 184, 166',        // #14B8A6
        study: '168, 85, 247',     // #A855F7
        cardBg: '15, 23, 42',
        baseAlpha: 0.24,
        activeAlpha: 0.92,
        crosshairAlpha: 0.45,
        streamAlpha: 0.16
      };
    }
    return {
      code: '29, 78, 216',         // #1D4ED8
      db: '15, 118, 110',          // #0F766E
      study: '126, 34, 206',       // #7E22CE
      cardBg: '237, 242, 247',
      baseAlpha: 0.22,
      activeAlpha: 0.88,
      crosshairAlpha: 0.38,
      streamAlpha: 0.14
    };
  }

  var palette = getPalette();
  var observer = new MutationObserver(function(){ palette = getPalette(); });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  function colorForCat(cat){
    if(cat === 'db') return palette.db;
    if(cat === 'study') return palette.study;
    return palette.code;
  }

  function layoutWorkspace(){
    terminals = [];
    // Posiciona os blocos de código/estudo nas laterais e cantos para emoldurar o conteúdo
    var slots = width < 760 ? [
      { rx: 0.06, ry: 0.12, snipIdx: 0 },
      { rx: 0.52, ry: 0.46, snipIdx: 2 },
      { rx: 0.08, ry: 0.76, snipIdx: 1 }
    ] : [
      { rx: 0.03, ry: 0.13, snipIdx: 0 },
      { rx: 0.74, ry: 0.16, snipIdx: 2 },
      { rx: 0.04, ry: 0.48, snipIdx: 1 },
      { rx: 0.73, ry: 0.52, snipIdx: 3 },
      { rx: 0.05, ry: 0.80, snipIdx: 5 },
      { rx: 0.72, ry: 0.82, snipIdx: 4 }
    ];

    for(var i = 0; i < slots.length; i++){
      var s = slots[i];
      var snip = SNIPPETS[s.snipIdx % SNIPPETS.length];
      var fullText = snip.lines.join('
');
      terminals.push({
        baseX: s.rx * width,
        baseY: s.ry * height,
        x: s.rx * width,
        y: s.ry * height,
        snipIdx: s.snipIdx,
        title: snip.title,
        cat: snip.cat,
        lines: snip.lines,
        totalChars: fullText.length,
        typedChars: Math.floor(Math.random() * fullText.length),
        speed: 0.28 + (i % 3) * 0.07,
        pauseTicks: 0,
        glow: 0
      });
    }

    // Colunas verticais sutis de fluxo binário/sintaxe alinhadas à grade de 56px
    streams = [];
    var cols = Math.max(6, Math.floor(width / 140));
    for(var c = 0; c < cols; c++){
      var colX = Math.round(((c + 0.5) * (width / cols)) / 56) * 56;
      streams.push({
        x: colX,
        y: Math.random() * height,
        vy: 0.65 + Math.random() * 0.75,
        chars: [
          STREAM_CHARS[(c * 3) % STREAM_CHARS.length],
          STREAM_CHARS[(c * 3 + 1) % STREAM_CHARS.length],
          STREAM_CHARS[(c * 3 + 2) % STREAM_CHARS.length],
          STREAM_CHARS[(c * 3 + 3) % STREAM_CHARS.length]
        ],
        cat: c % 3 === 0 ? 'code' : (c % 3 === 1 ? 'db' : 'study')
      });
    }
  }

  function resize(){
    width = window.innerWidth || document.documentElement.clientWidth;
    height = window.innerHeight || document.documentElement.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    layoutWorkspace();
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });

  window.addEventListener('pointermove', function(e){
    var nx = e.clientX;
    var ny = e.clientY;
    if(!mouse.active){
      mouse.x = nx;
      mouse.y = ny;
      mouse.lastTrailX = nx;
      mouse.lastTrailY = ny;
      mouse.active = true;
      if(glow) glow.style.opacity = '1';
    }
    mouse.tx = nx;
    mouse.ty = ny;

    // Rastro de sintaxe que nasce ao mover o mouse
    var dx = nx - mouse.lastTrailX;
    var dy = ny - mouse.lastTrailY;
    if(dx * dx + dy * dy > 1400){
      mouse.lastTrailX = nx;
      mouse.lastTrailY = ny;
      var glyph = TRAIL_GLYPHS[Math.floor(Math.random() * TRAIL_GLYPHS.length)];
      var cats = ['code', 'db', 'study'];
      trail.push({
        x: nx + (Math.random() - 0.5) * 16,
        y: ny + (Math.random() - 0.5) * 16,
        vx: dx * 0.04 + (Math.random() - 0.5) * 0.4,
        vy: -0.6 - Math.random() * 0.5,
        text: glyph,
        cat: cats[trail.length % 3],
        alpha: 0.85,
        scale: 1
      });
      if(trail.length > 22) trail.shift();
    }
  }, { passive: true });

  document.addEventListener('mouseleave', function(){
    mouse.active = false;
    if(glow) glow.style.opacity = '0';
  }, { passive: true });

  window.addEventListener('pointerdown', function(e){
    var x = e.clientX, y = e.clientY;
    ripples.push({ x: x, y: y, r: 10, maxR: 260, alpha: 0.85 });
    // Ao clicar, avança/ilumina os terminais próximos
    for(var i = 0; i < terminals.length; i++){
      var t = terminals[i];
      var dx = (t.x + 110) - x;
      var dy = (t.y + 42) - y;
      if(dx * dx + dy * dy < 320 * 320){
        t.glow = 1;
        t.typedChars = t.totalChars;
        t.pauseTicks = 50;
      }
    }
  }, { passive: true });

  function drawRoundedRect(x, y, w, h, r){
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  function step(){
    if(document.hidden){
      rafId = null;
      return;
    }
    tick += 1;
    ctx.clearRect(0, 0, width, height);

    if(mouse.active){
      mouse.x += (mouse.tx - mouse.x) * 0.2;
      mouse.y += (mouse.ty - mouse.y) * 0.2;
      if(glow){
        glow.style.transform = 'translate3d(' + mouse.x.toFixed(1) + 'px,' + mouse.y.toFixed(1) + 'px,0)';
      }
    }

    // 1. Interseções da Malha Blueprint que acendem perto do Mouse (Cruzetas "+" Técnicas)
    if(mouse.active){
      var gridStep = 56;
      var radius = 210;
      var startX = Math.max(0, Math.floor((mouse.x - radius) / gridStep) * gridStep);
      var endX = Math.min(width, Math.ceil((mouse.x + radius) / gridStep) * gridStep);
      var startY = Math.max(0, Math.floor((mouse.y - radius) / gridStep) * gridStep);
      var endY = Math.min(height, Math.ceil((mouse.y + radius) / gridStep) * gridStep);

      for(var gx = startX; gx <= endX; gx += gridStep){
        for(var gy = startY; gy <= endY; gy += gridStep){
          var dx = gx - mouse.x;
          var dy = gy - mouse.y;
          var distSq = dx * dx + dy * dy;
          if(distSq < radius * radius){
            var prox = 1 - Math.sqrt(distSq) / radius;
            // Leve deslocamento magnético dos cruzamentos da grade
            var wx = gx + (dx / (Math.sqrt(distSq) || 1)) * prox * 5;
            var wy = gy + (dy / (Math.sqrt(distSq) || 1)) * prox * 5;
            var cAlpha = (prox * palette.crosshairAlpha).toFixed(3);
            ctx.strokeStyle = 'rgba(' + palette.code + ',' + cAlpha + ')';
            ctx.lineWidth = 1.1;
            ctx.beginPath();
            ctx.moveTo(wx - 4.5, wy);
            ctx.lineTo(wx + 4.5, wy);
            ctx.moveTo(wx, wy - 4.5);
            ctx.lineTo(wx, wy + 4.5);
            ctx.stroke();
          }
        }
      }
    }

    // 2. Fluxo Vertical de Sintaxe / Dados (Data Streams)
    ctx.font = '600 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
    ctx.textAlign = 'center';
    for(var s = 0; s < streams.length; s++){
      var st = streams[s];
      st.y += st.vy;
      if(st.y > height + 90) st.y = -90;

      var sRgb = colorForCat(st.cat);
      var sBoost = 0;
      if(mouse.active){
        var sdx = st.x - mouse.x;
        var sdy = st.y - mouse.y;
        var sDistSq = sdx * sdx + sdy * sdy;
        if(sDistSq < 220 * 220){
          sBoost = (1 - Math.sqrt(sDistSq) / 220) * 0.45;
        }
      }

      for(var ch = 0; ch < st.chars.length; ch++){
        var cy = st.y - ch * 20;
        var charAlpha = (palette.streamAlpha + sBoost) * (1 - ch * 0.22);
        ctx.fillStyle = 'rgba(' + sRgb + ',' + Math.max(0.03, charAlpha).toFixed(3) + ')';
        ctx.fillText(st.chars[ch], st.x, cy);
      }
    }

    // 3. Blocos de Código & Estudo Autodigitáveis (Live Typing IDE Cards)
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    for(var i = 0; i < terminals.length; i++){
      var t = terminals[i];

      // Avança digitação ao vivo
      if(t.pauseTicks > 0){
        t.pauseTicks -= 1;
        if(t.pauseTicks === 0){
          // Troca para o próximo snippet do ciclo
          t.snipIdx = (t.snipIdx + 1) % SNIPPETS.length;
          var nextSnip = SNIPPETS[t.snipIdx];
          t.title = nextSnip.title;
          t.cat = nextSnip.cat;
          t.lines = nextSnip.lines;
          t.totalChars = nextSnip.lines.join('
').length;
          t.typedChars = 0;
        }
      } else {
        t.typedChars += t.speed;
        if(t.typedChars >= t.totalChars){
          t.typedChars = t.totalChars;
          t.pauseTicks = 150;
        }
      }

      t.glow *= 0.94;
      var cardW = 248;
      var cardH = 98;
      var centerX = t.baseX + cardW * 0.5;
      var centerY = t.baseY + cardH * 0.5;

      // Efeito Lente Raio-X e Parallax quando o mouse se aproxima do bloco de código
      var prox = 0;
      if(mouse.active){
        var mdx = mouse.x - centerX;
        var mdy = mouse.y - centerY;
        var mDist = Math.sqrt(mdx * mdx + mdy * mdy);
        if(mDist < 310){
          prox = 1 - mDist / 310;
          t.glow = Math.max(t.glow, prox);
        }
        // Parallax suave em relação ao cursor
        t.x += ((t.baseX + (mouse.x - width * 0.5) * -0.018) - t.x) * 0.1;
        t.y += ((t.baseY + (mouse.y - height * 0.5) * -0.018) - t.y) * 0.1;
      } else {
        t.x += (t.baseX - t.x) * 0.08;
        t.y += (t.baseY - t.y) * 0.08;
      }

      var vis = palette.baseAlpha + (palette.activeAlpha - palette.baseAlpha) * t.glow;
      var rgb = colorForCat(t.cat);

      // Moldura do mini-terminal / nota de estudo
      drawRoundedRect(t.x, t.y, cardW, cardH, 10);
      ctx.fillStyle = 'rgba(' + palette.cardBg + ',' + (0.35 + t.glow * 0.48).toFixed(3) + ')';
      ctx.fill();
      ctx.strokeStyle = 'rgba(' + rgb + ',' + (0.18 + t.glow * 0.55).toFixed(3) + ')';
      ctx.lineWidth = 1 + t.glow * 0.8;
      ctx.stroke();

      // Barra de título da janela de código
      ctx.beginPath();
      ctx.arc(t.x + 12, t.y + 12, 2.6, 0, Math.PI * 2);
      ctx.arc(t.x + 21, t.y + 12, 2.6, 0, Math.PI * 2);
      ctx.arc(t.x + 30, t.y + 12, 2.6, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + rgb + ',' + (vis * 0.85).toFixed(3) + ')';
      ctx.fill();

      ctx.font = '700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
      ctx.fillStyle = 'rgba(' + rgb + ',' + (vis * 0.95).toFixed(3) + ')';
      ctx.fillText(t.title, t.x + 40, t.y + 7);

      // Linhas sendo digitadas com cursor piscante
      ctx.font = '500 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
      var rem = Math.floor(t.typedChars);
      var lineY = t.y + 26;
      for(var ln = 0; ln < t.lines.length; ln++){
        if(rem <= 0) break;
        var fullLine = t.lines[ln];
        var slice = fullLine.slice(0, rem);
        rem -= fullLine.length + 1;

        ctx.fillStyle = 'rgba(' + rgb + ',' + vis.toFixed(3) + ')';
        ctx.fillText(slice, t.x + 12, lineY);

        // Desenha o cursor de digitação no final da linha ativa
        if(rem <= 0 && (Math.floor(tick / 18) % 2 === 0)){
          var cw = ctx.measureText(slice).width;
          ctx.fillRect(t.x + 14 + cw, lineY + 1, 5.5, 11);
        }
        lineY += 16;
      }
    }

    // 4. Rastro de Símbolos de Programação & Matemática que segue o Mouse
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for(var tr = trail.length - 1; tr >= 0; tr--){
      var item = trail[tr];
      item.x += item.vx;
      item.y += item.vy;
      item.alpha *= 0.95;
      item.scale += 0.008;
      if(item.alpha < 0.03){
        trail.splice(tr, 1);
        continue;
      }
      var tRgb = colorForCat(item.cat);
      ctx.font = '700 ' + Math.round(11 * item.scale) + 'px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
      ctx.fillStyle = 'rgba(' + tRgb + ',' + item.alpha.toFixed(3) + ')';
      ctx.fillText(item.text, item.x, item.y);
    }

    // 5. Ondas de Execução ao Clicar
    for(var r = ripples.length - 1; r >= 0; r--){
      var rp = ripples[r];
      rp.r += 5.5;
      rp.alpha *= 0.93;
      if(rp.r >= rp.maxR || rp.alpha < 0.02){
        ripples.splice(r, 1);
        continue;
      }
      ctx.beginPath();
      ctx.arc(rp.x, rp.y, rp.r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(' + palette.db + ',' + rp.alpha.toFixed(3) + ')';
      ctx.lineWidth = 1.6;
      ctx.stroke();

      if(rp.r < 95){
        ctx.font = '700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
        ctx.fillStyle = 'rgba(' + palette.db + ',' + rp.alpha.toFixed(3) + ')';
        ctx.fillText('[RUN · 200 OK]', rp.x, rp.y - rp.r - 8);
      }
    }

    rafId = window.requestAnimationFrame(step);
  }

  document.addEventListener('visibilitychange', function(){
    if(!document.hidden && !rafId){
      rafId = window.requestAnimationFrame(step);
    }
  });

  rafId = window.requestAnimationFrame(step);
})();
