from pathlib import Path
from html import escape as e
import json,re,os
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'; ORIGIN='https://jevai.it.com'
projects=json.loads((ROOT/'content/projects.json').read_text())
CATS={'route':('Model & skill routing','⇄'),'guard':('Agent guardrails','◇'),'review':('Code review','⌘'),'browser':('Browser & web','↗'),'write':('Writing & content','¶'),'office':('Workflows & data','▦'),'context':('Context management','≋'),'fun':('Games & experiments','✳'),'eval':('Evaluation','⌁'),'open':('Independent models','{ }')}
NAV=[('/','Directory'),('/what-is-jev/','What is Jev?'),('/guide/','The guide'),('/typesafe/','TypeSafe')]
def header(path):
 return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><nav class="container nav" aria-label="Main navigation"><a class="brand" href="/"><span class="mark"><img src="/assets/jester-mark.png" alt="" width="44" height="44"></span><span><span class="wordmark">Jev<span style="color:var(--green)">.ai</span></span><small>THE DIRECTORY</small></span></a><div class="nav-links" id="navigation">'+''.join(f'<a href="{u}"'+(' aria-current="page"' if path==u else '')+f'>{t}</a>' for u,t in NAV)+'</div><a class="external-button" href="https://typesafe.ai/" target="_blank" rel="noopener noreferrer">Official TypeSafe ↗</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="Toggle navigation">☰</button></nav></header>'
def footer():
 return '''<footer><div class="container"><div class="footer-top"><div><a class="brand" href="/">JEV<span style="color:var(--green)">.</span> <span style="font-size:14px;letter-spacing:0">Small decisions. New possibilities.</span></a><p>An independent directory and practical guide to the Jev ecosystem. Not affiliated with TypeSafe AI.</p></div><div class="footer-links"><a href="/">46 projects</a><a href="/guide/">Read the guide</a><a href="/typesafe/">Sources & resources</a><a href="/privacy/">Privacy</a></div></div><div class="footer-bottom"><span>© 2026 Jev Directory · jevai.it.com</span><span>Explore thoughtfully. Test on your own workload. &nbsp; <button class="cookie-settings" type="button">Analytics settings</button></span></div></div></footer><aside class="cookie-choice" id="analytics-choice" aria-label="Analytics preference" hidden><p>Allow Google Analytics to help us understand which guides and projects are useful? You can browse without it.</p><div class="cookie-actions"><button type="button" data-consent="granted">Allow analytics</button><button type="button" data-consent="denied">No thanks</button><a href="/privacy/">Privacy</a></div></aside>'''
def page(path,title,desc,body,kind='WebPage',noindex=False):
 folder=OUT/path.strip('/');folder.mkdir(parents=True,exist_ok=True)
 schema={'@context':'https://schema.org','@type':kind,'name':title,'description':desc,'url':ORIGIN+path,'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Jev Directory','url':ORIGIN+'/'}}
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#101014"><link rel="canonical" href="{ORIGIN+path}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{ORIGIN+path}"><meta property="og:site_name" content="Jev Directory"><meta name="twitter:card" content="summary"><link rel="icon" type="image/png" href="/assets/jester-mark.png"><link rel="stylesheet" href="/assets/styles.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{json.dumps(schema)}</script>{'<meta name="robots" content="noindex">' if noindex else ''}</head><body>{header(path)}{body}{footer()}</body></html>'''
 (folder/'index.html').write_text(html)
def inline(s):
 s=e(s);s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s);s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s);s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s);s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}"'+(' rel="noopener noreferrer"' if m[2].startswith('http') else '')+f'>{m[1]}</a>',s);return s
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def markdown(text):
 lines=text.splitlines();out=[];para=[];lst=None;code=None;table=[]
 def flush():
  nonlocal para,lst,table
  if para:out.append('<p>'+inline(' '.join(para))+'</p>');para=[]
  if lst:out.append('</'+lst+'>');lst=None
  if table:
   rows=[r for r in table if not re.match(r'^\|[\s:|\-]+\|$',r)]
   out.append('<div class="table-wrap"><table>')
   for i,r in enumerate(rows):
    tag='th' if i==0 else 'td';out.append('<tr>'+''.join(f'<{tag}>'+inline(c.strip())+f'</{tag}>' for c in r.strip('|').split('|'))+'</tr>')
   out.append('</table></div>');table=[]
 for line in lines:
  if line.startswith('```'):
   if code is None:flush();code=[]
   else:out.append('<pre><code>'+e('\n'.join(code))+'</code></pre>');code=None
   continue
  if code is not None:code.append(line);continue
  if not line.strip():flush();continue
  if line.startswith('<') and line.endswith('>'):flush();out.append(line);continue
  if line.startswith('|'): 
   if para or lst:flush()
   table.append(line);continue
  if line.startswith('#'):
   flush();m=re.match(r'(#+) (.*)',line);level=len(m[1]);out.append(f'<h{level} id="{slug(m[2])}">'+inline(m[2])+f'</h{level}>');continue
  if line.startswith('> '):flush();out.append('<blockquote><p>'+inline(line[2:])+'</p></blockquote>');continue
  m=re.match(r'(- |\d+\. )(.*)',line)
  if m:
   typ='ul' if m[1]=='- ' else 'ol'
   if lst!=typ:flush();out.append('<'+typ+'>');lst=typ
   out.append('<li>'+inline(m[2])+'</li>');continue
  if lst or table:flush()
  para.append(line)
 flush();return ''.join(out)
def article(path,title,desc,eyebrow,headline,filename):
 f=ROOT/'content'/filename
 if not f.exists():return
 source=f.read_text(); headings=re.findall(r'^## (.+)$',source,re.M)
 body='<main id="main" class="container"><header class="page-heading"><p class="eyebrow">'+eyebrow+'</p><h1>'+headline+'</h1><p class="lead">'+desc+'</p></header><div class="article-layout"><aside class="toc"><strong>On this page</strong>'+''.join(f'<a href="#{slug(h)}">{e(h)}</a>' for h in headings)+'</aside><article class="prose">'+markdown(source)+'</article></div></main>'
 page(path,title,desc,body)
buttons='<button class="category" type="button" data-category="all" aria-pressed="true"><span>All projects</span><span>46</span></button>'
for k,(name,icon) in CATS.items():buttons+=f'<button class="category" type="button" data-category="{k}" aria-pressed="false"><span>{name}</span><span>{sum(p["category"]==k for p in projects):02}</span></button>'
cards=[]
for p in projects:
 cat,icon=CATS[p['category']]
 cards.append(f'''<article class="project-card" id="{p['id']}" data-category="{p['category']}" data-name="{e(p['name'])}" data-search="{e((p['name']+' '+p['description']+' '+cat).lower())}" data-kind="{'repository' if p['kind']=='Repository' else 'report'}"><div class="card-top"><span class="project-icon" aria-hidden="true">{icon}</span><span class="source-kind">{'⌘ GitHub' if p['kind']=='Repository' else '↗ Demo / report'}</span></div><h3><a href="{e(p['url'])}" target="_blank" rel="noopener noreferrer">{e(p['name'])}</a></h3><p>{e(p['description'])}</p><div class="card-bottom"><span>{cat}</span><span class="arrow" aria-hidden="true">↗</span></div></article>''')
home='''<main id="main" class="container"><section class="hero"><div><p class="eyebrow">THE INDEPENDENT JEV PROJECT DIRECTORY</p><h1>46 JEV PROJECTS.<br><em>BIG DISRUPTION.</em></h1><p class="hero-description">46 ways to put Jev to work. Discover tools that route models, trim context, check code and turn everyday decisions into software.</p><div class="hero-links"><a href="#directory">Explore all 46 projects ↓</a><a href="/guide/">New to Jev? Read the guide ↗</a></div></div><div class="hero-panel" aria-label="46 projects across 10 categories"><div class="panel-top"><span>THE NEXT MOVE IS YOURS.</span><span>J / 01</span></div><div class="count">46<span>PROJECTS.<br>10 CATEGORIES.<br>PLENTY TO BUILD.</span></div><div class="panel-bottom"><span>CHOICE / SCORE / NOUL</span><span>EXPLORE ↗</span></div></div></section><div class="ticker" aria-hidden="true"><b>LESS OVERHEAD.</b><span>MODEL ROUTING</span><b>✳</b><span>CONTEXT COMPACTION</span><b>✳</b><span>AGENT GUARDRAILS</span><b>✳</b><span>BROWSER AUTOMATION</span></div><section class="directory" id="directory"><div class="section-heading"><h2>THE PROJECT INDEX <span style="color:var(--purple)">/ 46</span></h2><p>Community projects, demos & independent experiments.</p></div><div class="directory-layout"><aside class="categories" aria-label="Filter projects by category"><div class="categories-label mono">FIND YOUR NEXT MOVE</div>'''+buttons+'''<p class="sidebar-note">Built with Jev, or inspired by its approach.<br>Listing is not endorsement.<br><a href="/typesafe/">Meet the model’s creators ↗</a></p></aside><div><div class="toolbar"><label class="search-wrap"><span aria-hidden="true">⌕</span><input id="project-search" type="search" placeholder="Find a project, a use case, a new idea…" aria-label="Search projects"></label><select id="project-sort" aria-label="Sort projects"><option value="curated">Category order</option><option value="name">Name: A–Z</option></select></div><div class="result-meta"><span id="result-count" role="status" aria-live="polite">Showing all 46 projects</span><button id="reset-filters" type="button" hidden>Clear filters ×</button></div><div class="project-grid">'''+''.join(cards)+'''</div><div id="no-results" class="empty" hidden><h3>No projects found.</h3><p>Try another search or choose a different category.</p><button class="external-button" id="empty-reset" type="button">Show all projects</button></div></div></div></section><section class="learning"><div class="section-heading"><h2>UNDERSTAND THE DECISION.</h2><a href="/guide/" style="font-size:14px;color:var(--green)">The complete field guide ↗</a></div><div class="learn-grid"><article class="learn-card"><span class="mono">01 / WHAT</span><h3>What is Jev?</h3><p>Meet TypeSafe’s decision model. Context and questions go in; typed judgments come out.</p><a href="/what-is-jev/">Understand the model ↗</a></article><article class="learn-card"><span class="mono">02 / WHY</span><h3>Why use it?</h3><p>See where smaller, faster judgments can reduce overhead—and where a larger model still belongs.</p><a href="/why-jev/">Explore the trade-offs ↗</a></article><article class="learn-card"><span class="mono">03 / HOW</span><h3>How do I start?</h3><p>Define one decision, connect the API, test real examples and keep a fallback path.</p><a href="/how-to-use-jev/">Build your first workflow ↗</a></article></div></section></main>'''
page('/','Jev AI Directory — 46 Projects, Tools & Practical Guides','Explore 46 Jev projects for model routing, agent guardrails, browser automation and context management. Learn what Jev is, why it matters and how to use it.',home,'CollectionPage')
article('/what-is-jev/','What Is Jev? TypeSafe’s System One Model Explained','A practical introduction to typed decisions, the three question types and the role Jev can play inside software.','01 / UNDERSTAND THE MODEL','WHAT IS JEV?','what.md')
article('/why-jev/','Why Use Jev? Costs, Speed & Trade-offs','Find the decisions worth moving out of a generative model—and understand the costs that still remain.','02 / THE TRADE-OFF','WHY USE JEV?','why.md')
article('/how-to-use-jev/','How to Use Jev — A Practical Getting-Started Guide','Start with one useful decision. Define the options, connect your application and evaluate the result before automating it.','03 / BUILD A WORKFLOW','MAKE YOUR<br>FIRST MOVE.','how.md')
article('/guide/','Jev Guide — How Decision Models Work in Real Applications','An English adaptation of the supplied Chinese field guide, with worked examples, reported tests, limitations and a gradual integration plan.','THE FIELD GUIDE / SEPTEMBER 2026','LET CODE ACT.<br>LET JEV DECIDE.','guide.md')
article('/typesafe/','TypeSafe AI — Official Jev Links & Community Resources','The company behind Jev, its official documentation and useful perspectives from the wider community.','THE SOURCE / TYPESAFE AI','MEET THE PEOPLE<br>BEHIND THE MODEL.','typesafe.md')
article('/privacy/','Privacy & Analytics | Jev Directory','How this independent directory handles browsing, analytics preferences and external links.','SITE INFORMATION','PRIVACY &<br>ANALYTICS.','privacy.md')
paths=['/','/what-is-jev/','/why-jev/','/how-to-use-jev/','/guide/','/typesafe/','/privacy/']
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+p+'</loc></url>' for p in paths if (OUT/p.strip('/')/'index.html').exists())+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
page('/404/','Page Not Found | Jev Directory','Find your way back to the Jev project directory.','<main id="main" class="container error-page"><p class="eyebrow">THAT MOVE LEADS NOWHERE</p><h1>404.</h1><p>This page could not be found.</p><a class="external-button" href="/">Back to the directory →</a></main>',noindex=True)
(OUT/'404.html').write_text((OUT/'404/index.html').read_text())
print('Generated directory with',len(projects),'cards and',sum((OUT/p.strip('/')/'index.html').exists() for p in paths),'content routes.')
