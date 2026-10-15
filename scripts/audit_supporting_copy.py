"""Bounded presentation fixes on supporting routes; approved scopes and legal terms remain intact."""
from pathlib import Path
import json,re,sys
from bs4 import BeautifulSoup as B
root=Path(__file__).resolve().parent.parent
intros=json.loads((root/'content/service-overviews.json').read_text())
extra={
'website-landing.html':intros['service-16.html'],
'website-portfolio.html':intros['service-17.html'],
'website-business.html':intros['service-18.html'],
'website-shop.html':intros['service-19.html']}
changed=[]
for name,text in {**intros,**extra}.items():
 f=root/name;doc=B(f.read_text(),'html.parser');hero=doc.select_one('main .page-hero');p=hero.select_one('.lead') if hero else None
 if p:p.clear();p.append(text);changed.append(name)
 if p:
  main=doc.find('main');body=''.join(str(n) for n in main.contents);s=str(doc);m=re.search('const RewrittenPages=',s);start=m.end();d,end=json.JSONDecoder().raw_decode(s[start:]);d[name]=body;s=s[:start]+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+s[start+end:];f.write_text(s)
for name in ['privacy.html','recruiters.html']:
 f=root/name;doc=B(f.read_text(),'html.parser');main=doc.find('main')
 for p in main.select('p'):
  if name=='privacy.html' and 'calculator selections' in p.get_text():p.clear();p.append('Market preferences and project-brief drafts use browser storage. Package enquiry links pass the selected service, tier, and market to the contact form. Any enquiry confirmation details saved in this tab can be cleared on the confirmation page. Clearing browser data does not remove submitted records.')
  if name=='recruiters.html' and 'responsibilities I cannot verify' in p.get_text():p.clear();p.append('I am building my career in digital marketing and creative work. My experience combines exposure to marketing functions such as campaign development, content production and competitor research with several years of independent publishing and content work. This page links to experience entries, project case studies, and the downloadable CV so you can review the work and its context.')
 body=''.join(str(n) for n in main.contents);s=str(doc);m=re.search('const RewrittenPages=',s);start=m.end();d,end=json.JSONDecoder().raw_decode(s[start:]);d[name]=body;s=s[:start]+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+s[start+end:];f.write_text(s);changed.append(name)
p=root/'content/route-copy-audit.json';audit=json.loads(p.read_text())
for item in audit:
 if item['route'] in intros or item['route'] in extra:item['status']='Service overview rewritten; existing approved scope, tier records, and terms preserved. Full package-detail rewrite not performed.'
 if item['route']=='privacy.html':item['status']='Browser-storage description updated for package enquiries; other legal content preserved.'
 if item['route']=='recruiters.html':item['status']='Introduction refined and global consistency fixes applied; verified role details preserved.'
p.write_text(json.dumps(audit,ensure_ascii=False,indent=2));print('Supporting overview and consistency updates:',len(changed),'routes.')
