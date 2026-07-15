import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import {
  ArrowUpRight,
  BadgeCheck,
  Check,
  ChevronDown,
  Compass,
  GraduationCap,
  Map as MapIcon,
  MapPinned,
  Plus,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Sparkles,
  X,
} from 'lucide-react'
import { calculateScore } from './utils/scoring'
import { uniDataAdapter } from './utils/dataAdapter'
import MapExplorer from './components/MapExplorer'
import SpotlightCard from './components/SpotlightCard'
import './App.css'

const DEFAULT_WEIGHTS = {
  academic_fit: 30,
  eligibility_language: 20,
  cost_funding: 20,
  career_research: 15,
  living_risk: 10,
  confidence_deadline: 5,
}

const DEFAULT_PREFERENCES = { degreeFilter: 'All', onlyEnglish: false, maxTuition: 0 }
const MAX_COMPARE = 4

function text(value) {
  if (value == null) return ''
  if (typeof value === 'object') return value.en || value.tr || value.name || ''
  return String(value)
}

function scoreProgram(record) {
  try {
    const result = calculateScore(record, DEFAULT_PREFERENCES, DEFAULT_WEIGHTS)
    return Math.round((result.total_score / 10) * 10) / 10
  } catch {
    return null
  }
}

function loadSavedFilters() {
  try {
    return JSON.parse(localStorage.getItem('unirank-react-map-filters') || '{}')
  } catch {
    return {}
  }
}

function scoreBand(score) {
  if (score == null) return 'unknown'
  if (score >= 7) return 'great'
  if (score >= 5.5) return 'good'
  return 'consider'
}

function locationPrecision(program) {
  const level = String(program.location?.locationConfidence || '').toLowerCase()
  if (level === 'exact') return { label: 'Kampüs konumu', tone: 'exact', description: 'Koordinat kampüsü veya doğrulanmış yeri gösterir.' }
  if (level === 'city') return { label: 'Şehir seviyesi', tone: 'city', description: 'Kampüs içi konum henüz doğrulanmadı.' }
  return { label: 'Doğrulanmalı', tone: 'unknown', description: 'Konum hassasiyeti belirtilmemiş.' }
}

function distanceKm(first, second) {
  const [lat1, lon1] = [Number(first?.location?.latitude), Number(first?.location?.longitude)]
  const [lat2, lon2] = [Number(second?.location?.latitude), Number(second?.location?.longitude)]
  if (![lat1, lon1, lat2, lon2].every(Number.isFinite)) return null
  const rad = Math.PI / 180
  const deltaLat = (lat2 - lat1) * rad
  const deltaLon = (lon2 - lon1) * rad
  const a = Math.sin(deltaLat / 2) ** 2 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(deltaLon / 2) ** 2
  return Math.round(6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)))
}

function universityIdentity(program) {
  const normalized = [
    text(program.universityName),
    text(program.location?.city || program.city),
    text(program.location?.country || program.country),
  ].map((value) => value
    .trim()
    .toLocaleLowerCase('en-US')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, ''))
  return normalized.join('|')
}

function groupUniversities(programs) {
  const groups = new Map()
  programs.forEach((program) => {
    const key = universityIdentity(program)
    const current = groups.get(key) || []
    current.push(program)
    groups.set(key, current)
  })

  return Array.from(groups.entries()).map(([identity, group]) => {
    const sorted = [...group].sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
    const withCoordinates = sorted.filter((program) => program.location)
    const representative = withCoordinates.find((program) => String(program.location?.locationConfidence).toLowerCase() === 'exact')
      || withCoordinates[0]
      || sorted[0]
    const top = sorted[0]
    return {
      ...top,
      key: `university-${identity}`,
      location: representative.location || null,
      city: representative.city || top.city,
      country: representative.country || top.country,
      sourcePrograms: sorted,
      programCount: sorted.length,
    }
  }).sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
}

function App() {
  const initialFilters = loadSavedFilters()
  const [programs, setPrograms] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState('')
  const [search, setSearch] = useState(initialFilters.search || '')
  const [country, setCountry] = useState(initialFilters.country || 'all')
  const [englishOnly, setEnglishOnly] = useState(Boolean(initialFilters.englishOnly))
  const [exactOnly, setExactOnly] = useState(Boolean(initialFilters.exactOnly))
  const [showLabels, setShowLabels] = useState(initialFilters.showLabels !== false)
  const [selectedProgram, setSelectedProgram] = useState(null)
  const [comparedPrograms, setComparedPrograms] = useState([])

  useEffect(() => {
    window.uniDataAdapter = uniDataAdapter
    window.personalizationEnabled = false
  }, [])

  useEffect(() => {
    const controller = new AbortController()

    async function loadPrograms() {
      setStatus('loading')
      setError('')
      try {
        const response = await fetch('/api/universities', { signal: controller.signal })
        if (!response.ok) throw new Error(`Data request failed (${response.status})`)
        const payload = await response.json()
        if (payload.status !== 'success' || !Array.isArray(payload.data)) {
          throw new Error(payload.message || 'University data could not be loaded.')
        }

        const normalized = payload.data
          .map((record, index) => {
            const program = uniDataAdapter.normalizeUniversityRecord(record)
            return {
              ...program,
              key: `${program.id || program.universityName || 'program'}-${index}`,
              score: scoreProgram(record),
            }
          })
          .filter(Boolean)

        setPrograms(normalized)
        setStatus('ready')
      } catch (loadError) {
        if (loadError.name === 'AbortError') return
        setError(loadError.message || 'University data could not be loaded.')
        setStatus('error')
      }
    }

    loadPrograms()
    return () => controller.abort()
  }, [])

  useEffect(() => {
    localStorage.setItem('unirank-react-map-filters', JSON.stringify({
      search,
      country,
      englishOnly,
      exactOnly,
      showLabels,
    }))
  }, [search, country, englishOnly, exactOnly, showLabels])

  const countries = useMemo(() => Array.from(new Set(
    programs.map((program) => text(program.location?.country || program.country)).filter(Boolean),
  )).sort((left, right) => left.localeCompare(right)), [programs])

  const visiblePrograms = useMemo(() => {
    const needle = search.trim().toLocaleLowerCase('en-US')
    return programs
      .filter((program) => {
        const programCountry = text(program.location?.country || program.country)
        const searchable = [
          text(program.universityName),
          text(program.programName),
          text(program.location?.city || program.city),
          programCountry,
          ...(program.strongAreas || []),
        ].join(' ').toLocaleLowerCase('en-US')
        const languages = (program.teachingLanguage || []).join(' ').toLocaleLowerCase('en-US')
        const isExact = String(program.location?.locationConfidence || '').toLowerCase() === 'exact'
        return (!needle || searchable.includes(needle))
          && (country === 'all' || programCountry === country)
          && (!englishOnly || /\benglish\b/.test(languages))
          && (!exactOnly || isExact)
      })
      .sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
  }, [programs, search, country, englishOnly, exactOnly])

  const visibleUniversities = useMemo(() => groupUniversities(visiblePrograms), [visiblePrograms])
  const mappedUniversities = useMemo(() => visibleUniversities.filter((university) => university.location), [visibleUniversities])
  const unmappedUniversities = useMemo(() => visibleUniversities.filter((university) => !university.location), [visibleUniversities])

  useEffect(() => {
    if (selectedProgram && !visibleUniversities.some((university) => university.key === selectedProgram.key)) {
      setSelectedProgram(null)
    }
    setComparedPrograms((current) => current.filter((program) => visibleUniversities.some((candidate) => candidate.key === program.key)))
  }, [visibleUniversities, selectedProgram])

  const mappedCities = new Set(mappedUniversities.map((university) => `${university.location.city}-${university.location.country}`)).size
  const mappedCountries = new Set(mappedUniversities.map((university) => university.location.country || university.country).filter(Boolean)).size
  const exactLocations = mappedUniversities.filter((university) => String(university.location?.locationConfidence || '').toLowerCase() === 'exact').length

  const selectProgram = (program) => setSelectedProgram(program)
  const toggleCompare = (program) => {
    setComparedPrograms((current) => {
      if (current.some((item) => item.key === program.key)) return current.filter((item) => item.key !== program.key)
      if (current.length >= MAX_COMPARE) return current
      return [...current, program]
    })
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="UniRank konum keşfi">
          <span className="brand-mark"><GraduationCap size={21} strokeWidth={2.7} /></span>
          <span>UniRank<small>decision lab</small></span>
        </a>
        <div className="topbar-copy">
          <span className="eyebrow"><Sparkles size={14} /> AEROSPACE &amp; SPACE</span>
          <strong>Konum &amp; program keşfi</strong>
        </div>
        <button className="profile-button" type="button"><span>AY</span> Profilim <ChevronDown size={15} /></button>
      </header>

      <main id="top" className="dashboard">
        <aside className="filters" aria-label="Harita filtreleri">
          <div className="filters-heading">
            <div className="filters-icon"><SlidersHorizontal size={19} /></div>
            <div><span className="eyebrow">KEŞFİ ÖZELLEŞTİR</span><h1>Senin için filtrele</h1></div>
          </div>

          <label className="search-field">
            <Search size={18} aria-hidden="true" />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Program, üniversite veya şehir ara"
              aria-label="Program, üniversite veya şehir ara"
            />
          </label>

          <label className="filter-label" htmlFor="country-filter">Ülke</label>
          <div className="select-field">
            <Compass size={17} aria-hidden="true" />
            <select id="country-filter" value={country} onChange={(event) => setCountry(event.target.value)}>
              <option value="all">Tüm ülkeler</option>
              {countries.map((option) => <option key={option} value={option}>{option}</option>)}
            </select>
            <ChevronDown size={16} aria-hidden="true" />
          </div>

          <label className="toggle-row">
            <span><strong>Yalnızca İngilizce</strong><small>Öğretim dili İngilizce olanları göster</small></span>
            <input checked={englishOnly} onChange={(event) => setEnglishOnly(event.target.checked)} type="checkbox" />
            <i aria-hidden="true" />
          </label>

          <label className="toggle-row">
            <span><strong>Doğrulanmış kampüsler</strong><small>Yalnızca kampüs hassasiyetinde koordinatlar</small></span>
            <input checked={exactOnly} onChange={(event) => setExactOnly(event.target.checked)} type="checkbox" />
            <i aria-hidden="true" />
          </label>

          <label className="toggle-row">
            <span><strong>Şehir etiketleri</strong><small>Haritada şehir adlarını göster</small></span>
            <input checked={showLabels} onChange={(event) => setShowLabels(event.target.checked)} type="checkbox" />
            <i aria-hidden="true" />
          </label>

          <div className="filter-tip">
            <MapPinned size={18} />
            <p><strong>Konum ipucu:</strong> Kampüs konumu işaretlilerde haritayı yakınlaştırarak kampüsün şehirle ilişkisini doğrudan incele.</p>
          </div>

          <button
            className="reset-button"
            type="button"
            onClick={() => { setSearch(''); setCountry('all'); setEnglishOnly(false); setExactOnly(false) }}
          ><RefreshCw size={16} /> Filtreleri sıfırla</button>
        </aside>

        <section className="workspace" aria-label="Üniversite program haritası">
          <div className="workspace-heading">
            <div>
              <span className="eyebrow"><MapIcon size={14} /> KONUM ODAKLI KEŞİF</span>
              <h2>Üniversiteyi, bulunduğu yerle birlikte değerlendir.</h2>
              <p>Alternatifleri aynı haritada gör; kampüs ve şehir seviyesi konumları birbirinden ayır.</p>
            </div>
            <div className="live-badge"><span /> CANLI VERİ</div>
          </div>

          <div className="stats" aria-live="polite">
            <div><strong>{visibleUniversities.length}</strong><span>Üniversite</span></div>
            <div><strong>{mappedCities}</strong><span>Şehir</span></div>
            <div><strong>{exactLocations}</strong><span>Kampüs konumu</span></div>
            <div><strong>{mappedCountries}</strong><span>Ülke</span></div>
            <div className={unmappedUniversities.length ? 'stats-pending' : ''}><strong>{unmappedUniversities.length}</strong><span>Konum bekliyor</span></div>
          </div>

          {status === 'loading' && <div className="map-state"><span className="loading-orb" /> Harita verisi hazırlanıyor…</div>}
          {status === 'error' && (
            <div className="map-state map-state--error">
              <strong>Veriye ulaşılamadı.</strong><span>{error}</span><small>API sunucusunun çalıştığından emin olun ve tekrar deneyin.</small>
            </div>
          )}
          {status === 'ready' && (
            <MapExplorer
              programs={mappedUniversities}
              showLabels={showLabels}
              selectedProgram={selectedProgram}
              comparedPrograms={comparedPrograms}
              onSelectProgram={selectProgram}
              onToggleCompare={toggleCompare}
            />
          )}

          <section className="compare-deck" aria-label="Haritada karşılaştırılan programlar">
            <div className="compare-deck-heading">
              <div><span className="eyebrow"><MapPinned size={14} /> HARİTADA KIYASLA</span><h3>Konum kısa listen</h3></div>
              <span className={`compare-count ${comparedPrograms.length ? 'has-items' : ''}`}>{comparedPrograms.length}/{MAX_COMPARE}</span>
            </div>
            {!comparedPrograms.length && <p className="compare-empty">Haritadaki bir üniversiteyi veya sağdaki <strong>+ Kıyasla</strong> düğmesini seç. En fazla dört alternatifi birlikte konumlandırabilirsin.</p>}
            {!!comparedPrograms.length && <div className="compare-items">
              {comparedPrograms.map((program, index) => {
                const precision = locationPrecision(program)
                const distance = index > 0 ? distanceKm(comparedPrograms[0], program) : null
                return <article className="compare-item" key={program.key}>
                  <button className="compare-item-main" type="button" onClick={() => selectProgram(program)}>
                    <span className={`compare-index score-pill--${scoreBand(program.score)}`}>{index + 1}</span>
                    <span><strong>{text(program.universityName)}</strong><small>{text(program.location?.city)}, {text(program.location?.country)}</small></span>
                  </button>
                  <span className={`precision-chip precision-chip--${precision.tone}`}>{precision.label}</span>
                  {distance !== null && <span className="compare-distance">1. seçeneğe {distance.toLocaleString('tr-TR')} km</span>}
                  <button className="compare-remove" type="button" onClick={() => toggleCompare(program)} aria-label={`${text(program.universityName)} karşılaştırmadan çıkar`}><X size={15} /></button>
                </article>
              })}
            </div>}
            {!!comparedPrograms.length && <p className="compare-note">Haritada <b>1–{comparedPrograms.length}</b> numaralı noktalar ve aralarındaki düz mesafe gösterilir. Bu değer yolculuk süresi değildir.</p>}
          </section>
        </section>

        <aside className="results-panel" aria-label="Konum sonuçları">
          <div className="results-heading"><span className="eyebrow">KONUM LİSTESİ</span><h2>Haritadaki seçenekler</h2><p>Bir seçeneği odağa al veya kıyas listene ekle.</p></div>
          <div className="result-list">
            {mappedUniversities.slice(0, 8).map((program, index) => {
              const precision = locationPrecision(program)
              const isCompared = comparedPrograms.some((item) => item.key === program.key)
              const isFull = comparedPrograms.length >= MAX_COMPARE && !isCompared
              return <motion.article
                layout
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.22, delay: index * 0.025 }}
                className={`result-card ${selectedProgram?.key === program.key ? 'is-selected' : ''}`}
                key={program.key}
              >
                <button className="result-focus" type="button" onClick={() => selectProgram(program)}>
                  <span className="result-rank">{String(index + 1).padStart(2, '0')}</span>
                  <span className="result-body"><strong>{text(program.universityName)}</strong><small>{text(program.programName)}</small><em>{text(program.location.city)}, {text(program.location.country)}</em></span>
                  <span className={`score-pill score-pill--${scoreBand(program.score)}`}>{program.score ?? '—'}</span>
                </button>
                <footer className="result-card-footer">
                  <span className={`precision-chip precision-chip--${precision.tone}`}>{precision.label}</span>
                  <span className="program-count">{program.programCount} program</span>
                  <button className={`compare-toggle ${isCompared ? 'is-added' : ''}`} type="button" disabled={isFull} onClick={() => toggleCompare(program)}>
                    {isCompared ? <><Check size={13} /> Eklendi</> : <><Plus size={13} /> Kıyasla</>}
                  </button>
                </footer>
              </motion.article>
            })}
            {status === 'ready' && !mappedUniversities.length && <p className="empty-results">Bu filtrelerle eşleşen konumlu üniversite bulunamadı.</p>}
          </div>
          {mappedUniversities.length > 8 && <a className="all-results" href="#top">Filtrelerle sonuçları daralt <ArrowUpRight size={16} /></a>}
          {!!unmappedUniversities.length && <section className="missing-locations" aria-label="Konumu doğrulanması gereken üniversiteler">
            <div><span className="eyebrow">HARİTA KAPSAMI</span><strong>{unmappedUniversities.length} üniversitenin konumu doğrulanmalı</strong></div>
            <p>Bu üniversiteler sonuçlardan çıkarılmadı; resmi koordinat kaynağı olmadığı için haritaya tahmini bir iğne koymuyoruz.</p>
            <div className="missing-location-list">
              {unmappedUniversities.slice(0, 4).map((university) => <span key={university.key}>{text(university.universityName)}<small>{text(university.city || university.country || 'Konum bilgisi bekleniyor')}</small></span>)}
            </div>
          </section>}
          <div className="results-bento" aria-label="Konum veri rehberi">
            <div><span>KONUM VERİSİ</span><strong>Hassasiyeti gör</strong><small>“Kampüs konumu” tam nokta; “Şehir seviyesi” ise kampüs içi konum doğrulanmadığı anlamına gelir.</small></div>
            <i aria-hidden="true"><span /><span /><span /></i>
          </div>
          <SpotlightCard className="source-card">
            <BadgeCheck size={20} />
            <div><strong>Kaynak odaklı kararlar</strong><p>Konum bilgisi, program ayrıntıları ve resmi kaynaklarla birlikte değerlendirilmelidir.</p></div>
          </SpotlightCard>
        </aside>
      </main>
    </div>
  )
}

export default App
