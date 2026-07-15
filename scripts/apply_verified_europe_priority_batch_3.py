"""Record current, scoped funding, cost and timeline evidence for three European programmes."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-07-15"

def bi(en: str, tr: str) -> dict[str, str]: return {"en": en, "tr": tr}
def log(url: str, title: str, typ: str, fields: list[str], en: str, tr: str) -> dict[str, Any]:
    return {"url": url, "title": title, "source_type": typ, "access_status": "ok", "last_checked": CHECKED, "relevant_fields": fields, "confidence": "high", "notes": bi(en, tr)}
def load(name: str) -> tuple[Path,str,Any]:
    p=ROOT/"data_base"/name; raw=p.read_text(encoding="utf8"); return p,raw,json.loads(raw)
def rows(d: Any) -> list[dict[str,Any]]: return d if isinstance(d,list) else d.get("programs",d.get("universities",[]))
def save(p: Path,raw: str,d: Any) -> None:
    nl="\r\n" if "\r\n" in raw else "\n"; p.write_text(json.dumps(d,ensure_ascii=False,indent=2).replace("\n",nl)+nl,encoding="utf8")
def get(d: Any, ident: str) -> dict[str,Any]: return next(x for x in rows(d) if x.get("id")==ident)
def add(p: dict[str,Any], x: dict[str,Any]) -> None:
    p["source_log"]=[q for q in p.get("source_log",[]) if not(isinstance(q,dict) and q.get("url")==x["url"] and q.get("source_type")==x["source_type"])]+[x]

def estaca() -> None:
    p,raw,d=load("fransa.json"); r=get(d,"france_estaca_post_master")
    funding="https://www.estaca.fr/en/international/come-to-estaca/"
    housing="https://www.estaca.fr/en/campus-life/paris-saclay/housing-dining/"
    budget="https://www.campusfrance.org/en/preparing-budget-student-France"
    r["scholarship_profile"].update({"available_types":["Eiffel scholarship route and Campus France scholarship search (eligibility depends on nationality and call)"],"regional_scholarship_available":True,"regional_scholarship_name":"Eiffel / Campus France external funding routes","non_eu_eligible":True,"scholarship_application_url":funding,"funding_notes":bi("ESTACA directs international students to the French-government Eiffel scholarship and Campus France search tool. It does not claim every Post-Master applicant is eligible or funded.","ESTACA uluslararasi ogrencileri Fransiz hukumetinin Eiffel bursuna ve Campus France arama aracina yonlendirir. Her Post-Master adayinin uygun veya fonlanmis oldugunu iddia etmez.")})
    r["living_profile"].update({"monthly_living_cost_eur_min":800,"monthly_living_cost_eur_max":1200,"average_room_rent_eur_min":450,"average_room_rent_eur_max":800,"living_risk":"high","housing_difficulty":"high","housing_notes":bi("Campus France's current national planning guidance gives EUR 800-1,200/month for Paris, while ESTACA states it has no dedicated residence and tells foreign Master students to arrange housing before arrival via its platforms. The range is Paris planning guidance, not an ESTACA rent quote.","Campus France'in guncel ulusal planlama rehberi Paris icin aylik 800-1.200 EUR verir; ESTACA ise ozel yurdu olmadigini ve yabanci Master ogrencilerinin varistan once platformlariyla konut ayarlamasini soyler. Aralik ESTACA kira teklifi degil Paris planlama rehberidir.")})
    s=r.setdefault("source_profile",{}); add(s,log(funding,"ESTACA international students and scholarships","official_scholarship_page",["scholarship","funding"],"Official ESTACA page names Eiffel and Campus France search routes without a universal eligibility claim.","Resmi ESTACA sayfasi evrensel uygunluk iddiasi olmadan Eiffel ve Campus France yollarini adlandirir.")); add(s,log(housing,"ESTACA Paris-Saclay housing guidance","official_housing_page",["housing"],"Official page says there is no dedicated residence and advises early private-market search.","Resmi sayfa ozel yurt olmadigini ve erken ozel piyasa aramasini onerir.")); add(s,log(budget,"Campus France student budget preparation","official_cost_of_living_page",["living","housing"],"Official French-government guidance supplies planning context; it is not a school-specific price.","Resmi Fransiz hukumeti rehberi planlama baglami verir; okula ozgu fiyat degildir.")); s.update({"official_scholarship_page":funding,"official_housing_page":housing,"official_cost_of_living_page":budget,"last_verified":CHECKED}); s.setdefault("field_confidence",{}).update({"scholarship":"medium","living_profile":"medium","housing":"medium"}); save(p,raw,d)

def coimbra() -> None:
    p,raw,d=load("portekiz.json"); r=get(d,"u-coimbra")
    call="https://inforestudante.uc.pt/nonio/util/downloadPublicoFicheiroEdital.do?anoLectivo=2026%2F2027&curId=13241&fichId=6636652"
    funding="https://www.uc.pt/en/academic-services/awards-scholarships-uc/"
    r["application_timeline_profile"].update({"academic_year":"2026/2027 international-student call","intake_terms":["Autumn 2026"],"application_rounds":["15 December 2025-26 January 2026","16 February-15 April 2026","20 May-17 July 2026","Extra call: 7-14 August 2026"],"non_eu_deadline":"2026-08-14 (extra international-student call; all listed 2026/27 calls passed when checked)","application_deadline":"2026-08-14 (extra call; verify future cycle)","timeline_risk":"high","deadline_notes":bi("Dates are the official 2026/27 special competition for international students in the Aerospace Engineering Bachelor's degree. They are recorded as a closed reference only.","Tarihler Aerospace Engineering lisans programi icin resmi 2026/27 uluslararasi ogrenci ozel yarismasina aittir. Yalnizca kapanmis referans olarak kaydedilir.")})
    r["scholarship_profile"].update({"available_types":["University of Coimbra international-student merit scholarships and awards (eligibility/call dependent)"],"regional_scholarship_available":True,"regional_scholarship_name":"UC International Student Awards and Scholarships","non_eu_eligible":True,"scholarship_application_url":funding,"funding_notes":bi("UC lists merit scholarships and awards regulated for international students. The page is an official availability route, not a promise that every new Aerospace applicant receives an award; each call's rules must be checked.","UC, uluslararasi ogrenciler icin duzenlenmis basari burslarini ve odullerini listeler. Sayfa resmi bir uygunluk yoludur; her yeni Aerospace adayina odul vaadi degildir ve her cagrinin kurallari kontrol edilmelidir.")})
    s=r.setdefault("source_profile",{}); add(s,log(call,"University of Coimbra 2026/27 international Aerospace Engineering call","official_admission_page",["admission","deadline","non_eu_eligibility"],"Official notice gives programme-specific rounds and dates.","Resmi duyuru programa ozgu turlari ve tarihleri verir.")); add(s,log(funding,"University of Coimbra awards and scholarships for international students","official_scholarship_page",["scholarship","funding"],"Official UC page describes its regulated international-student scholarships and awards.","Resmi UC sayfasi duzenlenmis uluslararasi ogrenci burslarini ve odullerini aciklar.")); s.update({"official_admission_page":call,"official_scholarship_page":funding,"last_verified":CHECKED}); s.setdefault("field_confidence",{}).update({"application_timeline_profile":"high","scholarship":"medium"}); save(p,raw,d)

def ulb() -> None:
    p,raw,d=load("belcika.json"); r=get(d,"ulb-brussels")
    funding="https://www.ulb.be/en/non-exchange-international-students"
    r["scholarship_profile"].update({"available_types":["ULB international-funding information and external ARES/Wallonia-Brussels scholarship routes (eligibility depends on nationality, level and project)"],"regional_scholarship_available":True,"regional_scholarship_name":"ULB international funding information / ARES and WBI routes","scholarship_application_url":funding,"funding_notes":bi("ULB directs international students to its scholarship information and to ARES and Wallonia-Brussels International routes, which depend on nationality, study level and project. This is a verified route, not a universal award or a guarantee for the BRUfACE option.","ULB, uluslararasi ogrencileri burs bilgilerine ve uyruk, egitim duzeyi ve projeye bagli ARES ile Wallonia-Brussels International yollarina yonlendirir. Bu dogrulanmis bir yoldur; evrensel odul veya BRUfACE secenegi icin garanti degildir.")})
    s=r.setdefault("source_profile",{}); add(s,log(funding,"ULB international students: scholarships and support","official_scholarship_page",["scholarship","funding"],"Official ULB page directs international students to ULB scholarship information and ARES/WBI routes with eligibility-dependent scope.","Resmi ULB sayfasi uluslararasi ogrencileri uygunluga bagli kapsamdaki ULB burs bilgisi ve ARES/WBI yollarina yonlendirir.")); s.update({"official_scholarship_page":funding,"last_verified":CHECKED}); s.setdefault("field_confidence",{})["scholarship"]="medium"; save(p,raw,d)

estaca(); coimbra(); ulb(); print("Updated ESTACA, University of Coimbra and ULB with scoped official decision evidence.")
