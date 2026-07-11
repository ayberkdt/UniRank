import { useEffect, useMemo, useState } from 'react'
import L from 'leaflet'
import {
  GeoJSON,
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
  ZoomControl,
} from 'react-leaflet'
import { Focus, Layers3, MapPin, Minus, Plus, Route } from 'lucide-react'
import './MapExplorer.css'

const WORLD_BORDERS_URL = 'https://cdn.jsdelivr.net/gh/johan/world.geo.json@master/countries.geo.json'
const TILE_URLS = {
  clean: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png',
  detailed: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
}
const TILE_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function pointIcon(score, count) {
  const band = score == null ? 'unknown' : score >= 7 ? 'great' : score >= 5.5 ? 'good' : 'consider'
  const label = score == null ? '—' : score.toFixed(1)
  return L.divIcon({
    className: 'map-point-icon',
    iconSize: [50, 60],
    iconAnchor: [25, 54],
    popupAnchor: [0, -52],
    html: `<span class="map-pin map-pin--${band}"><small>UYUM</small><b>${label}</b>${count > 1 ? `<em>${count}</em>` : ''}</span>`,
  })
}

function cityIcon(city) {
  return L.divIcon({
    className: 'city-label-icon',
    iconSize: [1, 1],
    iconAnchor: [0, 0],
    html: `<span class="city-label">${escapeHtml(city)}</span>`,
  })
}

function clusterIcon(count) {
  return L.divIcon({
    className: 'map-cluster-icon',
    iconSize: [54, 54],
    iconAnchor: [27, 27],
    html: `<span class="map-cluster"><b>${count}</b><small>PROGRAM</small></span>`,
  })
}

function groupPrograms(programs) {
  const groups = new Map()
  programs.forEach((program) => {
    const latitude = Number(program.location?.latitude)
    const longitude = Number(program.location?.longitude)
    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return
    const key = `${latitude.toFixed(4)}:${longitude.toFixed(4)}`
    const current = groups.get(key) || []
    current.push(program)
    groups.set(key, current)
  })

  return Array.from(groups.entries()).map(([key, group]) => {
    const sorted = [...group].sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
    const top = sorted[0]
    return {
      key,
      latitude: Number(top.location.latitude),
      longitude: Number(top.location.longitude),
      city: top.location.city || top.city || 'Unknown city',
      country: top.location.country || top.country || '',
      top,
      programs: sorted,
      score: top.score,
    }
  })
}

function clusterPoints(points, zoom) {
  if (zoom >= 5) return points.map((point) => ({ ...point, type: 'point' }))

  const gridSize = zoom <= 2 ? 18 : zoom === 3 ? 10 : 5
  const clusters = new Map()
  points.forEach((point) => {
    const key = `${Math.floor((point.latitude + 90) / gridSize)}:${Math.floor((point.longitude + 180) / gridSize)}`
    const current = clusters.get(key) || []
    current.push(point)
    clusters.set(key, current)
  })

  return Array.from(clusters.entries()).map(([key, cluster]) => {
    if (cluster.length === 1) return { ...cluster[0], type: 'point' }
    const allPrograms = cluster.flatMap((point) => point.programs)
    const top = [...allPrograms].sort((left, right) => (right.score ?? -1) - (left.score ?? -1))[0]
    const totalPrograms = allPrograms.length
    return {
      key: `cluster-${key}`,
      type: 'cluster',
      latitude: cluster.reduce((sum, point) => sum + (point.latitude * point.programs.length), 0) / totalPrograms,
      longitude: cluster.reduce((sum, point) => sum + (point.longitude * point.programs.length), 0) / totalPrograms,
      programs: allPrograms,
      top,
      count: totalPrograms,
    }
  })
}

function MapViewport({ points, selectedProgram, fitSignal }) {
  const map = useMap()

  useEffect(() => {
    if (!points.length) return
    const selectedPoint = selectedProgram && points.find((point) => point.programs.some((program) => program.key === selectedProgram.key))
    if (selectedPoint) {
      map.flyTo([selectedPoint.latitude, selectedPoint.longitude], Math.max(map.getZoom(), 6), { duration: 0.55 })
      return
    }

    if (points.length === 1) {
      map.flyTo([points[0].latitude, points[0].longitude], 6, { duration: 0.55 })
      return
    }

    const bounds = L.latLngBounds(points.map((point) => [point.latitude, point.longitude]))
    map.fitBounds(bounds, { padding: [54, 54], maxZoom: 5, animate: Boolean(fitSignal) })
  }, [map, points, selectedProgram, fitSignal])

  return null
}

function CountryBorders() {
  const [borders, setBorders] = useState(null)
  const map = useMap()

  useEffect(() => {
    const pane = map.getPane('country-borders') || map.createPane('country-borders')
    pane.style.zIndex = '380'
    pane.style.pointerEvents = 'none'

    const controller = new AbortController()
    fetch(WORLD_BORDERS_URL, { signal: controller.signal })
      .then((response) => response.ok ? response.json() : Promise.reject(new Error('Border data unavailable')))
      .then(setBorders)
      .catch(() => {})

    return () => controller.abort()
  }, [map])

  if (!borders) return null
  return <GeoJSON
    data={borders}
    pane="country-borders"
    interactive={false}
    style={{
      color: '#80bd89',
      weight: 1.1,
      opacity: 0.86,
      fillColor: '#fdf9e8',
      fillOpacity: 0.32,
      lineCap: 'round',
      lineJoin: 'round',
    }}
  />
}

function ProgramPopup({ point, onSelectProgram }) {
  const top = point.top
  const annualCost = top.totalAcademicCost ?? top.tuitionPerYear

  return (
    <div className="program-popup">
      <span className="popup-place"><MapPin size={13} /> {point.city}, {point.country}</span>
      <h3>{top.universityName}</h3>
      <p>{top.programName}</p>
      <div className="popup-meta">
        <span><b>{top.score ?? '—'}</b> uyum</span>
        <span>{annualCost == null ? 'Ücret bilinmiyor' : `€${Number(annualCost).toLocaleString('tr-TR')}/yıl`}</span>
      </div>
      {point.programs.length > 1 && <small className="popup-count">Bu konumda {point.programs.length} program</small>}
      <div className="popup-actions">
        <button type="button" onClick={() => onSelectProgram(top)}>Programı seç</button>
        {top.programUrl && <a href={top.programUrl} target="_blank" rel="noreferrer">Resmi sayfa ↗</a>}
      </div>
    </div>
  )
}

function MapMarkers({ points, showLabels, selectedProgram, onSelectProgram }) {
  const map = useMap()
  const [zoom, setZoom] = useState(map.getZoom())
  useMapEvents({ zoomend: () => setZoom(map.getZoom()) })
  const displayedPoints = useMemo(() => clusterPoints(points, zoom), [points, zoom])
  const cityLabels = useMemo(() => zoom >= 4 ? [...points]
    .sort((left, right) => right.programs.length - left.programs.length)
    .slice(0, 22) : [], [points, zoom])

  return <>
    {showLabels && cityLabels.map((point) => (
      <Marker
        key={`label-${point.key}`}
        position={[point.latitude, point.longitude]}
        icon={cityIcon(point.city)}
        interactive={false}
      />
    ))}
    {displayedPoints.map((point) => point.type === 'cluster' ? (
      <Marker
        key={point.key}
        position={[point.latitude, point.longitude]}
        icon={clusterIcon(point.count)}
        title={`${point.count} programs in this area`}
        alt={`${point.count} programs in this area`}
        keyboard
        eventHandlers={{ click: () => map.flyTo([point.latitude, point.longitude], Math.min(zoom + 2, 6), { duration: 0.45 }) }}
      />
    ) : (
      <Marker
        key={point.key}
        position={[point.latitude, point.longitude]}
        icon={pointIcon(point.score, point.programs.length)}
        title={`${point.top.universityName}, ${point.top.programName}`}
        alt={`${point.top.universityName}, ${point.top.programName}`}
        riseOnHover
        keyboard
        eventHandlers={{ click: () => onSelectProgram(point.top) }}
      >
        <Popup closeButton={false} offset={[0, -5]}><ProgramPopup point={point} onSelectProgram={onSelectProgram} /></Popup>
      </Marker>
    ))}
    {selectedProgram && <Marker
      position={[selectedProgram.location.latitude, selectedProgram.location.longitude]}
      icon={L.divIcon({ className: 'selected-program-halo', iconSize: [72, 72], iconAnchor: [36, 36], html: '<span />' })}
      interactive={false}
    />}
  </>
}

export default function MapExplorer({ programs, showLabels, selectedProgram, onSelectProgram }) {
  const [detailedBasemap, setDetailedBasemap] = useState(true)
  const [fitSignal, setFitSignal] = useState(0)
  const points = useMemo(() => groupPrograms(programs), [programs])

  return (
    <div className="map-explorer">
      <MapContainer
        className="unirank-map"
        center={[34, 15]}
        zoom={3}
        minZoom={2}
        maxZoom={12}
        zoomControl={false}
        worldCopyJump
      >
        <TileLayer
          attribution={TILE_ATTRIBUTION}
          url={detailedBasemap ? TILE_URLS.detailed : TILE_URLS.clean}
          subdomains="abcd"
          maxZoom={19}
        />
        <CountryBorders />
        <MapViewport points={points} selectedProgram={selectedProgram} fitSignal={fitSignal} />
        <ZoomControl position="bottomright" />

        <MapMarkers points={points} showLabels={showLabels} selectedProgram={selectedProgram} onSelectProgram={onSelectProgram} />
      </MapContainer>

      <div className="map-toolbar" aria-label="Harita kontrolleri">
        <button type="button" className="map-focus" onClick={() => { onSelectProgram(null); setFitSignal((value) => value + 1) }}><Focus size={15} /> Sonuçlara odaklan</button>
        <label className="map-layer-toggle"><Layers3 size={15} /><span><strong>Yer adları</strong><small>{detailedBasemap ? 'Açık' : 'Kapalı'}</small></span><input type="checkbox" checked={detailedBasemap} onChange={(event) => setDetailedBasemap(event.target.checked)} /><i /></label>
      </div>
      <div className="map-key"><span><i className="key-dot key-dot--great" /> Güçlü uyum</span><span><i className="key-dot key-dot--good" /> İyi uyum</span><span><i className="key-dot key-dot--consider" /> Değerlendir</span><span><i className="key-cluster" /> Yakındaki programlar</span></div>
      <div className="map-decoration map-decoration--one"><Plus size={14} /></div>
      <div className="map-decoration map-decoration--two"><Minus size={14} /></div>
      <div className="map-route" aria-hidden="true"><Route size={17} /></div>
    </div>
  )
}
