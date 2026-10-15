(function(){'use strict';
const carousel=document.querySelector('.bella-carousel');if(!carousel)return;
const slides=Array.from(carousel.querySelectorAll('.bella-slide'));const previous=carousel.querySelector('.bella-prev'),next=carousel.querySelector('.bella-next'),count=carousel.querySelector('.bella-slide-count');let index=0;
function show(value){index=Math.max(0,Math.min(slides.length-1,value));slides.forEach((slide,i)=>{slide.hidden=i!==index;slide.setAttribute('aria-hidden',String(i!==index))});count.textContent=(index+1)+' / '+slides.length;previous.disabled=index===0;next.disabled=index===slides.length-1;}
carousel.classList.add('bella-enhanced');carousel.querySelector('.bella-carousel-controls').hidden=false;show(0);
previous.addEventListener('click',()=>show(index-1));next.addEventListener('click',()=>show(index+1));
carousel.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();show(event.key==='Home'?0:event.key==='End'?slides.length-1:index+(event.key==='ArrowRight'?1:-1))});
let start=null;carousel.addEventListener('touchstart',event=>{start=event.touches.length===1?{x:event.touches[0].clientX,y:event.touches[0].clientY}:null},{passive:true});carousel.addEventListener('touchend',event=>{if(!start||event.changedTouches.length!==1){start=null;return;}const dx=event.changedTouches[0].clientX-start.x,dy=event.changedTouches[0].clientY-start.y;start=null;if(Math.abs(dx)>=45&&Math.abs(dx)>Math.abs(dy)*1.3)show(index+(dx<0?1:-1))},{passive:true});carousel.addEventListener('touchcancel',()=>{start=null},{passive:true});
const videos=Array.from(document.querySelectorAll('.bella-video-grid video'));videos.forEach(video=>video.addEventListener('play',()=>videos.forEach(other=>{if(other!==video&&!other.paused)other.pause()})));
})();
