"""
hrc_data_scraper.py
-------------------
Scrapes REAL data for a heavy-machinery human-robot handoff project.

Sources
-------
  1. arXiv API          – HRC + handover + speed-safety papers
  2. Semantic Scholar   – broader academic coverage (no API key needed)
  3. ISO/TS 15066       – Annex A speed/force limits (hard-coded from standard)
  4. Dataset registry   – known public HRC datasets with access URLs

Requirements
------------
  pip install requests

Run
---
  python hrc_data_scraper.py

Outputs
-------
  hrc_papers.csv        – deduplicated papers (title, authors, year, abstract, url)
  iso_safety_limits.csv – ISO/TS 15066:2016 Annex A body-region limits
  hrc_datasets.csv      – public HRC dataset registry with reachability check
"""

import csv
import json
import os
import time
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    raise SystemExit("Missing dependency — run:  pip install requests")

OUT = os.path.dirname(os.path.abspath(__file__))

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "HRC-research-scraper/1.0 (academic use)"
})


# ── helpers ────────────────────────────────────────────────────────────────────

def get_json(url, params=None, timeout=15, pause=1.0):
    """GET -> parsed JSON, or None on failure."""
    try:
        r = SESSION.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        time.sleep(pause)
        return r.json()
    except Exception as e:
        print(f"    [!] {url[:70]} — {e}")
        return None


def get_text(url, params=None, timeout=15, pause=1.0):
    """GET -> raw text, or None on failure."""
    try:
        r = SESSION.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        time.sleep(pause)
        return r.text
    except Exception as e:
        print(f"    [!] {url[:70]} — {e}")
        return None


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  [+] {len(rows):>3} rows  ->  {os.path.basename(path)}")


# ══════════════════════════════════════════════════════════════════════════════
# 1.  arXiv  (https://export.arxiv.org/api/query)
# ══════════════════════════════════════════════════════════════════════════════

ARXIV_QUERIES = [
    "human robot handover speed safety assembly",
    "robot arm handoff industrial operator clearance",
    "adaptive robot speed human proximity collision",
    "ISO 15066 speed separation monitoring cobot",
    "human robot collaboration hesitation adaptive control",
]

ARXIV_NS = {"a": "http://www.w3.org/2005/Atom"}


def scrape_arxiv(max_per_query=10):
    print("\n[1/4]  arXiv API ...")
    base = "https://export.arxiv.org/api/query"
    seen, papers = set(), []

    for q in ARXIV_QUERIES:
        raw = get_text(base, params={
            "search_query": f"all:{q}",
            "start": 0,
            "max_results": max_per_query,
            "sortBy": "relevance",
        }, pause=3.0)          # arXiv rate limit: >= 3 s between requests

        if not raw:
            continue

        try:
            root = ET.fromstring(raw)
        except ET.ParseError as e:
            print(f"    [!] XML parse error: {e}")
            continue

        for entry in root.findall("a:entry", ARXIV_NS):
            arxiv_id = (entry.findtext("a:id", "", ARXIV_NS) or "").strip()
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)

            authors = [
                a.findtext("a:name", "", ARXIV_NS).strip()
                for a in entry.findall("a:author", ARXIV_NS)
            ]
            published = (entry.findtext("a:published", "", ARXIV_NS) or "")[:10]
            abstract = (
                (entry.findtext("a:summary", "", ARXIV_NS) or "")
                .replace("\n", " ").strip()
            )

            papers.append({
                "source":    "arXiv",
                "title":     (entry.findtext("a:title", "", ARXIV_NS) or "")
                             .replace("\n", " ").strip(),
                "authors":   "; ".join(authors[:5])
                             + (" et al." if len(authors) > 5 else ""),
                "year":      published[:4],
                "published": published,
                "abstract":  abstract[:500],
                "url":       arxiv_id,
                "query":     q,
            })

        print(f"    '{q[:50]}' -> {len(papers)} papers total")

    return papers


# ══════════════════════════════════════════════════════════════════════════════
# 2.  Semantic Scholar  (free public Graph API — no key required)
# ══════════════════════════════════════════════════════════════════════════════

SS_QUERIES = [
    "human robot handover speed safety industrial",
    "robot speed limit human operator proximity",
    "collaborative robot power force limiting assembly",
    "human robot handoff hesitation adaptive controller",
