import { useEffect, useMemo, useState } from 'react'
import {
  ArrowUpRight,
  BadgeCheck,
  ChevronDown,
  Compass,
  GraduationCap,
  Map as MapIcon,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Sparkles,
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

function App() {
  const initialFilters = loadSavedFilters()
  const [programs, setPrograms] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState('')
  const [search, setSearch] = useState(initialFilters.search || '')
  const [country, setCountry] = useState(initialFilters.country || 'all')
  const [englishOnly, setEnglishOnly] = useState(Boolean(initialFilters.englishOnly))
  const [showLabels, setShowLabels] = useState(initialFilters.showLabels !== false)
  const [selectedProgram, setSelectedProgram] = useState(null)

  useEffect(() => {
    // The scoring utility is shared with the existing UniRank interface.
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
            if (!program.location) return null
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
      showLabels,
    }))
  }, [search, country, englishOnly, showLabels])

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
        return (!needle || searchable.includes(needle))
          && (country === 'all' || programCountry === country)
          && (!englishOnly || /\benglish\b/.test(languages))
      })
      .sort((left, right) => (right.score ?? -1) - (left.score ?? -1))
  }, [programs, search, country, englishOnly])

  useEffect(() => {
    if (selectedProgram && !visiblePrograms.some((program) => program.key === selectedProgram.key)) {
      setSelectedProgram(null)
    }
  }, [visiblePrograms, selectedProgram])

  const mappedCities = new Set(visiblePrograms.map((program) => `${program.location.city}-${program.location.country}`)).size
  const verifiedPrograms = visiblePrograms.filter((program) => program.confidenceSummary === 'high').length

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="UniRank map explorer">
          <span className="brand-mark"><GraduationCap size={21} strokeWidth={2.7} /></span>
          <span>UniRank<small>decision lab</small></span>
        </a>
        <div className="topbar-copy">
          <span className="eyebrow"><Sparkles size={14} /> AEROSPACE &amp; SPACE</span>
          <strong>Program keşif haritası</strong>
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
            <span><strong>Şehir etiketleri</strong><small>Haritada şehir adlarını göster</small></span>
            <input checked={showLabels} onChange={(event) => setShowLabels(event.target.checked)} type="checkbox" />
            <i aria-hidden="true" />
          </label>

          <div className="filter-tip">
            <Sparkles size={18} />
            <p><strong>İpucu:</strong> Bir yer işaretine dokunarak program bilgisini aç, şehir kartından konuma odaklan.</p>
          </div>

          <button
            className="reset-button"
            type="button"
            onClick={() => { setSearch(''); setCountry('all'); setEnglishOnly(false) }}
          ><RefreshCw size={16} /> Filtreleri sıfırla</button>
        </aside>

        <section className="workspace" aria-label="Üniversite program haritası">
          <div className="workspace-heading">
            <div>
              <span className="eyebrow"><MapIcon size={14} /> ETKİLEŞİMLİ HARİTA</span>
              <h2>İyi bir program, iyi bir yerde başlar.</h2>
              <p>Ülke sınırları, şehir etiketleri ve program uygunluk sinyalleri aynı görünümde.</p>
            </div>
            <div className="live-badge"><span /> CANLI VERİ</div>
          </div>

          <div className="stats" aria-live="polite">
            <div><strong>{visiblePrograms.length}</strong><span>Haritalanan program</span></div>
            <div><strong>{mappedCities}</strong><span>Şehir</span></div>
            <div><strong>{verifiedPrograms}</strong><span>Yüksek kaynak güveni</span></div>
          </div>

          {status === 'loading' && <div className="map-state"><span className="loading-orb" /> Harita verisi hazırlanıyor…</div>}
          {status === 'error' && (
            <div className="map-state map-state--error">
              <strong>Veriye ulaşılamadı.</strong><span>{error}</span><small>API sunucusunun çalıştığından emin olun ve tekrar deneyin.</small>
            </div>
          )}
          {status === 'ready' && (
            <MapExplorer
              programs={visiblePrograms}
              showLabels={showLabels}
              selectedProgram={selectedProgram}
              onSelectProgram={setSelectedProgram}
            />
          )}
        </section>

        <aside className="results-panel" aria-label="Öne çıkan programlar">
          <div className="results-heading"><span className="eyebrow">ÖNE ÇIKANLAR</span><h2>Haritada öne çıkanlar</h2><p>Uyum skoruna göre sıralanır.</p></div>
          <div className="result-list">
            {visiblePrograms.slice(0, 6).map((program, index) => (
              <button
                className={`result-card ${selectedProgram?.key === program.key ? 'is-selected' : ''}`}
                type="button"
                key={program.key}
                onClick={() => setSelectedProgram(program)}
              >
                <span className="result-rank">{String(index + 1).padStart(2, '0')}</span>
                <span className="result-body"><strong>{text(program.universityName)}</strong><small>{text(program.programName)}</small><em>{text(program.location.city)}, {text(program.location.country)}</em></span>
                <span className={`score-pill score-pill--${scoreBand(program.score)}`}>{program.score ?? '—'}</span>
              </button>
            ))}
            {status === 'ready' && !visiblePrograms.length && <p className="empty-results">Bu filtrelerle eşleşen konumlu program bulunamadı.</p>}
          </div>
          <a className="all-results" href="#top">Tüm sonuçları listele <ArrowUpRight size={16} /></a>
          <SpotlightCard className="source-card">
            <BadgeCheck size={20} />
            <div><strong>Kaynak odaklı kararlar</strong><p>Harita skorları filtreleme için kullanılır; program ayrıntıları resmi kaynaklarla doğrulanmalıdır.</p></div>
          </SpotlightCard>
        </aside>
      </main>
    </div>
  )
}

function scoreBand(score) {
  if (score == null) return 'unknown'
  if (score >= 7) return 'great'
  if (score >= 5.5) return 'good'
  return 'consider'
}

export default App
