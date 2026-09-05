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
        return window.uniStorage.read('unirank_map_detailed', 'true') === 'true';
    }

    function persistDetailedPreference(value) {
        window.uniStorage.write('unirank_map_detailed', String(value));
    }

    function readPanelPreference() {
        return window.uniStorage.read('unirank_map_panel_collapsed', 'false') === 'true';
    }

    function persistPanelPreference(value) {
        window.uniStorage.write('unirank_map_panel_collapsed', String(value));
    }

    const initialDetailedMode = readDetailedPreference();
    // CARTO's public basemaps started stamping "API KEY REQUIRED" across every
    // tile, so the map had a watermark for a background.  Esri's dark canvas
    // needs no key, matches the graphite UI, and stops the tiles fighting the
    // score markers for attention.
    const tileAttribution = 'Tiles &copy; Esri &mdash; Esri, HERE, Garmin, OpenStreetMap contributors';

    window.unirankMap = L.map(mapElement, {
        zoomControl: false,
        worldCopyJump: true,
        minZoom: 2,
        maxZoom: 16
    }).setView([25, 10], 2);

    const map = window.unirankMap;
    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    // Calm mode is the unlabelled dark canvas, so the score markers stay
    // readable; detailed mode lays the matching place-name layer on top.
    // They must differ, or the "More map context" toggle silently does nothing.
    const baseTiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: tileAttribution,
        maxZoom: 16
    });
    const labelTiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16
    });

    // The tile layer already contains borders. Keeping a second remote GeoJSON
    // dependency made the entire map look broken whenever GitHub raw content
    // was blocked, despite markers and tiles being usable.

    const toggle = document.getElementById('map-detail-toggle');
    const detailStatus = document.getElementById('map-detail-status');
    const resultsListElement = document.getElementById('map-results-list');
    const resultsHeaderElement = document.querySelector('#map-results-panel .map-results-header');
    const mapWorkspace = document.getElementById('map-view-container');
    const panelToggle = document.getElementById('map-panel-toggle');
    const mapCanvasShell = mapElement.closest('.map-canvas-shell');
    const mapToolbarOverlay = document.querySelector('.map-toolbar-overlay');
    const mapLegend = document.querySelector('.map-legend');
    const mapToolbarActions = document.querySelector('.map-toolbar-actions');
    let mapStage = null;

    if (mapWorkspace && mapCanvasShell && mapToolbarOverlay && mapLegend) {
        mapStage = document.createElement('div');
        mapStage.className = 'map-stage';
        const contextStrip = document.createElement('div');
        contextStrip.className = 'map-context-strip';
        mapWorkspace.insertBefore(mapStage, mapCanvasShell);
        mapStage.append(contextStrip, mapCanvasShell);
        contextStrip.append(mapToolbarOverlay, mapLegend);
    }

    const fullscreenButton = mapToolbarActions && mapStage ? document.createElement('button') : null;
    if (fullscreenButton) {
        fullscreenButton.type = 'button';
        fullscreenButton.className = 'btn map-fullscreen-button';
        fullscreenButton.textContent = isTurkish() ? 'Tam ekran' : 'Full screen';
        fullscreenButton.setAttribute('aria-pressed', 'false');
        mapToolbarActions.appendChild(fullscreenButton);
    }
    let currentData = [];
    let currentLocatedData = [];
    let allMarkers = [];
    let isDetailed = false;
    const markerByKey = new Map();
    // The side panel is scrollable, so it can list far more than the old
    // six results; the cap only guards against absurdly long DOM lists.
    const MAX_LISTED_RESULTS = 30;
    let lastFittedSignature = '';
    let pendingFitSignature = '';

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
        if (score >= 6.5) return 'excellent';
        if (score >= 5.5) return 'strong';
        if (score >= 4.5) return 'moderate';
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

    function universityIdentity(normalized) {
        return [
            localizedValue(normalized?.universityName),
            normalized?.location?.city || normalized?.city || '',
            normalized?.location?.country || normalized?.country || ''
        ].map(value => String(value).trim().toLocaleLowerCase('en-US')).join('|');
    }

    function getLocations(data) {
        const candidates = data.map((row, index) => {
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

        const universities = new Map();
        candidates.forEach(candidate => {
            const key = universityIdentity(candidate.normalized);
            const current = universities.get(key);
            if (!current) {
                universities.set(key, {
                    ...candidate,
                    key: `university:${key}`,
                    sourcePrograms: [candidate],
                    programCount: 1
                });
                return;
            }

            const sourcePrograms = [...current.sourcePrograms, candidate];
            const currentScore = Number(current.row._score);
            const candidateScore = Number(candidate.row._score);
            const useCandidate = Number.isFinite(candidateScore) && (!Number.isFinite(currentScore) || candidateScore > currentScore);
            universities.set(key, {
                ...(useCandidate ? candidate : current),
                key: current.key,
                sourcePrograms,
                programCount: sourcePrograms.length
            });
        });

        return Array.from(universities.values());
    }

    function universityKey(item) {
        return universityIdentity(item.normalized);
    }

    function countUniversities(data) {
        const identities = new Set();
        data.forEach(row => {
            const normalized = window.uniDataAdapter
                ? window.uniDataAdapter.normalizeUniversityRecord(row)
                : null;
            if (normalized) identities.add(universityIdentity(normalized));
        });
        return identities.size;
    }

    function countLocatedPrograms(data) {
        return data.reduce((count, row) => {
            const normalized = window.uniDataAdapter
                ? window.uniDataAdapter.normalizeUniversityRecord(row)
                : null;
            return count + (Number.isFinite(normalized?.location?.latitude) && Number.isFinite(normalized?.location?.longitude) ? 1 : 0);
        }, 0);
    }

    function formatCost(value) {
        if (value === null || value === undefined || value === '') return '—';
        const number = Number(value);
        if (!Number.isFinite(number)) return '—';
        return `${number.toLocaleString(isTurkish() ? 'tr-TR' : 'en-US')}€`;
    }

    function updateModeText() {
        const statusFallback = isDetailed
            ? (isTurkish() ? 'Daha fazla yol ve yer etiketi gösteriliyor.' : 'More roads and place labels are shown.')
            : (isTurkish() ? 'Sade ve dikkat dağıtmayan harita açık.' : 'A clean, low-distraction map is on.');

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

        if (!map.hasLayer(baseTiles)) baseTiles.addTo(map);
        if (isDetailed) {
            if (!map.hasLayer(labelTiles)) labelTiles.addTo(map);
        } else if (map.hasLayer(labelTiles)) {
            map.removeLayer(labelTiles);
        }

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

    function applyMapFullscreenState(fullscreen) {
        if (!mapStage || !fullscreenButton) return;
        const active = Boolean(fullscreen);
        mapStage.classList.toggle('is-fullscreen', active);
        document.body.classList.toggle('map-fullscreen-active', active);
        fullscreenButton.textContent = active
            ? (isTurkish() ? 'Tam ekrandan çık' : 'Exit full screen')
            : (isTurkish() ? 'Tam ekran' : 'Full screen');
        fullscreenButton.setAttribute('aria-pressed', String(active));
        fullscreenButton.setAttribute('aria-label', fullscreenButton.textContent);
        window.setTimeout(() => map.invalidateSize(), 120);
    }

    async function setMapFullscreen(fullscreen) {
        if (!mapStage || !fullscreenButton) return;
        const active = Boolean(fullscreen);

        if (active) {
            // Apply a viewport-filling fallback immediately. When supported,
            // the native Fullscreen API then removes browser chrome as well.
            applyMapFullscreenState(true);
            if (document.fullscreenElement !== mapStage && typeof mapStage.requestFullscreen === 'function') {
                try {
                    await mapStage.requestFullscreen();
                } catch (error) {
                    console.warn('Native map fullscreen unavailable; using viewport fallback.', error);
                }
            }
            return;
        }

        if (document.fullscreenElement === mapStage && typeof document.exitFullscreen === 'function') {
            try {
                await document.exitFullscreen();
            } catch (error) {
                console.warn('Could not exit native map fullscreen cleanly.', error);
            }
        }
        applyMapFullscreenState(false);
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

        locatedData.slice(0, MAX_LISTED_RESULTS).forEach(item => {
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

    function updateSummary(locatedData) {
        const universityCount = new Set(locatedData.map(universityKey)).size;
        const locatedProgramCount = countLocatedPrograms(currentData);
        const missingProgramCount = Math.max(0, currentData.length - locatedProgramCount);
        const visibleListCount = Math.min(MAX_LISTED_RESULTS, universityCount);

        const countElement = document.getElementById('map-kpi-count');
        const universityElement = document.getElementById('map-kpi-universities');
        const missingElement = document.getElementById('map-kpi-missing');

        if (countElement) countElement.textContent = String(locatedProgramCount);
        if (universityElement) universityElement.textContent = String(universityCount);
        if (missingElement) missingElement.textContent = String(missingProgramCount);
        if (!resultsStatusElement) return;
        resultsStatusElement.setAttribute('role', 'status');
        resultsStatusElement.setAttribute('aria-live', 'polite');
        resultsStatusElement.setAttribute('aria-atomic', 'true');

        if (!currentData.length) {
            resultsStatusElement.textContent = isTurkish()
                ? 'Filtrelerle eşleşen program yok.'
                : 'No programs match the current filters.';
        } else if (!universityCount) {
            resultsStatusElement.textContent = isTurkish()
                ? `${missingProgramCount} programın harita koordinatı yok; sonuçlar liste görünümünde kullanılabilir.`
                : `${missingProgramCount} programs have no map coordinates; they remain available in list view.`;
        } else {
            const base = isTurkish()
                ? `${locatedProgramCount} koordinatlı program, ${universityCount} üniversite. İlk ${visibleListCount} üniversite gösteriliyor.`
                : `${locatedProgramCount} mapped programs across ${universityCount} universities. Showing the first ${visibleListCount} universities.`;
            const missing = missingProgramCount
                ? (isTurkish()
                    ? ` ${missingProgramCount} programın koordinatı eksik.`
                    : ` ${missingProgramCount} programs are missing coordinates.`)
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
        });

        renderResultsList(currentLocatedData);
        updateSummary(currentLocatedData);

        // Bring new result sets into view automatically. The signature check
        // keeps language switches and re-renders from resetting a view the
        // user has already panned or zoomed. While the map tab is hidden the
        // container has no size, so the fit is deferred until it is visible.
        const signature = currentLocatedData.map(item => item.key).sort().join(';');
        if (signature && signature !== lastFittedSignature) {
            if (mapElement.offsetParent === null) {
                pendingFitSignature = signature;
            } else {
                lastFittedSignature = signature;
                pendingFitSignature = '';
                window.fitMapToResults();
            }
        }
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
        map.invalidateSize({ pan: false });
        const group = L.featureGroup(allMarkers);
        const bounds = group.getBounds();
        if (bounds.isValid()) map.fitBounds(bounds, { padding: [50, 50], maxZoom: 8, animate: false });
    };

    if (toggle) {
        toggle.addEventListener('change', event => setMapMode(event.target.checked));
    }

    if (panelToggle) {
        panelToggle.addEventListener('click', () => {
            setMapPanelCollapsed(!mapWorkspace?.classList.contains('map-panel-collapsed'));
        });
    }

    if (fullscreenButton) {
        fullscreenButton.addEventListener('click', () => {
            setMapFullscreen(!mapStage?.classList.contains('is-fullscreen'));
        });
        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement || document.fullscreenElement === mapStage) {
                applyMapFullscreenState(document.fullscreenElement === mapStage);
            }
        });
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && mapStage?.classList.contains('is-fullscreen')) {
                setMapFullscreen(false);
            }
        });
    }

    window.addEventListener('unirank:dataUpdated', event => {
        updateMap(event.detail?.filteredData || []);
    });

    // switchView fires a resize event right after the map tab becomes
    // visible; that is the first safe moment to run a deferred fit.
    window.addEventListener('resize', () => {
        if (!pendingFitSignature || mapElement.offsetParent === null) return;
        map.invalidateSize();
        lastFittedSignature = pendingFitSignature;
        pendingFitSignature = '';
        window.fitMapToResults();
    });

    window.addEventListener('unirank:viewChanged', event => {
        if (event.detail?.view !== 'map') return;
        window.requestAnimationFrame(() => {
            map.invalidateSize({ pan: false });
            if (pendingFitSignature) {
                lastFittedSignature = pendingFitSignature;
                pendingFitSignature = '';
            }
            window.fitMapToResults();
        });
    });

    if (typeof ResizeObserver === 'function' && mapCanvasShell) {
        const mapResizeObserver = new ResizeObserver(() => {
            if (mapElement.offsetParent !== null) map.invalidateSize({ pan: false });
        });
        mapResizeObserver.observe(mapCanvasShell);
    }

    document.addEventListener('languageChanged', () => {
        updateModeText();
        if (fullscreenButton) {
            fullscreenButton.textContent = mapStage?.classList.contains('is-fullscreen')
                ? (isTurkish() ? 'Tam ekrandan çık' : 'Exit full screen')
                : (isTurkish() ? 'Tam ekran' : 'Full screen');
        }
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
