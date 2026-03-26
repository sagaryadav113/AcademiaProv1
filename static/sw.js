const CACHE_NAME = 'academiapro-static-v1';
const OFFLINE_URL = '/static/offline.html';

// Cache only static shell assets. Avoid caching API/AI responses for security and freshness.
const STATIC_ASSETS = [
  '/',
  '/static/modern-style.css',
  '/static/manifest.webmanifest',
  OFFLINE_URL
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Never cache API/dynamic endpoints to protect privacy and avoid stale sensitive data.
  if (
    url.pathname.startsWith('/ask-lab-ai') ||
    url.pathname.startsWith('/analyze-lab-file') ||
    url.pathname.startsWith('/detect-ai') ||
    url.pathname.startsWith('/check-plagiarism') ||
    url.pathname.startsWith('/upload') ||
    url.pathname.startsWith('/convert') ||
    url.pathname.startsWith('/test-connection') ||
    url.pathname.startsWith('/save-data') ||
    url.pathname.startsWith('/get-data')
  ) {
    return;
  }

  // Network-first for navigation: keep content fresh, fallback offline page if disconnected.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          return cached || caches.match(OFFLINE_URL);
        })
    );
    return;
  }

  // Cache-first for safe static assets only.
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          if (response && response.status === 200) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          }
          return response;
        });
      })
    );
  }
});
