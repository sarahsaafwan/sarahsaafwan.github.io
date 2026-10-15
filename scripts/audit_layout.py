"""Browser layout audit for all public portfolio routes.

Run a local server, then:
  python scripts/audit_layout.py --base-url http://localhost:8000/ --output /tmp/portfolio-audit
Requires Playwright and its Chromium browser. No forms are submitted.
The two owner-only routes redirect to the existing authenticated backend;
they are checked separately rather than bypassing authentication.
"""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://localhost:8000/');parser.add_argument('--output',default='/tmp/portfolio-layout-audit');parser.add_argument('--widths',default='375,390,430,768,820,1024,1280,1440,1920');args=parser.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
private={'enquiries.html','feedback-review.html'};routes=sorted(p.name for p in root.glob('*.html') if p.name not in private)
scan=(root/'scripts/scan_editorial_lines.js').read_text();results=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for width in map(int,args.widths.split(',')):
  context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
  for route in routes:
   page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   try:
    response=page.goto(args.base_url.rstrip('/')+'/'+route,wait_until='load');page.evaluate('document.fonts.ready');page.wait_for_function('!document.querySelector(".site-opening")')
    page.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=800){scrollTo(0,y);await new Promise(r=>setTimeout(r,10))}scrollTo(0,0)}')
    initial=page.evaluate(scan)
    page.locator('details').evaluate_all('(es)=>es.forEach(e=>e.open=true)')
    page.locator('[data-reflection-expand]').evaluate_all('(es)=>es.forEach(e=>e.click())')
    page.wait_for_timeout(50);expanded=page.evaluate(scan)
    page.screenshot(path=str(out/f'{width}-{route[:-5]}.png'),full_page=True,animations='disabled')
    results.append({'route':route,'width':width,'status':response.status,'errors':errors,'initial':initial,'expanded':expanded})
   except Exception as e:results.append({'route':route,'width':width,'error':str(e)})
   page.close()
  context.close();print(width,'finished',flush=True);(out/'results.json').write_text(json.dumps(results,indent=2))
 browser.close()
failures=[r for r in results if r.get('error') or r.get('errors') or any(r.get(k,{}).get('hits') or r.get(k,{}).get('scrollWidth',0)>r['width']+1 or r.get(k,{}).get('clipped') for k in ('initial','expanded'))]
print(len(results),'route/width checks;',len(failures),'findings requiring review')
raise SystemExit(bool(failures))
