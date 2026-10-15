/* Native details retain keyboard and no-script access to the full policy text. */
(() => {
 const root=document.querySelector('.policies-page');if(!root)return;
 const sections=[...root.querySelectorAll('.policy-section')];
 const links=[...root.querySelectorAll('.policy-nav a')];
 const mobile=matchMedia('(max-width:600px)');
 function setLayout(){sections.forEach(s=>{s.open=!mobile.matches||s.id===location.hash.slice(1)});}
 function openHash(){const target=sections.find(s=>'#'+s.id===location.hash);if(target)target.open=true;}
 function offset(){const header=document.querySelector('.header');const style=header&&getComputedStyle(header);root.style.setProperty('--policy-offset',((style&&['sticky','fixed'].includes(style.position)?header.getBoundingClientRect().height:0)+28)+'px');}
 links.forEach(a=>a.addEventListener('click',()=>{const target=sections.find(s=>'#'+s.id===a.hash);if(target)target.open=true;}));
 let pending=false;
 function current(){pending=false;const edge=parseFloat(getComputedStyle(root).getPropertyValue('--policy-offset'))+60;let selected=sections[0];for(const s of sections){if(s.getBoundingClientRect().top<=edge)selected=s;else break;}links.forEach(a=>{if(a.hash==='#'+selected.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}
 addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(current);}},{passive:true});
 addEventListener('hashchange',()=>{openHash();current();});addEventListener('resize',offset);mobile.addEventListener('change',setLayout);
 offset();setLayout();openHash();current();
})();
