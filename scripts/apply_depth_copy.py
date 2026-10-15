"""Apply the complete 15 October 2026 English handoff to the GitHub Pages site."""
from pathlib import Path
from html import escape
import re,json,subprocess,copy,sys
from bs4 import BeautifulSoup as B, NavigableString
from depth_copy_data import COPY,HOME_CARDS,WORK_CARDS,END_CTA,FEEDBACK,CV_INTRO
ROOT=Path(__file__).resolve().parent.parent;BASE='84712543c1e5ffd5f1505b7a4d2c06fc87fdd65f'
def original(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT,text=True)
def soup(text):return B(text,'html.parser')
def mainof(name):return soup(original(name)).find('main')
def inner(node):return ''.join(str(x) for x in node.contents)
def paras(text):return ''.join('<p>'+escape(p.strip())+'</p>' for p in text.split('\n\n') if p.strip())
def link(href,text,external=False):return '<a class="link-arrow" href="'+escape(href,quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+escape(text)+' <span aria-hidden="true">↗</span></a>'
def actions(*items):return '<div class="actions">'+''.join(items)+'</div>'
def header(data,back=False):return '<header class="page-hero depth-hero">'+(link('work.html','Back to selected work') if back else '')+'<p class="eyebrow">'+escape(data['eyebrow'])+'</p><h1>'+escape(data['title'])+'</h1>'+('<p class="lead depth-subtitle">'+escape(data['subtitle'])+'</p>' if data['subtitle'] else '')+'<div class="depth-prose">'+paras(data['intro'])+'</div></header>'
def section(heading,text,extra='',eyebrow=''):return '<section class="section depth-section">'+('<p class="eyebrow">'+escape(eyebrow)+'</p>' if eyebrow else '')+'<h2>'+escape(heading)+'</h2><div class="depth-prose">'+paras(text)+'</div>'+extra+'</section>'
def wrapper(body,cls=''):return '<article class="depth-page '+cls+'"><div class="wrap">'+body+'</div></article>'
def extlinks(main):
 seen=set();out=[]
 for a in main.select('a[href]'):
  href=a['href']
  if href.startswith(('https://','mailto:')) and href not in seen:seen.add(href);out.append(link(href,a.get_text(' ',strip=True).replace('↗','').strip(),href.startswith('https')))
 return actions(*out) if out else ''
def shared_cta():return '<section class="cta"><div class="wrap"><div><h2>'+END_CTA[0]+'</h2><p class="depth-cta-body">'+END_CTA[1]+'</p></div>'+actions(link('contact.html','Start a conversation'),link('mailto:sarahsaafwan@gmail.com','Email me'))+'</div></section>'
def trailing(main):return ''.join(str(x) for x in main.select(':scope > .explore-next'))+shared_cta()
oldwork=mainof('work.html');cards={x['data-project']:str(x) for x in oldwork.select('.card[data-project]')}
def card(slug,text):
 node=soup(cards[slug]).select_one('.card');p=node.find('p');p.clear();p.append(text);a=node.select_one('.card-button');a.clear();a.append('Read the full project ');sp=soup('<span aria-hidden="true">↗</span>').span;a.append(sp)
 return str(node)
PAGES={}
# Home: the full personal introduction, four selected projects, and preserved portrait/feedback.
d=COPY['index.html'];old=mainof('index.html');portrait=old.select_one('img[src="assets/sarah-safwan-portrait.jpg"]');portrait=portrait.find_parent('figure') or portrait
home=header(d)+ '<p class="depth-short-line">Marketing, creative direction, writing, and digital experiences.</p>'+actions(link('work.html','Explore my work'),link('cv.html','View my CV'),link('contact.html','Get in touch'))
parts=d['sections'];home+=section(parts[0][0],parts[0][1],'<div class="grid depth-project-grid">'+''.join(card(slug,text) for slug,text in HOME_CARDS.items())+'</div>','Selected work')
home+=section(parts[1][0],parts[1][1],'<div class="depth-portrait">'+str(portrait)+'</div>'+actions(link('experience.html','Read about my experience')),'How I got here')
home+=section(parts[2][0],parts[2][1],actions(link('services.html','Explore services'),link('calculator.html','Browse packages'),link('service-1.html','Social media content design'),link('service-2.html','Carousel and post production'),link('service-3.html','Short-form video editing')),'Services')
feedback=old.select_one('.feedback-section');homeclose=section(parts[3][0],parts[3][1],actions(link('contact.html','Start a conversation'),link('mailto:sarahsaafwan@gmail.com','Email me')))
resources=old.select_one('.home-pathways');res=''
if resources:
 links=[link(a['href'],a.find('h3').get_text(' ',strip=True) if a.find('h3') else a.get_text(' ',strip=True).replace('↗','')) for a in resources.select('a[href]')]
 res=section('More about working together','',actions(*links))
PAGES['index.html']=wrapper(home)+str(feedback)+wrapper(res+homeclose)
# Work: preserve filters and existing covers, while replacing every supplied project description.
d=COPY['work.html'];filters=oldwork.select_one('.filters');facets=oldwork.select_one('.portfolio-facets');count=oldwork.select_one('#work-count')
work=header(d)+actions(link('assets/Sarah_Safwan_Portfolio_2026.pdf','Download portfolio PDF'))+'<section class="section depth-work">'+str(filters)+str(facets)+str(count)+'<p id="work-empty" role="status" hidden>Nothing matches those filters yet. Try another category or view all projects.</p><div class="grid work-grid" id="project-grid">'+''.join(card(slug,text) for slug,text in WORK_CARDS.items())+'</div></section>'
PAGES['work.html']=wrapper(work)+shared_cta()
# Full narrative case studies, retaining their published project links.
for route in ['case-moving-truck.html','case-advertising-research.html','case-thy-academia.html','case-the-sae-talk.html','case-substack.html']:
 d=COPY[route];old=mainof(route);body=header(d,True)
 body+=''.join(section(h,t) for h,t in d['sections'])
 body+=extlinks(old)+actions(link('work.html','Back to selected work'))
 # The current DAXUEN pages have no visual assets. Preserve any media should the base change.
 for media in old.select('img,video,iframe,object'):body+='<div class="depth-preserved-media">'+str(media)+'</div>'
 PAGES[route]=wrapper(body)+trailing(old)
# BellaBelles: preserve all original media elements, carousel controls, and their hooks.
route='case-bellabelles-egypt.html';d=COPY[route];old=mainof(route);parts=d['sections'];body=header(d,True)
body+='<section class="section depth-section"><p class="eyebrow">01 / Personality storytelling</p><h2>'+escape(parts[0][0])+'</h2><div class="depth-media-row"><div class="depth-prose">'+paras(parts[0][1])+'</div>'+str(old.select_one('.bella-carousel'))+'</div></section>'
body+='<section class="section depth-section"><p class="eyebrow">02 / A more playful angle</p><h2>'+escape(parts[1][0])+'</h2><div class="depth-media-row"><div class="depth-prose">'+paras(parts[1][1])+'</div><div class="depth-static">'+str(old.select_one('.bella-static figure'))+'</div></div></section>'
figures=old.select('.bella-video-grid > figure');assert len(figures)==3
body+='<div class="bella-video-grid depth-video-sections">'
for i,((heading,text),figure) in enumerate(zip(parts[2:5],figures)):
 fig=copy.copy(figure);caption=fig.find('figcaption');openlink=copy.copy(caption.find('a'));caption.clear();caption.append(openlink)
 body+='<section class="section depth-section"><p class="eyebrow">'+('03 / Giving the products the attention' if i==0 else 'Short-form production')+'</p><h2>'+escape(heading)+'</h2><div class="depth-media-row"><div class="depth-prose">'+paras(text)+'</div>'+str(fig)+'</div></section>'
body+='</div>'+section(*parts[5])+str(old.select_one('.bella-project-links'))
PAGES[route]=wrapper(body,'bella-case')+trailing(old)
# Experience: full role descriptions, plus the unchanged credentials section.
route='experience.html';d=COPY[route];old=mainof(route);body=header(d)
rolelinks=[
 [('https://www.instagram.com/daxuen/','DAXUEN on Instagram'),('https://www.daxuen.com/','Visit DAXUEN')],
 [('case-bellabelles-egypt.html','Read the BellaBelles project'),('https://www.instagram.com/bellabelles.shop/','BellaBelles on Instagram'),('https://bellabelles.shop/','Visit BellaBelles')],
 [('https://www.instagram.com/thyacademia/','Instagram'),('https://thyacademia.medium.com/','Read on Medium')],
 [('https://open.spotify.com/show/0d1ueJYmkHtrESzCPtqx4n','Listen on Spotify'),('https://podcasts.apple.com/eg/podcast/the-sae-talk/id1885249003','Listen on Apple Podcasts')],[],[],[('https://sarahsafwan.substack.com/','Read on Substack')]]
for (heading,text),links in zip(d['sections'],rolelinks):body+=section(heading,text,actions(*(link(u,t,u.startswith('https')) for u,t in links)))
body+=actions(link('cv.html','View my CV'))
PAGES[route]=wrapper(body)+str(old.select_one('.credentials-section'))+shared_cta()
# Writing hub: independent formats, original external destinations, and existing project art.
route='writing.html';d=COPY[route];old=mainof(route);body=header(d)
for (heading,text),slug in zip(d['sections'][:3],['thy-academia','the-sae-talk','substack']):body+=section(heading,text,card(slug,WORK_CARDS[slug]))
body+=section(*d['sections'][3],extlinks(old));PAGES[route]=wrapper(body)+trailing(old)
# Services: full contextual writing, all 24 existing service records and market controls preserved.
route='services.html';d=COPY[route];old=mainof(route);body=header(d)+actions(link('calculator.html','Browse packages'),link('contact.html','Discuss a custom scope'))
for heading,text in d['sections']:body+=section(heading,text)
servicecatalogue=next(s for s in old.select('section') if s.select_one('.catalogue-section')) if any(s.select_one('.catalogue-section') for s in old.select('section')) else None
# Preserve the outer service-list section exactly, rather than copying individual price records.
servicecatalogue=next((s for s in old.select(':scope > section') if s.select_one('[data-service-id]')),None);assert servicecatalogue
market=old.select_one('#services-market') or old.select_one('#public-market') or old.select_one('select')
marketblock=''
if market:
 parent=market.parent
 while parent.parent and parent.parent!=old and parent.name not in ['section']:parent=parent.parent
 # Use just the market control group when possible.
 group=market.find_parent(class_='market-selector') or market.parent
 marketblock=str(group)
 if market.get('id') and servicecatalogue.select_one('#'+market['id']):marketblock=''
PAGES[route]=wrapper(body)+ '<section class="section"><div class="wrap"><h2>Explore the full service catalogue</h2>'+marketblock+'</div></section>'+str(servicecatalogue)+str(old.select_one('.feedback-section'))+shared_cta()
# Packages: presentation copy only. The approved JSON is never changed.
route='calculator.html';d=COPY[route];old=mainof(route);node=old.select_one('#services-packages');intro=node.select_one('.intro');control=copy.copy(intro.select_one('.control-block'));intro.clear()
intro.append(soup('<p class="eyebrow">SERVICES / PACKAGES</p><h1>'+d['title']+'</h1><div class="depth-prose">'+paras(d['intro'])+'</div>').div) if False else None
for x in soup('<p class="eyebrow">SERVICES / PACKAGES</p><h1>'+d['title']+'</h1><div class="depth-prose">'+paras(d['intro'])+'</div>').contents[:]:intro.append(x)
intro.append(control)
catalogue=node.select_one('.catalogue');top=catalogue.select_one('.catalogue-top');top.insert_before(soup('<p class="depth-tier-intro">'+d['sections'][0][1]+'</p>').p)
custom=node.select_one('.custom');custom.find('h2').string=d['sections'][1][0]
for p in custom.find_all('p'):
 if 'eyebrow' not in p.get('class',[]):p.string=d['sections'][1][1]
node['class']=node.get('class',[])+['depth-page'];PAGES[route]=str(node)
# Contact: retain the real form and every field, update labels and remove the old estimate UI.
route='contact.html';d=COPY[route];old=mainof(route);container=old.select_one('.wrap');hero=container.select_one('.page-hero');hero.replace_with(soup(header(d)).header)
form=old.select_one('#contact-form');form.find(['h2','h3']).string='A few details about your project.'
form.find(['h2','h3']).insert_after(soup('<p class="depth-form-intro">You don’t need to write a perfect brief. Tell me what you’re making, what you need help with, and anything that would be useful for me to know before replying.</p>').p)
labels={'enquiry-market':'Where will the work be commissioned?','enquiry-type':'What are you getting in touch about?','enquiry-service':'Which service best matches what you need?','message':'What’s the idea, and what would you like me to do?'}
for target,label in labels.items():
 n=form.find('label',attrs={'for':target});assert n,target;n.clear();n.append(label)
for target,text in [('budget-min','Optional, but useful if you’ve already set a range.'),('enquiry-deadline','A target date is useful even if it’s flexible.')]:
 control=form.find(id=target);helpid=target+'-help';control['aria-describedby']=helpid;control.insert_after(soup('<small id="'+helpid+'">'+text+'</small>').small)
est=form.select_one('#enquiry-estimate')
if est:est.decompose()
button=form.select_one('#enquiry-submit');button.clear();button.append('Send enquiry')
oldsmall=next((s for s in form.select('small') if 'saved privately' in s.get_text()),None)
if oldsmall:oldsmall.string='Your enquiry will be sent for review using the contact details you provide.'
container['class']=container.get('class',[])+['depth-page'];PAGES[route]=inner(old)
# Rhode: use the new opening, then retain every detailed strategic section and all existing artwork.
route='case-rhode.html';d=COPY[route];old=mainof(route);article=old.select_one('.rhode-case');wrap=article.select_one('.wrap');oldheader=wrap.select_one('header');facts=copy.copy(oldheader.select_one('.rhode-facts'));disclaimer=copy.copy(oldheader.select_one('.rhode-disclaimer'));act=copy.copy(oldheader.select_one('.actions'));new=soup(header(d,True)).header
new.append(disclaimer);new.append(act);new.append(facts);oldheader.replace_with(new)
oldintro=wrap.select_one('#interactive-prototype-title')
if oldintro:oldintro.find_parent('section').decompose()
for heading,text in reversed(d['sections']):new.insert_after(soup(section(heading,text)).section)
# Correct only visual-language descriptions; never edit the strategy PDF or source imagery.
for text in wrap.find_all(string=True):
 if text.parent.name not in ['script','style']:
  val=str(text).replace('Warm neutrals, clean typography','Cool white and gray backgrounds, clean typography').replace('warm neutral palette','cool white and gray palette')
  if val!=str(text):text.replace_with(val)
article['class']=article.get('class',[])+['depth-page'];PAGES[route]=inner(old)
# CV: introduction only; downloads, certificates, dates, and facts are kept as supplied.
old=mainof('cv.html');hero=old.select_one('.page-hero');p=hero.select_one('.lead');p.clear();p.append(CV_INTRO);PAGES['cv.html']=inner(old)
# Global editorial changes apply to real rendered text and navigation, not protected pricing records.
DASH='—'
def normalize(s):return re.sub(r'[ \t]+\|[ \t]+',' | ',s.replace(DASH,' | '))
def global_dom(main,route):
 for n in main.select('.cta'):
  if route=='index.html':continue
  h=n.find('h2');h.clear();h.append(END_CTA[0]);parent=h.parent
  for p in parent.find_all('p',recursive=False):p.decompose()
  h.insert_after(soup('<p class="depth-cta-body">'+END_CTA[1]+'</p>').p)
 for sectionnode in main.select('.feedback-section'):
  h=sectionnode.find('h2');p=h.find_next_sibling('p') if h else None
  if p:p.clear();p.append(FEEDBACK)
 for a in main.select('.card-button'):a.clear();a.append('Read the full project ↗')
 for a in main.select('a[href]'):
  if a.get('href')=='calculator.html':
   label=a.get_text(' ',strip=True)
   if re.search(r'estimate|calculator|services\s*&\s*packages',label,re.I):
    a.clear();a.append('Packages' if label.lower().replace('↗','').strip() in ['calculator','services & packages','rate calculator'] else 'Browse packages ↗')
 # Supporting prose: replace obsolete UI references while retaining factual/legal scope.
 for n in main.find_all(string=True):
  if n.parent.name in ['script','style']:continue
  val=str(n)
  for before,after in [('public calculator','package catalogue'),('the calculator','the package catalogue'),('calculator estimate','package enquiry'),('saved draft estimate','selected package'),('draft pricing estimate','package starting prices')]:val=re.sub(re.escape(before),after,val,flags=re.I)
  if val!=str(n):n.replace_with(val)
 return main
AUDIT=[]
for f in sorted(ROOT.glob('*.html')):
 doc=soup(original(f.name));main=doc.find('main')
 if not main:continue
 status='Full supplied copy implemented' if f.name in COPY and f.name not in ['case-rhode.html'] else 'Supplied introduction implemented; verified details preserved' if f.name=='cv.html' else 'Consistency audit only; detailed rewrite not supplied'
 if f.name=='case-rhode.html':status='Supplied opening and summary implemented; detailed strategic sections preserved'
 if f.name in PAGES:main.clear();frag=soup(PAGES[f.name]);[main.append(x) for x in list(frag.contents)]
 global_dom(main,f.name)
 # Preserve the established page-wide shell, changing just the navigation label.
 for a in doc.select('a[href="calculator.html"]'):
  label=a.get_text(' ',strip=True)
  if label.replace('↗','').strip() in ['Services & Packages','Calculator','Rate Calculator']:a.clear();a.append('Packages')
 # The real HTML and its runtime page override must contain the same complete body.
 body=normalize(inner(main));main.clear();[main.append(x) for x in list(soup(body).contents)]
 title=(COPY[f.name]['title']+' | Sarah Safwan') if f.name in COPY else normalize(doc.title.get_text() if doc.title else f.stem+' | Sarah Safwan')
 if doc.title:doc.title.string=title
 if f.name in COPY:
  data=COPY[f.name];description=data['intro'].split('\n\n')[0] or data['sections'][0][1].split('\n\n')[0];description=re.split(r'(?<=[.!?])\s',description)[0]
  for meta in doc.select('meta'):
   key=meta.get('name') or meta.get('property')
   if key in ['og:title','twitter:title']:meta['content']=title
   if key in ['description','og:description','twitter:description']:meta['content']=description
 text=str(doc);m=re.search('const RewrittenPages=',text)
 if m:
  start=m.end();data,end=json.JSONDecoder().raw_decode(text[start:]);data[f.name]=body;text=text[:start]+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+text[start+end:]
 else:text=text.replace('</head>','<script>const RewrittenPages='+json.dumps({f.name:body},ensure_ascii=False).replace('<','\\u003c')+';</script></head>')
 m=re.search('const RewrittenTitles=',text)
 if m:
  start=m.end();data,end=json.JSONDecoder().raw_decode(text[start:]);data[f.name]=title;text=text[:start]+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+text[start+end:]
 if 'href="depth-copy.css"' not in text:text=text.replace('</head>','<link rel="stylesheet" href="depth-copy.css"></head>')
 if 'copy-presentation.js' not in text:text=text.replace('</head>','<script src="copy-presentation.js" defer></script></head>')
 # Never leave an em dash in HTML text, ARIA labels, metadata, or inline content.
 text=normalize(text)
 f.write_text(text)
 AUDIT.append({'route':f.name,'status':status,'words':len(soup(body).get_text(' ',strip=True).split())})
(ROOT/'content/depth-copy.json').write_text(json.dumps(COPY,ensure_ascii=False,indent=2))
(ROOT/'content/route-copy-audit.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2))
print('Implemented',len(PAGES),'supplied page bodies/intros and audited',len(AUDIT),'rendered routes.')
