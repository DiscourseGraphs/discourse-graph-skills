/* Standalone HTML starter 1.0.0. */
(() => {
  'use strict';
  const themeKey = 'standalone-html:theme:v1';
  const systemTheme = matchMedia('(prefers-color-scheme: dark)');
  let chosenTheme = null;
  try { const saved = localStorage.getItem(themeKey); if (saved === 'dark' || saved === 'light') chosenTheme = saved; } catch {}
  const applyTheme = () => document.documentElement.classList.toggle('dark', chosenTheme ? chosenTheme === 'dark' : systemTheme.matches);
  applyTheme();

  function initialize() {
    const status = document.getElementById('ui-status');
    const announce = text => { status.textContent = text; };
    const themeButton = document.getElementById('theme-toggle');
    const syncTheme = () => { applyTheme(); if (themeButton) themeButton.setAttribute('aria-pressed', String(document.documentElement.classList.contains('dark'))); };
    systemTheme.addEventListener('change', syncTheme);
    if (themeButton) {
      themeButton.hidden = false;
      syncTheme();
      themeButton.addEventListener('click', () => {
        chosenTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        syncTheme();
        try { localStorage.setItem(themeKey, chosenTheme); announce(''); }
        catch { announce('Theme changed for this page. Your browser couldn’t save the preference.'); }
      });
    }

    const details = [...document.querySelectorAll('details[data-level]')];
    const allDetails = [...document.querySelectorAll('#content details')];
    document.querySelectorAll('[data-disclose]').forEach(button => {
      const root = button.dataset.root ? document.getElementById(button.dataset.root) : document.getElementById('content');
      const targets = () => [...(root?.querySelectorAll('details[data-level]') || [])].filter(detail => detail.dataset.level === button.dataset.disclose && !detail.closest('[hidden]'));
      if (!root || !targets().length) return;
      button.hidden = false;
      button.addEventListener('click', () => targets().forEach(detail => { detail.open = button.dataset.open === 'true'; }));
    });
    document.querySelectorAll('[data-disclosure-controls]').forEach(controls => { controls.hidden = !controls.querySelector('[data-disclose]:not([hidden])'); });

    const search = document.getElementById('page-search');
    const searchStatus = document.getElementById('search-status');
    const searchItems = [...document.querySelectorAll('[data-search-item]')];
    let searchSnapshot = null;
    function updateSearch() {
      if (!search) return;
      const query = search.value.trim().toLocaleLowerCase();
      if (!query) {
        if (searchSnapshot) {
          searchSnapshot.forEach((state, element) => { element.hidden = state.hidden; if (element instanceof HTMLDetailsElement) element.open = state.open; });
          searchSnapshot = null;
        }
        searchStatus.textContent = '';
        return;
      }
      if (!searchSnapshot) searchSnapshot = new Map([...new Set([...allDetails, ...searchItems])].map(element => [element, { hidden: element.hidden, open: element.open }]));
      let count = 0;
      searchItems.forEach(item => {
        const activePanel = !item.closest('[data-tab-panel][hidden]');
        const matches = activePanel && item.textContent.toLocaleLowerCase().includes(query);
        item.hidden = activePanel ? !matches : searchSnapshot.get(item).hidden;
        if (matches) {
          count++;
          for (let node = item; node; node = node.parentElement) if (node instanceof HTMLDetailsElement) node.open = true;
        }
      });
      details.filter(detail => detail.dataset.level === 'group').forEach(group => {
        const children = [...group.querySelectorAll('[data-search-item]')];
        if (children.length && !group.closest('[data-tab-panel][hidden]')) group.hidden = !children.some(item => !item.hidden);
      });
      searchStatus.textContent = count ? `${count} matching ${count === 1 ? 'item' : 'items'}.` : 'No matching items.';
    }
    if (search && searchItems.length) {
      document.getElementById('search-controls').hidden = false;
      search.addEventListener('input', updateSearch);
      document.getElementById('clear-search').addEventListener('click', () => { search.value = ''; updateSearch(); search.focus(); });
    }

    const tabControllers = new Map();
    document.querySelectorAll('[data-tabs]').forEach(root => {
      const tabs = [...root.querySelectorAll('[role="tab"]')].filter(tab => tab.closest('[data-tabs]') === root);
      const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
      const tablist = root.querySelector('[role="tablist"]');
      if (!tablist || !tabs.length || panels.some(panel => !panel || panel.closest('[data-tabs]') !== root)) return;
      const activate = tab => {
        tabs.forEach((current, index) => {
          const selected = current === tab;
          current.setAttribute('aria-selected', String(selected));
          current.tabIndex = selected ? 0 : -1;
          panels[index].hidden = !selected;
        });
        updateSearch();
      };
      tablist.hidden = false;
      tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => activate(tab));
        tab.addEventListener('keydown', event => {
          const destination = event.key === 'ArrowRight' ? (index + 1) % tabs.length : event.key === 'ArrowLeft' ? (index + tabs.length - 1) % tabs.length : event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : null;
          if (destination === null) return;
          event.preventDefault(); activate(tabs[destination]); tabs[destination].focus();
        });
        tabControllers.set(panels[index], () => activate(tab));
      });
      activate(tabs.find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0]);
    });

    function revealHash() {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const target = document.getElementById(id);
      if (!target) return;
      if (search?.value) { search.value = ''; updateSearch(); }
      const ancestors = [];
      for (let node = target; node; node = node.parentElement) ancestors.unshift(node);
      ancestors.forEach(node => { tabControllers.get(node)?.(); if (node instanceof HTMLDetailsElement) node.open = true; });
      const focusTarget = target instanceof HTMLDetailsElement ? target.querySelector(':scope > summary') : target;
      if (!focusTarget.hasAttribute('tabindex')) focusTarget.tabIndex = -1;
      requestAnimationFrame(() => {
        target.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
        focusTarget.focus({ preventScroll: true });
      });
      document.querySelectorAll('.page-nav a').forEach(link => {
        if (link.hash === location.hash) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
      });
    }
    document.addEventListener('click', event => {
      const link = event.target.closest('a[href^="#"]');
      if (link && link.hash && link.hash === location.hash) revealHash();
    });
    window.addEventListener('hashchange', revealHash);
    if (location.hash) revealHash();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
