(function(){
  'use strict';

  function ready(fn){
    if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',fn)}else{fn()}
  }

  ready(function(){
    if(location.pathname.indexOf('/blog/')!==0){return}
    var byline=document.querySelector('.byline');
    var canonical=document.querySelector('link[rel="canonical"]');
    var heading=document.querySelector('h1');
    if(!byline||!canonical||!heading||document.querySelector('.article-share')){return}

    var url=canonical.href;
    var title=heading.textContent.trim();
    var bar=document.createElement('div');
    bar.className='article-share';
    bar.setAttribute('aria-label','Share or follow this guide');
    bar.innerHTML='<span>Useful on the floor?</span><button class="tool-action primary" type="button" data-share-guide>Share guide</button><button class="tool-action" type="button" data-copy-guide>Copy link</button><a class="tool-action" href="/feed.xml">Follow via RSS</a><span class="tool-status" role="status" aria-live="polite"></span>';
    byline.insertAdjacentElement('afterend',bar);

    var status=bar.querySelector('.tool-status');
    function copyLink(){
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(function(){status.textContent='Link copied.'},function(){status.textContent='Copy was unavailable in this browser.'});
      }else{
        status.textContent='Copy was unavailable in this browser.';
      }
    }
    bar.querySelector('[data-copy-guide]').addEventListener('click',copyLink);
    bar.querySelector('[data-share-guide]').addEventListener('click',function(){
      if(navigator.share){
        navigator.share({title:title,url:url}).then(function(){status.textContent='Guide shared.'}).catch(function(err){if(err&&err.name!=='AbortError'){copyLink()}});
      }else{
        copyLink();
      }
    });
  });
})();
