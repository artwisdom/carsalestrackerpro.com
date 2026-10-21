/* Dealer Ops Daily signup — one block per page, placed where intent is highest:
   under calculator results, at the end of each guide, mid-homepage, below the tracker.
   Self-contained (injects its own styles) so it also works on pages without site.css.
   Submits to Buttondown's embed endpoint through a hidden iframe, so the reader stays
   on the page. Each signup is tagged with the page type for attribution. */
(function(){
  'use strict';

  var BUTTONDOWN_USER = 'dealeropsdaily';
  var ARCHIVE_URL = 'https://carsalestrackerpro.com/brief/';

  function ready(fn){
    if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',fn)}else{fn()}
  }

  var CSS = '' +
    '.dod-signup{margin:34px 0;padding:22px 22px 18px;border:1px solid var(--border,#E2E8F0);' +
      'border-radius:var(--radius,14px);background:var(--surface,#fff);box-shadow:var(--shadow,none)}' +
    '.dod-signup .dod-kicker{font-size:.72rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;' +
      'color:var(--primary,#0891B2);margin:0 0 6px}' +
    '.dod-signup h2{font-size:1.2rem;line-height:1.3;margin:0 0 6px;color:var(--text,#0F172A);text-wrap:balance}' +
    '.dod-signup p{margin:0 0 14px;color:var(--text2,#475569);font-size:.95rem;line-height:1.55}' +
    '.dod-signup form{display:flex;gap:8px;flex-wrap:wrap}' +
    '.dod-signup input[type=email]{flex:1 1 220px;min-width:0;font:inherit;font-size:1rem;padding:11px 13px;' +
      'border:1px solid var(--border,#E2E8F0);border-radius:10px;background:var(--bg,#F8FAFC);color:var(--text,#0F172A)}' +
    '.dod-signup button{font:inherit;font-weight:700;font-size:.95rem;padding:11px 18px;border:0;border-radius:10px;' +
      'cursor:pointer;color:#fff;background:linear-gradient(135deg,var(--primary,#0891B2),var(--primary-d,#0284C7))}' +
    '.dod-signup button[disabled]{opacity:.6;cursor:default}' +
    '.dod-signup .dod-fine{margin:10px 0 0;font-size:.78rem;color:var(--text3,#64748B)}' +
    '.dod-signup .dod-fine a{color:inherit;text-decoration:underline}' +
    '.dod-signup .dod-done{font-weight:600;color:var(--text,#0F172A);margin:0}' +
    '.dod-signup .dod-hidden{position:absolute;width:1px;height:1px;border:0;left:-9999px}' +
    '.dod-home-wrap{max-width:1160px;margin:0 auto;padding:0 24px}' +
    '.dod-signup.dod-home{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,440px);' +
      'gap:6px 44px;align-items:center;padding:30px 32px}' +
    '.dod-home .dod-copy p:last-child{margin-bottom:0}' +
    '@media(max-width:760px){.dod-signup.dod-home{display:block;padding:22px}' +
      '.dod-home .dod-copy p:last-child{margin-bottom:14px}.dod-home-wrap{padding:0 18px}}' +
    '@media(max-width:480px){.dod-signup button{width:100%}}';

  var COPY = {
    calculator: {
      kicker: 'Free daily brief',
      head: 'Your number moves every month. The market moves every morning.',
      body: 'Dealer Ops Daily: the wholesale, rate and incentive moves that change today’s conversations, plus one tactic worth stealing — in five minutes, before the doors open.'
    },
    guide: {
      kicker: 'Free daily brief',
      head: 'Get a guide like this every weekday morning',
      body: 'Dealer Ops Daily is the five-minute brief for people who sell cars: market numbers that matter on the floor, one tactic worth stealing, and the F&I and compliance moves worth knowing.'
    },
    home: {
      kicker: 'Free daily brief',
      head: 'The 5-minute morning brief for people who sell cars',
      body: 'Market numbers that change today’s conversations, one tactic worth stealing, and the F&I and compliance moves that separate the floor from the desk. Every weekday, before the doors open.'
    },
    landing: {
      kicker: 'Subscribe free',
      head: 'Get tomorrow morning\u2019s brief',
      body: 'Five minutes, every weekday, before the doors open. Free \u2014 and one click to unsubscribe from any issue.'
    },
    issue: {
      kicker: 'Free daily brief',
      head: 'Get the next one in your inbox',
      body: 'Five minutes, every weekday, before the doors open: the market numbers that change today\u2019s conversations, one tactic worth stealing, and a huddle starter for the morning meeting.'
    },
    tracker: {
      kicker: 'Free daily brief',
      head: 'Track your deals here. Track the market in your inbox.',
      body: 'Dealer Ops Daily: five minutes every weekday on what moved in wholesale, rates and compliance — written for the floor, not the corner office.'
    }
  };

  function placement(){
    // A page can reserve an exact spot: <div data-dod-mount="landing"></div>
    var mount = document.querySelector('[data-dod-mount]');
    if(mount){
      var k = mount.getAttribute('data-dod-mount');
      return {kind: COPY[k] ? k : 'guide', anchor: mount, where: 'afterbegin'};
    }
    var path = location.pathname;
    if(/^\/tools\/[^/]+/.test(path)){
      var results = document.querySelector('.compare-results') || document.querySelector('section.calc');
      if(results) return {kind:'calculator', anchor:results, where:'afterend'};
    }
    if(path === '/' || path === '/index.html'){
      var trust = document.querySelector('.trust-section') || document.querySelector('.faq-home');
      if(trust) return {kind:'home', anchor:trust, where:'beforebegin'};
    }
    if(path.indexOf('/tracker') === 0){
      var info = document.querySelector('.tracker-info');
      if(info) return {kind:'tracker', anchor:info, where:'afterend'};
    }
    var article = document.querySelector('article');
    if(article){
      var note = article.querySelector('.editor-note');
      return note ? {kind:'guide', anchor:note, where:'beforebegin'}
                  : {kind:'guide', anchor:article, where:'beforeend'};
    }
    return null;
  }

  function el(tag, attrs, text){
    var n = document.createElement(tag);
    for(var k in attrs){ if(Object.prototype.hasOwnProperty.call(attrs,k)) n.setAttribute(k, attrs[k]); }
    if(text) n.textContent = text;
    return n;
  }

  function build(kind){
    var c = COPY[kind];
    var frameName = 'dod-sub-' + kind;
    var box = el('section', {'class':'dod-signup' + (kind === 'home' ? ' dod-home' : ''),
                             'aria-labelledby':'dod-signup-title'});
    var copy = el('div', {'class':'dod-copy'});
    var action = el('div', {'class':'dod-action'});
    copy.appendChild(el('p', {'class':'dod-kicker'}, c.kicker));
    copy.appendChild(el('h2', {'id':'dod-signup-title'}, c.head));
    copy.appendChild(el('p', {}, c.body));
    box.appendChild(copy);
    box.appendChild(action);

    var form = el('form', {
      'action':'https://buttondown.com/api/emails/embed-subscribe/' + BUTTONDOWN_USER,
      'method':'post', 'target':frameName
    });
    var label = el('label', {'for':'dod-email-'+kind, 'class':'dod-hidden'}, 'Email address');
    var input = el('input', {'type':'email', 'name':'email', 'id':'dod-email-'+kind,
      'required':'', 'autocomplete':'email', 'placeholder':'you@dealership.com'});
    var button = el('button', {'type':'submit'}, 'Get the brief');
    form.appendChild(label);
    form.appendChild(input);
    form.appendChild(el('input', {'type':'hidden', 'name':'embed', 'value':'1'}));
    form.appendChild(el('input', {'type':'hidden', 'name':'tag', 'value':'web-' + kind}));
    form.appendChild(el('input', {'type':'hidden', 'name':'referrer_url', 'value':location.href}));
    form.appendChild(button);
    action.appendChild(form);

    var fine = el('p', {'class':'dod-fine'});
    fine.appendChild(document.createTextNode('Free. Weekday mornings. Unsubscribe anytime. Written by AI from public industry sources and machine-checked before it sends — '));
    fine.appendChild(el('a', {'href':ARCHIVE_URL, 'target':'_blank', 'rel':'noopener'}, 'read a recent issue'));
    fine.appendChild(document.createTextNode('.'));
    action.appendChild(fine);

    var frame = el('iframe', {'name':frameName, 'title':'Signup', 'class':'dod-hidden', 'tabindex':'-1', 'aria-hidden':'true'});
    box.appendChild(frame);

    // The hidden iframe's load event fires when Buttondown answers the POST (its
    // response is cross-origin, so we can't read it). A timer covers browsers that
    // don't fire load for the response.
    var submitted = false, finished = false;
    function showDone(){
      if(finished) return;
      finished = true;
      var done = el('p', {'class':'dod-done', 'role':'status'},
        'Almost there — check your inbox for a confirmation email and click the link inside.');
      form.replaceWith(done);
    }
    frame.addEventListener('load', function(){ if(submitted) showDone(); });
    form.addEventListener('submit', function(){
      submitted = true;
      button.disabled = true;
      button.textContent = 'Sending…';
      setTimeout(showDone, 5000);
    });
    if(kind !== 'home') return box;
    // The homepage has no article container; match its 1160px section grid.
    var wrap = el('div', {'class':'dod-home-wrap'});
    wrap.appendChild(box);
    return wrap;
  }

  ready(function(){
    if(BUTTONDOWN_USER.indexOf('__') === 0) return;  // not configured yet
    if(document.querySelector('.dod-signup')) return;
    var p = placement();
    if(!p) return;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    p.anchor.insertAdjacentElement(p.where, build(p.kind));
  });
})();
