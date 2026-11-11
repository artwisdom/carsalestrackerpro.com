/* Progressive enhancement: native overflow and every Etsy link work without JS. */
(() => {
  'use strict';
  const track = document.getElementById('etsy-products');
  if (!track) return;
  const cards = Array.from(track.children);
  const previous = document.getElementById('etsy-previous');
  const next = document.getElementById('etsy-next');
  const position = document.getElementById('etsy-position');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  previous.parentElement.hidden = false;
  const step = () => cards[0].getBoundingClientRect().width + parseFloat(getComputedStyle(track).gap);
  function update() {
    const bounds = track.getBoundingClientRect();
    const visible = cards.map((card, index) => ({rect: card.getBoundingClientRect(), index}))
      .filter(({rect}) => rect.left >= bounds.left - 2 && rect.right <= bounds.right + 2);
    const first = visible.length ? visible[0].index + 1 : Math.min(cards.length, Math.max(1, Math.round(track.scrollLeft / step()) + 1));
    const last = visible.length ? visible[visible.length - 1].index + 1 : first;
    previous.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    position.textContent = first === last ? `Product ${first} of ${cards.length}` : `Products ${first}–${last} of ${cards.length}`;
  }
  function move(direction) { track.scrollBy({left: direction * step(), behavior: reducedMotion.matches ? 'auto' : 'smooth'}); }
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', event => {
    if (event.target !== track) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1);
    } else if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault();
      track.scrollTo({left: event.key === 'Home' ? 0 : track.scrollWidth, behavior: reducedMotion.matches ? 'auto' : 'smooth'});
    }
  });
  let timer;
  track.addEventListener('scroll', () => {clearTimeout(timer); timer = setTimeout(update, 100);}, {passive: true});
  window.addEventListener('resize', update);
  update();
})();
