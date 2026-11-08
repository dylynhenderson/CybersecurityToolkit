document.addEventListener('DOMContentLoaded', async () => {
  const omitToggle = document.getElementById('omitToggle');
  const masterToggle = document.getElementById('masterToggle');
  const statusEl = document.getElementById('status');
  const domainEl = document.getElementById('domainDisplay');

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  let hostname = null;
  try {
    const u = new URL(tab && tab.url);
    if (/^https?:$/.test(u.protocol)) hostname = u.hostname;
    else if (u.protocol === 'file:') hostname = 'file://'; // For test suite chiefly
  } catch (_) {}

  const state = await chrome.storage.local.get(['omittedDomains', 'masterEnabled']);
  let omitted = Array.isArray(state.omittedDomains) ? state.omittedDomains : [];
  let master = state.masterEnabled !== false;

  function render() {
    masterToggle.checked = master;
    if (!hostname) {
      domainEl.textContent = 'Not available on this page';
      omitToggle.disabled = true;
      statusEl.textContent = '';
      return;
    }
    domainEl.textContent = hostname;
    omitToggle.checked = omitted.includes(hostname);
    const active = master && !omitted.includes(hostname);
    statusEl.textContent = active ? 'Protection active on this site' : 'Protection off on this site';
    statusEl.classList.toggle('off', !active);
  }
  render();

  omitToggle.addEventListener('change', async () => {
    omitted = omitToggle.checked
      ? [...new Set([...omitted, hostname])]
      : omitted.filter((d) => d !== hostname);
    await chrome.storage.local.set({ omittedDomains: omitted });
    render();
  });

  masterToggle.addEventListener('change', async () => {
    master = masterToggle.checked;
    await chrome.storage.local.set({ masterEnabled: master });
    render();
  });
});
