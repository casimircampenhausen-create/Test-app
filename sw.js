// Bei jeder Änderung an App-Dateien CACHE_VERSION erhöhen, sonst bleibt die alte Version im Cache.
const CACHE_VERSION = 'v1';
const CACHE_NAME = 'habit-tracker-' + CACHE_VERSION;

// Relative Pfade: lösen sich gegen den SW-Scope auf (funktioniert unter /repo-name/).
const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('habit-tracker-') && k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Cache-First für gleiche Origin; bei Cache-Miss Netzwerk und Ergebnis nachcachen.
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => {
      if (hit) return hit;
      return fetch(req).then(res => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, copy));
        }
        return res;
      }).catch(() => {
        // Offline-Fallback für Seitennavigation (z. B. Start über Home-Bildschirm-Icon)
        if (req.mode === 'navigate') return caches.match('./index.html');
        return Response.error();
      });
    })
  );
});
