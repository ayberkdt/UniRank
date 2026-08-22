(function () {
    "use strict";

    const $ = (selector) => document.querySelector(selector);
    const currentLanguage = () => (["en", "tr"].includes(window.currentLanguage) ? window.currentLanguage : "en");
    const localized = (value, language = currentLanguage()) => {
        if (value == null) return "";
        if (typeof value === "string") return value;
        return value[language] || value.en || value.tr || "";
    };
    const escapeHtml = (value) => String(value ?? "").replace(/[&<>'"]/g, (character) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
    })[character]);

    const copy = {
        en: {
            programmes: "Programmes", calendar: "Application calendar", scholarships: "Scholarships", researchFit: "Research fit",
            heroKicker: "Türkiye → world funding map", heroTitle: "Build the funding plan before the application rush.",
            heroText: "Compare who can apply, what is covered, exact or reference deadlines, required documents and the official route—without treating last year's call as a current deadline.",
            browse: "Browse scholarships", backPrograms: "Back to programmes", calendarKicker: "Deadline runway",
            calendarTitle: "What happens next?", calendarText: "Confirmed dates use live countdowns. Previous calls are visibly marked as reference only.",
            legendOpen: "Open / current", legendWatch: "Date to confirm", legendReference: "Previous-cycle reference",
            resultsKicker: "Verified opportunity library", resultsTitle: "Scholarships you can realistically investigate",
            searchPlaceholder: "Search scholarship, country, condition or document", levelLabel: "Level", allLevels: "All levels",
            master: "Master", phd: "PhD", research: "Research", statusLabel: "Cycle status", allStatuses: "All statuses", openStatus: "Open / current",
            awaitingStatus: "Awaiting publication", closedStatus: "Closed current cycle", conditionalStatus: "Needs route confirmation",
            fitLabel: "Aerospace fit", allFits: "All relevance", highFit: "High / STEM", lowFit: "Special-purpose",
            mismatchKicker: "Avoid false leads", mismatchTitle: "Frequently confused, but currently not available to Turkish citizens",
            mismatchText: "Country eligibility can change. These exclusions reflect the latest official call checked on 22 August 2026.",
            footerPolicy: "No guessed deadlines. Every critical field links to an official source.",
            nextDeadline: "Next confirmed deadline", currentCycle: "2027/28 current cycle", closesIn: (days) => `${days} days left`,
            closesToday: "Closes today", deadlinePassed: "Current cycle closed", noFutureExact: "No future exact deadline published",
            noFutureExactBody: "Watch the yellow cards below; they will switch to a confirmed countdown when an official call is released.",
            routes: "researched routes", verifiedEligible: "verified for Türkiye", liveDeadlines: "future exact dates", officialSources: "official sources",
            exactDeadline: "Confirmed deadline", previousReference: "Previous-cycle reference", programmeSpecific: "Programme-specific timing",
            notPublished: "2027/28 exact date not published", routeConfirmation: "Country route must be confirmed", currentClosed: "2027/28 cycle closed",
            open: "Open", awaiting: "Awaiting call", closed: "Closed", conditional: "Confirm route", typicalWindow: "Typical window",
            coverage: "What it covers", requirements: "Key conditions", details: "Documents & official sources", documents: "Required documents",
            sources: "Official sources", source: "Official source", confidence: "Source confidence", risk: "Watch point", daysAgo: (days) => `Closed ${days} days ago`,
            remaining: (days) => `${days} days remaining`, results: (shown, total) => `${shown} of ${total} routes shown`,
            noResults: "No scholarship matches these filters. Try clearing one filter.", lastVerified: "Research verified",
            previousCycleWarning: "Reference only — not the 2027/28 deadline", noCentralChecklist: "Use the programme-specific official checklist.",
            updatedAutomatically: "Countdown updates automatically from today's date.", levels: { bachelor: "Bachelor", master: "Master", phd: "PhD", research: "Research", partial_study: "Partial study", postgraduate: "Postgraduate", graduate_study: "Graduate study" }
        },
        tr: {
            programmes: "Programlar", calendar: "Başvuru takvimi", scholarships: "Burslar", researchFit: "Araştırma uyumu",
            heroKicker: "Türkiye → dünya burs haritası", heroTitle: "Başvuru yoğunluğu başlamadan burs planını kur.",
            heroText: "Kimlerin başvurabileceğini, kapsamı, kesin veya referans tarihleri, gerekli belgeleri ve resmî başvuru yolunu karşılaştır; geçen yılın çağrısını güncel son tarih sanma.",
            browse: "Bursları incele", backPrograms: "Programlara dön", calendarKicker: "Son tarih rotası",
            calendarTitle: "Sırada ne var?", calendarText: "Doğrulanmış tarihler canlı geri sayım kullanır. Eski çağrılar yalnızca referans olarak açıkça işaretlenir.",
            legendOpen: "Açık / güncel", legendWatch: "Tarih doğrulanacak", legendReference: "Önceki dönem referansı",
            resultsKicker: "Doğrulanmış fırsat kütüphanesi", resultsTitle: "Gerçekçi biçimde inceleyebileceğin burslar",
            searchPlaceholder: "Burs, ülke, şart veya belge ara", levelLabel: "Seviye", allLevels: "Tüm seviyeler",
            master: "Yüksek lisans", phd: "Doktora", research: "Araştırma", statusLabel: "Dönem durumu", allStatuses: "Tüm durumlar", openStatus: "Açık / güncel",
            awaitingStatus: "Yayın bekleniyor", closedStatus: "Güncel dönem kapandı", conditionalStatus: "Başvuru yolu doğrulanmalı",
            fitLabel: "Havacılık-uzay uyumu", allFits: "Tüm uygunluklar", highFit: "Yüksek / STEM", lowFit: "Özel amaçlı",
            mismatchKicker: "Yanlış rotaları ele", mismatchTitle: "Sık karıştırılan ancak şu anda Türk vatandaşlarına açık olmayanlar",
            mismatchText: "Ülke uygunluğu değişebilir. Bu dışlamalar 22 Ağustos 2026'da kontrol edilen son resmî çağrıyı yansıtır.",
            footerPolicy: "Tahminî son tarih yok. Her kritik alan resmî kaynağa bağlıdır.",
            nextDeadline: "Sıradaki doğrulanmış son tarih", currentCycle: "2027/28 güncel dönemi", closesIn: (days) => `${days} gün kaldı`,
            closesToday: "Bugün kapanıyor", deadlinePassed: "Güncel dönem kapandı", noFutureExact: "Gelecekteki kesin tarih henüz yayımlanmadı",
            noFutureExactBody: "Aşağıdaki sarı kartları takip et; resmî çağrı çıktığında doğrulanmış geri sayıma dönüşürler.",
            routes: "araştırılmış burs rotası", verifiedEligible: "Türkiye için doğrulanmış", liveDeadlines: "gelecekteki kesin tarih", officialSources: "resmî kaynak",
            exactDeadline: "Doğrulanmış son tarih", previousReference: "Önceki dönem referansı", programmeSpecific: "Programa özel takvim",
            notPublished: "2027/28 kesin tarihi yayımlanmadı", routeConfirmation: "Ülke rotası doğrulanmalı", currentClosed: "2027/28 dönemi kapandı",
            open: "Açık", awaiting: "Çağrı bekleniyor", closed: "Kapandı", conditional: "Rotayı doğrula", typicalWindow: "Tipik dönem",
            coverage: "Neleri karşılıyor", requirements: "Temel şartlar", details: "Belgeler ve resmî kaynaklar", documents: "İstenen belgeler",
            sources: "Resmî kaynaklar", source: "Resmî kaynak", confidence: "Kaynak güveni", risk: "Dikkat noktası", daysAgo: (days) => `${days} gün önce kapandı`,
            remaining: (days) => `${days} gün kaldı`, results: (shown, total) => `${total} rotanın ${shown} tanesi gösteriliyor`,
            noResults: "Bu filtrelerle eşleşen burs yok. Bir filtreyi temizlemeyi dene.", lastVerified: "Araştırma doğrulama tarihi",
            previousCycleWarning: "Yalnızca referans — 2027/28 son tarihi değildir", noCentralChecklist: "Programa özel resmî belge listesini kullan.",
            updatedAutomatically: "Geri sayım bugünün tarihine göre otomatik güncellenir.", levels: { bachelor: "Lisans", master: "Yüksek lisans", phd: "Doktora", research: "Araştırma", partial_study: "Kısmi öğrenim", postgraduate: "Lisansüstü", graduate_study: "Lisansüstü eğitim" }
        }
    };

    const accents = { GB: "#8fa8e8", US: "#ef8675", EU: "#51c8b3", HU: "#d7c765", IT: "#58b99b", FR: "#7799ef", TR: "#f18046", DE: "#d7c765" };
    const state = { catalog: null, query: "", level: "all", status: "all", fit: "all" };
    const today = () => { const date = new Date(); return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 12); };
    const parseDate = (iso) => iso ? new Date(`${iso}T12:00:00`) : null;
    const dayDistance = (iso) => Math.ceil((parseDate(iso) - today()) / 86400000);
    const formatDate = (iso, language = currentLanguage()) => parseDate(iso)?.toLocaleDateString(language === "tr" ? "tr-TR" : "en-GB", { day: "numeric", month: "long", year: "numeric" }) || "";
    const statusOf = (item) => ({
        open: "open", closed_current_cycle: "closed", awaiting_publication: "awaiting", programme_calls_pending: "awaiting",
        published_country_deadline_required: "conditional"
    })[item.cycle.status] || "awaiting";
    const statusLabel = (status, c) => c[status] || c.awaiting;
    const languageText = (value) => escapeHtml(localized(value));
    const list = (items, limit) => (items || []).slice(0, limit).map((item) => `<li>${languageText(item)}</li>`).join("");

    function applyCopy() {
        const language = currentLanguage();
        const c = copy[language];
        document.documentElement.lang = language;
        document.querySelectorAll("[data-copy]").forEach((element) => {
            const value = c[element.dataset.copy];
            if (typeof value === "string") element.textContent = value;
        });
        document.querySelectorAll("[data-placeholder]").forEach((element) => {
            element.placeholder = c[element.dataset.placeholder] || "";
        });
        if (typeof window.updateLanguageToggleUI === "function") window.updateLanguageToggleUI();
    }

    function deadlineModel(item, c) {
        const cycle = item.cycle;
        if (cycle.deadline) {
            const days = dayDistance(cycle.deadline);
            const label = cycle.status === "closed_current_cycle" ? c.currentClosed : c.exactDeadline;
            const countdown = days > 0 ? c.remaining(days) : days === 0 ? c.closesToday : c.daysAgo(Math.abs(days));
            return { kind: cycle.status === "open" && days >= 0 ? "open" : "reference", label, date: formatDate(cycle.deadline), iso: cycle.deadline, note: cycle.deadline_time || "", countdown };
        }
        if (cycle.reference_deadline) {
            return { kind: "reference", label: c.previousReference, date: formatDate(cycle.reference_deadline), iso: cycle.reference_deadline, note: `${cycle.reference_academic_year || ""} · ${c.previousCycleWarning}`, countdown: c.notPublished };
        }
        const typical = localized(cycle.typical_window);
        return { kind: "watch", label: cycle.status === "published_country_deadline_required" ? c.routeConfirmation : (typical ? c.programmeSpecific : c.notPublished), date: typical || c.notPublished, iso: "", note: cycle.academic_year || "2027/2028", countdown: cycle.status === "published_country_deadline_required" ? c.conditional : c.awaiting };
    }

    function renderNext() {
        const language = currentLanguage();
        const c = copy[language];
        const future = state.catalog.scholarships.filter((item) => item.cycle.deadline && dayDistance(item.cycle.deadline) >= 0 && statusOf(item) === "open").sort((a, b) => a.cycle.deadline.localeCompare(b.cycle.deadline))[0];
        const panel = $("#funding-next");
        if (!future) {
            panel.innerHTML = `<span>${escapeHtml(c.nextDeadline)}</span><h2>${escapeHtml(c.noFutureExact)}</h2><p>${escapeHtml(c.noFutureExactBody)}</p>`;
            return;
        }
        const days = dayDistance(future.cycle.deadline);
        panel.innerHTML = `<span>${escapeHtml(c.nextDeadline)}</span><h2>${languageText(future.name)}</h2><p>${escapeHtml(c.currentCycle)}</p><time datetime="${future.cycle.deadline}">${escapeHtml(formatDate(future.cycle.deadline, language))}</time><b>${escapeHtml(days === 0 ? c.closesToday : c.closesIn(days))}</b><small>${escapeHtml(c.updatedAutomatically)}</small>`;
    }

    function renderStats() {
        const c = copy[currentLanguage()];
        const items = state.catalog.scholarships;
        const verified = items.filter((item) => item.turkish_applicant_status.startsWith("verified_eligible")).length;
        const future = items.filter((item) => item.cycle.deadline && dayDistance(item.cycle.deadline) >= 0).length;
        const sources = items.reduce((sum, item) => sum + (item.source_profile.sources || []).length, 0);
        const values = [[items.length, c.routes], [verified, c.verifiedEligible], [future, c.liveDeadlines], [sources, c.officialSources]];
        $("#funding-stats").innerHTML = values.map(([value, label], index) => `<div class="funding-stat"><span>0${index + 1}</span><strong>${value}</strong><small>${escapeHtml(label)}</small></div>`).join("");
    }

    function renderCalendar() {
        const c = copy[currentLanguage()];
        const ordered = [...state.catalog.scholarships].sort((a, b) => {
            const aDate = a.cycle.deadline || a.cycle.reference_deadline || "9999";
            const bDate = b.cycle.deadline || b.cycle.reference_deadline || "9999";
            const aWeight = a.cycle.deadline && dayDistance(a.cycle.deadline) >= 0 ? 0 : a.cycle.reference_deadline ? 2 : 1;
            const bWeight = b.cycle.deadline && dayDistance(b.cycle.deadline) >= 0 ? 0 : b.cycle.reference_deadline ? 2 : 1;
            return aWeight - bWeight || aDate.localeCompare(bDate);
        });
        $("#funding-calendar-track").innerHTML = ordered.map((item) => {
            const deadline = deadlineModel(item, c);
            const time = deadline.iso ? `<time datetime="${deadline.iso}">${escapeHtml(deadline.date)}</time>` : `<time>${escapeHtml(deadline.date)}</time>`;
            return `<article class="funding-date-card funding-date-card--${deadline.kind}"><div class="funding-date-card__top"><span>${escapeHtml(item.destination.flag)}</span><span class="funding-date-card__status">${escapeHtml(deadline.label)}</span></div><h3>${languageText(item.name)}</h3><p>${languageText(item.destination)}</p>${time}<b>${escapeHtml(deadline.countdown)}</b><small>${escapeHtml(deadline.note)}</small></article>`;
        }).join("");
    }

    function searchableText(item) {
        const language = currentLanguage();
        return [localized(item.name, language), localized(item.provider, language), localized(item.destination, language), ...(item.coverage || []).map((x) => localized(x, language)), ...(item.requirements || []).map((x) => localized(x, language)), ...(item.required_documents || []).map((x) => localized(x, language))].join(" ").toLocaleLowerCase(language === "tr" ? "tr-TR" : "en-US");
    }

    function matches(item) {
        const query = state.query.trim().toLocaleLowerCase(currentLanguage() === "tr" ? "tr-TR" : "en-US");
        const levelMatch = state.level === "all" || item.levels.includes(state.level) || (state.level === "master" && item.levels.some((level) => ["postgraduate", "graduate_study"].includes(level)));
        return (!query || searchableText(item).includes(query)) && levelMatch && (state.status === "all" || statusOf(item) === state.status) && (state.fit === "all" || item.aerospace_relevance === state.fit);
    }

    function renderCard(item) {
        const c = copy[currentLanguage()];
        const status = statusOf(item);
        const deadline = deadlineModel(item, c);
        const levels = item.levels.map((level) => `<span>${escapeHtml(c.levels[level] || level)}</span>`).join("");
        const deadlineTime = deadline.iso ? `<time datetime="${deadline.iso}">${escapeHtml(deadline.date)}</time>` : `<time>${escapeHtml(deadline.date)}</time>`;
        const documents = item.required_documents?.length ? `<ol>${list(item.required_documents)}</ol>` : `<p class="scholarship-detail__note">${languageText(item.documents_note || c.noCentralChecklist)}</p>`;
        const sources = (item.source_profile.sources || []).map((source) => `<a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)} <span aria-hidden="true">↗</span></a>`).join("");
        const risk = item.risk_notes?.length ? `<p class="scholarship-card__risk"><strong>${escapeHtml(c.risk)}:</strong> ${languageText(item.risk_notes[0])}</p>` : "";
        return `<article class="scholarship-card" style="--country-accent:${accents[item.destination.code] || "#8fa8e8"}">
            <header class="scholarship-card__header"><span class="scholarship-card__flag" aria-hidden="true">${escapeHtml(item.destination.flag)}</span><div><h3>${languageText(item.name)}</h3><p>${languageText(item.provider)} · ${languageText(item.destination)}</p></div><span class="scholarship-status scholarship-status--${status}">${escapeHtml(statusLabel(status, c))}</span></header>
            <div class="scholarship-card__route">${levels}<span>${escapeHtml(item.cycle.academic_year || "")}</span></div>
            <div class="scholarship-card__deadline"><div><span>${escapeHtml(deadline.label)}</span>${deadlineTime}<small>${escapeHtml(deadline.note)}</small></div><b>${escapeHtml(deadline.countdown)}</b></div>
            <div class="scholarship-card__body"><section><h4>${escapeHtml(c.coverage)}</h4><ul>${list(item.coverage, 3)}</ul></section><section><h4>${escapeHtml(c.requirements)}</h4><ul>${list(item.requirements, 3)}</ul></section></div>
            ${risk}<details><summary><span>${escapeHtml(c.details)}</span><span aria-hidden="true">⌄</span></summary><div class="scholarship-detail"><section><h4>${escapeHtml(c.documents)}</h4>${documents}</section><section><h4>${escapeHtml(c.sources)}</h4><div class="scholarship-sources">${sources}</div></section><span class="scholarship-confidence">${escapeHtml(c.confidence)}: ${escapeHtml(item.source_profile.confidence)} · ${escapeHtml(c.lastVerified)} ${escapeHtml(item.source_profile.last_verified)}</span></div></details>
        </article>`;
    }

    function renderResults() {
        const c = copy[currentLanguage()];
        const all = state.catalog.scholarships;
        const filtered = all.filter(matches);
        $("#results-meta").textContent = c.results(filtered.length, all.length);
        $("#scholarship-grid").innerHTML = filtered.length ? filtered.map(renderCard).join("") : `<div class="scholarship-empty"><p>${escapeHtml(c.noResults)}</p></div>`;
    }

    function renderMismatches() {
        const c = copy[currentLanguage()];
        $("#mismatch-grid").innerHTML = state.catalog.common_mismatches.map((item) => `<article class="mismatch-card"><span aria-hidden="true">×</span><div><h3>${languageText(item.name)}</h3><p>${languageText(item.reason)}</p></div><a href="${escapeHtml(item.source.url)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(c.source)}">↗</a></article>`).join("");
        $("#last-verified").textContent = `${c.lastVerified}: ${state.catalog.last_verified}`;
    }

    function render() {
        if (!state.catalog) return;
        applyCopy();
        renderNext(); renderStats(); renderCalendar(); renderResults(); renderMismatches();
    }

    function bindFilters() {
        const bindings = [["#scholarship-search", "query", "input"], ["#level-filter", "level", "change"], ["#status-filter", "status", "change"], ["#fit-filter", "fit", "change"]];
        bindings.forEach(([selector, key, event]) => $(selector).addEventListener(event, (input) => { state[key] = input.target.value; renderResults(); }));
        $("#open-main-calendar").addEventListener("click", () => { window.location.href = "index.html?calendar=open"; });
        document.addEventListener("languageChanged", render);
    }

    async function init() {
        applyCopy(); bindFilters();
        try {
            const response = await fetch("/api/scholarships", { cache: "no-store" });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const payload = await response.json();
            state.catalog = payload.data || payload;
            render();
        } catch (error) {
            $("#scholarship-grid").innerHTML = `<div class="scholarship-empty"><p>Scholarship data could not be loaded: ${escapeHtml(error.message)}</p></div>`;
        }
    }

    init();
    window.setInterval(() => { if (state.catalog) { renderNext(); renderCalendar(); renderResults(); } }, 60000);
})();
