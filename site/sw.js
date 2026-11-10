// Scholarship Radar: installable app + offline copy of the last listings seen.
// Network first, always: listings and deadlines change daily, so the saved copy is
// used only when the device is offline. Requests to other sites (Supabase, fonts,
// analytics) are left alone.
const CACHE = 'radar-v1';
const FILES = [
  '/',
  '/privacy.html',
  '/config.js',
  '/manifest.webmanifest',
  '/data/opportunities.json',
  '/data/featured.json',
  '/data/scholarships.json',
  '/data/qa.json',
  '/img/logo-mark.png',
  '/img/icon-192.png',
  '/img/icon-512.png',
  '/favicon-32.png',
  '/favicon.png',
  '/apple-touch-icon.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.all(FILES.map((f) => c.add(new Request(f, {cache: 'reload'})).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return res;
      })
      .catch(() =>
        caches.match(e.request, {ignoreSearch: true}).then((hit) => {
          if (hit) return hit;
          if (e.request.mode === 'navigate') return caches.match('/');
          return Response.error();
        })
      )
  );
});
