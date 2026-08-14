"""Check accessibility of every unique active-catalogue source URL.

This is a transport/access audit, not a semantic proof that a page supports a
claim. It never updates research records automatically. The JSON report can be
reviewed before source statuses are changed.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
SCOPE = json.loads((ROOT / "config" / "catalog_scope.json").read_text(encoding="utf-8"))
ALIASES = SCOPE.get("country_aliases") or {}
EXCLUDED = {ALIASES.get(value, value) for value in SCOPE.get("excluded_countries", [])}
# Some university WAFs reject bespoke bot tokens even for a single bounded GET.
# A browser-compatible identifier avoids false ``blocked`` results while the
# Range header and small response read keep the audit lightweight.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def ssl_context() -> ssl.SSLContext:
    """Return a verifier that also sees the Windows certificate stores.

    The bundled workspace Python can have a smaller OpenSSL trust bundle than
    Windows itself.  Without importing the OS stores, valid university sites
    that open in the browser and ``curl.exe`` are falsely reported as broken.
    """
    context = ssl.create_default_context()
    if not hasattr(ssl, "enum_certificates"):
        return context
    certificates: list[str] = []
    for store in ("ROOT", "CA"):
        try:
            entries = ssl.enum_certificates(store)
        except OSError:
            continue
        for certificate, encoding, _trust in entries:
            if encoding == "x509_asn":
                certificates.append(ssl.DER_cert_to_PEM_cert(certificate))
    if certificates:
        context.load_verify_locations(cadata="".join(certificates))
    return context


SSL_CONTEXT = ssl_context()


def windows_curl_check(url: str, timeout: float) -> dict[str, Any] | None:
    """Use Windows Schannel only when bundled Python cannot build the TLS chain."""
    if os.name != "nt":
        return None
    marker = "__UNIRANK_CURL_RESULT__"
    try:
        completed = subprocess.run(
            [
                "curl.exe",
                "--silent",
                "--show-error",
                "--head",
                "--location",
                "--max-time",
                str(max(1, int(timeout))),
                "--user-agent",
                USER_AGENT,
                "--write-out",
                f"\n{marker}%{{http_code}}|%{{content_type}}|%{{url_effective}}",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0 or marker not in completed.stdout:
        return None
    payload = completed.stdout.rsplit(marker, 1)[1].strip()
    parts = payload.split("|", 2)
    if len(parts) != 3 or not parts[0].isdigit():
        return None
    status_code = int(parts[0])
    content_type = parts[1]
    final_url = parts[2] or url
    redirected = final_url.rstrip("/") != url.rstrip("/")
    return {
        "url": url,
        "final_url": final_url,
        "status_code": status_code,
        "content_type": content_type,
        "access_status": classify(status_code, content_type, redirected, None),
        "redirected": redirected,
        "error": None,
        "checked_at": date.today().isoformat(),
        "transport_note": "Python TLS chain failed; verified with Windows Schannel via curl.exe.",
    }


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("programs", "universities"):
            if isinstance(payload.get(key), list):
                return [row for row in payload[key] if isinstance(row, dict)]
    return []


def display(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("en") or value.get("tr") or ""
    return str(value or "").strip()


def record_country(record: dict[str, Any]) -> str:
    value = display(record.get("country") or record.get("Country"))
    return ALIASES.get(value, value)


def classify(status_code: int | None, content_type: str, redirected: bool, error: str | None) -> str:
    if status_code in {404, 410}:
        return "not_found"
    if status_code in {401, 403, 406, 409, 423, 429}:
        return "blocked"
    if status_code is not None and 200 <= status_code < 400:
        if "pdf" in content_type.lower():
            return "pdf"
        return "redirects" if redirected else "ok"
    if status_code is not None and status_code >= 500:
        return "blocked"
    if error:
        return "broken"
    return "unknown"


def check(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.5",
            "Range": "bytes=0-32767",
        },
        method="GET",
    )
    status_code = None
    content_type = ""
    final_url = url
    error = None
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            status_code = response.getcode()
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            response.read(1024)
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        final_url = exc.geturl() or url
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        error = f"HTTP {exc.code}"
    except Exception as exc:  # network/TLS/DNS errors are report data
        error = f"{type(exc).__name__}: {exc}"

    if error and "CERTIFICATE_VERIFY_FAILED" in error:
        fallback = windows_curl_check(url, timeout)
        if fallback is not None:
            return fallback

    redirected = final_url.rstrip("/") != url.rstrip("/")
    return {
        "url": url,
        "final_url": final_url,
        "status_code": status_code,
        "content_type": content_type,
        "access_status": classify(status_code, content_type, redirected, error),
        "redirected": redirected,
        "error": error,
        "checked_at": date.today().isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--url", action="append", default=[], help="Check only this exact stored source URL; repeatable.")
    parser.add_argument(
        "--record-id",
        action="append",
        default=[],
        help="Check only URLs used by this exact record id; repeatable.",
    )
    parser.add_argument(
        "--include-research-queue",
        action="store_true",
        help="Also include official candidate and exclusion sources from research_queue/program_candidates_v2.json.",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    usage: dict[str, list[dict[str, str]]] = defaultdict(list)
    stored_statuses: dict[str, set[str]] = defaultdict(set)
    for path in sorted(DATA.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for record in rows(payload):
            if record_country(record) in EXCLUDED:
                continue
            record_id = str(record.get("id") or record.get("Uni_ID") or "unknown")
            for source in (record.get("source_profile") or {}).get("source_log") or []:
                if not isinstance(source, dict) or not display(source.get("url")):
                    continue
                url = display(source["url"])
                usage[url].append({
                    "file": path.name,
                    "record_id": record_id,
                    "source_type": display(source.get("source_type")),
                })
                stored_statuses[url].add(display(source.get("access_status")))

    if args.include_research_queue:
        queue_path = ROOT / "research_queue" / "program_candidates_v2.json"
        queue = json.loads(queue_path.read_text(encoding="utf-8-sig"))
        for candidate in queue.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            candidate_id = display(candidate.get("candidate_id")) or "unknown"
            candidate_sources = candidate.get("discovery_sources") or []
            if not candidate_sources and display(candidate.get("official_program_url")):
                discovery = candidate.get("discovery_source") or {}
                candidate_sources = [
                    {
                        "url": candidate["official_program_url"],
                        "source_type": discovery.get("source_type"),
                        "access_status": discovery.get("access_status"),
                    }
                ]
            for source in candidate_sources:
                if not isinstance(source, dict) or not display(source.get("url")):
                    continue
                url = display(source["url"])
                usage[url].append(
                    {
                        "file": "research_queue/program_candidates_v2.json",
                        "record_id": candidate_id,
                        "source_type": display(source.get("source_type")),
                    }
                )
                stored_statuses[url].add(display(source.get("access_status")))

    urls = sorted(usage)
    if args.record_id:
        requested_records = set(args.record_id)
        urls = [
            url for url in urls
            if any(item.get("record_id") in requested_records for item in usage[url])
        ]
    if args.url:
        requested = set(args.url)
        missing = sorted(requested.difference(usage))
        if missing:
            parser.error(f"URL is not present in active source logs: {', '.join(missing)}")
        urls = [url for url in urls if url in requested]
    if args.limit > 0:
        urls = urls[:args.limit]
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 16))) as executor:
        futures = {executor.submit(check, url, args.timeout): url for url in urls}
        for number, future in enumerate(as_completed(futures), 1):
            result = future.result()
            url = result["url"]
            result["stored_access_statuses"] = sorted(stored_statuses[url])
            result["uses"] = usage[url]
            results.append(result)
            if number % 25 == 0 or number == len(urls):
                print(f"Checked {number}/{len(urls)} unique source URLs", flush=True)

    results.sort(key=lambda item: item["url"])
    counts: dict[str, int] = defaultdict(int)
    for result in results:
        counts[result["access_status"]] += 1
    report = {
        "checked_at": date.today().isoformat(),
        "scope_id": SCOPE.get("scope_id"),
        "unique_urls_checked": len(results),
        "status_counts": dict(sorted(counts.items())),
        "results": results,
    }
    print(json.dumps(report["status_counts"], ensure_ascii=False, sort_keys=True))
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
