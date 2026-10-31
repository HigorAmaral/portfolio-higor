// Gerenciador de Tema (Dark / Light Mode)
(function(){
  var btn = document.getElementById('theme-toggle');
  var iconSun = document.getElementById('theme-icon-sun');
  var iconMoon = document.getElementById('theme-icon-moon');
  var html = document.documentElement;

  function getPreferredTheme(){
    var saved = localStorage.getItem('theme');
    if(saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
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
    localStorage.setItem('theme', theme);
  }

  applyTheme(getPreferredTheme());

  btn.addEventListener('click', function(){
    var current = html.getAttribute('data-theme') || 'light';
    applyTheme(current === 'dark' ? 'light' : 'dark');
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

    var speed = isDeleting ? 40 : 80;
    if(!isDeleting && charIdx === current.length){
      speed = 1800;
      isDeleting = true;
    } else if(isDeleting && charIdx === 0){
      isDeleting = false;
      wordIdx = (wordIdx + 1) % words.length;
      speed = 400;
    }

    setTimeout(tick, speed);
  }
  tick();
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
    var email = 'amarahigor@gmail.com';
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
  var colors = ['#4f46e5', '#8b86ff', '#ec4899', '#f59e0b', '#10b981', '#06b6d4'];
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

  var start = Date.now();
  function animate(){
    var elapsed = Date.now() - start;
    if(elapsed > 2500){
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(function(p){
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
    });
    requestAnimationFrame(animate);
  }
  animate();
}

// Tilt 3D sutil nos Cards (Desktop)
function initTilt(){
  if(!window.matchMedia('(hover: hover)').matches) return;
  var cards = document.querySelectorAll('.card, .focus-card, .award-card');
  cards.forEach(function(card){
    card.addEventListener('mousemove', function(e){
      var rect = card.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      var cx = rect.width / 2;
      var cy = rect.height / 2;
      var dx = (x - cx) / cx;
      var dy = (y - cy) / cy;
      card.style.transform = 'perspective(900px) rotateX(' + (-dy * 4) + 'deg) rotateY(' + (dx * 4) + 'deg) translateY(-4px)';
    });
    card.addEventListener('mouseleave', function(){
      card.style.transform = '';
    });
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

// Efeito reveal ao scrollar
(function(){
  var els = document.querySelectorAll('section h2, .card, .timeline > div, .focus-card, .award-card');
  if(!('IntersectionObserver' in window)){ return; }
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, {threshold: 0.12});
  els.forEach(function(el){
    el.classList.add('reveal');
    io.observe(el);
  });
})();


// Barra de Progresso de Leitura no Topo
(function(){
  var bar = document.getElementById('scroll-progress');
  if(!bar) return;
  window.addEventListener('scroll', function(){
    var winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = height > 0 ? (winScroll / height) * 100 : 0;
    bar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
  }, {passive: true});
})();

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
      {"titulo": "Front-end & Web", "descricao": "Interfaces rápidas, responsivas e organizadas em componentes.", "tecnologias": ["JavaScript", "HTML5", "CSS3", "React", "Vue"]},
      {"titulo": "Back-end & APIs", "descricao": "APIs RESTful, autenticação, segurança e painéis administrativos.", "tecnologias": ["Python", "Django", "Gunicorn", "PostgreSQL"]},
      {"titulo": "Dados & Ferramentas", "descricao": "Modelagem relacional, Git, GitHub e ambientes de desenvolvimento.", "tecnologias": ["PostgreSQL", "MySQL", "Git", "VS Code", "Linux/Windows"]},
      {"titulo": "Design & UI/UX", "descricao": "Protótipos navegáveis no Figma e design systems pensados no usuário.", "tecnologias": ["Figma", "UI/UX", "Prototipagem"]},
      {"titulo": "Idiomas & Comunicação", "descricao": "Inglês intermediário para documentação técnica e comunicação.", "tecnologias": ["Inglês (4 anos KNN)", "Boa comunicação"]}
    ],
    "projetos": [
      {
        "nome": "Hackathon Fábrica 2k26",
        "badge": "🏆 Desenvolvido em 24h · Maratona Hackathon",
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
          "badge": "🏆 Hackathon 24H · IA Aplicada",
          "desafio": "Criar uma solução tecnológica completa em apenas 24 horas contínuas para apoiar professores da rede pública a adaptar atividades e avaliações para crianças neuroatípicas de 6 a 9 anos (com TEA e TDAH), além de estruturar relatórios de observação em sala de aula.",
          "solucao": "Desenvolvemos em equipe uma aplicação web em Python e Django integrada com modelos de Inteligência Artificial. A ferramenta analisa o plano de aula do professor e gera versões adaptadas com linguagem direta, suporte imagético, redução de sobrecarga sensorial e roteiros lúdicos diferenciados. Deploy efetuado no ambiente da Fábrica de Software do IFC.",
          "aprendizados": "Trabalho ágil sob altíssima pressão de tempo, prototipagem relâmpago, integração de IA no backend Django e entrega de um produto funcional pronto para uso em sala de aula em 24 horas."
        }
      },
      {
        "nome": "Portfólio Pessoal & API REST",
        "badge": "⚡ API REST ao vivo (OpenAPI 3.0)",
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
          "badge": "⚡ Django 6 · PostgreSQL · Swagger",
          "desafio": "Construir uma aplicação web rápida, moderna e de custo zero de infraestrutura (Render Free Tier), porém com arquitetura, testes e padrões de segurança de nível sênior.",
          "solucao": "Estruturação de backend Django com PostgreSQL na nuvem, esteira de CI/CD no GitHub Actions com 21 testes unitários automatizados, documentação interativa Swagger (/api/docs/), rate limiting por IP confiável (True-Client-IP), proteção estrita de headers (CSP, HSTS, COOP), auditoria de CVEs com pip-audit e bot keep-alive para zero downtime.",
          "aprendizados": "Implementação prática de esteira de integração contínua (CI/CD), arquitetura resiliente na nuvem, hardening contra ataques cibernéticos e documentação padronizada OpenAPI 3.0."
        }
      },
      {
        "nome": "Santory Pizzaria",
        "badge": "🍕 Projeto Integrador · IFC",
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
          "badge": "🍕 Vue 3 · Django REST · Vercel · Render · Projeto Integrador",
          "desafio": "A Pizzaria Santory operava com fluxos semi-manuais e anotações em papel para pedidos de balcão e telefone, causando lentidão no atendimento, erros na transmissão dos pedidos à cozinha, falta de controle de estoque de ingredientes e ausência de rastreamento de entregas ou pagamentos online.",
          "solucao": "Desenvolvimento de um ecossistema web integrado com arquitetura desacoplada: interface SPA reativa em Vue 3 (Vite) na Vercel e backend RESTful com Django no Render. Modelagem relacional completa (DER), controle automático de estoque com baixa por insumo, PDV em tempo real para salão/cozinha, perfis de acesso (Administrador, Atendente, Pizzaiolo, Entregador e Cliente) e catálogo interativo com personalização de pedidos.",
          "aprendizados": "Arquitetura cliente-servidor desacoplada (Vue 3 + Django API), engenharia de requisitos com 37 RFs e 20 regras de negócio, modelagem de banco de dados relacional (DER), trabalho em equipe com Git/GitHub e deploy em múltiplos provedores em nuvem (Vercel e Render)."
        }
      },
      {
        "nome": "Projeto BSI: Microprocessos Acadêmicos",
        "badge": "🔬 Pesquisa Científica & BPMN · IFC",
        "dominio": "ifc-araquari.edu.br/bsi",
        "descricao": "Mapeamento e análise aprofundada dos microprocessos acadêmicos do Bacharelado em Sistemas de Informação no IFC Câmpus Araquari com modelagem BPMN, avaliação pelo modelo PEMM (Michael Hammer), diretrizes estratégicas 5W2H e engenharia de requisitos com conformidade LGPD.",
        "tecnologias": ["BPMN / BPM", "Engenharia de Requisitos", "Modelo PEMM", "Matriz 5W2H", "LGPD", "LaTeX"],
        "github": "",
        "demo": "",
        "pdf": "/static/projeto-bsi-microprocessos.pdf",
        "status": "em_andamento",
        "status_label": "Em andamento",
        "categoria": "backend",
        "estudo_caso": {
          "titulo": "Mapeamento & Análise de Microprocessos (BSI IFC)",
          "badge": "🔬 BPMN · Modelo PEMM · 5W2H · Engenharia de Requisitos · LaTeX",
          "desafio": "A dispersão de plataformas (SIGAA, SEI, Google Forms) e o trâmite manual nos registros discentes do IFC geravam retrabalho na secretaria acadêmica, falta de rastreabilidade de solicitações para os alunos e diagnóstico de maturidade inicial (P0 em indicadores e infraestrutura de TI).",
          "solucao": "Estruturação qualitativa da trajetória discente em 4 fases (Entrada, Rotina, Pedidos Especiais e Conclusão), modelagem formal de 4 fluxos em BPMN (matrículas, TCC, dispensas, regime disciplinar), aplicação do modelo de maturidade PEMM de Michael Hammer, plano de ação 5W2H e levantamento rigoroso de 8 Requisitos Funcionais (RF01-RF08) e 4 Não-Funcionais (RNF01-RNF04) com proteção de dados e acessibilidade.",
          "aprendizados": "Domínio prático de Gestão de Processos de Negócio (BPM/BPMN), Engenharia de Requisitos aplicada ao contexto educacional público federal, diagnóstico organizacional e redação científica técnica avançada com diagramação em LaTeX."
        }
      }
    ]
  };

  var base = (document.querySelector('meta[name="api-base"]') || {}).content || '';
  var api = base.replace(/\/$/, '') + '/api/conteudo/';
  var currentFilter = 'todos';
  var allProjects = DEFAULTS.projetos;

  // Gerenciamento do Modal de Estudo de Caso
  var modalBackdrop = document.getElementById('modal-case');
  var modalClose = document.getElementById('modal-close');
  var modalTitle = document.getElementById('modal-title');
  var modalBadge = document.getElementById('modal-badge');
  var modalDesafio = document.getElementById('modal-desafio');
  var modalSolucao = document.getElementById('modal-solucao');
  var modalAprendizados = document.getElementById('modal-aprendizados');
  var modalFooter = document.getElementById('modal-footer');

  function fecharModal(){
    if(modalBackdrop){
      modalBackdrop.classList.remove('open');
      modalBackdrop.setAttribute('aria-hidden', 'true');
    }
  }

  function abrirModalEstudo(p){
    var ec = p.estudo_caso;
    if(!ec || !modalBackdrop) return;

    modalTitle.textContent = ec.titulo || p.nome;
    modalBadge.textContent = ec.badge || p.badge || 'Estudo de Caso';
    modalDesafio.textContent = ec.desafio || 'Desafio técnico em produção.';
    modalSolucao.textContent = ec.solucao || 'Solução estruturada com boas práticas de engenharia de software.';
    modalAprendizados.textContent = ec.aprendizados || 'Evolução técnica e trabalho colaborativo.';

    modalFooter.innerHTML = '';
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

  function cardProjeto(p){
    var c = el('div', 'card novo');

    // Mockup visual de navegador no topo do card
    var prev = el('div', 'project-preview');
    var dots = el('div', 'dots');
    dots.innerHTML = '<span></span><span></span><span></span>';
    prev.appendChild(dots);
    var uStr = p.dominio || (p.demo ? p.demo.replace(/^https?:\/\//, '').split('/')[0] : (p.github ? p.github.replace(/^https?:\/\//, '') : 'higor.dev'));
    prev.appendChild(el('span', 'preview-url', uStr));
    c.appendChild(prev);

    // Selo de destaque (Hackathon 24h, Swagger OpenAPI, etc)
    var bText = p.badge || (p.nome.includes('Hackathon') ? '🏆 Hackathon 24h' : (p.nome.includes('Portfólio') ? '⚡ API REST ao vivo' : ''));
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
      p.tecnologias.forEach(function(t){ ch.appendChild(el('span', 'chip', String(t))); });
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

  function cardSkill(h){
    var c = el('div', 'card novo'), top = el('div', 'topo');
    top.appendChild(el('h3', '', String(h.titulo)));
    c.appendChild(top);
    c.appendChild(el('p', '', String(h.descricao || '')));
    if(h.tecnologias && h.tecnologias.length){
      var ch = el('div', 'chips');
      h.tecnologias.forEach(function(t){ ch.appendChild(el('span', 'chip', String(t))); });
      c.appendChild(ch);
    }
    return c;
  }

  function renderProjetos(){
    var pg = document.getElementById('projetos-grid');
    if(!pg) return;
    pg.textContent = '';
    var filtrados = allProjects.filter(function(p){
      if(currentFilter === 'todos') return true;
      return detectCategoria(p) === currentFilter;
    });

    filtrados.forEach(function(p){
      pg.appendChild(cardProjeto(p));
    });

    if(!filtrados.length){
      pg.appendChild(el('p', 'muted', 'Nenhum projeto encontrado nesta categoria.'));
    }
    initTilt();
  }

  function render(d){
    var sg = document.getElementById('skills-grid');
    if(sg){
      sg.textContent = '';
      (d.habilidades || []).forEach(function(h){ sg.appendChild(cardSkill(h)); });
    }
    if(d.projetos && d.projetos.length){
      // Mescla projetos da API com os estudos de caso locais e links completos
      allProjects = d.projetos.map(function(proj){
        var local = DEFAULTS.projetos.find(function(dp){
          var p1 = (proj.nome || '').toLowerCase();
          var p2 = (dp.nome || '').toLowerCase();
          return (p1.includes('bsi') && p2.includes('bsi')) || (p1.includes('hackathon') && p2.includes('hackathon')) || (p1.includes('portf') && p2.includes('portf')) || (p1.includes('santory') && p2.includes('santory')) || p1.includes(p2.slice(0, 8)) || p2.includes(p1.slice(0, 8));
        });
        return Object.assign({}, local || {}, proj);
      });
    }
    renderProjetos();
    initTilt();
  }

  var filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(function(btn){
    btn.addEventListener('click', function(){
      filterButtons.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter') || 'todos';
      renderProjetos();
    });
  });

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
      navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function(){});
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

// Botão Voltar ao Topo
(function(){
  var btn = document.getElementById('back-to-top');
  if(!btn) return;
  var ticking = false;
  window.addEventListener('scroll', function(){
    if(!ticking){
      window.requestAnimationFrame(function(){
        if(window.scrollY > 350){
          btn.classList.add('visible');
        } else {
          btn.classList.remove('visible');
        }
        ticking = false;
      });
      ticking = true;
    }
  }, {passive: true});
  btn.addEventListener('click', function(){
    window.scrollTo({top: 0, behavior: 'smooth'});
  });
})();
