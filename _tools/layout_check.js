(async () => {
  const res = { w: innerWidth, h: innerHeight }; const issues = [];
  const tabs = [...document.querySelectorAll('.nav-btn')];
  for (const b of tabs) {
    b.click(); await new Promise(r => setTimeout(r, 350));
    const tab = document.querySelector('.tab.active'); const d = document.documentElement;
    if (d.scrollWidth > innerWidth + 1) issues.push(tab.id + ': h-scroll ' + d.scrollWidth);
    const over = [...tab.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > innerWidth + 2 || r.left < -2) && getComputedStyle(e).position !== 'fixed'; }).slice(0, 3).map(e => e.tagName + '.' + String(e.className).slice(0, 25));
    if (over.length) issues.push(tab.id + ': offscreen ' + over.join(','));
  }
  const nav = [...document.querySelectorAll('.nav-btn')].map(b => { const s = b.querySelector('span:last-child'); return s.scrollWidth > b.clientWidth + 1; });
  if (nav.some(Boolean)) issues.push('nav label overflow: ' + nav.map((v, i) => v ? i : '').filter(x => x !== '').join());
  const navEl = document.querySelector('.bottom-nav'); const nr = navEl.getBoundingClientRect();
  res.navPos = nr.left < 5 && nr.height > innerHeight * 0.8 ? 'sidebar' : 'bottom';
  const small = [...document.querySelectorAll('.tab.active button, .bottom-nav button, .tab.active a, .tab.active select')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 30 || r.width < 30); }).length;
  res.smallTargets = small;
  const col = document.querySelector('.tab.active'); res.contentW = Math.round(col.getBoundingClientRect().width);
  tabs[0].click(); res.issues = issues; return res;
})()
