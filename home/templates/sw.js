const assets_cache_name = "medstore-assets-cache";
const asset_files = [
    '/static/favicon.ico',
    '/static/cart.js',
    '/static/pikachu.js',
    '/static/style.css'
];

self.addEventListener('install', event=>{
  event.waitUntil(caches.open(assets_cache_name)
  .then(asset_cache=>{
    asset_cache.addAll(asset_files);
  })
  .then(self.skipWaiting())
  .catch(err=>{
    console.info(`%cUnable to Cache resources: %c${err}`, `color: 'blue';`, `color: red`);
  })
  )
});

// Disable Caches while in development mode
self.addEventListener('fetch', event=>{
  if(!event.request.url.startsWith(location.origin) || event.request.url.startsWith('http://localhost')){
    event.respondWith(fetch(event.request));
    return;
  }

  // Respond from caches for the same-origin pages
  event.respondWith(
    caches.match(event.request).then(res=>{
      // Respond with cache only for the static pages
      return res || fetch(event.request);
      }).catch(()=>{
      // Provide fallback when offline
    })
  )

  event.waitUntil(
    // Update the cache
    caches.open(assets_cache_name).then(asset_cache=>{
      fetch(event.request).then(res=>{
        asset_cache.put(event.request, res);
      })
    })
  )
})
