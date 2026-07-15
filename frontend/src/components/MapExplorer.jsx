import { useEffect, useMemo, useState } from 'react'
import L from 'leaflet'
import {
  CircleMarker,
  GeoJSON,
  MapContainer,
  Marker,
  Polyline,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
  ZoomControl,
} from 'react-leaflet'
import { Focus, Map as MapIcon, MapPin, Route, Satellite, X } from 'lucide-react'
import './MapExplorer.css'

const WORLD_BORDERS_URL = 'https://cdn.jsdelivr.net/gh/johan/world.geo.json@master/countries.geo.json'
const BASEMAPS = {
  street: {
    label: 'Harita',
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
  },
  satellite: {
    label: 'Uydu',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri',
  },
}

const COUNTRY_TONES = [
  { fill: '#ffe8a8', stroke: '#cf9731', accent: '#dfaa3f' },
  { fill: '#ccebc8', stroke: '#61a46c', accent: '#55a763' },
  { fill: '#cce8f8', stroke: '#5d9cc0', accent: '#5aa4ce' },
  { fill: '#e5d5f5', stroke: '#9875b5', accent: '#9c75bd' },
  { fill: '#ffd8cf', stroke: '#ca7c69', accent: '#d88270' },
  { fill: '#cef0e8', stroke: '#55a794', accent: '#53ab99' },
  { fill: '#f7dfc4', stroke: '#c98e50', accent: '#d59652' },
  { fill: '#d9e1f6', stroke: '#778bc3', accent: '#738bc4' },
]

function countryTone(value) {
  const name = String(value || 'world')
  let hash = 0
  for (let index = 0; index < name.length; index += 1) hash = ((hash << 5) - hash) + name.charCodeAt(index)
  return COUNTRY_TONES[Math.abs(hash) % COUNTRY_TONES.length]
}

function geoCountryName(feature) {
  const properties = feature?.properties || {}
  return properties.ADMIN || properties.name || properties.NAME_EN || properties.NAME || properties.sovereignt || 'world'
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function precision(program) {
  return String(program?.location?.locationConfidence || '').toLowerCase() === 'exact' ? 'exact' : 'city'
}

function precisionLabel(program) {
  return precision(program) === 'exact' ? 'Kampüs konumu' : 'Şehir seviyesi'
}

function pointIcon(score, count, locationLevel, compareIndex) {
  const band = score == null ? 'unknown' : score >= 7 ? 'great' : score >= 5.5 ? 'good' : 'consider'
  const label = score == null ? '—' : score.toFixed(1)
  const context = locationLevel === 'exact' ? 'KAMPÜS' : 'ŞEHİR'
  const badge = compareIndex || (count > 1 ? count : '')
  return L.divIcon({
    className: 'map-point-icon',
    iconSize: [52, 62],
    iconAnchor: [26, 55],
    popupAnchor: [0, -53],
    html: `<span class="map-pin map-pin--${band} map-pin--${locationLevel}"><small>${context}</small><b>${label}</b>${badge ? `<em>${badge}</em>` : ''}</span>`,
  })
}

function cityIcon(city, country) {
  const tone = countryTone(country)
  return L.divIcon({
    className: 'city-label-icon',
    iconSize: [1, 1],
    iconAnchor: [0, 0],
    html: `<span class="city-label" style="--city-tone:${tone.accent}"><i></i>${escapeHtml(city)}</span>`,
  })
}

function clusterIcon(count, country) {
  const tone = countryTone(country)
  return L.divIcon({
    className: 'map-cluster-icon',
    iconSize: [54, 54],
    iconAnchor: [27, 27],
    html: `<span class="map-cluster" style="--cluster-tone:${tone.accent};--cluster-shadow:${tone.stroke}"><b>${count}</b><small>ÜNİVERSİTE</small></span>`,
  })
}

function dominantCountry(universities) {
  const counts = new Map()
  universities.forEach((university) => {
    const country = university.location?.country || university.country || ''
    counts.set(country, (counts.get(country) || 0) + 1)
  })
  return Array.from(counts.entries()).sort((left, right) => right[1] - left[1])[0]?.[0] || ''
}

function groupUniversitiesByCoordinate(universities) {
  const groups = new Map()
  universities.forEach((university) => {
    const latitude = Number(university.location?.latitude)
    const longitude = Number(university.location?.longitude)
    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return
    const key = `${latitude.toFixed(4)}:${longitude.toFixed(4)}`
    const current = groups.get(key) || []
    current.push(university)
    groups.set(key, current)
  })

  return Array.from(groups.entries()).map(([key, group]) => {
    const sorted = [...group].sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
    const top = sorted[0]
    return {
      key,
      latitude: Number(top.location.latitude),
      longitude: Number(top.location.longitude),
      city: top.location.city || top.city || 'Bilinmeyen şehir',
      country: top.location.country || top.country || '',
      top,
      universities: sorted,
      score: top.score,
    }
  })
}

function clusterPoints(points, zoom) {
  if (zoom >= 7) return points.map((point) => ({ ...point, type: 'point' }))

  const gridSize = zoom <= 2 ? 18 : zoom === 3 ? 10 : zoom === 4 ? 5 : zoom === 5 ? 2.5 : 1
  const clusters = new Map()
  points.forEach((point) => {
    const key = `${Math.floor((point.latitude + 90) / gridSize)}:${Math.floor((point.longitude + 180) / gridSize)}`
    const current = clusters.get(key) || []
    current.push(point)
    clusters.set(key, current)
  })

  return Array.from(clusters.entries()).map(([key, cluster]) => {
    if (cluster.length === 1) return { ...cluster[0], type: 'point' }
    const allUniversities = cluster.flatMap((point) => point.universities)
    const top = [...allUniversities].sort((left, right) => (right.score ?? -1) - (left.score ?? -1))[0]
    const totalUniversities = allUniversities.length
    return {
      key: `cluster-${key}`,
      type: 'cluster',
      latitude: cluster.reduce((sum, point) => sum + (point.latitude * point.universities.length), 0) / totalUniversities,
      longitude: cluster.reduce((sum, point) => sum + (point.longitude * point.universities.length), 0) / totalUniversities,
      universities: allUniversities,
      top,
      count: totalUniversities,
      country: dominantCountry(allUniversities),
    }
  })
}

function fitMapTo(map, positions, maxZoom, duration = 0.55) {
  if (!positions.length) return
  if (positions.length === 1) {
    map.flyTo(positions[0], maxZoom, { duration })
    return
  }
  map.flyToBounds(L.latLngBounds(positions), { padding: [60, 60], maxZoom, duration })
}

function MapViewport({ points, selectedProgram, comparedPrograms, viewRequest }) {
  const map = useMap()

  useEffect(() => {
    if (!points.length) return
    if (viewRequest.mode === 'detail' && selectedProgram?.location) {
      const zoom = precision(selectedProgram) === 'exact' ? 15 : 12
      fitMapTo(map, [[selectedProgram.location.latitude, selectedProgram.location.longitude]], zoom)
      return
    }
    if (viewRequest.mode === 'compare' && comparedPrograms.length) {
      const positions = comparedPrograms.map((program) => [program.location.latitude, program.location.longitude])
      fitMapTo(map, positions, comparedPrograms.length === 1 ? (precision(comparedPrograms[0]) === 'exact' ? 15 : 12) : 6)
      return
    }
    fitMapTo(map, points.map((point) => [point.latitude, point.longitude]), 5)
  }, [map, points, selectedProgram, comparedPrograms, viewRequest])

  return null
}

function CountryBorders() {
  const [borders, setBorders] = useState(null)
  const map = useMap()

  useEffect(() => {
    const outlinePane = map.getPane('country-outlines') || map.createPane('country-outlines')
    const fillPane = map.getPane('country-fills') || map.createPane('country-fills')
    outlinePane.style.zIndex = '370'
    fillPane.style.zIndex = '380'
    outlinePane.style.pointerEvents = 'none'
    fillPane.style.pointerEvents = 'none'

    const controller = new AbortController()
    fetch(WORLD_BORDERS_URL, { signal: controller.signal })
      .then((response) => response.ok ? response.json() : Promise.reject(new Error('Border data unavailable')))
      .then(setBorders)
      .catch(() => {})

    return () => controller.abort()
  }, [map])

  if (!borders) return null
  return <>
    <GeoJSON
      data={borders}
      pane="country-outlines"
      interactive={false}
      style={{ color: '#fffdf5', weight: 3.5, opacity: 0.72, fillOpacity: 0, lineCap: 'round', lineJoin: 'round' }}
    />
    <GeoJSON
      data={borders}
      pane="country-fills"
      interactive={false}
      style={(feature) => {
        const tone = countryTone(geoCountryName(feature))
        return {
          color: tone.stroke,
          weight: 0.9,
          opacity: 0.35,
          fillColor: tone.fill,
          fillOpacity: 0.16,
          lineCap: 'round',
          lineJoin: 'round',
        }
      }}
    />
  </>
}

function ProgramPopup({ point, comparedPrograms, onSelectProgram, onToggleCompare }) {
  const top = point.top
  const annualCost = top.totalAcademicCost ?? top.tuitionPerYear
  const isCompared = comparedPrograms.some((program) => program.key === top.key)
  const locationLevel = precision(top)

  return (
    <div className="program-popup">
      <span className="popup-place"><MapPin size={13} /> {point.city}, {point.country}</span>
      <div className={`popup-precision popup-precision--${locationLevel}`}>{precisionLabel(top)}</div>
      <h3>{top.universityName}</h3>
      <p>{top.programName}</p>
      <div className="popup-meta">
        <span><b>{top.score ?? '—'}</b> uyum</span>
        <span>{annualCost == null ? 'Ücret bilinmiyor' : `€${Number(annualCost).toLocaleString('tr-TR')}/yıl`}</span>
      </div>
      {locationLevel === 'city' && <small className="popup-location-note">Kampüs içi konum doğrulanmadı; şehir bağlamını inceleyebilirsin.</small>}
      {top.programCount > 1 && <small className="popup-count">Bu üniversitede {top.programCount} program kaydı</small>}
      {point.universities.length > 1 && <small className="popup-count">Aynı koordinatta {point.universities.length} üniversite</small>}
      <div className="popup-actions">
        <button type="button" onClick={() => onSelectProgram(top)}>Yakın çevreyi gör</button>
        <button className="popup-compare" type="button" onClick={() => onToggleCompare(top)}>{isCompared ? 'Listeden çıkar' : 'Kıyasla'}</button>
      </div>
    </div>
  )
}

function ComparisonRoute({ comparedPrograms }) {
  const positions = comparedPrograms.map((program) => [program.location.latitude, program.location.longitude])
  if (positions.length < 2) return null
  return <Polyline positions={positions} pathOptions={{ color: '#213c55', weight: 2.5, opacity: 0.74, dashArray: '8 9', lineCap: 'round' }} />
}

function MapMarkers({ points, showLabels, selectedProgram, comparedPrograms, onSelectProgram, onToggleCompare }) {
  const map = useMap()
  const [zoom, setZoom] = useState(map.getZoom())
  useMapEvents({ zoomend: () => setZoom(map.getZoom()) })
  const displayedPoints = useMemo(() => clusterPoints(points, zoom), [points, zoom])
  const cityLabels = useMemo(() => zoom >= 6 ? [...points]
    .sort((left, right) => right.universities.length - left.universities.length)
    .slice(0, 22) : [], [points, zoom])

  return <>
    <ComparisonRoute comparedPrograms={comparedPrograms} />
    {zoom >= 6 && points.map((point) => {
      const tone = countryTone(point.country)
      return <CircleMarker
        key={`zone-${point.key}`}
        center={[point.latitude, point.longitude]}
        radius={Math.min(24, 9 + (point.universities.length * 3))}
        pathOptions={{ color: tone.accent, weight: 1.2, opacity: 0.46, fillColor: tone.fill, fillOpacity: 0.25 }}
        interactive={false}
      />
    })}
    {showLabels && cityLabels.map((point) => (
      <Marker
        key={`label-${point.key}`}
        position={[point.latitude, point.longitude]}
        icon={cityIcon(point.city, point.country)}
        interactive={false}
      />
    ))}
    {displayedPoints.map((point) => point.type === 'cluster' ? (
      <Marker
        key={point.key}
        position={[point.latitude, point.longitude]}
        icon={clusterIcon(point.count, point.country)}
        title={`${point.count} üniversite bu alanda`}
        alt={`${point.count} üniversite bu alanda`}
        keyboard
        eventHandlers={{ click: () => map.flyTo([point.latitude, point.longitude], Math.min(zoom + 2, 6), { duration: 0.45 }) }}
      />
    ) : (() => {
      const compareIndex = point.universities.reduce((index, university) => index || (comparedPrograms.findIndex((candidate) => candidate.key === university.key) + 1), 0)
      return <Marker
        key={point.key}
        position={[point.latitude, point.longitude]}
        icon={pointIcon(point.score, point.universities.length, precision(point.top), compareIndex)}
        title={`${point.top.universityName}, ${point.top.programName}`}
        alt={`${point.top.universityName}, ${point.top.programName}`}
        riseOnHover
        keyboard
        eventHandlers={{ click: () => onSelectProgram(point.top) }}
      >
        <Popup closeButton={false} offset={[0, -5]}><ProgramPopup point={point} comparedPrograms={comparedPrograms} onSelectProgram={onSelectProgram} onToggleCompare={onToggleCompare} /></Popup>
      </Marker>
    })())}
    {selectedProgram && <Marker
      position={[selectedProgram.location.latitude, selectedProgram.location.longitude]}
      icon={L.divIcon({ className: 'selected-program-halo', iconSize: [76, 76], iconAnchor: [38, 38], html: '<span />' })}
      interactive={false}
    />}
  </>
}

export default function MapExplorer({ programs, showLabels, selectedProgram, comparedPrograms, onSelectProgram, onToggleCompare }) {
  const [basemap, setBasemap] = useState('street')
  const [viewRequest, setViewRequest] = useState({ mode: 'all', id: 0 })
  const points = useMemo(() => groupUniversitiesByCoordinate(programs), [programs])

  useEffect(() => {
    if (selectedProgram) setViewRequest((current) => ({ mode: 'detail', id: current.id + 1 }))
  }, [selectedProgram])

  const focusAll = () => {
    onSelectProgram(null)
    setViewRequest((current) => ({ mode: 'all', id: current.id + 1 }))
  }
  const focusCompared = () => setViewRequest((current) => ({ mode: 'compare', id: current.id + 1 }))
  const selectedPrecision = selectedProgram ? precision(selectedProgram) : null

  return (
    <div className="map-explorer">
      <MapContainer
        className={`unirank-map unirank-map--${basemap}`}
        center={[34, 15]}
        zoom={3}
        minZoom={2}
        maxZoom={18}
        zoomControl={false}
        worldCopyJump
      >
        <TileLayer
          key={basemap}
          attribution={BASEMAPS[basemap].attribution}
          url={BASEMAPS[basemap].url}
          subdomains="abcd"
          maxZoom={19}
        />
        {basemap === 'street' && <CountryBorders />}
        <MapViewport points={points} selectedProgram={selectedProgram} comparedPrograms={comparedPrograms} viewRequest={viewRequest} />
        <ZoomControl position="bottomright" />
        <MapMarkers points={points} showLabels={showLabels} selectedProgram={selectedProgram} comparedPrograms={comparedPrograms} onSelectProgram={onSelectProgram} onToggleCompare={onToggleCompare} />
      </MapContainer>

      <div className="map-reading-card">
        <span><MapPin size={17} /></span>
        <div><small>KONUM OKUMASI</small><strong>İğneye dokun, sonra çevreyi incele.</strong></div>
      </div>
      <div className="map-toolbar" aria-label="Harita kontrolleri">
        <div className="basemap-toggle" aria-label="Harita katmanı">
          <button className={basemap === 'street' ? 'is-active' : ''} type="button" onClick={() => setBasemap('street')}><MapIcon size={14} /> Harita</button>
          <button className={basemap === 'satellite' ? 'is-active' : ''} type="button" onClick={() => setBasemap('satellite')}><Satellite size={14} /> Uydu</button>
        </div>
        <button type="button" className="map-focus" onClick={focusAll}><Focus size={15} /> Tüm sonuçlar</button>
        <button type="button" className="map-compare-focus" disabled={comparedPrograms.length === 0} onClick={focusCompared}><Route size={15} /> Kıyaslamaya odaklan</button>
      </div>
      {selectedProgram && <div className="map-selection-card">
        <button type="button" onClick={() => onSelectProgram(null)} aria-label="Konum kartını kapat"><X size={14} /></button>
        <span className={`selection-marker selection-marker--${selectedPrecision}`}><MapPin size={15} /></span>
        <div><small>{precisionLabel(selectedProgram)}</small><strong>{selectedProgram.universityName}</strong><em>{selectedProgram.location.city}, {selectedProgram.location.country}</em></div>
      </div>}
      <div className="map-key"><span><i className="key-exact" /> Kampüs konumu</span><span><i className="key-city" /> Şehir seviyesi</span><span><i className="key-route" /> Kıyas mesafesi</span></div>
    </div>
  )
}
