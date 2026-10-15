"""Build the approved policy copy into the existing static and runtime page bodies."""
from pathlib import Path
from html import escape as e
import json,re
from bs4 import BeautifulSoup as B
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'content/working-together.json').read_text())
def paragraphs(items):return ''.join('<p>'+e(x)+'</p>' for x in items)
def block(kind,value):
 if kind=='h':return '<h3>'+e(value)+'</h3>'
 if kind=='p':return '<p>'+e(value)+'</p>'
 if kind=='ul':return '<ul>'+''.join('<li>'+e(x)+'</li>' for x in value)+'</ul>'
 if kind=='table':return '<table><caption>'+e(value['caption'])+'</caption><thead><tr>'+''.join('<th scope="col">'+e(x)+'</th>' for x in value['head'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+e(row[0])+'</th><td>'+e(row[1])+'</td></tr>' for row in value['rows'])+'</tbody></table>'
nav='<nav class="policy-nav" aria-label="Project policies sections"><p class="eyebrow">On this page</p><ol>'+''.join('<li><a href="#'+x['id']+'"><span aria-hidden="true">'+str(i).zfill(2)+'</span>'+e(x['title'])+'</a></li>' for i,x in enumerate(d['sections'],1))+'</ol></nav>'
sections=''.join('<details class="policy-section" id="'+x['id']+'" open><summary><span class="policy-number" aria-hidden="true">'+str(i).zfill(2)+'</span><h2>'+e(x['title'])+'</h2><span class="policy-toggle" aria-hidden="true">+</span></summary><div class="policy-body">'+''.join(block(*v) for v in x['blocks'])+'</div></details>' for i,x in enumerate(d['sections'],1))
body='<article class="policies-page"><div class="wrap"><header class="policy-intro page-hero"><p class="eyebrow">Project Policies</p><h1>Working Together</h1><div class="policy-prose">'+paragraphs(d['intro'])+'</div></header><div class="policy-layout">'+nav+'<div class="policy-sections">'+sections+'</div></div></div><section class="policy-closing"><div class="wrap"><h2>'+e(d['closing']['title'])+'</h2><div class="policy-prose">'+paragraphs(d['closing']['paragraphs'])+'</div><a class="button" href="contact.html?type=project">Request a Quote <span aria-hidden="true">↗</span></a></div></section></article>'
p=root/'terms.html';s=B(p.read_text(),'html.parser');s.title.string='Working Together | Sarah Safwan';s.find('meta',attrs={'name':'description'})['content']='Payments, revisions, timelines, usage rights and handover: a clear guide to working with Sarah Safwan.'
for key in ['og:title','twitter:title']:
 tag=s.find('meta',attrs={'property':key}) or s.find('meta',attrs={'name':key});tag['content']='Working Together | Sarah Safwan'
for key in ['og:description','twitter:description']:
 tag=s.find('meta',attrs={'property':key}) or s.find('meta',attrs={'name':key});tag['content']=s.find('meta',attrs={'name':'description'})['content']
m=s.find('main');m.clear();m.append(B(body,'html.parser'))
script=next(x for x in s.select('script:not([src])') if 'const RewrittenPages=' in x.get_text());script.string='const RewrittenTitles='+json.dumps({'terms.html':'Working Together | Sarah Safwan'})+';const RewrittenPages='+json.dumps({'terms.html':body},ensure_ascii=True).replace('<','\\u003c')+';'
ld=s.find('script',attrs={'type':'application/ld+json'});data=json.loads(ld.string);data['name']='Working Together | Sarah Safwan';data['description']=s.find('meta',attrs={'name':'description'})['content'];ld.string=json.dumps(data)
existing=s.select_one('link[href^="policies.css"]')
if existing:existing.decompose()
existing=s.select_one('script[src^="policies.js"]')
if existing:existing.decompose()
s.head.append(B('<link rel="stylesheet" href="policies.css?v=policies-20261015">','html.parser'));s.body.append(B('<script src="policies.js?v=policies-20261015" defer></script>','html.parser'));p.write_text(str(s))
