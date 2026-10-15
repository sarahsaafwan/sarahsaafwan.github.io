/* Display-only punctuation cleanup; approved pricing records and visitor-entered values stay unchanged. */
(()=>{'use strict';
const normalize=text=>text.replace(/\u2014/g,' | ');
function update(node){
 if(node.nodeType===3){if(node.parentElement&&!node.parentElement.closest('script,style,textarea,input')&&node.data.includes('\u2014'))node.data=normalize(node.data);return;}
 if(node.nodeType!==1)return;
 if(node.matches('script,style,textarea,input')){for(const attr of ['aria-label','title','placeholder','alt'])if(node.hasAttribute(attr)&&node.getAttribute(attr).includes('\u2014'))node.setAttribute(attr,normalize(node.getAttribute(attr)));return;}
 for(const attr of ['aria-label','title','placeholder','alt'])if(node.hasAttribute(attr)&&node.getAttribute(attr).includes('\u2014'))node.setAttribute(attr,normalize(node.getAttribute(attr)));
 if(node.matches('a[href="calculator.html"]')&&node.textContent.trim()==='Services & Packages')node.textContent='Packages';
 for(const child of Array.from(node.childNodes))update(child);
}
function start(){update(document.body);document.title=normalize(document.title);new MutationObserver(records=>records.forEach(record=>{if(record.type==='characterData')update(record.target);else record.addedNodes.forEach(update)})).observe(document.body,{subtree:true,childList:true,characterData:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
