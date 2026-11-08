'use strict';

const EXIT_TRAP_MS = 300;
const COOLDOWN_MS = 2000;

// Per-tab short-lived state (service workers may sleep, so this is best-effort).
const lastBack = new Map();   // tabId -> { time, origin }
const lastSkip = new Map();   // tabId -> time

chrome.runtime.onInstalled.addListener(async () => {
  const { masterEnabled, omittedDomains } = await chrome.storage.local.get(['masterEnabled', 'omittedDomains']);
  const init = {};
  if (masterEnabled === undefined) init.masterEnabled = true;
  if (!Array.isArray(omittedDomains)) init.omittedDomains = [];
  if (Object.keys(init).length) await chrome.storage.local.set(init);
});

async function isGuarded(hostname) {
  const { masterEnabled = true, omittedDomains = [] } =
    await chrome.storage.local.get(['masterEnabled', 'omittedDomains']);
  return masterEnabled !== false && !omittedDomains.includes(hostname);
}

function originOf(url) {
  try { return new URL(url).origin; } catch (_) { return null; }
}

// User pressed Back/Forward
chrome.webNavigation.onCommitted.addListener(async (d) => {
  if (d.frameId !== 0) return;
  const origin = originOf(d.url);
  if (!origin) return;

  const quals = d.transitionQualifiers || [];
  if (quals.includes('forward_back')) {
    lastBack.set(d.tabId, { time: Date.now(), origin });
    return;
  }

  // Instant same-origin client redirect right after Back, exit trap
  if (quals.includes('client_redirect')) await maybeSkip(d.tabId, d.url);
});

// Same-document redirects (pushState/replaceState) right after Back
chrome.webNavigation.onHistoryStateUpdated.addListener(async (d) => {
  if (d.frameId !== 0) return;
  await maybeSkip(d.tabId, d.url);
});

async function maybeSkip(tabId, url) {
  const back = lastBack.get(tabId);
  const origin = originOf(url);
  if (!back || !origin || back.origin !== origin) return;
  if (Date.now() - back.time > EXIT_TRAP_MS) return;
  if (Date.now() - (lastSkip.get(tabId) || 0) < COOLDOWN_MS) return;

  const u = new URL(url);
  const hostname = u.protocol === 'file:' ? 'file://' : u.hostname;
  if (!(await isGuarded(hostname))) return;

  lastSkip.set(tabId, Date.now());
  lastBack.delete(tabId);
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      world: 'MAIN',
      func: () => history.go(-2)
    });
  } catch (_) { /* tab closed or restricted page */ }
}

chrome.tabs.onRemoved.addListener((tabId) => {
  lastBack.delete(tabId);
  lastSkip.delete(tabId);
});
