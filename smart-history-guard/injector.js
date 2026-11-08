(function () {
  'use strict';
  if (window.__SHG_INSTALLED__) return;
  Object.defineProperty(window, '__SHG_INSTALLED__', { value: true });

  const BURST_MS = 1000;          // pushes closer together than this are a "burst"
  const GESTURE_MS = 1000;        // a verified gesture stays valid this long...
  const GESTURE_PUSH_BUDGET = 2;  // ...and authorises at most this many pushes
  const UI_STATE_KEYS = /^(modal|dialog|drawer|overlay|tab|tabid|activetab|panel|popup|lightbox|view)$/i;
  const GESTURE_EVENTS = ['click', 'keydown', 'pointerdown', 'mouseup', 'touchend'];

  let isOmitted = false;
  let lastGesture = -Infinity;
  let gestureBudget = 0;
  let lastAttempt = -Infinity;    // time of the previous push attempt (allowed or not)

  // Diagnostics for manual testing: type __SHG_STATS__ in the DevTools console.
  const stats = { allowed: 0, downgraded: 0 };
  Object.defineProperty(window, '__SHG_STATS__', { value: stats });

  // Record trusted gestures in the capture phase on BOTH window and document,
  // so they are logged before any page handler (inline or otherwise) runs.
  function onGesture(e) {
    if (!e.isTrusted) return;               // scripts cannot fake a gesture
    lastGesture = Date.now();
    gestureBudget = GESTURE_PUSH_BUDGET;
  }
  [window, document].forEach((target) => {
    GESTURE_EVENTS.forEach((evt) => {
      target.addEventListener(evt, onGesture, { capture: true, passive: true });
    });
  });

  // Config arrives from the isolated content script as a JSON string.
  window.addEventListener('__SHG_CONFIG_UPDATE__', (e) => {
    try {
      const cfg = JSON.parse(e.detail);
      if (cfg && typeof cfg.omitted === 'boolean') isOmitted = cfg.omitted;
    } catch (_) { /* ignore malformed */ }
  });
  window.dispatchEvent(new CustomEvent('__SHG_CONFIG_REQUEST__'));

  function resolve(url) {
    try { return new URL(String(url), window.location.href); } catch (_) { return null; }
  }
  const stripHash = (u) => u.href.split('#')[0];

  function hasUiIdentifier(state) {
    if (!state || typeof state !== 'object') return false;
    try { return Object.keys(state).some((k) => UI_STATE_KEYS.test(k)); } catch (_) { return false; }
  }

  // Returns true when this pushState should be turned into replaceState.
  function shouldDowngrade(state, url) {
    const now = Date.now();
    const current = new URL(window.location.href);
    const target = (url === undefined || url === null) ? current : resolve(url);
    if (!target) return false;              // invalid URL: let the native call throw

    if (target.href !== current.href && stripHash(target) === stripHash(current)) return false;

    if (target.href === current.href) return !hasUiIdentifier(state);

    const sinceLast = now - lastAttempt;
    lastAttempt = now;
    if (now - lastGesture < GESTURE_MS && gestureBudget > 0) {
      gestureBudget--;
      return false;
    }

    return sinceLast < BURST_MS;
  }

  const nativePush = history.pushState;
  const nativeReplace = history.replaceState;

  history.pushState = new Proxy(nativePush, {
    apply(target, thisArg, args) {
      if (isOmitted) return Reflect.apply(target, thisArg, args);
      let downgrade = false;
      try { downgrade = shouldDowngrade(args[0], args[2]); } catch (_) {}
      if (downgrade) { stats.downgraded++; return Reflect.apply(nativeReplace, thisArg, args); }
      stats.allowed++;
      return Reflect.apply(target, thisArg, args);
    }
  });
})();
