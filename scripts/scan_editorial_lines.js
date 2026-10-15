() => {
 const visible=e=>{for(let a=e;a;a=a.parentElement){if(a.tagName==='DETAILS'&&!a.open&&!e.closest('summary'))return false;}const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)!==0&&r.width>0&&r.height>0&&!e.closest('[hidden],dialog:not([open])')};
 const name=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.classList.length?'.'+[...e.classList].slice(0,3).join('.'): '');
 let texts=[],borders=[],clipped=[],pseudo=[];
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 const canvas=document.createElement('canvas').getContext('2d');
 for(let n;n=walker.nextNode();){const e=n.parentElement;if(!n.textContent.trim()||!visible(e)||['SCRIPT','STYLE','OPTION','TEXTAREA'].includes(e.tagName))continue;
  const s=getComputedStyle(e);canvas.font=s.font;let metric=canvas.measureText('Hg');const ascent=metric.actualBoundingBoxAscent||parseFloat(s.fontSize)*.75;const descent=metric.actualBoundingBoxDescent||parseFloat(s.fontSize)*.2;const glyphH=ascent+descent;
  const range=document.createRange();range.selectNodeContents(n);
  for(const r of range.getClientRects()){if(r.width<1||r.height<1)continue;const box={x:r.x+scrollX,y:r.y+scrollY+(r.height-glyphH)/2,w:r.width,h:glyphH};let crop=e,painted=true;while(crop&&crop!==document.body){const cs=getComputedStyle(crop),cr=crop.getBoundingClientRect();if(['hidden','clip'].includes(cs.overflowY)&&(box.y>=cr.bottom+scrollY||box.y+box.h<=cr.y+scrollY))painted=false;crop=crop.parentElement;}if(!painted)continue;texts.push({...box,el:e,name:name(e),text:n.textContent.trim().slice(0,80)});
   let parent=e;while(parent&&parent!==document.body){const st=getComputedStyle(parent);if(['hidden','clip'].includes(st.overflowY)||['hidden','clip'].includes(st.overflowX)){const pr=parent.getBoundingClientRect();if((box.y<pr.y+scrollY-2||box.y+box.h>pr.bottom+scrollY+2)&&st.overflowY!=='visible'&&!parent.matches('.cover,.site-opening'))clipped.push({text:n.textContent.trim().slice(0,60),parent:name(parent)});}parent=parent.parentElement;}
  }
 }
 for(const e of document.querySelectorAll('body *')){if(!visible(e)||['INPUT','TEXTAREA','SELECT','IFRAME','VIDEO','IMG'].includes(e.tagName))continue;const s=getComputedStyle(e);
  for(const raw of e.getClientRects()){
   let r={x:raw.x,y:raw.y,width:raw.width,height:raw.height,bottom:raw.bottom};let a=e.parentElement;while(a&&a!==document.body){const st=getComputedStyle(a),ar=a.getBoundingClientRect();if(['hidden','clip','auto','scroll'].includes(st.overflowX)){const right=Math.min(r.x+r.width,ar.right);r.x=Math.max(r.x,ar.x);r.width=right-r.x;}a=a.parentElement;}if(r.width<=0)continue;
   for(const side of ['Top','Bottom']){const size=parseFloat(s['border'+side+'Width']);if(size>0&&s['border'+side+'Style']!=='none'&&s['border'+side+'Color']!=='rgba(0, 0, 0, 0)')borders.push({x:r.x+scrollX,y:scrollY+(side==='Top'?r.y:r.bottom-size),w:r.width,h:size,el:e,name:name(e)+':'+side});}
  }
  for(const ps of ['::before','::after']){const p=getComputedStyle(e,ps);if(p.content==='none'||p.content==='normal'||p.display==='none')continue;
   if(p.position==='absolute'&&(parseFloat(p.borderTopWidth)||parseFloat(p.borderBottomWidth)))pseudo.push({element:name(e),pseudo:ps,content:p.content,z:p.zIndex,pointer:p.pointerEvents});}
 }
 const hits=[];
 for(const border of borders){for(const t of texts){if(t.x+t.w<=border.x+2||t.x>=border.x+border.w-2||t.y+t.h<=border.y+.5||t.y>=border.y+border.h-.5)continue;
  hits.push({border:border.name,textElement:t.name,text:t.text,x:Math.round(border.x),y:Math.round(border.y),own:border.el.contains(t.el)});
 }}
 const overflow=[...document.querySelectorAll('body *')].filter(e=>visible(e)&&e.getBoundingClientRect().right>innerWidth+2&&!e.closest('.site-opening')).slice(0,15).map(name);
 return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,hits: [...new Map(hits.map(x=>[JSON.stringify(x),x])).values()],clipped:[...new Map(clipped.map(x=>[JSON.stringify(x),x])).values()],pseudo,overflow};
}
