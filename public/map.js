function initUniRankMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    if (typeof L === 'undefined') {
        console.error('Leaflet is not loaded; map view cannot start.');
        return;
    }

    const simpleMode = localStorage.getItem('unirank_map_detailed') !== 'true';
    const countryShapesUrl = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson';
    const palette = ['#ffd166', '#b8e986', '#a8dadc', '#cdb4db', '#ffb4a2', '#90dbf4', '#f7b267'];

    window.unirankMap = L.map(mapElement, {
        zoomControl: false,
        worldCopyJump: true,
        minZoom: 1.5,
        maxZoom: 18
    }).setView([25, 10], 2.3);

    L.control.zoom({ position: 'bottomright' }).addTo(window.unirankMap);

    // The detailed layer is intentionally opt-in. The default view is a calm,
    // tile-free atlas so the important objects (countries, cities, universities)
    // stay readable instead of competing with roads and labels.
    const detailedTiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    });

    const createMarkerLayer = () => {
        if (typeof L.markerClusterGroup === 'function') {
            return L.markerClusterGroup({
                showCoverageOnHover: false,
                maxClusterRadius: 40,
                iconCreateFunction: function (cluster) {
                    const children = cluster.getAllChildMarkers();
                    const totalScore = children.reduce((sum, marker) => sum + Number(marker.options.score || 0), 0);
                    const avgScore = children.length ? totalScore / children.length : 0;
                    let colorClass = 'cluster-weak';
                    if (avgScore >= 8.5) colorClass = 'cluster-excellent';
                    else if (avgScore >= 7.0) colorClass = 'cluster-strong';
                    else if (avgScore >= 5.5) colorClass = 'cluster-moderate';

                    return L.divIcon({
                        html: `<div class="custom-cluster ${colorClass}"><span>${children.length}</span></div>`,
                        className: 'custom-cluster-icon',
                        iconSize: [40, 40]
                    });
                }
            });
        }

        // A failed optional MarkerCluster request must not make all pins vanish.
        console.warn('MarkerCluster is unavailable; using a plain marker layer.');
        return L.layerGroup();
    };

    const plainMarkers = L.layerGroup();
    const clusteredMarkers = createMarkerLayer();
    let markers = plainMarkers;
    markers.addTo(window.unirankMap);
    const countryLabelLayer = L.layerGroup();
    const cityLabelLayer = L.layerGroup();
    let countryShapesLayer = null;
    let countryShapesPromise = null;
    let allMarkers = [];
    let currentData = [];
    let isDetailed = false;

    const toggle = document.getElementById('map-detail-toggle');
    const modeBadge = document.getElementById('map-mode-badge');
    const detailStatus = document.getElementById('map-detail-status');

    function t(key, fallback) {
        return typeof window.t === 'function' ? window.t(key) : fallback;
    }

    function escapeHtml(value) {
        return String(value ?? '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function scoreClass(score) {
        if (score >= 8.5) return 'marker-excellent';
        if (score >= 7.0) return 'marker-strong';
        if (score >= 5.5) return 'marker-moderate';
        return 'marker-weak';
    }

    function getCountryName(feature) {
        const properties = feature && feature.properties ? feature.properties : {};
        return properties.ADMIN || properties.NAME || properties.name || properties.Country || '';
    }

    function colorForCountry(name) {
        let hash = 0;
        for (let i = 0; i < name.length; i += 1) hash = (hash * 31 + name.charCodeAt(i)) >>> 0;
        return palette[hash % palette.length];
    }

    function styleCountry(feature) {
        const name = getCountryName(feature);
        return {
            color: '#ffffff',
            weight: 1.2,
            opacity: 0.9,
            fillColor: colorForCountry(name),
            fillOpacity: 0.48
        };
    }

    function addCountryShapes() {
        if (countryShapesLayer) {
            countryShapesLayer.addTo(window.unirankMap);
            return;
        }
        if (countryShapesPromise) return;

        countryShapesPromise = fetch(countryShapesUrl)
            .then(response => {
                if (!response.ok) throw new Error(`Country map request failed (${response.status})`);
                return response.json();
            })
            .then(geojson => {
                countryShapesLayer = L.geoJSON(geojson, {
                    style: styleCountry,
                    onEachFeature: (feature, layer) => {
                        const name = getCountryName(feature);
                        if (name) layer.bindTooltip(escapeHtml(name), { sticky: true, className: 'simple-map-tooltip' });
                        layer.on({
                            mouseover: event => event.target.setStyle({ weight: 2, fillOpacity: 0.68 }),
                            mouseout: event => countryShapesLayer.resetStyle(event.target)
                        });
                    }
                });
                if (!isDetailed) countryShapesLayer.addTo(window.unirankMap);
            })
            .catch(error => {
                // Labels and pins remain useful if a third-party GeoJSON request
                // is blocked; the simple map should degrade gracefully.
                console.warn('Simple country shapes could not be loaded:', error.message);
            });
    }

    function getLocations(data) {
        return data.map(row => {
            const normalized = window.uniDataAdapter
                ? window.uniDataAdapter.normalizeUniversityRecord(row)
                : null;
            if (!normalized || !normalized.location) return null;
            const { latitude, longitude } = normalized.location;
            if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return null;
            return { row, normalized, latitude, longitude };
        }).filter(Boolean);
    }

    function addCountryLabel(country, items) {
        const latitude = items.reduce((sum, item) => sum + item.latitude, 0) / items.length;
        const longitude = items.reduce((sum, item) => sum + item.longitude, 0) / items.length;
        const label = window.getCountryName ? window.getCountryName(country) : country;
        const icon = L.divIcon({
            className: 'simple-country-icon',
            html: `<div class="simple-country-label"><span class="simple-country-dot"></span><span>${escapeHtml(label)}</span><b>${items.length}</b></div>`,
            iconSize: [0, 0],
            iconAnchor: [0, 0]
        });
        L.marker([latitude, longitude], { icon, keyboard: false, interactive: false }).addTo(countryLabelLayer);
    }

    function renderPlaceLabels(locatedData) {
        countryLabelLayer.clearLayers();
        cityLabelLayer.clearLayers();

        const countries = new Map();
        const cities = new Map();
        locatedData.forEach(item => {
            const country = item.normalized.location.country || item.normalized.country || 'Unknown';
            const city = item.normalized.location.city || item.normalized.city || 'Unknown city';
            if (!countries.has(country)) countries.set(country, []);
            countries.get(country).push(item);
            const cityKey = `${country}::${city}`;
            if (!cities.has(cityKey)) cities.set(cityKey, { name: city, country, items: [] });
            cities.get(cityKey).items.push(item);
        });

        countries.forEach((items, country) => addCountryLabel(country, items));

        // City labels appear after zooming in, keeping the default world view
        // friendly and uncluttered while preserving the real university point.
        if (window.unirankMap.getZoom() < 3.4) return;
        cities.forEach(cityGroup => {
            const latitude = cityGroup.items.reduce((sum, item) => sum + item.latitude, 0) / cityGroup.items.length;
            const longitude = cityGroup.items.reduce((sum, item) => sum + item.longitude, 0) / cityGroup.items.length;
            const icon = L.divIcon({
                className: 'simple-city-icon',
                html: `<div class="simple-city-label"><span class="simple-city-dot"></span>${escapeHtml(cityGroup.name)}</div>`,
                iconSize: [0, 0],
                iconAnchor: [0, 0]
            });
            L.marker([latitude, longitude], { icon, keyboard: false, interactive: false }).addTo(cityLabelLayer);
        });
    }

    function setSimpleLayerVisibility() {
        if (isDetailed) {
            if (countryShapesLayer) window.unirankMap.removeLayer(countryShapesLayer);
            window.unirankMap.removeLayer(countryLabelLayer);
            window.unirankMap.removeLayer(cityLabelLayer);
            return;
        }

        addCountryShapes();
        countryLabelLayer.addTo(window.unirankMap);
        if (window.unirankMap.getZoom() >= 3.4) cityLabelLayer.addTo(window.unirankMap);
        else window.unirankMap.removeLayer(cityLabelLayer);
    }

    function updateModeText() {
        if (modeBadge) modeBadge.textContent = t(isDetailed ? 'map_detailed_badge' : 'map_simple_badge', isDetailed ? 'Detailed map' : 'Friendly atlas');
        if (detailStatus) detailStatus.textContent = t(isDetailed ? 'map_detailed_toggle_desc' : 'map_simple_status', isDetailed ? 'Real-world map is on.' : 'Friendly atlas is on by default.');
    }

    function setMapMode(detailed, persist = true) {
        isDetailed = Boolean(detailed);
        if (persist) localStorage.setItem('unirank_map_detailed', String(isDetailed));
        if (toggle) toggle.checked = isDetailed;

        const nextMarkerLayer = isDetailed ? clusteredMarkers : plainMarkers;
        if (markers !== nextMarkerLayer) {
            window.unirankMap.removeLayer(markers);
            markers = nextMarkerLayer;
            markers.addTo(window.unirankMap);
            updateMap(currentData);
        }

        if (isDetailed) {
            detailedTiles.addTo(window.unirankMap);
            mapElement.classList.add('map-detailed-mode');
            mapElement.classList.remove('map-simple-mode');
        } else {
            window.unirankMap.removeLayer(detailedTiles);
            mapElement.classList.add('map-simple-mode');
            mapElement.classList.remove('map-detailed-mode');
        }
        setSimpleLayerVisibility();
        updateModeText();
        window.unirankMap.invalidateSize();
    }

    function formatCost(value) {
        if (value === null || value === undefined || value === '') return '\u2014';
        const number = Number(value);
        if (!Number.isFinite(number)) return '—';
        return `${number.toLocaleString('en-US')}€`;
    }

    function updateMap(data) {
        currentData = Array.isArray(data) ? data : [];
        const locatedData = getLocations(currentData);
        markers.clearLayers();
        allMarkers = [];
        let totalScore = 0;

        locatedData.forEach(({ row, normalized: n, latitude, longitude }) => {
            const rawScore = Number(row._score);
            const score = Number.isFinite(rawScore) ? rawScore : 0;
            const colorClass = scoreClass(score);
            const iconHtml = `<div class="custom-marker ${colorClass}"><span class="marker-score">${score.toFixed(1)}</span></div>`;
            const customIcon = L.divIcon({
                className: 'unirank-marker-icon',
                html: iconHtml,
                iconSize: [32, 42],
                iconAnchor: [16, 38],
                popupAnchor: [0, -38]
            });

            const marker = L.marker([latitude, longitude], { icon: customIcon, score });
            const title = window.localizedValue ? window.localizedValue(n.universityName) : n.universityName;
            const program = window.localizedValue ? window.localizedValue(n.programName) : n.programName;
            const city = n.location.city || n.city || '';
            const country = n.location.country || n.country || '';
            const popupContent = `
                <div class="map-popup-card">
                    <div class="map-popup-header ${colorClass}-bg">
                        <h3>${escapeHtml(title || n.id)}</h3>
                        <p>${escapeHtml([city, country].filter(Boolean).join(', '))}</p>
                    </div>
                    <div class="map-popup-body">
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('program', 'Program'))}</span>
                            <span class="map-popup-val">${escapeHtml(program || '—')}</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('yearly_cost', 'Yearly Cost'))}</span>
                            <span class="map-popup-val">${escapeHtml(formatCost(n.totalAcademicCost ?? n.tuitionPerYear))}</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${escapeHtml(t('col_score', 'Score'))}</span>
                            <span class="map-popup-val score-val">${score.toFixed(1)} / 10</span>
                        </div>
                        <button class="btn btn-sm map-detail-button" data-map-detail-id="${escapeHtml(n.id)}">${escapeHtml(t('detail', 'Details'))}</button>
                    </div>
                </div>`;

            marker.bindPopup(popupContent, { minWidth: 260, className: 'custom-map-popup' });
            marker.on('popupopen', event => {
                const button = event.popup.getElement()?.querySelector('[data-map-detail-id]');
                if (button) button.addEventListener('click', () => window.openDrawerById(button.dataset.mapDetailId));
            });
            markers.addLayer(marker);
            allMarkers.push(marker);
            totalScore += score;
        });

        renderPlaceLabels(locatedData);
        if (!isDetailed) setSimpleLayerVisibility();
        const countElement = document.getElementById('map-kpi-count');
        const scoreElement = document.getElementById('map-kpi-avg-score');
        if (countElement) countElement.textContent = String(locatedData.length);
        if (scoreElement) scoreElement.textContent = locatedData.length ? (totalScore / locatedData.length).toFixed(1) : '0.0';
    }

    window.openDrawerById = function (id) {
        const row = (window.filteredData || currentData).find(item => {
            const recordId = item.Uni_ID || item.id || item.name || item.university;
            return recordId === id;
        });
        if (row && window.openDrawer) window.openDrawer(row);
    };

    window.fitMapToResults = function () {
        if (allMarkers.length > 0) {
            const group = new L.featureGroup(allMarkers);
            window.unirankMap.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 8 });
        }
    };

    if (toggle) {
        toggle.addEventListener('change', event => setMapMode(event.target.checked));
    }
    window.unirankMap.on('zoomend', () => {
        if (!isDetailed) {
            renderPlaceLabels(getLocations(currentData));
            setSimpleLayerVisibility();
        }
    });

    window.addEventListener('unirank:dataUpdated', event => {
        updateMap(event.detail?.filteredData || []);
    });

    setMapMode(simpleMode ? false : true, false);
    updateMap(window.filteredData || []);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUniRankMap);
} else {
    initUniRankMap();
}
