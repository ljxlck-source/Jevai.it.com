from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.refs=[];self.ids=set();self.h1=0;self.titles=0;self.meta={};self.canon=[];self.cards=0;self.images=[];self.jsons=[];self.injson=False;self.buffer='';self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if t=='title':self.titles+=1
  if 'id' in a:assert a['id'] not in self.ids, 'duplicate id '+a['id'];self.ids.add(a['id'])
  if t=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if t=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
  if t=='article' and 'project-card' in a.get('class',''):self.cards+=1
  for field in ['href','src','poster']:
   if field in a:self.refs.append(a[field])
  if t=='img':self.images.append(a)
  if t=='script' and a.get('type')=='application/ld+json':self.injson=True;self.buffer=''
 def handle_data(self,d):
  if self.injson:self.buffer+=d
 def handle_endtag(self,t):
  if t=='script' and self.injson:self.jsons.append(json.loads(self.buffer));self.injson=False
pages={f:Page(f.read_text()) for f in OUT.rglob('*.html')}
for file,p in pages.items():
 assert p.h1==1,(file,'H1 count',p.h1)
 assert p.titles==1 and p.meta.get('description'),(file,'missing metadata')
 assert len(p.canon)==1 and p.canon[0].startswith('https://jevai.it.com/'),(file,'canonical')
 for a in p.images:assert 'alt' in a and 'width' in a and 'height' in a,(file,'image metadata')
 for ref in p.refs:
  u=urlparse(ref)
  assert ref!='#',(file,'placeholder link')
  if u.scheme or u.netloc:continue
  dest=OUT/unquote(u.path).lstrip('/') if u.path else file
  if dest.is_dir():dest=dest/'index.html'
  assert dest.exists(),(file,'broken reference',ref)
  if u.fragment and dest.suffix=='.html':assert unquote(u.fragment) in pages[dest].ids,(file,'broken anchor',ref)
project_data=json.loads((ROOT/'content/projects.json').read_text())
assert len(project_data)==46 and len({p['url'] for p in project_data})==46
home=pages[OUT/'index.html'];assert home.cards==46
assert all(p['url'] in home.refs for p in project_data)
assert len({p['category'] for p in project_data})==10
assert 'G-6B7H863MFF' in (OUT/'assets/site.js').read_text()
assert len(re.findall(r'\S+', (ROOT/'content/guide.md').read_text()))>3500
print(f'PASS: {len(pages)} HTML documents, 46 original project URLs, 10 categories, metadata, local assets, internal anchors, structured data, GA ID and guide length.')
