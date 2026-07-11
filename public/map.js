function initUniRankMap() {
    const mapElement = document.getElementById('map');
    const fallbackElement = document.getElementById('map-fallback');
    const resultsStatusElement = document.getElementById('map-results-status');

    // Inline controls may call this even when Leaflet failed to load.
    window.fitMapToResults = function () {};

    function isTurkish() {
        return window.currentLanguage === 'tr';
    }

    function t(key, fallback) {
        const translated = typeof window.t === 'function' ? window.t(key) : '';
        return translated && translated !== key ? translated : fallback;
    }

    function showFallback() {
        const message = isTurkish()
            ? 'Harita şu anda yüklenemiyor. Sonuçları liste görünümünde inceleyebilirsiniz.'
            : 'The map is currently unavailable. You can still review the results in list view.';

        if (fallbackElement) {
            fallbackElement.hidden = false;
            fallbackElement.classList.add('is-visible');
            fallbackElement.removeAttribute('aria-hidden');
            const messageElement = fallbackElement.querySelector('[data-map-fallback-message]');
            if (messageElement) messageElement.textContent = message;
            else fallbackElement.textContent = message;
        }

        if (resultsStatusElement) {
            resultsStatusElement.setAttribute('role', 'status');
            resultsStatusElement.setAttribute('aria-live', 'polite');
            resultsStatusElement.textContent = message;
        }
    }

    if (!mapElement) return;

    if (typeof L === 'undefined') {
        console.error('Leaflet is not loaded; map view cannot start.');
        mapElement.setAttribute('aria-hidden', 'true');
        showFallback();
        document.addEventListener('languageChanged', showFallback);
        return;
    }

    if (fallbackElement) {
        fallbackElement.hidden = true;
        fallbackElement.classList.remove('is-visible');
        fallbackElement.setAttribute('aria-hidden', 'true');
    }

    function readDetailedPreference() {
        try {
            const stored = localStorage.getItem('unirank_map_detailed');
            return stored === null ? true : stored === 'true';
        } catch (error) {
            return true;
        }
    }

    function persistDetailedPreference(value) {
        try {
            localStorage.setItem('unirank_map_detailed', String(value));
        } catch (error) {
            // The map remains usable when storage is unavailable.
        }
    }

    function readPanelPreference() {
        try {
            return localStorage.getItem('unirank_map_panel_collapsed') === 'true';
        } catch (error) {
            return false;
        }
    }

    function persistPanelPreference(value) {
        try {
            localStorage.setItem('unirank_map_panel_collapsed', String(value));
        } catch (error) {
            // The panel remains usable when storage is unavailable.
        }
    }

    const initialDetailedMode = readDetailedPreference();
    const tileAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>';

    window.unirankMap = L.map(mapElement, {
        zoomControl: false,
        worldCopyJump: true,
        minZoom: 2,
        maxZoom: 18
    }).setView([25, 10], 2);

    const map = window.unirankMap;
    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    const calmTiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', {
        attribution: tileAttribution,
        subdomains: 'abcd',
        maxZoom: 20
    });
    const detailedTiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: tileAttribution,
        subdomains: 'abcd',
        maxZoom: 20
    });

    fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                style: {
                    color: '#1cb0f6',
                    weight: 2.5,
                    opacity: 0.7,
                    fillColor: '#ffffff',
                    fillOpacity: 0.0,
                    lineCap: 'round',
                    lineJoin: 'round'
                },
                interactive: false
            }).addTo(map);
        })
        .catch(err => console.error('Failed to load country borders GeoJSON:', err));

    const toggle = document.getElementById('map-detail-toggle');
    const modeBadge = document.getElementById('map-mode-badge');
    const detailStatus = document.getElementById('map-detail-status');
    const resultsListElement = document.getElementById('map-results-list');
    const resultsHeaderElement = document.querySelector('#map-results-panel .map-results-header');
    const mapWorkspace = document.getElementById('map-view-container');
    const panelToggle = document.getElementById('map-panel-toggle');
    let currentData = [];
    let currentLocatedData = [];
    let allMarkers = [];
    let isDetailed = false;
    const markerByKey = new Map();

    function escapeHtml(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function localizedValue(value) {
        if (typeof window.localizedValue === 'function') return window.localizedValue(value);
        if (value == null) return '';
        if (typeof value === 'object') return value.en || value.tr || value.name || '';
        return String(value);
    }

    function scoreBand(score) {
        if (score >= 6.0) return 'excellent';
        if (score >= 5.5) return 'strong';
        if (score >= 5.0) return 'moderate';
        return 'weak';
    }

    function scoreClass(score, prefix) {
        return `${prefix}-${scoreBand(score)}`;
    }

    function createMarkerLayer() {
        if (typeof L.markerClusterGroup === 'function') {
            return L.markerClusterGroup({
                showCoverageOnHover: false,
                maxClusterRadius: 25,
                spiderfyOnMaxZoom: true,
                spiderfyDistanceMultiplier: 1.2,
                zoomToBoundsOnClick: true,
                iconCreateFunction: function (cluster) {
                    const children = cluster.getAllChildMarkers();
                    const totalScore = children.reduce((sum, marker) => sum + Number(marker.options.score || 0), 0);
                    const averageScore = children.length ? totalScore / children.length : 0;
                    const colorClass = scoreClass(averageScore, 'cluster');
                    const label = isTurkish()
                        ? `${children.length} program, ortalama skor ${averageScore.toFixed(1)}`
                        : `${children.length} programs, average score ${averageScore.toFixed(1)}`;

                    return L.divIcon({
                        html: `<div class="custom-cluster ${colorClass}" role="img" aria-label="${escapeHtml(label)}"><span class="cluster-count" aria-hidden="true">${children.length}</span><small aria-hidden="true">${isTurkish() ? 'PROG.' : 'PROGS'}</small></div>`,
                        className: 'custom-cluster-icon',
                        iconSize: [54, 54]
                    });
                }
            });
        }

        console.warn('MarkerCluster is unavailable; using a plain marker layer.');
        return L.layerGroup();
    }

    const markers = createMarkerLayer();
    markers.addTo(map);

    function getLocations(data) {
        return data.map((row, index) => {
            const normalized = window.uniDataAdapter
                ? window.uniDataAdapter.normalizeUniversityRecord(row)
                : null;
            if (!normalized || !normalized.location) return null;

            const { latitude, longitude } = normalized.location;
            if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return null;

            const baseId = normalized.id || row.Uni_ID || row.id || row.name || row.university || 'program';
            return {
                key: `${String(baseId)}::${index}`,
                row,
                normalized,
                latitude,
                longitude
            };
        }).filter(Boolean);
    }

    function universityKey(item) {
        const university = localizedValue(item.normalized.universityName) || item.normalized.id || item.key;
        return String(university).trim().toLocaleLowerCase('en-US');
    }

    function formatCost(value) {
        if (value === null || value === undefined || value === '') return '—';
        const number = Number(value);
        if (!Number.isFinite(number)) return '—';
        return `${number.toLocaleString(isTurkish() ? 'tr-TR' : 'en-US')}€`;
    }

    function updateModeText() {
        const badgeFallback = isDetailed
            ? (isTurkish() ? 'Daha fazla yer etiketi' : 'More place labels')
            : (isTurkish() ? 'Sakin harita' : 'Calm map');
        const statusFallback = isDetailed
            ? (isTurkish() ? 'Daha fazla yol ve yer etiketi gösteriliyor.' : 'More roads and place labels are shown.')
            : (isTurkish() ? 'Sade ve dikkat dağıtmayan harita açık.' : 'A clean, low-distraction map is on.');

        if (modeBadge) {
            modeBadge.removeAttribute('data-i18n');
            modeBadge.textContent = badgeFallback;
        }
        if (detailStatus) {
            detailStatus.removeAttribute('data-i18n');
            detailStatus.textContent = statusFallback;
        }
        if (toggle) {
            toggle.checked = isDetailed;
            toggle.setAttribute('aria-label', statusFallback);
        }

        mapElement.setAttribute('role', 'region');
        mapElement.setAttribute(
            'aria-label',
            isTurkish() ? 'Filtrelenmiş üniversite programları haritası' : 'Map of filtered university programs'
        );
    }

    function setMapMode(detailed, persist = true) {
        isDetailed = Boolean(detailed);
        if (persist) persistDetailedPreference(isDetailed);

        const nextLayer = isDetailed ? detailedTiles : calmTiles;
        const previousLayer = isDetailed ? calmTiles : detailedTiles;
        if (map.hasLayer(previousLayer)) map.removeLayer(previousLayer);
        if (!map.hasLayer(nextLayer)) nextLayer.addTo(map);

        mapElement.classList.toggle('map-detailed-mode', isDetailed);
        mapElement.classList.toggle('map-simple-mode', !isDetailed);
        updateModeText();
        map.invalidateSize();
    }

    function setMapPanelCollapsed(collapsed, persist = true) {
        if (!mapWorkspace || !panelToggle) return;

        const isCollapsed = Boolean(collapsed);
        if (persist) persistPanelPreference(isCollapsed);
        mapWorkspace.classList.toggle('map-panel-collapsed', isCollapsed);
        resultsHeaderElement?.toggleAttribute('inert', isCollapsed);
        resultsListElement?.toggleAttribute('inert', isCollapsed);
        panelToggle.setAttribute('aria-expanded', String(!isCollapsed));
        panelToggle.setAttribute(
            'aria-label',
            isCollapsed
                ? (isTurkish() ? 'En iyi üniversiteler panelini aç' : 'Expand top universities panel')
                : (isTurkish() ? 'En iyi üniversiteler panelini daralt' : 'Collapse top universities panel')
        );

        const icon = panelToggle.querySelector('[data-map-panel-icon]');
        if (icon) icon.textContent = isCollapsed ? '›' : '‹';

        window.setTimeout(() => map.invalidateSize(), 220);
    }

    function openDrawerForRow(row, id) {
        if (typeof window.openDrawer === 'function') {
            window.openDrawer(row);
            return;
        }
        if (typeof window.openDrawerById === 'function') window.openDrawerById(id);
    }

    function focusMapResult(item) {
        const marker = markerByKey.get(item.key);
        if (!marker) return;

        const targetZoom = Math.min(map.getMaxZoom(), Math.max(map.getZoom(), 8));
        map.setView([item.latitude, item.longitude], targetZoom, { animate: false });

        const openPopup = () => {
            marker.openPopup();
            const markerElement = marker.getElement();
            if (markerElement) markerElement.focus({ preventScroll: true });
        };

        if (typeof markers.zoomToShowLayer === 'function') {
            markers.zoomToShowLayer(marker, openPopup);
        } else {
            openPopup();
        }
    }

    function renderResultsList(locatedData) {
        if (!resultsListElement) return;
        resultsListElement.replaceChildren();
        resultsListElement.setAttribute('aria-label', isTurkish() ? 'Harita sonuçları' : 'Map results');

        if (!locatedData.length) {
            const empty = document.createElement('p');
            empty.className = 'map-results-empty';
            empty.textContent = isTurkish()
                ? 'Haritada gösterilebilecek sonuç yok.'
                : 'There are no results that can be shown on the map.';
            resultsListElement.appendChild(empty);
            return;
        }

        locatedData.slice(0, 6).forEach(item => {
            const n = item.normalized;
            const title = localizedValue(n.universityName) || String(n.id || '—');
            const program = localizedValue(n.programName) || '—';
            const city = n.location.city || n.city || '';
            const country = n.location.country || n.country || '';
            const location = [city, country].filter(Boolean).join(', ');
            const rawScore = Number(item.row._score);
            const score = Number.isFinite(rawScore) ? rawScore : 0;

            const itemElement = document.createElement('div');
            itemElement.className = 'map-result-item';

            const cardButton = document.createElement('button');
            cardButton.type = 'button';
            cardButton.className = 'map-result-card';
            cardButton.setAttribute(
                'aria-label',
                isTurkish()
                    ? `${title}, ${program}, skor ${score.toFixed(1)}. Haritada göster.`
                    : `${title}, ${program}, score ${score.toFixed(1)}. Show on map.`
            );

            const content = document.createElement('span');
            content.className = 'map-result-card__content';

            const titleElement = document.createElement('span');
            titleElement.className = 'map-result-card__title';
            titleElement.textContent = title;

            const programElement = document.createElement('span');
            programElement.className = 'map-result-card__program';
            programElement.textContent = program;

            const metaElement = document.createElement('span');
            metaElement.className = 'map-result-card__meta';
            metaElement.textContent = location || (isTurkish() ? 'Konum belirtilmemiş' : 'Location not specified');

            const scoreElement = document.createElement('span');
            scoreElement.className = `map-result-card__score map-score map-score--${scoreBand(score)}`;
            scoreElement.textContent = score.toFixed(1);
            scoreElement.setAttribute('aria-hidden', 'true');

            content.append(titleElement, programElement, metaElement);
            cardButton.append(content, scoreElement);
            cardButton.addEventListener('click', () => focusMapResult(item));

            const detailButton = document.createElement('button');
            detailButton.type = 'button';
            detailButton.className = 'map-result-detail';
            detailButton.textContent = '→';
            detailButton.setAttribute(
                'aria-label',
                isTurkish() ? `${title} program detaylarını aç` : `Open program details for ${title}`
            );
            detailButton.addEventListener('click', () => openDrawerForRow(item.row, n.id));

            itemElement.append(cardButton, detailButton);
            resultsListElement.appendChild(itemElement);
        });
    }

    function updateSummary(locatedData, totalScore) {
        const locatedCount = locatedData.length;
        const universityCount = new Set(locatedData.map(universityKey)).size;
        const missingCount = Math.max(0, currentData.length - locatedCount);
        const visibleListCount = Math.min(6, locatedCount);

        const countElement = document.getElementById('map-kpi-count');
        const universityElement = document.getElementById('map-kpi-universities');
        const missingElement = document.getElementById('map-kpi-missing');
        const averageScoreElement = document.getElementById('map-kpi-avg-score');

        if (countElement) countElement.textContent = String(locatedCount);
        if (universityElement) universityElement.textContent = String(universityCount);
        if (missingElement) missingElement.textContent = String(missingCount);
        if (averageScoreElement) {
            averageScoreElement.textContent = locatedCount ? (totalScore / locatedCount).toFixed(1) : '—';
        }

        if (!resultsStatusElement) return;
        resultsStatusElement.setAttribute('role', 'status');
        resultsStatusElement.setAttribute('aria-live', 'polite');
        resultsStatusElement.setAttribute('aria-atomic', 'true');

        if (!currentData.length) {
            resultsStatusElement.textContent = isTurkish()
                ? 'Filtrelerle eşleşen program yok.'
                : 'No programs match the current filters.';
        } else if (!locatedCount) {
            resultsStatusElement.textContent = isTurkish()
                ? `${missingCount} programın harita koordinatı yok; sonuçlar liste görünümünde kullanılabilir.`
                : `${missingCount} programs have no map coordinates; they remain available in list view.`;
        } else {
            const base = isTurkish()
                ? `${locatedCount} koordinatlı program, ${universityCount} üniversite. İlk ${visibleListCount} sonuç gösteriliyor.`
                : `${locatedCount} mapped programs across ${universityCount} universities. Showing the first ${visibleListCount}.`;
            const missing = missingCount
                ? (isTurkish()
                    ? ` ${missingCount} programın koordinatı eksik.`
                    : ` ${missingCount} programs are missing coordinates.`)
                : '';
            resultsStatusElement.textContent = `${base}${missing}`;
        }
    }

    function updateMap(data) {
        currentData = Array.isArray(data) ? data : [];
        currentLocatedData = getLocations(currentData);
        markers.clearLayers();
        markerByKey.clear();
        allMarkers = [];
        let totalScore = 0;

        currentLocatedData.forEach(item => {
            const { row, normalized: n, latitude, longitude } = item;
            const rawScore = Number(row._score);
            const score = Number.isFinite(rawScore) ? rawScore : 0;
            const colorClass = scoreClass(score, 'marker');
            const title = localizedValue(n.universityName) || String(n.id || '—');
            const program = localizedValue(n.programName) || '—';
            const city = n.location.city || n.city || '';
            const country = n.location.country || n.country || '';
            const accessibleLabel = isTurkish()
                ? `${title}, ${program}, skor ${score.toFixed(1)} / 10`
                : `${title}, ${program}, score ${score.toFixed(1)} out of 10`;
            const iconHtml = `<div class="custom-marker ${colorClass}"><small class="marker-label" aria-hidden="true">${isTurkish() ? 'UYUM' : 'FIT'}</small><span class="marker-score">${score.toFixed(1)}</span></div>`;
            const customIcon = L.divIcon({
                className: 'unirank-marker-icon',
                html: iconHtml,
                iconSize: [46, 54],
                iconAnchor: [23, 49],
                popupAnchor: [0, -47]
            });

            const marker = L.marker([latitude, longitude], {
                icon: customIcon,
                score,
                title: accessibleLabel,
                alt: accessibleLabel,
                keyboard: true,
                riseOnHover: true
            });
            const popupContent = `
                <div class="map-popup-card">
                    <div class="map-popup-header ${colorClass}-bg">
                        <h3>${escapeHtml(title)}</h3>
                        <p>${escapeHtml([city, country].filter(Boolean).join(', '))}</p>
                    </div>
                    <div class="map-popup-body">
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('program', isTurkish() ? 'Program' : 'Program'))}</span>
                            <span class="map-popup-val">${escapeHtml(program)}</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('yearly_cost', isTurkish() ? 'Yıllık ücret' : 'Yearly cost'))}</span>
                            <span class="map-popup-val">${escapeHtml(formatCost(n.totalAcademicCost ?? n.tuitionPerYear))}</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('col_score', isTurkish() ? 'Skor' : 'Score'))}</span>
                            <span class="map-popup-val score-val">${score.toFixed(1)} / 10</span>
                        </div>
                        <button class="btn btn-sm map-detail-button" type="button" data-map-detail-id="${escapeHtml(n.id)}">${escapeHtml(t('detail', isTurkish() ? 'Detay' : 'Details'))}</button>
                    </div>
                </div>`;

            marker.bindPopup(popupContent, { minWidth: 260, className: 'custom-map-popup' });
            marker.on('add', () => {
                const markerElement = marker.getElement();
                if (!markerElement) return;
                markerElement.setAttribute('aria-label', accessibleLabel);
                markerElement.setAttribute('role', 'button');
            });
            marker.on('popupopen', event => {
                const button = event.popup.getElement()?.querySelector('[data-map-detail-id]');
                if (button) button.onclick = () => openDrawerForRow(row, n.id);
            });

            markers.addLayer(marker);
            markerByKey.set(item.key, marker);
            allMarkers.push(marker);
            totalScore += score;
        });

        renderResultsList(currentLocatedData);
        updateSummary(currentLocatedData, totalScore);
    }

    window.openDrawerById = function (id) {
        const wantedId = String(id ?? '');
        const row = (window.filteredData || currentData).find(item => {
            const normalized = window.uniDataAdapter
                ? window.uniDataAdapter.normalizeUniversityRecord(item)
                : null;
            const recordId = normalized?.id || item.Uni_ID || item.id || item.name || item.university;
            return String(recordId ?? '') === wantedId;
        });
        if (row && typeof window.openDrawer === 'function') window.openDrawer(row);
    };

    window.fitMapToResults = function () {
        if (!allMarkers.length) return;
        const group = L.featureGroup(allMarkers);
        map.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 8 });
    };

    if (toggle) {
        toggle.addEventListener('change', event => setMapMode(event.target.checked));
    }

    if (panelToggle) {
        panelToggle.addEventListener('click', () => {
            setMapPanelCollapsed(!mapWorkspace?.classList.contains('map-panel-collapsed'));
        });
    }

    window.addEventListener('unirank:dataUpdated', event => {
        updateMap(event.detail?.filteredData || []);
    });

    document.addEventListener('languageChanged', () => {
        updateModeText();
        setMapPanelCollapsed(mapWorkspace?.classList.contains('map-panel-collapsed'), false);
        updateMap(currentData);
    });

    setMapMode(initialDetailedMode, false);
    setMapPanelCollapsed(readPanelPreference(), false);
    updateMap(window.filteredData || []);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUniRankMap);
} else {
    initUniRankMap();
}
