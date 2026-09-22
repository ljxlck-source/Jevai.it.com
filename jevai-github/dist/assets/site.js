(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  menu?.addEventListener('click', () => {const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.getElementById('navigation').classList.toggle('open',open);});
  const input=document.getElementById('project-search');
  if(input){
    const cards=[...document.querySelectorAll('.project-card')];
    const buttons=[...document.querySelectorAll('[data-category][aria-pressed]')];
    const grid=document.querySelector('.project-grid');const count=document.getElementById('result-count');const reset=document.getElementById('reset-filters');const sort=document.getElementById('project-sort');let category='all';
    const params=new URLSearchParams(location.search);const initial=params.get('category');if(buttons.some(b=>b.dataset.category===initial)) category=initial;
    input.value=params.get('q')||'';
    function update(){const q=input.value.trim().toLowerCase();let visible=0;for(const card of cards){card.hidden=!((category==='all'||card.dataset.category===category)&&card.dataset.search.includes(q));if(!card.hidden)visible++;}
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category===category)));
      count.textContent=visible===46?'Showing all 46 projects':`Showing ${visible} of 46 projects`;reset.hidden=category==='all'&&!q;document.getElementById('no-results').hidden=visible>0;
      const next=new URL(location.href);next.searchParams.delete('category');next.searchParams.delete('q');if(category!=='all')next.searchParams.set('category',category);if(q)next.searchParams.set('q',input.value.trim());history.replaceState(null,'',next.pathname+next.search+next.hash);
    }
    function clear(){category='all';input.value='';update();}
    buttons.forEach(b=>b.addEventListener('click',()=>{category=b.dataset.category;update();}));input.addEventListener('input',update);reset.addEventListener('click',clear);document.getElementById('empty-reset').addEventListener('click',clear);
    sort.addEventListener('change',()=>{const ordered=sort.value==='name'?[...cards].sort((a,b)=>a.dataset.name.localeCompare(b.dataset.name)):cards;ordered.forEach(card=>grid.appendChild(card));});update();
  }
  const calc=document.getElementById('savings-calc');if(calc){const update=()=>{const spend=Math.max(0,Number(calc.querySelector('[name=spend]').value)||0),share=Math.min(100,Math.max(0,Number(calc.querySelector('[name=share]').value)||0)),reduction=Math.min(100,Math.max(0,Number(calc.querySelector('[name=reduction]').value)||0));calc.querySelector('output').textContent=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(spend*share/100*reduction/100)+' / month';};calc.addEventListener('input',update);update();}
  const consentBox=document.getElementById('analytics-choice');const KEY='jev-analytics-consent';let consent=null;try{consent=localStorage.getItem(KEY);}catch{}
  function startAnalytics(){if(window.__jevAnalytics)return;window.__jevAnalytics=true;window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments);};window.gtag('js',new Date());window.gtag('config','G-6B7H863MFF',{page_location:location.origin+location.pathname,allow_google_signals:false,allow_ad_personalization_signals:false});const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id=G-6B7H863MFF';document.head.appendChild(script);}
  if(consent==='granted'){window['ga-disable-G-6B7H863MFF']=false;startAnalytics();}else if(!consent){consentBox.hidden=false;}
  document.querySelectorAll('[data-consent]').forEach(b=>b.addEventListener('click',()=>{consent=b.dataset.consent;try{localStorage.setItem(KEY,consent);}catch{}consentBox.hidden=true;window['ga-disable-G-6B7H863MFF']=consent!=='granted';if(consent==='granted'){window.gtag?.('consent','update',{analytics_storage:'granted'});startAnalytics();}else{window.gtag?.('consent','update',{analytics_storage:'denied'});for(const cookie of document.cookie.split(';')){const name=cookie.split('=')[0].trim();if(name.startsWith('_ga')){document.cookie=name+'=; Max-Age=0; path=/';document.cookie=name+'=; Max-Age=0; path=/; domain='+location.hostname;}}}}));
  document.querySelectorAll('.cookie-settings').forEach(b=>b.addEventListener('click',()=>{consentBox.hidden=false;consentBox.querySelector('button').focus();}));
})();

// Optional agent interface; ordinary browser controls remain the primary UI.
(() => {
  const context=document.modelContext;
  if(!context?.registerTool || !document.getElementById('project-search')) return;
  const lifecycle=new AbortController();
  const categories=[...document.querySelectorAll('.category')].map(b=>b.dataset.category);
  try {
    Promise.resolve(context.registerTool({
      name:'filter_jev_directory',
      title:'Filter the Jev project directory',
      description:'Update the visible directory search and category, then return matching project names, summaries and source links. Does not open links or execute projects.',
      inputSchema:{type:'object',properties:{query:{type:'string',maxLength:200},category:{type:'string',enum:categories}},additionalProperties:false},
      annotations:{readOnlyHint:false,untrustedContentHint:true},
      execute(input){
        if(!input||typeof input!=='object'||Array.isArray(input))throw new Error('Expected an object.');
        if(Object.keys(input).some(k=>!['query','category'].includes(k)))throw new Error('Unknown field.');
        if(input.query!==undefined&&(typeof input.query!=='string'||input.query.length>200))throw new Error('Query must be text up to 200 characters.');
        if(input.category!==undefined&&!categories.includes(input.category))throw new Error('Unknown category.');
        const field=document.getElementById('project-search');field.value=input.query||'';
        const selected=input.category||'all';[...document.querySelectorAll('.category')].find(b=>b.dataset.category===selected).click();field.dispatchEvent(new Event('input',{bubbles:true}));
        const projects=[...document.querySelectorAll('.project-card')].filter(c=>!c.hidden).map(c=>({name:c.dataset.name,category:c.dataset.category,description:c.querySelector('p').textContent,url:c.querySelector('h3 a').href}));
        return {count:projects.length,projects};
      }
    },{signal:lifecycle.signal})).catch(()=>{});
    window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
  }catch{}
})();
