document.addEventListener('DOMContentLoaded', () => {
    // Wait until leaflet is fully loaded
    if (typeof L === 'undefined') {
        console.error('Leaflet is not loaded!');
        return;
    }

    window.unirankMap = L.map('map', {
        zoomControl: false // We will move it to a better position
    }).setView([48.1351, 11.5820], 4); // Default center (Europe)

    L.control.zoom({
        position: 'bottomright'
    }).addTo(window.unirankMap);

    // CartoDB Voyager tiles for a clean, vibrant, readable theme (Duolingo-esque)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(window.unirankMap);

    // Setup MarkerCluster
    const markers = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 40,
        iconCreateFunction: function (cluster) {
            const children = cluster.getAllChildMarkers();
            let totalScore = 0;
            children.forEach(m => {
                totalScore += parseFloat(m.options.score || 0);
            });
            const avgScore = totalScore / children.length;
            
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

    window.unirankMap.addLayer(markers);

    let allMarkers = [];

    // Listen to data updates from script.js
    window.addEventListener('unirank:dataUpdated', (e) => {
        const data = e.detail.filteredData || [];
        updateMap(data);
    });

    function getMarkerColorClass(score) {
        if (score >= 8.5) return 'marker-excellent';
        if (score >= 7.0) return 'marker-strong';
        if (score >= 5.5) return 'marker-moderate';
        return 'marker-weak';
    }

    function updateMap(data) {
        markers.clearLayers();
        allMarkers = [];
        let totalScore = 0;
        let validLocations = 0;

        data.forEach(row => {
            const n = window.uniDataAdapter ? window.uniDataAdapter.normalizeUniversityRecord(row) : null;
            if (!n || !n.location || !n.location.latitude || !n.location.longitude) return;

            const lat = n.location.latitude;
            const lng = n.location.longitude;
            const score = row._score || 0;
            const colorClass = getMarkerColorClass(score);

            const iconHtml = `<div class="custom-marker ${colorClass}"><span class="marker-score">${score.toFixed(1)}</span></div>`;
            
            const customIcon = L.divIcon({
                className: 'unirank-marker-icon',
                html: iconHtml,
                iconSize: [32, 32],
                iconAnchor: [16, 32],
                popupAnchor: [0, -32],
            });

            const marker = L.marker([lat, lng], {
                icon: customIcon,
                score: score
            });

            // Popup Content
            const t = window.t || (k => k);
            const title = window.localizedValue(n.universityName) || n.id;
            const program = window.localizedValue(n.programName) || "—";
            const cost = n.totalAcademicCost || "—";

            const popupContent = `
                <div class="map-popup-card">
                    <div class="map-popup-header ${colorClass}-bg">
                        <h3>${title}</h3>
                        <p>${n.location.city || ''}, ${n.location.country || ''}</p>
                    </div>
                    <div class="map-popup-body">
                        <div class="map-popup-row">
                            <span class="map-popup-label">${t("program")}</span>
                            <span class="map-popup-val">${program}</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${t("yearly_cost") || "Yearly Cost"}</span>
                            <span class="map-popup-val">${cost}€</span>
                        </div>
                        <div class="map-popup-row">
                            <span class="map-popup-label">${t("col_score") || "Score"}</span>
                            <span class="map-popup-val score-val">${score.toFixed(1)} / 10</span>
                        </div>
                        <button class="btn btn-sm" style="width:100%; margin-top: 12px; background:#1cb0f6; color:white; border-radius:12px; border:none; box-shadow:0 4px 0 #1899d6; font-weight:700; transition: transform 0.1s; transform: translateY(0);" onmousedown="this.style.transform='translateY(4px)'; this.style.boxShadow='none'" onmouseup="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 0 #1899d6'" onclick="window.openDrawerById('${n.id}')">${t("detail")}</button>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, {
                minWidth: 260,
                className: 'custom-map-popup'
            });

            markers.addLayer(marker);
            allMarkers.push(marker);
            
            totalScore += score;
            validLocations++;
        });

        // Update KPIs
        document.getElementById('map-kpi-count').textContent = validLocations;
        document.getElementById('map-kpi-avg-score').textContent = validLocations > 0 ? (totalScore / validLocations).toFixed(1) : "0.0";
    }

    // Helper to open drawer directly from map popup
    window.openDrawerById = function(id) {
        if (!window.filteredData) return;
        const row = window.filteredData.find(r => {
            const rId = r.Uni_ID || r.id || r.name;
            return rId === id;
        });
        if (row && window.openDrawer) {
            window.openDrawer(row);
        }
    };

    window.fitMapToResults = function() {
        if (allMarkers.length > 0) {
            const group = new L.featureGroup(allMarkers);
            window.unirankMap.fitBounds(group.getBounds(), { padding: [50, 50] });
        }
    };

    // Auto fit on load? No, let the user zoom or fit themselves, except maybe on first heavy filter change.
});
