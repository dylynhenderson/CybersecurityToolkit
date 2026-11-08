(function () {
  'use strict';
  const hostname = window.location.protocol === 'file:' ? 'file://' : window.location.hostname;

  function currentOmitted(res) {
    const masterEnabled = res.masterEnabled !== false;
    const omitted = Array.isArray(res.omittedDomains) ? res.omittedDomains : [];
    return !masterEnabled || omitted.includes(hostname);
  }

  function syncConfig() {
    try {
      chrome.storage.local.get(['omittedDomains', 'masterEnabled'], (res) => {
        if (chrome.runtime.lastError) return;
        window.dispatchEvent(new CustomEvent('__SHG_CONFIG_UPDATE__', {
          detail: JSON.stringify({ omitted: currentOmitted(res || {}) })
        }));
      });
    } catch (_) { /* extension context invalidated */ }
  }

  syncConfig();
  window.addEventListener('__SHG_CONFIG_REQUEST__', syncConfig);
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === 'local') syncConfig();
  });
})();
