/* Service Worker do portfólio — cache offline seguro.
 * Estratégias:
 *  - Página inicial (/): network-first, cai para o cache quando offline.
 *  - /static/: cache-first (arquivos versionados e imutáveis na prática).
 *  - /api/conteudo/: stale-while-revalidate (cards aparecem offline).
 *  - Demais rotas (/api/*, painel, POSTs): nunca são interceptadas nem cacheadas.
 */
const VERSAO = 'v1';
const CACHE_PAGINAS = 'higor-paginas-' + VERSAO;
const CACHE_ESTATICOS = 'higor-estaticos-' + VERSAO;
const CACHE_API = 'higor-api-' + VERSAO;
const CACHES_ATUAIS = [CACHE_PAGINAS, CACHE_ESTATICOS, CACHE_API];

const PRECACHE = [
  '/',
  '/manifest.webmanifest',
  '/static/pwa/icon-192.png',
  '/static/pwa/icon-512.png',
  '/static/pwa/apple-touch-icon.png',
  '/static/pwa/favicon-32.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_PAGINAS)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((chaves) => Promise.all(
        chaves.filter((c) => c.startsWith('higor-') && !CACHES_ATUAIS.includes(c)).map((c) => caches.delete(c))
      ))
      .then(() => self.clients.claim())
  );
});

function respostaCacheavel(resp) {
  return resp && resp.ok && resp.type === 'basic';
}

async function networkFirst(request) {
  const cache = await caches.open(CACHE_PAGINAS);
  try {
    const resp = await fetch(request);
    if (respostaCacheavel(resp)) cache.put('/', resp.clone());
    return resp;
  } catch (e) {
    const emCache = await cache.match('/');
    return emCache || new Response(
      '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<title>Offline</title><body style="font-family:system-ui;background:#0e1120;color:#e2e8f0;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center">' +
      '<div><h1>Você está offline</h1><p>Conecte-se à internet e tente novamente.</p></div>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE_ESTATICOS);
  const emCache = await cache.match(request);
  if (emCache) return emCache;
  const resp = await fetch(request);
  // PDFs grandes só são guardados depois de abertos uma vez
  if (respostaCacheavel(resp)) cache.put(request, resp.clone());
  return resp;
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_API);
  const emCache = await cache.match(request);
  const rede = fetch(request)
    .then((resp) => { if (respostaCacheavel(resp)) cache.put(request, resp.clone()); return resp; })
    .catch(() => emCache);
  return emCache || rede;
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (request.mode === 'navigate' && url.pathname === '/') {
    event.respondWith(networkFirst(request));
    return;
  }
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(request));
    return;
  }
  if (url.pathname === '/api/conteudo/') {
    event.respondWith(staleWhileRevalidate(request));
  }
  // Qualquer outra rota segue direto para a rede, sem cache.
});
