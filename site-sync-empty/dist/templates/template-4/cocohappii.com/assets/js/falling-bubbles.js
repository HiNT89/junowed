(function () {
  // Config
  var COUNT = 40;
  var CONTAINER_ID = 'falling-bubbles';
  // Continuous spawn config
  var CONTINUOUS_SPAWN = true;
  var SPAWN_INTERVAL_MS = 500; // spawn one bubble every 500ms

  function createContainer() {
    var c = document.createElement('div');
    c.id = CONTAINER_ID;
    c.className = 'falling-bubbles';
    c.setAttribute('aria-hidden', 'true');
    document.body.appendChild(c);
    return c;
  }

  function rand(min, max) { return Math.random() * (max - min) + min; }

  function makeBubble(i) {
    var b = document.createElement('div');
    b.className = 'bubble';

    var isBlue = Math.random() > 0.5;
    var size = Math.round(rand(4, 12)); // px
    var left = rand(0, 100); // vw
    var dx = (rand(-20, 20)).toFixed(2) + 'vw'; // horizontal drift
    // shorter durations and only small non-negative delays to avoid bubbles waiting at the top
    var duration = rand(4, 10).toFixed(2) + 's';
    var delay = (rand(0, 1)).toFixed(2) + 's';

    b.style.width = size + 'px';
    b.style.height = size + 'px';
    b.style.left = left + 'vw';
    // start visually above the viewport so they don't appear 'stuck' on page elements
    b.style.top = '-12vh';
    b.style.setProperty('--dx', dx);
    // Apply same duration/delay to both animations (fall + fade)
    b.style.animationDuration = duration + ', ' + duration;
    b.style.animationDelay = delay + ', ' + delay;
    b.style.animationIterationCount = '1, 1';
    b.style.animationFillMode = 'forwards, forwards';

    b.style.backgroundColor = isBlue ? 'var(--color-primary-light, rgba(124,154,194,0.9))' : '#ffffff';
    b.style.boxShadow = isBlue ? '0 0 12px rgba(124,154,194,0.4)' : '0 0 12px rgba(255,255,255,0.6)';

    // Remove bubble element when its animations finish to avoid accumulation
    b.addEventListener('animationend', function () {
      try { b.remove(); } catch (e) { if (b.parentNode) b.parentNode.removeChild(b); }
    }, { once: true });

    return b;
  }

  // Init
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    var container = createContainer();
    // stagger initial spawn so many bubbles don't sit at the top at once
    for (var i = 0; i < COUNT; i++) {
      (function(i){
        setTimeout(function(){ container.appendChild(makeBubble(i)); }, i * 120);
      })(i);
    }

    // continuous gentle spawn (one bubble every SPAWN_INTERVAL_MS)
    if (CONTINUOUS_SPAWN) {
      setInterval(function(){ container.appendChild(makeBubble()); }, SPAWN_INTERVAL_MS);
    }
  }

  init();
})();
