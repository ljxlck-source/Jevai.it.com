from pathlib import Path
from html import escape as e
import json,re,os
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'; ORIGIN='https://jevai.it.com'
projects=json.loads((ROOT/'content/projects.json').read_text())
CATS={'route':('Model & skill routing','⇄'),'guard':('Agent guardrails','◇'),'review':('Code review','⌘'),'browser':('Browser & web','↗'),'write':('Writing & content','¶'),'office':('Workflows & data','▦'),'context':('Context management','≋'),'fun':('Games & experiments','✳'),'eval':('Evaluation','⌁'),'open':('Independent models','{ }')}
NAV=[('/','Directory'),('/what-is-jev/','What is Jev?'),('/how-to-use-jev/','How to use Jev'),('/examples/','Examples'),('/typesafe/','Official TypeSafe resources')]
def header(path):
 return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><nav class="container nav" aria-label="Main navigation"><a class="brand" href="/"><span class="mark"><img src="/assets/jester-mark.png" alt="" width="44" height="44"></span><span><span class="wordmark">Jev<span style="color:var(--green)">.ai</span></span><small>THE DIRECTORY</small></span></a><div class="nav-links" id="navigation">'+''.join(f'<a href="{u}"'+(' aria-current="page"' if path==u else '')+f'>{t}</a>' for u,t in NAV)+'</div><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="Toggle navigation">☰</button></nav></header>'
def footer():
 return '''<footer><div class="container"><div class="footer-top"><div><a class="brand" href="/">JEV<span style="color:var(--green)">.</span> <span style="font-size:14px;letter-spacing:0">Small decisions. New possibilities.</span></a><p>An independent directory and practical guide to the Jev ecosystem. Not affiliated with TypeSafe AI.</p></div><div class="footer-links"><a href="/">Browse projects</a><a href="/examples/">Examples</a><a href="/typesafe/">Official TypeSafe resources</a><a href="/privacy/">Privacy</a></div></div><div class="footer-bottom"><span>© 2026 Jev Directory · jevai.it.com</span><span>Explore thoughtfully. Test on your own workload. &nbsp; <button class="cookie-settings" type="button">Analytics settings</button></span></div></div></footer><aside class="cookie-choice" id="analytics-choice" aria-label="Analytics preference" hidden><p>Allow Google Analytics to help us understand which guides and projects are useful? You can browse without it.</p><div class="cookie-actions"><button type="button" data-consent="granted">Allow analytics</button><button type="button" data-consent="denied">No thanks</button><a href="/privacy/">Privacy</a></div></aside>'''
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
buttons='<button class="category" type="button" data-category="all" aria-pressed="true"><span>All projects</span></button>'
for k,(name,icon) in CATS.items():buttons+=f'<button class="category" type="button" data-category="{k}" aria-pressed="false"><span>{name}</span></button>'
cards=[]
for p in projects:
 cat,icon=CATS[p['category']]
 cards.append(f'''<article class="project-card" id="{p['id']}" data-category="{p['category']}" data-name="{e(p['name'])}" data-search="{e((p['name']+' '+p['description']+' '+cat).lower())}" data-kind="{'repository' if p['kind']=='Repository' else 'report'}"><div class="card-top"><span class="project-icon" aria-hidden="true">{icon}</span><span class="source-kind">{'⌘ GitHub' if p['kind']=='Repository' else '↗ Demo / report'}</span></div><h3><a href="{e(p['url'])}" target="_blank" rel="noopener noreferrer">{e(p['name'])}</a></h3><p>{e(p['description'])}</p><div class="card-bottom"><span>{cat}</span><span class="arrow" aria-hidden="true">↗</span></div></article>''')
home='''<main id="main" class="container"><section class="hero hero-simple"><p class="eyebrow">JEV AI DIRECTORY</p><h1>Jev turns AI tasks into<br><em>multiple-choice questions.</em></h1><p class="hero-description">Discover what people build with the Jev model—and where they use it. Explore projects for model and skill routing, agent guardrails, code review, browser automation and more.</p><div class="hero-links"><a href="#directory">Browse projects ↓</a><a href="/what-is-jev/">What is Jev? ↗</a></div></section><section class="directory" id="directory"><div class="section-heading"><h2>Explore Jev use cases</h2><p>Community projects, demos & independent experiments.</p></div><div class="directory-layout"><aside class="categories" aria-label="Filter projects by category"><div class="categories-label mono">BROWSE BY USE CASE</div>'''+buttons+'''<p class="sidebar-note">Built with Jev, or inspired by its approach.<br>Listing is not endorsement.<br><a href="/typesafe/">Meet the model’s creators ↗</a></p></aside><div><div class="toolbar"><label class="search-wrap"><span aria-hidden="true">⌕</span><input id="project-search" type="search" placeholder="Find a project, a use case, a new idea…" aria-label="Search projects"></label><select id="project-sort" aria-label="Sort projects"><option value="curated">Category order</option><option value="name">Name: A–Z</option></select></div><div class="result-meta"><span id="result-count" role="status" aria-live="polite">Showing all projects</span><button id="reset-filters" type="button" hidden>Clear filters ×</button></div><div class="project-grid">'''+''.join(cards)+'''</div><div id="no-results" class="empty" hidden><h3>No projects found.</h3><p>Try another search or choose a different category.</p><button class="external-button" id="empty-reset" type="button">Show all projects</button></div></div></div></section><section class="learning"><div class="section-heading"><h2>UNDERSTAND THE DECISION.</h2></div><div class="learn-grid"><article class="learn-card"><span class="mono">01 / WHAT</span><h3>What is Jev?</h3><p>Meet TypeSafe’s decision model. Context and questions go in; typed judgments come out.</p><a href="/what-is-jev/">Understand the model ↗</a></article><article class="learn-card"><span class="mono">02 / EXAMPLES</span><h3>See Jev in action</h3><p>Follow a comment-triage example, inspect the output and see where business rules matter.</p><a href="/examples/">Explore examples ↗</a></article><article class="learn-card"><span class="mono">03 / HOW</span><h3>How do I start?</h3><p>Define one decision, connect the API, test real examples and keep a fallback path.</p><a href="/how-to-use-jev/">Build your first workflow ↗</a></article></div></section></main>'''
page('/','Jev AI Directory — Explore Jev Model Projects & Use Cases','Explore how developers use Jev to route AI models, select agent skills, improve agent safety, review code and automate browsers. Find projects by use case.',home,'CollectionPage')
article('/what-is-jev/','What Is Jev? A One-Minute Overview','Learn what Jev does, where it fits and how to start testing it.',"JEV / LEARN",'What is Jev?','what.md')
article('/how-to-use-jev/','How to Use Jev: Four Steps with Your AI Coding Agent','Get access, install the TypeSafe skill, create an API key and ask your coding agent to build a workflow.',"JEV / LEARN",'How to use Jev in four steps','how.md')
article('/examples/','Jev Examples: Comment Triage and Ticket Routing','Follow an author-reported comment-triage demonstration and explore a structured ticket-routing request.',"JEV / LEARN",'Jev examples','examples.md')
article('/why-jev/','Why System One, and Why Jev?','Explore why System One, and Why Jev?, with practical guidance adapted from the source article.',"JEV / LEARN",'Why System One, and Why Jev?','why.md')
article('/question-types/','Jev Question Types: Noul, Choice and Score','Explore jev Question Types: Noul, Choice and Score, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev Question Types: Noul, Choice and Score','question-types.md')
article('/confidence/','Jev Confidence and Parallel Questions','Explore jev Confidence and Parallel Questions, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev Confidence and Parallel Questions','confidence.md')
article('/performance/','Jev Speed, Cost and Accuracy','Explore jev Speed, Cost and Accuracy, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev Speed, Cost and Accuracy','performance.md')
article('/demos/','Jev Official Demos and Community Projects','Explore jev Official Demos and Community Projects, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev Official Demos and Community Projects','demos.md')
article('/use-cases/','Jev in Practice: Worked Examples','Explore jev in Practice: Worked Examples, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev in Practice: Worked Examples','use-cases.md')
article('/limitations/','Jev Limitations: When Not to Use It','Explore jev Limitations: When Not to Use It, with practical guidance adapted from the source article.',"JEV / LEARN",'Jev Limitations: When Not to Use It','limitations.md')
article('/integration/','A Gradual Jev Integration Plan','Explore a Gradual Jev Integration Plan, with practical guidance adapted from the source article.',"JEV / LEARN",'A Gradual Jev Integration Plan','integration.md')
article('/typesafe/','Official TypeSafe Resources | Jev AI Directory','Find TypeSafe’s website, Jev documentation, console and official resources, plus clearly labeled community references.',"JEV / LEARN",'Official TypeSafe resources','typesafe.md')
article('/privacy/','Privacy & Analytics | Jev Directory','How browsing, analytics preferences and external links work.',"JEV / LEARN",'Privacy & analytics','privacy.md')
page("/guide/","Jev Overview | Jev Directory","Continue to the Jev overview.",'<main id="main" class="container error-page"><h1>Start with Jev</h1><p><a href="/what-is-jev/">Read the quick overview →</a></p></main>',noindex=True)
(OUT/"_redirects").write_text("/guide /what-is-jev/ 301\n/guide/ /what-is-jev/ 301\n")
paths=['/', '/what-is-jev/', '/how-to-use-jev/', '/examples/', '/why-jev/', '/question-types/', '/confidence/', '/performance/', '/demos/', '/use-cases/', '/limitations/', '/integration/', '/typesafe/', '/privacy/']
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+p+'</loc></url>' for p in paths if (OUT/p.strip('/')/'index.html').exists())+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
page('/404/','Page Not Found | Jev Directory','Find your way back to the Jev project directory.','<main id="main" class="container error-page"><p class="eyebrow">THAT MOVE LEADS NOWHERE</p><h1>404.</h1><p>This page could not be found.</p><a class="external-button" href="/">Back to the directory →</a></main>',noindex=True)
(OUT/'404.html').write_text((OUT/'404/index.html').read_text())
print('Generated directory with',len(projects),'cards and',sum((OUT/p.strip('/')/'index.html').exists() for p in paths),'content routes.')
