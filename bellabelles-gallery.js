(()=>{'use strict';
const base='assets/bellabelles/';
const slides=[
['01 - Which Bellabelles Girl Are You - Cover.jpeg','Carousel cover'],
['02 - The Seaside Sweetheart - Blush Pony.jpeg','The Seaside Sweetheart'],
['03 - The Autumn Muse - Autumn Cascade.jpeg','The Autumn Muse'],
['04 - The Golden Girl - The Whale.jpeg','The Golden Girl'],
['05 - Which Bellabelles Girl Are You - CTA.jpeg','Carousel ending']
];
const still=['Static 02- Fixing Pain As An Adult.jpeg','Fixing Pain as an Adult'];
const videos=[['Animated 01 - Jewelry Wishlist.mp4','Jewelry Wishlist'],['copy_575A0191-2D03-439C-918E-EEB96D17056F.mp4','Video creative 01'],['copy_6204935F-8F49-4E8E-8789-F054B861B612.mp4','Video creative 02']];
const gallery=document.getElementById('bellabelles-media-gallery');if(!gallery)return;
const url=name=>base+encodeURIComponent(name);
function picture(pair){const figure=document.createElement('figure');figure.className='bella-figure';const img=document.createElement('img');img.src=url(pair[0]);img.alt=pair[1];img.loading='lazy';img.decoding='async';figure.append(img);const caption=document.createElement('figcaption');caption.textContent=pair[1];figure.append(caption);return figure;}
function run(){gallery.replaceChildren();const header=document.createElement('h3');header.textContent='Which Bellabelles Girl Are You?';gallery.append(header);
const carousel=document.createElement('div');carousel.className='bella-carousel';carousel.tabIndex=0;carousel.setAttribute('aria-label','Five-slide jewellery carousel');slides.forEach(p=>carousel.append(picture(p)));gallery.append(carousel);
const sub=document.createElement('h3');sub.textContent='Other selected work';gallery.append(sub);
const stillGrid=document.createElement('div');stillGrid.className='bella-still';stillGrid.append(picture(still));gallery.append(stillGrid);
const grid=document.createElement('div');grid.className='bella-video-grid';videos.forEach(p=>{const figure=document.createElement('figure');const video=document.createElement('video');video.src=url(p[0]);video.controls=true;video.preload='metadata';video.playsInline=true;video.setAttribute('aria-label',p[1]);figure.append(video);const caption=document.createElement('figcaption');caption.textContent=p[1];figure.append(caption);grid.append(figure)});gallery.append(grid);}
fetch(url(slides[0][0]),{method:'HEAD'}).then(r=>{if(r.ok)run();else gallery.innerHTML='<p>The original project files are being added to this gallery.</p>';}).catch(()=>gallery.innerHTML='<p>The original project files are being added to this gallery.</p>');
})();