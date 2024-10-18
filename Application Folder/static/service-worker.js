const CACHE_NAME = 'water-damage-inspection-v1';
const urlsToCache = [
    '/',
    '/mobile',
    '/static/css/custom.css',
    '/static/js/app.js',
    '/static/images/logo.svg',
    'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
