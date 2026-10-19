(() => {
  const form = document.querySelector('form[name="quote-request"]');
  const emit = (name, data) => { if (typeof window.gtag === 'function') window.gtag('event', name, data); };
  document.querySelectorAll('[data-track-call]').forEach(link => link.addEventListener('click', () => emit('referral_phone_click', {page_path: location.pathname})));
  if (!form) return;
  const state = form.elements.state, zip = form.elements.zip, note = document.getElementById('coverage-note');
  // Initial inquiry ZIPs are a screening aid, not a representation of provider coverage.
  const initialZips = new Set(['77535','77575','77327','77328','77336','77532','77561','77538','77564']);
  form.elements.source_page.value = location.origin + location.pathname;
  function screen() {
    state.setCustomValidity(''); zip.setCustomValidity('');
    note.className = 'small coverage-note';
    form.elements.coverage_review.value = 'pending';
    if (state.value === 'outside') {
      state.setCustomValidity('This project accepts Texas property requests only.');
      note.textContent = 'This project accepts Texas property requests only. Please contact a provider serving your property.';
      note.classList.add('error'); return false;
    }
    const value = zip.value.trim();
    const looksTexas = /^(7[5-9]\d{3}|73301|73344|885\d{2})$/.test(value.slice(0,5));
    if (/^\d{5}(-\d{4})?$/.test(value) && !looksTexas) {
      zip.setCustomValidity('This ZIP does not appear to be a Texas ZIP. Check the property location.');
      note.textContent = 'This ZIP does not appear to be in Texas. Check the property ZIP; this project cannot accept out-of-state requests.';
      note.classList.add('error'); return false;
    }
    if (initialZips.has(value.slice(0,5))) {
      note.textContent = 'This ZIP is in the initial inquiry area. Operator availability and property coverage still require review.';
      form.elements.coverage_review.value = 'initial_area_not_confirmed';
    } else if (value.length >= 5) {
      note.textContent = 'This ZIP is outside the initial inquiry list. Your request will be flagged for location review; a referral is not guaranteed.';
      note.classList.add('review'); form.elements.coverage_review.value = 'outside_initial_area_manual_review';
    } else note.textContent = 'Texas requests only. ZIP codes help us screen location; they do not confirm operator coverage.';
    return true;
  }
  state.addEventListener('change', screen); zip.addEventListener('input', screen);
  form.addEventListener('submit', event => {
    if (!screen() || !form.reportValidity()) { event.preventDefault(); return; }
    form.elements.request_id.value = 'SPD-' + (window.crypto?.randomUUID?.() || Date.now().toString(36));
    emit('referral_form_submit_attempt', {page_path: location.pathname});
  });
})();