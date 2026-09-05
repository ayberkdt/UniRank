/**
 * Application calendar page bootstrap.
 *
 * The calendar used to be a dialog inside the programmes page, which meant
 * it borrowed that page's data loader, its drawer and its navigation.  On its
 * own page it only needs the records; everything else is the dashboard
 * module, which renders into the ids this file's HTML provides.
 *
 * Opening a programme from here goes back to the programmes page with the
 * record pre-selected (index.html?program=<id>), which that page already
 * understands.
 */
(function () {
    'use strict';

    let inFlight = null;

    function isUndergraduate(record) {
        const degreeText = [record?.degree_level, record?.program_degree, record?.degree]
            .map(value => String(value || '')).join(' ').toLowerCase();
        return /\b(bachelor|b\.\s*sc\.?|bsc|undergraduate|first[- ]cycle|lisans)\b/.test(degreeText);
    }

    async function loadRecords({ silent = false } = {}) {
        if (inFlight) return inFlight;
        inFlight = (async () => {
            try {
                const response = await fetch('/api/universities');
                if (!response.ok) throw new Error(`API request failed (${response.status})`);
                const json = await response.json();
                if (json.status !== 'success' || !Array.isArray(json.data)) throw new Error(json.message || 'API request failed.');
                const records = json.data.filter(record => !isUndergraduate(record));
                window.uniRankRecords = records;
                window.dispatchEvent(new CustomEvent('unirank:recordsLoaded', {
                    detail: { records, refreshedAt: new Date().toISOString(), silent }
                }));
                return true;
            } catch (error) {
                console.warn('Calendar data load failed:', error);
                if (!silent) showLoadError(error);
                return false;
            } finally {
                inFlight = null;
            }
        })();
        return inFlight;
    }

    function showLoadError(error) {
        const list = document.getElementById('deadline-program-list');
        if (!list) return;
        const turkish = window.currentLanguage === 'tr';
        list.innerHTML = `<div class="deadline-empty-state" role="alert"><span aria-hidden="true">⚠</span><h3>${turkish ? 'Takvim verisi yüklenemedi' : 'The calendar data could not be loaded'}</h3><p>${String(error?.message || '')}</p></div>`;
    }

    // The dashboard calls this on its own schedule (every 15 minutes, on
    // focus, when the connection returns).
    window.refreshUniRankData = () => loadRecords({ silent: true });

    // "Open programme" hands over to the programmes page, which owns the
    // detail rail.
    window.openDrawer = record => {
        const normalized = window.uniDataAdapter?.normalizeUniversityRecord(record);
        const id = normalized?.id || record?.id || record?.programme_id;
        if (!id) return;
        window.location.href = `index.html?program=${encodeURIComponent(id)}`;
    };

    function start() {
        if (typeof window.applyTranslations === 'function') window.applyTranslations();
        loadRecords();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
})();
