document.addEventListener('DOMContentLoaded', ()=>{
  const path = (location.pathname.replace(/\/+$/,'') || '/').toLowerCase();
  document.querySelectorAll('.nav a').forEach(a=>{
    const href = (a.getAttribute('href') || '').toLowerCase().replace(/\/+$/,'');
    const isMatch =
      href === path ||
      (href === '/' && (path === '/' || path === '/index.html')) ||
      (href === '/roadmap' && (path === '/index.html' || path === '/'));
    if (isMatch) a.classList.add('active');
  });
});


