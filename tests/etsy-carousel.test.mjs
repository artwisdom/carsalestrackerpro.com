import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
const html = readFileSync(new URL('../tools/index.html', import.meta.url),'utf8');
const source = readFileSync(new URL('../assets/etsy-carousel.js', import.meta.url),'utf8');
test('seven purchase links, one preserved unavailable product, and honest artwork fallbacks', () => {
  const ids = [...html.matchAll(/href="https:\/\/www.etsy.com\/listing\/(\d+)\//g)].map(m => m[1]);
  assert.deepEqual(ids,['4501279794','4606044319','4606063160','4538788064','4539318423','4540313722','4577173310']);
  assert.match(html,/data-availability="unavailable" data-etsy-url="https:\/\/www.etsy.com\/listing\/4522138350\/"/);
  assert.match(html,/<h3>Activity Scorecard<\/h3>/);
  assert.match(html,/<span class="availability-note">Currently unavailable<\/span>/);
  assert.equal((html.match(/See product preview on Etsy/g)||[]).length,5);
  assert.equal((html.match(/original product artwork/g)||[]).length,3);
  assert.ok(!html.includes('sheet-grid'));
});
function setup(reduce=false, padding=0) {
 const listeners = {};
 const track = {scrollLeft:0,clientWidth:620,scrollWidth:2540,listeners:{},getBoundingClientRect:()=>({left:0,right:620}),addEventListener(k,f){this.listeners[k]=f},scrollBy(o){this.lastMove=o},scrollTo(o){this.lastMove=o}};
 track.children=Array.from({length:8},(_,i)=>({getBoundingClientRect:()=>({width:300,left:i*320+padding-track.scrollLeft,right:i*320+300+padding-track.scrollLeft})}));
 const button=()=>({disabled:false,parentElement:{hidden:true},addEventListener(k,f){this[k]=f}});
 const prev=button(),next=button(),position={};
 const elements={'etsy-products':track,'etsy-previous':prev,'etsy-next':next,'etsy-position':position};
 vm.runInNewContext(source,{document:{getElementById:id=>elements[id]},window:{matchMedia:()=>({matches:reduce}),addEventListener:(k,f)=>listeners[k]=f},getComputedStyle:()=>({gap:'20'}),clearTimeout(){},setTimeout:f=>{f();return 1}});
 return {track,prev,next,position,listeners};
}
test('start/end states and resize count',()=>{
 const x=setup(); assert.equal(x.prev.disabled,true); assert.equal(x.next.disabled,false); assert.equal(x.position.textContent,'Products 1–2 of 8');
 x.track.scrollLeft=1920; x.track.listeners.scroll(); assert.equal(x.next.disabled,true); assert.equal(x.position.textContent,'Products 7–8 of 8');
 x.track.scrollLeft=0;x.track.clientWidth=300;x.track.getBoundingClientRect=()=>({left:0,right:300});x.listeners.resize();assert.equal(x.position.textContent,'Product 1 of 8');
});
test('buttons, arrows, Home/End and reduced motion',()=>{
 for(const reduce of [false,true]){
 const x=setup(reduce);x.next.click();assert.equal(x.track.lastMove.left,320);assert.equal(x.track.lastMove.behavior,reduce?'auto':'smooth');
 for(const [key,left] of [['ArrowLeft',-320],['ArrowRight',320],['Home',0],['End',2540]]){let prevented=false;x.track.listeners.keydown({target:x.track,key,preventDefault(){prevented=true}});assert.equal(prevented,true);assert.equal(x.track.lastMove.left,left);}
 x.track.lastMove=null;x.track.listeners.keydown({target:{},key:'ArrowRight'});assert.equal(x.track.lastMove,null);
 }
});
test('progressive controls, accessible links, and scoped motion styling',()=>{
 assert.match(html,/class="controls" hidden/);
 assert.match(html,/id="etsy-position"[^>]*>8 products</);
 assert.equal((html.match(/class="etsy-card"/g)||[]).length,8);
 assert.equal((html.match(/opens in a new tab/g)||[]).length,7);
 const css=readFileSync(new URL('../assets/etsy-carousel.css',import.meta.url),'utf8');
 assert.match(css,/@media\(prefers-reduced-motion:reduce\)/);
 assert.match(html,/id="etsy-products" tabindex="0"/);
});

test('Home keeps the previous control disabled at the padded snap origin', () => {
 const x=setup(true,4);x.track.scrollLeft=4;x.track.listeners.scroll();
 assert.equal(x.prev.disabled,true);
 x.track.scrollLeft=324;x.track.listeners.scroll();assert.equal(x.prev.disabled,false);
});
