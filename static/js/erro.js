  (function(){
    var b = document.getElementById('voltar');
    if(!b) return;
    // Só mostra "Página anterior" se houver histórico dentro do próprio site
    var temHistorico = history.length > 1 && document.referrer && document.referrer.indexOf(location.host) !== -1;
    if(!temHistorico){ b.style.display = 'none'; return; }
    b.addEventListener('click', function(){ history.back(); });
  })();
  (function(){
    var r = document.getElementById('recarregar');
    if(r) r.addEventListener('click', function(){ location.reload(); });
  })();
