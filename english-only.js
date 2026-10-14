(function(){
'use strict';
document.documentElement.lang='en';document.documentElement.dir='ltr';
try{localStorage.removeItem('sarah-portfolio-language');}catch{}
const url=new URL(location.href);if(url.searchParams.has('lang')){url.searchParams.delete('lang');history.replaceState(history.state,'',url.pathname+url.search+url.hash);}
})();
