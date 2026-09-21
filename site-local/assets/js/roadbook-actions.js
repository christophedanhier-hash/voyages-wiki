// Actions roadbook — 📥📦🔗 (identique à BAVI)
(function(){
  if(document.querySelector('.roadbook-actions')) return;
  
  const path = window.location.pathname.replace(/\/$/,'').split('/').pop() || 'roadbook';
  const repo = 'christophedanhier-hash/voyages-wiki';
  const label = 'archive';
  
  const bar = document.createElement('div');
  bar.className = 'roadbook-actions';
  bar.style.cssText = 'display:flex;gap:8px;margin:12px 0;flex-wrap:wrap';
  bar.innerHTML = `
    <button onclick="window.print()" style="padding:4px 12px;background:var(--md-code-bg);border:1px solid var(--md-default-fg-color--lightest);border-radius:4px;cursor:pointer;font-size:.75rem" title="Imprimer en PDF">📥 PDF</button>
    <a href="https://github.com/${repo}/issues/new?title=archive%3A+${path}&body=D%C3%A9placer+dans+archive%2F&labels=${label}" target="_blank" style="padding:4px 12px;background:var(--md-code-bg);border:1px solid var(--md-default-fg-color--lightest);border-radius:4px;cursor:pointer;font-size:.75rem;text-decoration:none;color:var(--md-default-fg-color)" title="Archiver ce roadbook">📦 Archiver</a>
    <a href="https://raw.githubusercontent.com/${repo}/main/docs/${path}/index.md" target="_blank" style="padding:4px 12px;background:var(--md-code-bg);border:1px solid var(--md-default-fg-color--lightest);border-radius:4px;cursor:pointer;font-size:.75rem;text-decoration:none;color:var(--md-default-fg-color)" title="Voir le markdown source">🔗 Raw</a>
  `;
  
  const h1 = document.querySelector('article h1');
  if(h1) h1.after(bar);
})();
