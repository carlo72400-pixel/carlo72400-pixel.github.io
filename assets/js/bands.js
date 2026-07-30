(function(){
  var PAGES=[['about','01','INFO','the studio'],['stills','02','PHOTO MODE','frames from the floor'],
    ['archive','03','ARCHIVE','client work'],['playback','04','PLAYBACK','the film'],
    ['feed','05','FEED','on the grid'],['rates','06','RATES','the rate card'],
    ['contact','07','STANDBY','let us cut something']];
  PAGES.forEach(function(pg){
    var sec=document.getElementById(pg[0]); if(!sec) return;
    var b=document.createElement('div'); b.className='pagebreak'; b.setAttribute('data-page',pg[0]); b.setAttribute('aria-hidden','true');
    b.innerHTML='<span class="pb-no">REEL '+pg[1]+' / 07</span><span class="pb-name">'+pg[2]+'</span><span class="pb-desc">'+pg[3]+'</span>';
    sec.parentNode.insertBefore(b, sec);
  });
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener('click', function(e){
      var id=a.getAttribute('href').slice(1);
      if(!id || id==='top'){ e.preventDefault(); window.scrollTo({top:0,behavior:'smooth'}); return; }
      var band=document.querySelector('.pagebreak[data-page="'+id+'"]');
      var tgt=band||document.getElementById(id);
      if(tgt){ e.preventDefault(); tgt.scrollIntoView({behavior:'smooth',block:'start'}); }
    });
  });
  var tb=document.getElementById('toTop');
  if(tb){
    var onScroll=function(){ tb.classList.toggle('show', window.scrollY > window.innerHeight*0.85); };
    window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
    tb.addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); });
  }
})();
