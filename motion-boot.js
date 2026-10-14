/* Hide the pre-rendered main only until its one reveal sequence is prepared. */
(function(){if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)||!Element.prototype.animate)return;document.documentElement.classList.add('motion-boot');window.setTimeout(()=>document.documentElement.classList.remove('motion-boot'),5000);})();
